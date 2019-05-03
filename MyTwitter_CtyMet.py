# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 07:56:21 2018

pull statistics by county stats on
"""
import time
import numpy

start = time.time()

pathFileOut = "[your file location]"
fOut = open(pathFileOut,'w')

#  load GeoIds
pathFileGeo = "[your file location]"
fGeo = open(pathFileGeo, 'r+')
geoID, county = [], []
for line in fGeo:
    line = line.strip()
    ffields = line.split('|')
    geoID.append(int(ffields[2]))
    county.append(ffields[1])
fGeo.close()

#  load data to process
pathFileMaster = "[your file location]"
fIn = open(pathFileMaster, 'r+')
nname, geoIDF, lat, lon, mood, re, grade, dw, pol, sub, modal, ent = [], [], [],  [], [], [], [], [], [], [], [], []
aux, conj, det, intt, prep, pro = [], [], [], [], [], []
icnt = 0
for line in fIn:
    icnt = icnt + 1
    if icnt > 1:
        line = line.strip()
        ffields = line.split('|')
        nname.append(ffields[4])
        geoIDF.append(int(ffields[24]))
        lat.append(float(ffields[29]))
        lon.append(float(ffields[30]))
        mood.append(float(ffields[23]))
        re.append(float(ffields[10]))
        grade.append(float(ffields[11]))
        dw.append(float(ffields[12]))
        pol.append(float(ffields[13]))
        sub.append(float(ffields[14]))
        modal.append(float(ffields[15]))
        ent.append(float(ffields[16]))
        aux.append(float(ffields[17]))
        conj.append(float(ffields[18]))
        det.append(float(ffields[19]))
        intt.append(float(ffields[20]))
        prep.append(float(ffields[21]))
        pro.append(float(ffields[22]))
fIn.close()

# pull stats by county and summarize
#  process one county at a time 
icnt=0
for iii in range(len(geoID)):
    icnt = icnt + 1
#    if icnt>1: break
    
    nnameT, moodT, reT, gradeT, dwT, polT, subT, modalT, entT = [], [], [], [], [], [], [], [], []
    auxT, conjT, detT, inttT, prepT, proT = [], [], [], [], [], []
    x = [ii for ii, xx in enumerate(geoIDF) if xx == geoID[iii]]

    for i in range(len(x)):
        nnameT.append(nname[x[i]])
        moodT.append(mood[x[i]])
        reT.append(re[x[i]])
        gradeT.append(grade[x[i]])
        dwT.append(dw[x[i]])
        polT.append(pol[x[i]])
        subT.append(sub[x[i]])
        modalT.append(modal[x[i]])
        entT.append(ent[x[i]])
        auxT.append(aux[x[i]])
        conjT.append(conj[x[i]])
        detT.append(det[x[i]])
        inttT.append(intt[x[i]])
        prepT.append(prep[x[i]])
        proT.append(pro[x[i]])
    try:
        a = set(nnameT)
        line = ''
        line = str(geoID[iii]) + '|'+ county[iii] + '|' + str(len(x)) + '|' 
        line = line + str(lat[x[0]]) + '|' + str(lon[x[0]]) + '|' 
        line = line + str(len(a)) + '|' + str(numpy.mean(moodT)) + '|'  + str(numpy.mean(reT)) + '|'
        line = line + str(numpy.mean(gradeT)) + '|' + str(numpy.mean(dwT)) + '|' + str(numpy.mean(polT)) + '|'
        line = line + str(numpy.mean(subT)) + '|' + str(numpy.mean(modalT)) + '|' + str(numpy.mean(entT)) + '|'
        line = line + str(numpy.mean(auxT)) + '|' + str(numpy.mean(conjT)) + '|' + str(numpy.mean(detT)) + '|'
        line = line + str(numpy.mean(inttT)) + '|' + str(numpy.mean(prepT)) + '|' + str(numpy.mean(proT)) + '|'

        line = line + str(numpy.var(moodT)) + '|'  + str(numpy.var(reT)) + '|'
        line = line + str(numpy.var(gradeT)) + '|' + str(numpy.var(dwT)) + '|' + str(numpy.var(polT)) + '|'
        line = line + str(numpy.var(subT)) + '|' + str(numpy.var(modalT)) + '|' + str(numpy.var(entT)) + '|'
        line = line + str(numpy.var(auxT)) + '|' + str(numpy.var(conjT)) + '|' + str(numpy.var(detT)) + '|'
        line = line + str(numpy.var(inttT)) + '|' + str(numpy.var(prepT)) + '|' + str(numpy.var(proT))

        line = line + '\n'
        fOut.write(line)
    except:
        print(county[iii])

fOut.close()

end = time.time()
print(end - start)