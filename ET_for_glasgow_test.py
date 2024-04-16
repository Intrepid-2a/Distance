 #!/usr/bin/env python
# -*- coding: utf-8 -*-

import psychopy
from psychopy import core, visual, gui, data, event
from psychopy.tools.coordinatetools import pol2cart, cart2pol
import numpy as np
import random, datetime, os
from glob import glob
from itertools import compress

import sys, os
sys.path.append(os.path.join('..', 'EyeTracking'))
from EyeTracking import localizeSetup, EyeTracker, fusionStim


## path
expInfo = {'ID':'test', 'hemifield':['left','right']}
dlg = gui.DlgFromDict(expInfo, title='Infos', screen=0)
ID = expInfo['ID'].lower()
hemifield = expInfo['hemifield']

main_path = '../data/distance/'
data_path = main_path
eyetracking_path = main_path + 'eyetracking/' + ID + '/'

#[head, tail] = os.path.split(os.getcwd())
#data_path = os.path.join(head, 'data', 'distance')
#eyetracking_path = os.path.join(data_path, 'eyetracking', ID)

os.makedirs(data_path, exist_ok=True)
os.makedirs(eyetracking_path, exist_ok=True)

y = 1
et_filename = ID + '_dist_' + ('LH' if hemifield == 'left' else 'RH') + '_'
while len(glob(eyetracking_path + et_filename + str(y) + '.*')):
    y += 1

col_back = [ 0.55,  0.45, -1.00]  #changed by belen to prevent red bleed
col_both = [1,1,1]

## window & elements
win = visual.Window([1500,800],allowGUI=True, monitor='ExpMon',screen=1, units='deg', viewPos = [0,0], fullscr = True, color= col_back)
win.mouseVisible = False

fixation_yes = visual.ShapeStim(win, vertices = ((0, -2), (0, 2), (0,0), (-2, 0), (2, 0)), lineWidth = 2, units = 'pix', size = (10, 10), closeShape = False, lineColor = col_both)
fixation_no  = visual.ShapeStim(win, vertices = ((0, -2), (0, 2), (0,0), (-2, 0), (2, 0)), lineWidth = 2, units = 'pix', size = (10, 10), closeShape = False, lineColor = col_both, ori = -45)
fixation = fixation_yes


colors = {'both'   : col_both,
          'back'   : col_back} 
## eyetracking
tracker = EyeTracker(tracker           = 'eyelink',
                     trackEyes         = [True, True],
                     fixationWindow    = 2.0,
                     minFixDur         = 0.2,
                     fixTimeout        = 3.0,
                     psychopyWindow    = win,
                     filefolder        = eyetracking_path,
                     filename          = et_filename+str(y),
                     samplemode        = 'average',
                     calibrationpoints = 5,
                     colors            = colors)                            

visual.TextStim(win,'screen 1').draw()
win.flip()
event.waitKeys()

## setup and initialize eye-tracker
tracker.initialize(calibrationScale=(0.35, 0.35))

visual.TextStim(win,'screen 2').draw()
win.flip()
event.waitKeys()

tracker.calibrate()

visual.TextStim(win,'screen 3').draw()
win.flip()
event.waitKeys()

tracker.startcollecting()

good_fixation = tracker.waitForFixation()

print('Good fixation? {}'.format(good_fixation))

visual.TextStim(win,'screen 4').draw()
win.flip()
event.waitKeys()

while 1:
    k = event.getKeys(['space', 'escape'])

    if k:
        break
    
    if tracker.gazeInFixationWindow(fixationStimuli = fixation_yes):
        fixation = fixation_yes
    else:
        fixation = fixation_no
        
    fixation.draw()
    win.flip()

tracker.comment('testing comments')

tracker.shutdown()
win.close()
core.quit()
