# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 07:45:01 2018

calculate confidence intervals for nonstandard student T
"""
import time
import scipy.stats

sstart = time.time()
print('')

df = 3.33
nc = 3.59
loc = -1.28
scale = 2.7

pathFileOut = "[your data location]"
fOut = open(pathFileOut,'w')

inter = scipy.stats.nct.interval(0.01, df = df, nc = nc, loc = loc, scale = scale)
ttext = '.01' + '|' + str(inter[0]) + '|' + str(inter[1]) + '\n'
fOut.write(ttext)

conf = 0
for i in range(19):
    conf = round(conf + .05, 2)
    inter = scipy.stats.nct.interval(conf, df = df, nc = nc, loc = loc, scale = scale)
    ttext = str(conf) + '|' + str(inter[0]) + '|' + str(inter[1]) + '\n'
    fOut.write(ttext)

inter = scipy.stats.nct.interval(0.99, df = df, nc = nc, loc = loc, scale = scale)
ttext = '.99' + '|' + str(inter[0]) + '|' + str(inter[1]) + '\n'
fOut.write(ttext)    
    
fOut.close()
print('')
endd = time.time()
print('Elapse Time:', round(endd - sstart,2))