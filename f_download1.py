# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 14:09:15 2022

@author: Joobing
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
from requests import get #from requests.exceptions import ParseError


from random import randint
from IPython.display import clear_output
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def redir(tokens):  #[<a>]:[href].text #<link,rel=canonical,[0]>
    '''redir: takes in html tags (tokens) containing dynamic links to target (external) addresses, returns permanent link (and occasionaly, content of the linked webpage?)'''

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



def diclis(d):
    return pd.DataFrame.from_dict(d,orient='index').transpose()
def parse(allPs, mainlength, lastlength):#SUGGESTED 250 , 450
    '''extracts main body of an article from all (html) paragraphs of a given address (e.g. all the ads and warnings etc)
    also separates first and last paragraphs for cross checking'''
    first=''
    last_paragraph=''
    extra_paragraph=''
    extra_paragraph_2=''
    content=""
    parsed=0
    for i in range(len(allPs)):
        
        if len(allPs[i].text.replace(" ", "")) > mainlength:
            #print('\n\n'+allPs[i].text.strip(),'\n',str(i),':',str(len(allPs[i].text.replace(" ", ""))))
            content=content+'\n'+allPs[i].text.strip()
            parsed=1

        elif i+2 in range(len(allPs)) and len(allPs[i+1].text.replace(" ", "")) > lastlngth:
            #print('\n\n'+allPs[i].text.strip(),'\n',str(i),':',str(len(allPs[i].text.replace(" ", ""))))
            content=content+'\n'+allPs[i].text.strip()               
            parsed=1
            
        elif i+2 in range(len(allPs)) and len(allPs[i+2].text.replace(" ", "")) > lastlngth: 
            first=first+'\n'+allPs[i].text.strip()               
            parsed=1

        else:
            if parsed == 1:
                last_paragraph= last_paragraph + allPs[i].text.strip()
                if i+2 in range(len(allPs)): 
                    extra_paragraph= extra_paragraph + allPs[i+1].text.strip()
                    extra_paragraph_2= extra_paragraph_2 + allPs[i+2].text.strip()                                   
                elif i+1 in range(len(allPs)): 
                    extra_paragraph= extra_paragraph + allPs[i+1].text.strip()                    
                else:
                    extra_paragraph= None
                #print('\nlast\n'+allPs[i].text.strip(),'\n',str(i),':',str(len(allPs[i].text.replace(" ", ""))))
                #print('\nlatest\n'+allPs[i+1].text.strip(),'\n',str(i+1),':',str(len(allPs[i+1].text.replace(" ", ""))))            
                break
            else: pass
    return [first, content, last_paragraph, extra_paragraph, extra_paragraph_2]


def download(path):  #[<a>]:[href].text #<link,rel=canonical,[0]>
    tokens = BeautifulSoup(get(path, "html.parser").text, "html.parser").find_all('ul', class_="simpleList")[0].find_all('a')    
    links = redir(tokens[7:10])['site']

    i=-1
    j=-1
    content=[]
    URL=[]
    status=[]
    link_number=[]
    link=[]
    site=[]
    start_time = time()
    requests = 0
    for l in links:
        i=i+1
        
        if 'missing:' not in l:
        
            try:
                site.append(re.search('//(.+?)/', l).group(1))
            except:
                site.append(re.search('\.(.+?)\.', l).group(1))
            try: 
                page=get(l, headers=headers, timeout=20)
            
                #print([i,int(str(page).split()[1][1:4])], l)
                status.append(page)
                link_number.append(i)
                if int(str(page).split()[1][1:4])==200:
                    URL.append("see: ['unknown_redir_page']"+'['+str(j)+'],number:'+str(j))
                    content.append(parse(BeautifulSoup(page.text, 'html.parser').find_all('p')))
                    link.append(site[i])
    
                else:
                    URL.append('404')        
                    content.append(None)   
                    link.append(None) 

            except Timeout:
                status.append('Timeout')
                link_number.append(i)    
                URL.append('Timeout')
                content.append(None)
                link.append(None)
                

            except ConnectionError as e:             
                status.append('ConnectionError')
                link_number.append(i)    
                URL.append('NoResponse')
                content.append(None)
                link.append(None)
            
            except:
                URL.append('UnknownError')
                status.append('Unknown')
                content.append(None)
                link_number.append(i)
                link.append(None)

        else:
            link_number.append(i)    
            site.append(l)
            status.append('missing link')
            URL.append('missing link')
            content.append(None)
            link.append(None)
            

    return {'link_number':link_number,'site':site,'status':status,'URL':URL,'link':link,'content':content}

