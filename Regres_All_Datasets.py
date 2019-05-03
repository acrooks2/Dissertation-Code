# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 09:30:57 2018

4 Linear regression models at the state level;  Calculate all datasets
"""
import time
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.linear_model import RidgeCV, LassoCV
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import ElasticNet

start = time.time()

ptr = 5

names = []
names.append('Boston')
names.append('Olympic')
names.append('Sandy')
names.append('Syria')
names.append('Zombie')
names.append('MyTwitter')

files = []
files.append('1_Boston_Tweets')
files.append('4_Olympic_Tweets')
files.append('6_Sandy_Tweets')
files.append('7_Syria_Tweets')
files.append('8_Zombie_Tweets')
files.append('9_MyTwitter')

alphas = 10**np.linspace(10,-3,100)*0.5

#  calculate simple multiregression
def simple(x, y):
    mod = LinearRegression(normalize=True).fit(x, y)
    r2 = round(mod.score(x, y),2)
    return r2, mod.coef_

#  calculate ridge regression
def ridge(x, y):
    ridgecv = RidgeCV(alphas = alphas, scoring = 'neg_mean_squared_error', normalize = True)
    ridgecv.fit(x, y)
    ridgereg = Ridge(alpha=ridgecv.alpha_,normalize=True, max_iter=1e5)
    ridgereg.fit(x, y)
    r2 = round(ridgereg.score(x, y),2)
    return r2, ridgereg.coef_
    
#  calculate lasso regression
def lasso(x, y):
    lassocv = LassoCV(alphas = None, cv = 10, max_iter = 10000, normalize = True)
    lassocv.fit(x, y)
    lassoreg = Lasso(alpha=.00005,normalize=True, max_iter=1e5)
    lassoreg.set_params(alpha=lassocv.alpha_)
    lassoreg.fit(x,y)
    r2 = round(lassoreg.score(x, y),2)
    return r2, lassoreg.coef_

#  calculate elastic regression
def elasticNet(x, y):
    enet = ElasticNet(alpha=.01, l1_ratio=0.7, max_iter=1e5)
    enet.fit(x, y)
    r2 = round(enet.score(x, y),2)
    return r2, enet.coef_

#  set up the string to be printed
def printString(mmodel, state, demo, r2, coef):
    ttext = mmodel + '|' + state + '|' + demo + '|' + str(r2) + '|' + str(round(coef[0],5)) + '|' 
    ttext = ttext + str(round(coef[1],5)) + '|' + str(round(coef[2],5))
    ttext = ttext + '|' + str(round(coef[3],5))   + '\n'
#   + '|' + str(round(coef[4],5))
#    ttext = ttext + '|' + str(round(coef[5],5)) + '|' + str(round(coef[6],5))  + '\n'
#    ttext = ttext + '|' + str(round(coef[6],5)) + '|' + str(round(coef[7],5)) + '|' + str(round(coef[8],5)) + '\n'
    return ttext

#  load GeoIds
pathFileGeo = "[your file location]"
fGeo = open(pathFileGeo, 'r+')
stateM, county, geoID = [], [], []
for line in fGeo:
    line = line.strip()
    ffields = line.split('|')
    stateM.append(ffields[0])
    county.append(ffields[1])
    geoID.append(int(ffields[2]))
fGeo.close()

#  load states
pathFileState = "[state names]"
fState = open(pathFileState, 'r+')
states = []
for line in fState:
    line = line.strip()
    states.append(line)
fState.close()

#if __name__ == "__main__":
def doWork(file1, name1):
#  open output file
#    pathFileOut1 = '[your location]' + files[ptr] + '/' + names[ptr] +'_NewRegression_Avg.txt'
    pathFileOut1 = '[your location]' + file1 + '/' + name1 +'_NewRegression_Avg_Final_AllLLV.txt'
    fOut1 = open(pathFileOut1,'w')
    
#  load data to process
#    pathFileMaster = '[your location]' + files[ptr] + '/' + names[ptr] + '_LR.txt'
    pathFileMaster = '[your location]' + file1 + '/' + name1 + '_LR.txt'
    fIn = open(pathFileMaster, 'r+', encoding='utf-8')
    geo, lat, lon = [], [], []
    perCap, age, whit, blk, ind, asia, haw, other = [], [], [], [], [], [], [], []
    lhs, hs, mhs, ba = [], [], [], []
    reA, gradeA, dwA, polA, subA, modalA, entA = [], [], [], [], [], [], []
    reV, gradeV, dwV, polV, subV, modalV, entV = [], [], [], [], [], [], []
    icnt = 0
    for line in fIn:
        icnt = icnt + 1
        if icnt > 1:    #  skip first line
            line = line.strip()
            ffields = line.split('|')
            geo.append(int(ffields[0]))
            lat.append(float(ffields[4]))
            lon.append(float(ffields[5]))
#  demographic data
            perCap.append(float(ffields[37]))
            age.append(float(ffields[38]))
            whit.append(float(ffields[39]))
            blk.append(float(ffields[40]))
            ind.append(float(ffields[41]))
            asia.append(float(ffields[42]))
            haw.append(float(ffields[43]))
            other.append(float(ffields[44]))
            lhs.append(float(ffields[45]))
            hs.append(float(ffields[46]))
            mhs.append(float(ffields[47]))
            ba.append(float(ffields[48]))

# average language variables
            reA.append(ffields[8])
            gradeA.append(ffields[9])
            dwA.append(ffields[10])
            polA.append(ffields[11])
            subA.append(ffields[12])
            modalA.append(ffields[13])
            entA.append(ffields[14])
# variance language variables
            reV.append(ffields[23])
            gradeV.append(ffields[24])
            dwV.append(ffields[25])
            polV.append(ffields[26])
            subV.append(ffields[27])
            modalV.append(ffields[28])
            entV.append(ffields[29])
    fIn.close()

#  set up the data for the regressions by state
    icnt, jcnt =[0, 0]
    for state in states:
#  open a file to dump the causal data
        pathFileState = '[your location]' + file1 + '/States/' + state + '_causal.txt'
        fState = open(pathFileState,'w')
        header = ''
        header = header + 'GeoID|Capita|Age|White|Black|Indian|Asian|Hawaii|Other|LessHS|HS|MoreHS|BA|'
        header = header + 'RE_Avg|Grade_Avg|DW_Avg|Pol_Avg|Subj_Avg|Modal_Avg|CC_Ent_Avg|Lat|Lon\n'
        fState.write(header)

        icnt = icnt + 1
        xx = [ii for ii, xxx in enumerate(stateM) if xxx == state]
        if len(xx) > 0:
            YperCap = np.zeros(len(xx))
            Yage = np.zeros(len(xx))
            Ywhit = np.zeros(len(xx))
            Yblk = np.zeros(len(xx))
            Yind = np.zeros(len(xx))
            Yasia = np.zeros(len(xx))
            Yhaw = np.zeros(len(xx))
            Yother = np.zeros(len(xx))
            Ylhs = np.zeros(len(xx))
            Yhs = np.zeros(len(xx))
            Ymhs = np.zeros(len(xx))
            Yba = np.zeros(len(xx))

            xA = np.ndarray((len(xx), 9))
            xA.fill(0)
            kcnt = 0
            for i in range(len(xx)):
                try:
                    zz = geo.index(geoID[xx[i]])

                    YperCap[kcnt] = perCap[zz]
                    Yage[kcnt] = age[zz]
                    Ywhit[kcnt] = whit[zz]
                    Yblk[kcnt] = blk[zz]
                    Yind[kcnt] = ind[zz]
                    Yasia[kcnt] = asia[zz]
                    Yhaw[kcnt] = haw[zz]
                    Yother[kcnt] = other[zz]
                    Ylhs[kcnt] = lhs[zz]
                    Yhs[kcnt] = hs[zz]
                    Ymhs[kcnt] = mhs[zz]
                    Yba[kcnt] = ba[zz]
                    """
                    xA[kcnt,0] = reA[zz]
                    xA[kcnt,1] = gradeA[zz]
                    xA[kcnt,2] = dwA[zz]
                    xA[kcnt,3] = polA[zz]
                    xA[kcnt,4] = subA[zz]
                    xA[kcnt,5] = modalA[zz]
                    xA[kcnt,6] = entA[zz]
                    xA[kcnt,7] = lat[zz]
                    xA[kcnt,8] = lon[zz]
                    
                    xA[kcnt,0] = reV[zz]
                    xA[kcnt,1] = gradeV[zz]
                    xA[kcnt,2] = dwV[zz]
                    xA[kcnt,3] = polV[zz]
                    xA[kcnt,4] = subV[zz]
                    xA[kcnt,5] = modalV[zz]
                    xA[kcnt,6] = entV[zz]
                    xA[kcnt,7] = lat[zz]
                    xA[kcnt,8] = lon[zz]
                    """
                    xA[kcnt,0] = subV[zz]
                    xA[kcnt,1] = entV[zz]
                    xA[kcnt,2] = polV[zz]
                    xA[kcnt,3] = modalV[zz]
                    xA[kcnt,4] = lat[zz]
                    xA[kcnt,5] = lon[zz]
                    numVars = 6
                    kcnt = kcnt + 1
                    
#  causal string

                    cause = ''
                    cause = cause + str(geo[zz]) + '|' + str(perCap[zz]) + '|' + str(age[zz])
                    cause = cause + '|' + str(whit[zz]) + '|' + str(blk[zz]) + '|' + str(ind[zz]) + '|' + str(asia[zz])
                    cause = cause + '|' + str(haw[zz]) + '|' + str(other[zz]) + '|' + str(lhs[zz]) + '|' + str(hs[zz]) + '|' + str(mhs[zz])
                    cause = cause + '|' + str(ba[zz])  + '|' + str(reA[zz]) + '|' + str(gradeA[zz])
                    cause = cause + '|' + str(dwA[zz]) + '|' + str(polA[zz]) + '|' + str(subA[zz]) + '|' + str(modalA[zz])
                    cause = cause + '|' + str(entA[zz]) + '|' + str(lat[zz]) + '|' + str(lon[zz]) + '\n'
                    fState.write(cause)
                except:
                    continue


            fState.close()
            print(state, len(xx), kcnt)
            
            YperCap = np.resize(YperCap, kcnt)
            Yage = np.resize(Yage, kcnt)
            Ywhit = np.resize(Ywhit, kcnt)
            Yblk = np.resize(Yblk, kcnt)
            Yind = np.resize(Yind, kcnt)
            Yasia = np.resize(Yasia, kcnt)
            Yhaw = np.resize(Yhaw, kcnt)
            Yother = np.resize(Yother, kcnt)
            Ylhs = np.resize(Ylhs, kcnt)
            Yhs = np.resize(Yhs, kcnt)
            Ymhs = np.resize(Ymhs, kcnt)
            Yba = np.resize(Yba, kcnt)

            xA = np.resize(xA, (kcnt, numVars))

#  *****************   calculate simple regresion    
#            try:
            if kcnt>-1:
                r2, coef = simple(xA, YperCap)
                ttext = printString('Simple', state, 'PerCap', r2, coef)
                fOut1.write(ttext)

                r2, coef = simple(xA, Yage)
                ttext = printString('Simple', state, 'Age', r2, coef)
                fOut1.write(ttext)

                r2, coef = simple(xA, Ywhit)
                ttext = printString('Simple', state, 'White', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = simple(xA, Yblk)
                ttext = printString('Simple', state, 'Black', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = simple(xA, Yind)
                ttext = printString('Simple', state, 'Indian', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = simple(xA, Yasia)
                ttext = printString('Simple', state, 'Asian', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = simple(xA, Yother)
                ttext = printString('Simple', state, 'Other', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = simple(xA, Ylhs)
                ttext = printString('Simple', state, 'lessHS', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = simple(xA, Yhs)
                ttext = printString('Simple', state, 'HS', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = simple(xA, Ymhs)
                ttext = printString('Simple', state, 'moreHS', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = simple(xA, Yba)
                ttext = printString('Simple', state, 'BA', r2, coef)
                fOut1.write(ttext)
#            except:
#                continue
   
#  *****************   calculate ridge regresion
            try:
                r2, coef = ridge(xA, YperCap)
                ttext = printString('Ridge', state, 'PerCap', r2, coef)
                fOut1.write(ttext)

                r2, coef = ridge(xA, Yage)
                ttext = printString('Ridge', state, 'Age', r2, coef)
                fOut1.write(ttext)

                r2, coef = ridge(xA, Ywhit)
                ttext = printString('Ridge', state, 'White', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = ridge(xA, Yblk)
                ttext = printString('Ridge', state, 'Black', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = ridge(xA, Yind)
                ttext = printString('Ridge', state, 'Indian', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = ridge(xA, Yasia)
                ttext = printString('Ridge', state, 'Asian', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = ridge(xA, Yother)
                ttext = printString('Ridge', state, 'Other', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = ridge(xA, Ylhs)
                ttext = printString('Ridge', state, 'lessHS', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = ridge(xA, Yhs)
                ttext = printString('Ridge', state, 'HS', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = ridge(xA, Ymhs)
                ttext = printString('Ridge', state, 'moreHS', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = ridge(xA, Yba)
                ttext = printString('Ridge', state, 'BA', r2, coef)
                fOut1.write(ttext)
            except:
                continue
     
#  *****************   calculate lasso regresion
            try:
                r2, coef = lasso(xA, YperCap)
                ttext = printString('Lasso', state, 'PerCap', r2, coef)
                fOut1.write(ttext)

                r2, coef = lasso(xA, Yage)
                ttext = printString('Lasso', state, 'Age', r2, coef)
                fOut1.write(ttext)

                r2, coef = lasso(xA, Ywhit)
                ttext = printString('Lasso', state, 'White', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = lasso(xA, Yblk)
                ttext = printString('Lasso', state, 'Black', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = lasso(xA, Yind)
                ttext = printString('Lasso', state, 'Indian', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = lasso(xA, Yasia)
                ttext = printString('Lasso', state, 'Asian', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = lasso(xA, Yother)
                ttext = printString('Lasso', state, 'Other', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = lasso(xA, Ylhs)
                ttext = printString('Lasso', state, 'lessHS', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = lasso(xA, Yhs)
                ttext = printString('Lasso', state, 'HS', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = lasso(xA, Ymhs)
                ttext = printString('Lasso', state, 'moreHS', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = lasso(xA, Yba)
                ttext = printString('Lasso', state, 'BA', r2, coef)
                fOut1.write(ttext)
            except:
                continue
 
#  *****************   calculate elastic net regresion
            try:
                r2, coef = elasticNet(xA, YperCap)
                ttext = printString('EN', state, 'PerCap', r2, coef)
                fOut1.write(ttext)

                r2, coef = elasticNet(xA, Yage)
                ttext = printString('EN', state, 'Age', r2, coef)
                fOut1.write(ttext)

                r2, coef = elasticNet(xA, Ywhit)
                ttext = printString('EN', state, 'White', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = elasticNet(xA, Yblk)
                ttext = printString('EN', state, 'Black', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = elasticNet(xA, Yind)
                ttext = printString('EN', state, 'Indian', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = elasticNet(xA, Yasia)
                ttext = printString('EN', state, 'Asian', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = elasticNet(xA, Yother)
                ttext = printString('EN', state, 'Other', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = elasticNet(xA, Ylhs)
                ttext = printString('EN', state, 'lessHS', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = elasticNet(xA, Yhs)
                ttext = printString('EN', state, 'HS', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = elasticNet(xA, Ymhs)
                ttext = printString('EN', state, 'moreHS', r2, coef)
                fOut1.write(ttext)
    
                r2, coef = elasticNet(xA, Yba)
                ttext = printString('EN', state, 'BA', r2, coef)
                fOut1.write(ttext)
            except:
                continue
    fOut1.close()  

if __name__ == "__main__":
    for i in range(len(files)):
        doWork(files[i], names[i])
        
    end = time.time()
    print('\nProcessing time',round(end - start,2), 'seconds')
