# -*- coding: utf-8 -*-
'''
Created on Sat Oct 20 14:58:26 2018

use the scipy list of distributions to find the best fit for the data
'''
import time
import scipy.stats
import numpy as np
import warnings
import matplotlib.pyplot as plt
import pandas as pd
import math

sstart = time.time()
print('')

pathFileOut = 'where you want the output file to be'
fOut = open(pathFileOut,'w')

#  load all the distributions in scipy
cdfs = [
        'alpha',                #  alpha
        'anglit',               #  anglit
        'arcsine',              #  arcsine
        'argus',                #  Argus distribution
        'beta',                 #  beta
        'betaprime',            #  beta prime
        'bradford',             #  Bradford
        'burr',                 #  Burr (Type III)
        'burr12',               #  Burr (Type XII)
        'cauchy',               #  Cauchy
        'chi',                  #  chi
        'chi2',                 #  chi-squared
        'cosine',               #  cosine
        'dgamma',               #  double gamma
        'dweibull',             #  double Weibull
        'erlang',               #  Erlang
        'expon',                #  exponential
        'exponnorm',            #  exponentially modified Normal
        'exponweib',            #  exponentiated Weibull
        'exponpow',             #  exponential power
        'f',                    #  F
        'fatiguelife',          #  fatigue-life (Birnbaum-Saunders)
        'fisk',                 #  Fisk
        'foldcauchy',           #  folded Cauchy
        'foldnorm',             #  folded normal
        'frechet_r',            #  Frechet right (or Weibull minimum)
        'frechet_l',            #  Frechet left (or Weibull maximum)
        'genlogistic',          #  generalized logistic
        'gennorm',              #  generalized normal
        'genpareto',            #  generalized Pareto
        'genexpon',             #  generalized exponential
        'genextreme',           #  generalized extreme value
        'gausshyper',           #  Gauss hypergeometric
        'gamma',                #  gamma
        'gengamma',             #  generalized gamma
        'genhalflogistic',      #  generalized half-logistic
        'gilbrat',              #  Gilbrat
        'gompertz',             #  Gompertz (or truncated Gumbel)
        'gumbel_r',             #  right-skewed Gumbel
        'gumbel_l',             #  left-skewed Gumbel
        'halfcauchy',           #  Half-Cauchy
        'halflogistic',         #  half-logistic
        'halfnorm',             #  half-normal
        'halfgennorm',          #  The upper half of a generalized normal
        'hypsecant',            #  hyperbolic secant
        'invgamma',             #  inverted gamma
        'invgauss',             #  inverse Gaussicontinuous random variable
        'invweibull',           #  inverted Weibull
        'johnsonsb',            #  Johnson SB
        'johnsonsu',            #  Johnson SU
        'kappa4',               #  Kappa 4 parameter distribution
        'kappa3',               #  Kappa 3 parameter distribution
        'ksone',                #  General Kolmogorov-Smirnov one-sided test
        'kstwobign',            #  Kolmogorov-Smirnov two-sided test for large N
        'laplace',              #  Laplace
        'levy',                 #  Levy
        'levy_l',               #  left-skewed Levy
#        'levy_stable',          #  Levy-stable
        'logistic',             #  logistic (or Sech-squared)
        'loggamma',             #  log gamma
        'loglaplace',           #  log-Laplace
        'lognorm',              #  lognormal
        'lomax',                #  Lomax (Pareto of the second kind)
        'maxwell',              #  Maxwell
        'mielke',               #  Mielke’s Beta-Kappa
        'nakagami',             #  Nakagami
        'ncx2',                 #  non-central chi-squared
        'ncf',                  #  non-central F distribution
        'nct',                  #  non-central Student’s T
        'norm',                 #  normal
        'pareto',               #  Pareto
        'pearson3',             #  pearson type III
        'powerlaw',             #  power-function
        'powerlognorm',         #  power log-normal
        'powernorm',            #  power normal
        'rdist',                #  R-distributed
        'reciprocal',           #  reciprocal
        'rayleigh',             #  Rayleigh
        'rice',                 #  Rice
        'recipinvgauss',        #  reciprocal inverse Gaussicontinuous random variable
        'semicircular',         #  semicircular
        'skewnorm',             #  skew-normal random variable
        't',                    #  Student’s T
        'trapz',                #  trapezoidal
        'triang',               #  triangular
        'truncexpon',           #  truncated exponential
        'truncnorm',            #  truncated normal
        'tukeylambda',          #  Tukey-Lamdba
        'uniform',              #  uniform
        'vonmises',             #  Von Mises
        'vonmises_line',        #  Von Mises
        'wald',                 #  Wald
        'weibull_min',          #  Frechet right (or Weibull minimum)
        'weibull_max',          #  Frechet left (or Weibull maximum)
        'wrapcauchy'           #  wrapped Cauchy
]

#  load the data to be fitted
pathFileMaster = 'input data to be fitted'
fIn = open(pathFileMaster, 'r+')
icnt, ddata = [0 , np.zeros(10000)]   #  create and array bigger than the number of data point
for line in fIn:
    line = line.strip()
    ddata[icnt] = float(line)
    icnt = icnt + 1
fIn.close()
ddata = np.resize(ddata,icnt)   # resize the np array
size, xMin, xMax = icnt, int(np.min(ddata)), int(np.max(ddata))     # size is the number of points; llimit is the number of bins to use
if xMax > 250:  #  can play with this a bit; more for visual
    llimit = xMax 
else: llimit = xMax

#  cycle through all the distributions in scipy
D_save, p_save, icnt = [math.inf, math.inf, 0]
cdf_list, D_list = [], []
cdf_save = ''
for cdf in cdfs:
#    print(cdf)
    icnt = icnt + 1
    if icnt  > 0: 
            with warnings.catch_warnings():     # Ignore warnings from data that can't be fit
                warnings.filterwarnings('ignore')
                parameters = eval('scipy.stats.'+cdf+'.fit(ddata)')  #  fit the data set against every probability distribution

                D, p = scipy.stats.kstest(ddata, cdf, args=parameters)  #  apply the Kolmogorov-Smirnov one sided test
                D, p = [round(D,2), round(p,2)]     # keep the outpu visually appealing
                
#  add the code at the end here to plot distributions as you go
#  set up and write the output to be looked out after complete
                ttext = ''
                for i in range(len(parameters)):
                    ttext = ttext + str(round(parameters[i],2)) + '|'
                ttext = cdf + '|' + str(D) + '|' + str(p) + '|' + ttext[0:len(ttext)-1] + '\n'
                fOut.write(ttext)
                D_list.append(D)
                cdf_list.append(cdf)
                if D < D_save:  #  save the best
                    D_save = D
                    p_save = p
                    cdf_save = cdf

#  show the best fits
plt.figure(figsize=(12,8))
h = plt.hist(ddata, bins=llimit, normed=True, alpha=0.5, color='C4')
cdf_list = []
cdf_list.append('nct')      #  after analyzing the output; I forced the distribution I wanted; substitude D_Save to get the best
for i in range(len(cdf_list)):  # set it up so I could process as many distributions I wanted on output
            with warnings.catch_warnings():     # Ignore warnings from data that can't be fit
                cdf_save = cdf_list[i]

                dist = getattr(scipy.stats, cdf_save)
                param = dist.fit(ddata)
                arg = param[:-2]
                loc = param[-2]
                scale = param[-1]

# Get sane start and end points of distribution
                start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
                end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

# Build PDF and turn into pandas Series
                x = np.linspace(start, end, size)
                y = dist.pdf(x, loc=loc, scale=scale, *arg)
                pdf = pd.Series(y, x)
                ax = pdf.plot(lw=2, label=cdf_save, legend=True)

# plot the histogram and the fit
plt.legend(loc='upper right')
#plt.xlim(xMin, xMax)
plt.xlim(xMin, 50)
plt.xlabel('Mortality to Prescription Rate Ratio')
plt.ylabel('Probability')
plt.show()

#  clean up
print(xMax)
print(cdf_save, D_save, p_save)

fOut.close()
endd = time.time()
print('\nElapse Time:', round(endd - sstart,2))