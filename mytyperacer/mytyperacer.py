#!/usr/bin/env python2
import json
import numpy as np
import matplotlib.pyplot as plt
import os
import requests
import sys
import time

username = 'skrivemaskinen'

url = "http://data.typeracer.com/games?playerId=tr:skrivemaskinen&n=99999999&offset=0"
r = requests.get(url)
status_code = r.status_code
if status_code == 404:
    print('ERROR: status code: %s Not Found' % status_code)
    sys.exit(1)

content = r.content
outfile = 'data/data_' + time.strftime("%Y%m%d") + '.json'
if not os.path.isfile(outfile):
    f = open(outfile, 'w')
    f.write(content)
    f.close()

with open(outfile) as datafile:
    data = json.load(datafile)

wpm = []
for i, d in enumerate(data):
    wpm.append(d['wpm'])

wpm = np.asarray(list(reversed(wpm)))
min=np.min(wpm)
max=np.max(wpm)
median=np.median(wpm)
mean=np.mean(wpm)
window=5
recent_mean=np.mean(wpm[-10:])

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

outplotfile = 'plot/' + os.path.splitext(os.path.basename(outfile))[0] + '.png'
fig, ax = plt.subplots( nrows=1, ncols=1 )
plt.title("Typing Speed in TyperRacer (Recent avg=%i)" % recent_mean, fontsize=13)
plt.xlabel("\nRace no.", fontsize=10)
plt.ylabel("Words per minute (5 chars/word)", fontsize=10)
plt.plot(wpm, color='#cccccc')
plt.plot(moving_average(wpm, n=window), color='#000000', label='Moving avg. (n=%s)' % window)
plt.legend()
plt.legend(prop={'size':9})
fig.savefig(outplotfile)
plt.close(fig)
