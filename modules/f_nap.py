# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 20:26:52 2019
nap
@author: u811717
"""

def nap(a,b,response,requests,start_time)
    # Monitor the requests
    sleep(randint(3,6))

    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)
    
    # Throw a warning for non-200 status codes
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))
    
    # Break the loop if the number of requests is greater than expected
    if requests > 50:
        warn('Number of requests was greater than expected.')  
        #sleep(randint(10,25))
        #break  