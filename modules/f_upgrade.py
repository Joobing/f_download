# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 20:13:22 2019
upgrade
@author: u811717
"""
def upgrade(a,b):
    jam={}
    for k in a.keys():
        jam[str(k)]=a[str(k)]+b[str(k)]
    return jam
