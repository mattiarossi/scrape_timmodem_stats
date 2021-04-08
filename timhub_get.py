from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import  ElementNotInteractableException
from pyvirtualdisplay import Display
from selenium.webdriver.common.action_chains import ActionChains
import os
import re
import time
import json
import argparse

#
# author: mattia rossi
# date: 2021-04-01
# objective: via an automated browser, log into a Technicolor C1100T DSL Modem
# navigate to the the DSL statistics page, scrape specific statistics, and
# write the variables and statistics to a JSON record and log the record for
# future CSV export, visualization and analysis
# 
# Liberally inspired by code at: https://github.com/jearlcalkins/scrape_dsl_modem_stats
#


def refp(astr, groupn):
    pfp = re.compile('([-+]?[0-9]*\.?[0-9]+)')
    result = pfp.findall(astr)
    return result[groupn-1]

def maybe_goheadless(monitor):
    if monitor == 'no':
        display = Display(visible=0, size=(800, 600))
        display.start()

def get_modem(ip):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.binary_location = "/usr/bin/chromium-browser"
    driver = webdriver.Chrome(options=options)
    url = 'http://' + ip
    driver.get(url)
    return driver

def enter_pw(pw):
    ctr = 1
    while ctr < 6:
        try:
            passwordElement = driver.find_element_by_xpath("//input[@id='password']")
            passwordElement.send_keys(pw)
            ctr = 0
            break
        except NoSuchElementException as Exception:
            #print("admin_password  is NOT yet there")
            ctr += 1
            time.sleep(1)
    


def enter_user(user):
    usernameElement = driver.find_element_by_id("user")
    if usernameElement.get_attribute('value') == user:
        return
    else:
        usernameElement.clear()
        usernameElement.send_keys(user)

def get_dsl_status():
    # the data in the <p> DSL Status and its <table> holds summary information 
    # the DSL Line Status, simply tells you GOOD, POOR, and ???
    # the DSL Downstream and DSL Upstream tell you the configured caps
    # there is SNR, CRC and attenuation stats (dB) also available
    # i'll get these summary stats from other paragraphs.
    #dslUpstream: 0.895 Mbps
    #dslDownstream: 23.103 Mbps
    #dslLineStatus: GOOD
    #print("dslUpstream:",refp(dslUpstreamBitRate.text), " Mbps")
    #print("dslDownstream:",refp(dslDownstreamBitRate.text), " Mbps")
    #print("dslLineStatus:", dslLineStatusBitRate.text)

    sample = {}
    dslUpstreamElement = driver.find_element_by_id("cbr")
    sample['dslUpstreamBitRate'] = float(refp(dslUpstreamElement.text,1)) 
    sample['dslDownstreamBitRate'] = float(refp(dslUpstreamElement.text,2)) 
    dslMaxUpstreamElement = driver.find_element_by_id("mabr")
    sample['dslMaxUpstreamBitRate'] = float(refp(dslMaxUpstreamElement.text,1)) 
    sample['dslMaxDownstreamBitRate'] = float(refp(dslMaxUpstreamElement.text,2)) 

    dslLineStatusElement = driver.find_element_by_id("dsl_status")
    sample['dslLineStatusElement'] = dslLineStatusElement.text

    dslAttenuationElement = driver.find_element_by_id("la")
    sample['dslUpstreamAttenuation'] = float(refp(dslAttenuationElement.text,1)) 
    sample['dslDownstreamAttenuation'] = float(refp(dslAttenuationElement.text,2)) 
    return sample





def get_dsl_power():
    # the <p> DSL Power paragraph and its <tr> table holds SNR, Power, which
    # are captured, whereas three attenuation stats are available.
    # this dataset appears to refresh every 6 seconds
    #print("SNR_downstream:", refp(SNR_downstream.text),"dB")
    #print("SNR_upstream:", refp(SNR_upstream.text),"dB")
    #print("Power_downstream:", refp(Power_downstream.text),"dbm")
    #print("Power_upstream:", refp(Power_upstream.text),"dbm")

    sample = {}
    ctr = 1
    while ctr < 6:
        try:
            SNR_downstream = driver.find_element_by_id('nm')
            sample['SNR_downstream'] =  float(refp(SNR_downstream.text,2))
            sample['SNR_upstream'] =  float(refp(SNR_downstream.text,1))
            ctr = 0
            break
        except NoSuchElementException as Exception:
            print("dsl_power is NOT yet there")
            ctr += 1
            time.sleep(1)

    if ctr == 0:

        Power_downstream = driver.find_element_by_id('ptl')
        sample['Power_upstream'] =  float(refp(Power_downstream.text,1))
        sample['Power_downstream'] = float(refp(Power_downstream.text,2))

        return sample 
    else:
        sample['SNR_downstream'] = -1.0 
        sample['SNR_upstream'] =-1.0
        sample['Power_downstream'] = -1.0 
        sample['Power_upstream'] = -1.0

        return sample 



def gotoMain():

    try:
        url = 'http://' + ip +"/network-expert-dsl.lp"
        driver.get(url)
        return 1
    except NoSuchElementException as Exception:
        time.sleep(1)
    return -1

def doLoginButton():
    #don't bother waiting, the usesrname and passwords have waits
    login_button = driver.find_element_by_xpath("//input[@name='ok']").click()

def doLogoutButton(reboot):
    if reboot == 'no':
        return 1
    else:
        try:
            url = 'http://' + ip +"/logout.lp"
            driver.get(url)
            return 1
        except NoSuchElementException as Exception:
            time.sleep(1)
        return -1
    return 0




json_fname = "json_timhub.txt"

data = {}
samples = {}

# change the below, and they become your passline defaults.  you can always 
# override these variables on the passline
# from a security perspective, you can hard code your password here, or you
# can call this application, and pass the password on the command line
# your call
password = 'admin'
ip = '192.168.101.1'
username = 'Administrator'
reboot = 'no'
monitor = "no"
clear = 'no'

parser = argparse.ArgumentParser()
parser.add_argument('-u', default=username, help="username")
parser.add_argument('-i', default=ip, help="ip")
parser.add_argument('-p', default=password, help="password")
parser.add_argument('-m', default=monitor, help="monitor")

args = parser.parse_args()

username = args.u
ip = args.i
password = args.p
monitor = args.m

result = os.system("pkill chromedriver")
result = os.system("pkill chromium")
result = os.system("pkill Xvfb")

ts0 = int(round(time.time() * 1000))

maybe_goheadless(monitor)

driver = get_modem(ip)

enter_pw(password)
enter_user(username)
doLoginButton()
driver.maximize_window()

gotoMain()

samples.update(get_dsl_power())

samples.update(get_dsl_status())



ts1 = int(round(time.time() * 1000))
delta_ts = ts1 - ts0

doLogoutButton(reboot)
time.sleep(1)

driver.close()
driver.quit()

data[ts0] = samples      # all the samples in that dict, are the value to the ts0 index
data_json = json.dumps(data) + '\n'
fo = open(json_fname, "a+")
fo.write(data_json)
fo.close()

result = os.system("pkill Xvfb")
