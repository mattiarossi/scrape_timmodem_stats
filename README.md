# scrape_dsl_modem_stats
scrape TIM Modem (AKA Technicolor DGA4130) stats with the python selenium module.  the applciation is: timhub_get.py

Liberally inspired by code at https://github.com/jearlcalkins/scrape_dsl_modem_stats

#### Logged DSL and router stats
everytime the timhub_get.py application successfully runs it scrapes the dsl modem data, the data will be logged as a JSON record, and appended to the **json_timhub.txt** file.  The following is a single JSON dataset example:  

*`
{"1617891288187": {"SNR_downstream": 6.2, "SNR_upstream": 6.1, "Power_upstream": 5.8, "Power_downstream": 14.5, "dslUpstreamBitRate": 21599.0, "dslDownstreamBitRate": 50273.0, "dslMaxUpstreamBitRate": 22819.0, "dslMaxDownstreamBitRate": 50349.0, "dslLineStatusElement": "Connesso", "dslUpstreamAttenuation": 5.3, "dslDownstreamAttenuation": 16.0}}
`*  

The record is key'd to epoch time in milliseconds (ms).  In this example, the 1617891288187 time is: 04/08/2021 @ 2:14pm (UTC)  
The following variables are available, along with recently scrapped dls modem data:
1617891288187 (timestamp key for the following variables  
1. SNR_downstream 6.2  
2. SNR_upstream 6.1
3. Power_downstream 14.5  
4. Power_upstream 5.8  
5. dslUpstreamBitRate 50349.0  
6. dslDownstreamBitRate 50273.0  
7. dslMaxUpstreamBitRate 22819.0  
8. dslMaxDownstreamBitRate 50349.0  
9. dslUpstreamAttenuation 5.3
10. dslDownstreamAttenuation 16.0  
11. dslLineStatusElement Connesso  

The application timhub_json2csv.py will convert **json_timhub.txt** to **out.csv**  

the following is a 4 record snippet of the out.txt CSV file:  
`ts,SNR_downstream,SNR_upstream,Power_downstream,Power_upstream,dslDownstreamBitRate,dslUpstreamBitRate,dslMaxDownstreamBitRate,dslMaxUpstreamBitRate,dslDownstreamAttenuation,dslUpstreamAttenuation,dslLineStatusElement
1617750852707,11.9,9.9,14.3,5.3,38781.0,10799.0,39220.0,18455.0,16.0,5.3,Connesso
1617751158767,11.9,10.1,14.3,5.3,38781.0,10799.0,39262.0,18485.0,16.0,5.3,Connesso
1617751464717,11.9,10.1,14.3,5.3,38781.0,10799.0,39293.0,18848.0,16.0,5.3,Connesso
1617751770758,11.9,10.3,14.3,5.3,38781.0,10799.0,39362.0,19403.0,16.0,5.3,Connesso




#### Environmental Assumptions:  

+ python3 Python 3.7.3 (default, Dec 20 2019, 18:57:59  
+ pip3  


This application controls the RPI chromium web browser, as if a user were surfing, using the keyboard and mouse. The chromedriver is a google chrome API, that allows programmatic control over their browser.  

If you want to turn-off headless operations, you can watch the application start the browser, go the modem (site) and navigate to the page holding the DSL variables, then logout. It's fun to watch the application take control of the browser. Watching the application, is often helpful when troubleshooting issues.  

#### Install the applicaton

`sudo apt-get update`  
`sudo apt-get upgrade`   
`sudo apt-get install xvfb`      
`sudo pip3 install pyvirtualdisplay`      
`sudo apt-get install chromium-chromedriver`     
`pip3 install -U selenium`
 
#### Download the code
goto this link and hit the clone or download button:  
https://github.com/mattiarossi/scrape_timmodem_stats  

or
 
from a terminal session, run the following cmd:  
`wget https://github.com/mattiarossi/scrape_timmodem_stats/blob/master/timhub_get.py`  


#### how-to run examples  
view the pass variable options:
`python3 timhub_get.py -h`  

run the application, taking default modem IP, username: admin, password: (what is on line 24)  
`python3 timhub_get.py`

run the application, passing the modem's password 'G0CUBz':  
`python3 timhub_get.py -p G0CUBz`  

run the application from the crontab
```
0,30 * * * * python3 timhub_get.py -i 192.168.0.1
2,32 * * * * python3 timhub_json2csv.py 
```
The modem will be scraped at the top (0) and bottom half (30) of the hour, every hour (timhub_get.py)
The json log file (json_timhub.txt) will be converted to a csv file (out.csv) at 2 minutes and 32 minutes after the hour, every hour (timhub_json2csv.py)




