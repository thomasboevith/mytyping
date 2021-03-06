#!/usr/bin/env python2
# Get, store, and visualize Typeracer results
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import requests
import shutil
import sys
import time


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


# Get data
url = "http://data.typeracer.com/games?playerId=tr:skrivemaskinen&n=999999999"
r = requests.get(url)
status_code = r.status_code
if status_code == 404:
    print('ERROR: status code: %s Not Found' % status_code)
    sys.exit(1)

content = r.content

# Store data
outfile = 'data/data.json'
f = open(outfile, 'w')
f.write(content)
f.close()

# Compute statistics
with open(outfile) as datafile:
    data = json.load(datafile)

# Words per minute
wpm = [d['wpm'] for d in data]
wpm = np.asarray(list(reversed(wpm)))
window_size = 5
wpm_moving_avg = moving_average(wpm, n=window_size)
recent_mean = np.mean(wpm[-10:])

outplotfile = 'plot/newest.png'
fig, ax = plt.subplots(nrows=1, ncols=1)
today = time.strftime("%Y%m%d")
plt.title("Typing Speed in TyperRacer, %s (Recent avg.=%i)" \
          % (today, recent_mean), fontsize=13)
plt.xlabel("\nRace no.", fontsize=10)
plt.ylabel("Words per minute (5 chars/word)", fontsize=10)
plt.plot(wpm, color='#cccccc')
plt.plot(wpm_moving_avg, color='#000000', \
             label='Moving avg. (n=%s)' % window_size)
plt.legend(prop={'size': 9})
fig.savefig(outplotfile)
plt.close(fig)
