# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 12:21:34 2019
f_RetrieveLinks
@author: u811717
"""

import pickle
import lxml.html as html
import numpy as np
import pandas as pd
from warnings import warn
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
from xml.etree import ElementTree

from time import time
from time import sleep
from bs4 import BeautifulSoup
from requests import get


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}



def geturl(tags):      #[<>]:[href]
    URL=[]
    for tag in tags:
        URL.append(tag['href'])
    return URL

def xtract(string,attribute):    #text:[href]
    return(html.fromstring(string).xpath('//@'+str(attribute)))
    
def href(string):    #text:[href]
    return(html.fromstring(string).xpath('//@href'))

'''redir: takes in html tags (tokens) containing dynamic links to target (external) addresses, returns permanent link (and occasionaly, content of the linked webpage?)'''
def redir(tokens):  #[<a>]:[href].text #<link,rel=canonical,[0]>
    i=-1
    #j=-1

    site=[]#permanent url for the target site
    status=[]#whether target address retreived anything
    link_number=[]#nth target site from all the target addresses
    URL=[]#all canonical links within the target address, including it's (own) target address (usually that's all you get)
    
    unknown_redir_page=[]
    start_time =time()
    requests = 0
    for l in tokens:
        i=i+1
        try:
            site.append(l['href']) #(re.search('offsite-(.*)&', l['href']).group(1))
        except:
            pass#site.append(re.search('page-action=(.*)&', l['href']).group(1))
        
        link_number.append(i)
 
       
        try:
            page=get(l['href'], headers=headers, timeout=20)          
            status.append(page)
            #print([i,page.status_code])
            
            if int(page.status_code)==200:
                try: 
                    URL.append(BeautifulSoup(page.text, "html.parser").find_all('link', attrs={"rel":"canonical"})[0]['href'])
                except: 
                    URL.append("see: ['status'].text      status code : "+str(page.status_code)) #URL.append("see: ['unknown_redir_page']"+'['+str(j)+'],number:'+str(j))
            else:
                URL.append("see: ['status'].text "+str(page.status_code))   
                
            sleep(np.random.randint(3,6))     
        
             
        
        except Timeout:
            status.append('Timeout')
            URL.append('Timeout')            
            
            
        except ConnectionError as e:             
            status.append('ConnectionError')
            URL.append('NoResponse')
        
        except:
            status.append(page)            
            URL.append("see: ['status'].text "+str(page.status_code))   


    return {'link_number':link_number,'site':site,'status':status,'URL':URL} #,'unknown_redir_page':[unknown_redir_page]


















'''redir: takes in tokens of external links, returns actual link, or occasionaly, content of the linked webpage'''
'''def redir(tokens):  #[<a>]:[href].text #<link,rel=canonical,[0]>
    i=-1
    j=-1
    unknown_redir_page=[]
    URL=[]
    status=[]
    link_number=[]
    site=[]
    start_time = time()
    requests = 0
    for l in tokens:
        i=i+1
        site.append(re.search('offsite-(.*)&', l['href']).group(1))
        try: 
            page=get('https://www.imdb.com/' + l['href'], headers=headers)
            print([i,int(str(page).split()[1][1:4])])
            status.append(page)
            link_number.append(i)
            if int(str(page).split()[1][1:4])==200:
                try: URL.append(BeautifulSoup(page.text, "html.parser").find_all('link', attrs={"rel":"canonical"})[0]['href'])
                except: 
                    j+=1
                    URL.append("see: ['unknown_redir_page']"+'['+str(j)+'],number:'+str(j))
                    unknown_redir_page.append(page.text)
            else:
                URL.append('404')        
        
        except ConnectionError as e:             
            status.append('ConnectionError')
            link_number.append(i)    
            URL.append('NoResponse')
        
        except:
            URL.append('UnknownError')        


    return {'link_number':link_number,'site':site,'status':status,'URL':URL,'unknown_redir_page':[unknown_redir_page]}
'''




'''
try:
    # python 2.7+
    # pylint: disable=no-member
    ParseError = ElementTree.ParseError
except ImportError:
    # python 2.6-
    # pylint: disable=no-member
    from xml.parsers import expat
    ParseError = expat.ExpatError
'''

'''
URL.append(
        
        BeautifulSoup(
                get('https://www.imdb.com/' + urls[9]['href'], headers=headers).text
                , "html.parser").find_all(href=True)
                        'link', attrs={"rel":"canonical"})[0]['href']
        
        )
'''