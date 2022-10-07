# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 10:56:15 2019
f:ParseContent
@author: u811717
"""

'''????FIRST PARAGRAPH???'''

def parse(allPs):
    first=''
    last_paragraph=''
    extra_paragraph=''
    extra_paragraph_2=''
    content=""
    parsed=0
    for i in range(len(allPs)):
        
        if len(allPs[i].text.replace(" ", "")) > 250:
            #print('\n\n'+allPs[i].text.strip(),'\n',str(i),':',str(len(allPs[i].text.replace(" ", ""))))
            content=content+'\n'+allPs[i].text.strip()
            parsed=1

        elif i+2 in range(len(allPs)) and len(allPs[i+1].text.replace(" ", "")) > 450:
            #print('\n\n'+allPs[i].text.strip(),'\n',str(i),':',str(len(allPs[i].text.replace(" ", ""))))
            content=content+'\n'+allPs[i].text.strip()               
            parsed=1
            
        elif i+2 in range(len(allPs)) and len(allPs[i+2].text.replace(" ", "")) > 450: 
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

        #content=content+str(i)+':'+str(len(allPs[i].text.replace(" ", "")))+'\n\n'+allPs[i].text.strip()

'''
for s in review[3][1]:
    #print(type(s.text))
    if len(s.text.replace(" ", "")) > 140:
        print('\n\n',len(s.text.replace(" ", "")),':',s.text.strip())
'''
