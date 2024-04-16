#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Distance comparison across blind spot
TWCF IIT vs PP experiment 2a
Adapted from 'final before eye-tracking' code to work on both Glasgow and Toronto sites
"""


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

######
#### Initialize experiment
######

def doDistanceTask(ID=None, hemifield=None, location=None):
    ## parameters
    nRevs   = 10   #
    nTrials = 30  # at least 10 reversals and 30 trials for each staircase (~ 30*8 staircases = 250 trials)
    letter_height = 1

    
    # site specific handling
    if location == None:
        if os.sys.platform == 'linux':
            location = 'toronto'
        else:
            location = 'glasgow'

    if location == 'glasgow':
        
        ## path
        expInfo = {'ID':'test', 'hemifield':['left','right']}
        dlg = gui.DlgFromDict(expInfo, title='Infos', screen=0)
        ID = expInfo['ID'].lower()
        hemifield = expInfo['hemifield']
        
        main_path = '../data/distance/'
        data_path = main_path
        eyetracking_path = main_path + 'eyetracking/' + ID + '/'
        
        os.makedirs(data_path, exist_ok=True)
        os.makedirs(eyetracking_path, exist_ok=True)
        
        x = 1
        filename = ID + '_dist_' + ('LH' if hemifield == 'left' else 'RH') + '_'
        while (filename + str(x) + '.txt') in os.listdir(data_path):
            x += 1
        y = 1
        et_filename = ID + '_dist_' + ('LH' if hemifield == 'left' else 'RH') + '_'
        while len(glob(eyetracking_path + et_filename + str(y) + '.*')):
            y += 1
        
        ## blindspot
        bs_file = open(glob(main_path + 'mapping/' + ID + '_LH_blindspot*.txt')[-1], 'r')
        bs_param = bs_file.read().replace('\t','\n').split('\n')
        bs_file.close()
        spot_left_cart = eval(bs_param[1])
        spot_left = cart2pol(spot_left_cart[0], spot_left_cart[1])
        spot_left_size = eval(bs_param[3])
    
        bs_file = open(glob(main_path + 'mapping/' + ID + '_RH_blindspot*.txt')[-1],'r')
        bs_param = bs_file.read().replace('\t','\n').split('\n')
        bs_file.close()
        spot_righ_cart = eval(bs_param[1])
        spot_righ = cart2pol(spot_righ_cart[0], spot_righ_cart[1])
        spot_righ_size = eval(bs_param[3])
    
        if hemifield == 'left':
            spot_cart = spot_left_cart
            spot      = spot_left
            spot_size = spot_left_size
        else:
            spot_cart = spot_righ_cart
            spot      = spot_righ
            spot_size = spot_righ_size
    
        '''
        distance of reference between dots (target)
        => width of blindspot + 2 (dot width, padding) + 2 (to account for a max jitter of 1 on either side)
        '''
        tar =  spot_size[0] + 2 + 2
    
        # size of blind spot + 2 (dot width, padding)
        if hemifield == 'left' and spot_cart[1] < 0:
            ang_up = (cart2pol(spot_cart[0], spot_cart[1] - spot_size[1])[0] - spot[0]) + 2
        else:
            ang_up = (cart2pol(spot_cart[0], spot_cart[1] + spot_size[1])[0] - spot[0]) + 2
    
        ## colours
        col_file = open(glob(main_path + 'color/' + ID + '_col_cal*.txt')[-1],'r')
        col_param = col_file.read().replace('\t','\n').split('\n')
        col_file.close()
        col_ipsi = eval(col_param[3]) if hemifield == 'left' else eval(col_param[5]) # left or right
        col_cont = eval(col_param[5]) if hemifield == 'left' else eval(col_param[3]) # right or left
        col_back = [ 0.55,  0.45, -1.00]  #changed by belen to prevent red bleed
        col_both = [eval(col_param[3])[1], eval(col_param[5])[0], -1] 
    
        ## window & elements
        win = visual.Window([1500,800],allowGUI=True, monitor='ExpMon',screen=1, units='deg', viewPos = [0,0], fullscr = True, color= col_back)
        win.mouseVisible = False
        fixation = visual.ShapeStim(win, vertices = ((0, -2), (0, 2), (0,0), (-2, 0), (2, 0)), lineWidth = 4, units = 'pix', size = (10, 10), closeShape = False, lineColor = col_both)
    
        hiFusion = fusionStim(win = win, pos = [0, 7], colors = [col_both,col_back])
        loFusion = fusionStim(win = win, pos = [0,-7], colors = [col_both,col_back]) 
        
        blindspot = visual.Circle(win, radius = .5, pos = [7,0], units = 'deg', fillColor=col_ipsi, lineColor = None)
        blindspot.pos = spot_cart
        blindspot.size = spot_size
        
        ## eyetracking
        colors = {'both'   : col_both,
                  'back'   : col_back} 
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
        
    elif location == 'toronto':
    
        # not sure what you want to do here, maybe check if parameters are defined, otherwise throw an error? Or keep the gui in that case?
        
        
        expInfo = {}
        askQuestions = False
        if ID == None:
            expInfo['ID'] = ''
            askQuestions = True
        if hemifield == None:
            expInfo['hemifield'] = ['left','right']
            askQuestions = True
        if askQuestions:
            dlg = gui.DlgFromDict(expInfo, title='Infos', screen=0)

        if ID == None:
            ID = expInfo['ID'].lower()
        if hemifield == None:
            hemifield = expInfo['hemifield']
        
        ## path
        main_path = '../data/distance/'
        data_path = main_path
        eyetracking_path = main_path + 'eyetracking/' + ID + '/'
        x = 1
        filename = ID + '_dist_' + ('LH' if hemifield == 'left' else 'RH') + '_'
        while (filename + str(x) + '.txt') in os.listdir(data_path):
            x += 1
        y = 1
        et_filename = ID + '_dist_' + ('LH' if hemifield == 'left' else 'RH') + '_'
        while len(glob(eyetracking_path + et_filename + str(y) + '.*')):
            y += 1
        
        # this _should_ already be handled by the Runner utility: setupDataFolders()
        os.makedirs(data_path, exist_ok=True)
        os.makedirs(eyetracking_path, exist_ok=True)
        

        
        trackEyes = [True, True]
        
        # get everything shared from central:
        setup = localizeSetup(location=location, trackEyes=trackEyes, filefolder=eyetracking_path, filename=et_filename+str(y), task='distance', ID=ID) # data path is for the mapping data, not the eye-tracker data!
    
        # unpack all this
        win = setup['win']
    
        colors = setup['colors']
        col_both = colors['both']
        if hemifield == 'left':
            col_ipsi, col_contra = colors['left'], colors['right']
        if hemifield == 'right':
            col_contra, col_ipsi = colors['left'], colors['right']
    
        hiFusion = setup['fusion']['hi']
        loFusion = setup['fusion']['lo']
    
        blindspot = setup['blindspotmarkers'][hemifield]
        
        fixation = setup['fixation']
    
        tracker = setup['tracker']
        
    else:
        raise ValueError("Location should be 'glasgow' or 'toronto', was {}".format(location))


    # create output file:
    respFile = open(data_path + filename + str(x) + '.txt','w')
    respFile.write(''.join(map(str, ['Start: \t' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M') + '\n'])))
    respFile.write('\t'.join(map(str, ['Resp',
                                    'Targ_loc',
                                    'Foil_loc',
                                    'Targ_len',
                                    'Difference',
                                    'Which_first',
                                    'Targ_chosen',
                                    'Reversal',
                                    'Foil_type',
                                    'Eye',
                                    'Gaze_out',
                                    'Stair',
                                    'Trial'])) + '\n')
    respFile.close()
    print(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
    print("Resp",
        "Targ_loc",
        "Foil_loc",
        "Targ_len",
        "Difference",
        "Which_first",
        "Targ_chosen",
        "Reversal",
        "Foil_type",
        "Eye",
        "Gaze_out",
        "Stair")

    gazeFile = open(eyetracking_path + filename + str(x) + '_gaze.txt','w')
    gazeFile.write("Trial\tStair\tTrial_stair\tTime\tGaze\n")
    gazeFile.close()

    ## instructions
    visual.TextStim(win,'Troughout the experiment you will fixate at a white cross that will be located at the center of the screen.\n \
    It is important that you fixate on this cross at all times.\n\n \
    You will be presented with pairs of dots. You will have to indicate which dots were closer together.\n\n \
    Left arrow = first pair of dots were closer together.\n\n \
    Right arrow = second pair of dots were closer together.\n\n\n \
    Press the space bar to start the experiment.', height = letter_height,wrapWidth=30, color = 'black').draw()
    win.flip()
    k = ['wait']
    while k[0] not in ['q','space']:
        k = event.waitKeys()
    if k[0] in ['q']:
        win.close()
        core.quit()


    ######
    #### Prepare stimulation
    ######

    ## stimuli
    point_1 = visual.Circle(win, radius = .5, pos = pol2cart(00, 3), units = 'deg', fillColor = col_both, lineColor = None)
    point_2 = visual.Circle(win, radius = .5, pos = pol2cart(00, 6), units = 'deg', fillColor = col_both, lineColor = None)
    point_3 = visual.Circle(win, radius = .5, pos = pol2cart(45, 3), units = 'deg', fillColor = col_both, lineColor = None)
    point_4 = visual.Circle(win, radius = .5, pos = pol2cart(45, 6), units = 'deg', fillColor = col_both, lineColor = None)

    blindspot.autoDraw = True 

    ## prepare trials
    positions = {
        "left-top": [(spot_left[0] - ang_up, spot_left[1] - tar/2), (spot_left[0] - ang_up, spot_left[1] + tar/2)],
        "left-mid": [(spot_left[0] +     00, spot_left[1] - tar/2), (spot_left[0] +     00, spot_left[1] + tar/2)],
        "left-bot": [(spot_left[0] + ang_up, spot_left[1] - tar/2), (spot_left[0] + ang_up, spot_left[1] + tar/2)],
        "righ-top": [(spot_righ[0] + ang_up, spot_righ[1] - tar/2), (spot_righ[0] + ang_up, spot_righ[1] + tar/2)],
        "righ-mid": [(spot_righ[0] +     00, spot_righ[1] - tar/2), (spot_righ[0] +     00, spot_righ[1] + tar/2)],
        "righ-bot": [(spot_righ[0] - ang_up, spot_righ[1] - tar/2), (spot_righ[0] - ang_up, spot_righ[1] + tar/2)],
    }

    if hemifield == 'left':
        # First column is target, second column is foil
        pos_array = [["left-mid", "left-top"],
                     ["left-mid", "left-bot"],
                     ["left-top", "left-bot"],
                     ["left-bot", "left-top"]]
    else:
        pos_array = [["righ-mid", "righ-top"],
                     ["righ-mid", "righ-bot"],
                     ["righ-top", "righ-bot"],
                     ["righ-bot", "righ-top"]]

    pos_array_bsa = pos_array[0:2]
    pos_array_out = pos_array[2:4]


    ######
    #### Prepare eye tracking
    ######

    ## setup and initialize eye-tracker
    tracker.initialize(calibrationScale=(0.35, 0.35))
    tracker.calibrate()
    win.flip()
    fixation.draw()
    win.flip()

    k = event.waitKeys()
    if k[0] in ['q']:
        respFile.close()
        win.close()
        core.quit()

    tracker.startcollecting()

    ######
    #### Staircase
    ######

    trial_clock = core.Clock()

    foil_type = [1, -1] * 4
    eye = ['left', 'left', 'right', 'right'] * 2
    pos_arrays = [pos_array_bsa[:]] * 4 + [pos_array_out[:]] * 4

    intervals = [3.5,3, 2.5, 2, 1.5, 1, .5, 0, -.5, -1, -1.5, -2, -2.5, -3, -3.5]
    position = [[]] * 8
    trial_stair = [0] * 8
    revs = [0] * 8
    direction = [1] * 8
    cur_int = [0] * 8
    reversal = False
    resps = [[True],[False]] * 4
    stairs_ongoing = [True] * 8

    trial = 1
    abort = False
    recalibrate = False

    while any(stairs_ongoing):

        increment = True

        ## choose staircase
        which_stair = random.choice(list(compress([x for x in range(len(stairs_ongoing))], stairs_ongoing)))

        ## set trial
        if position[which_stair] == []:
            random.shuffle(pos_arrays[which_stair])
            position[which_stair] = pos_arrays[which_stair][:]
        pos = position[which_stair].pop()

        shift = random.sample([-1, -.5, 0, .5, .1], 2)
        dif = intervals[cur_int[which_stair]] * foil_type[which_stair]
        which_first = random.choice(['Targ', 'Foil'])

        if which_first == 'Targ':
            point_1.pos = pol2cart(positions[pos[0]][0][0], positions[pos[0]][0][1]       + shift[0])
            point_2.pos = pol2cart(positions[pos[0]][1][0], positions[pos[0]][1][1]       + shift[0])
            point_3.pos = pol2cart(positions[pos[1]][0][0], positions[pos[1]][0][1]       + shift[1])
            point_4.pos = pol2cart(positions[pos[1]][1][0], positions[pos[1]][1][1] + dif + shift[1])
        else:
            point_3.pos = pol2cart(positions[pos[0]][0][0], positions[pos[0]][0][1]       + shift[0])
            point_4.pos = pol2cart(positions[pos[0]][1][0], positions[pos[0]][1][1]       + shift[0])
            point_1.pos = pol2cart(positions[pos[1]][0][0], positions[pos[1]][0][1]       + shift[1])
            point_2.pos = pol2cart(positions[pos[1]][1][0], positions[pos[1]][1][1] + dif + shift[1])

        if eye[which_stair] == hemifield:
            point_1.fillColor = col_ipsi
            point_2.fillColor = col_ipsi
            point_3.fillColor = col_ipsi
            point_4.fillColor = col_ipsi
        else:
            point_1.fillColor = col_cont
            point_2.fillColor = col_cont
            point_3.fillColor = col_cont
            point_4.fillColor = col_cont
        
        hiFusion.resetProperties()
        loFusion.resetProperties()
        
        gaze_out = False
        
        ## pre trial fixation
        tracker.comment('pre-fixation')
        if not tracker.waitForFixation(fixationStimuli = [fixation, hiFusion, loFusion]):
            recalibrate = True
            gaze_out = True
        
        gazeFile = open(eyetracking_path + filename + str(x) + '_gaze.txt','a')
        if not gaze_out:
            ## trial
            stim_comments = ['pair 2 off', 'pair 1 off', 'pair 2 on', 'pair 1 on']
            tracker.comment('start trial %d'%(trial))
            trial_clock.reset()
        
            while trial_clock.getTime() < 1.3 and not abort:
                t = trial_clock.getTime()
                
                gazeFile.write('\t'.join(map(str, [trial,
                               which_stair,
                               trial_stair[which_stair] + 1,
                               round(t,2),
                               tracker.lastsample()])) + "\n")
                
                
                if not tracker.gazeInFixationWindow():
                    gaze_out = True
                    break
                    
                hiFusion.draw()
                loFusion.draw()
                fixation.draw()
        
                if .1 <= trial_clock.getTime() < .5:
                    if len(stim_comments) == 4:
                        tracker.comment(stim_comments.pop()) # pair 1 on
                    point_1.draw()
                    point_2.draw()
                elif .5 <= trial_clock.getTime() < 0.9:
                    if len(stim_comments) == 3:
                        tracker.comment(stim_comments.pop()) # pair 2 on
                    point_1.draw()
                    point_2.draw()
                    point_3.draw()
                    point_4.draw()
                elif 0.9 <= trial_clock.getTime() < 1.3:
                    if len(stim_comments) == 2:
                        tracker.comment(stim_comments.pop()) # pair 1 off
                    point_3.draw()
                    point_4.draw()
        
                win.flip()
                
                
                k = event.getKeys(['q'])
                if k and 'q' in k:
                    abort = True
                    break
            
            if len(stim_comments) == 1:
                tracker.comment(stim_comments.pop()) # pair 2 off
            gazeFile.close()

        if abort:
            break
        
        if not gaze_out:
        
            ## response
            fixation.ori += 45
            fixation.color = 'black'
            hiFusion.draw()
            loFusion.draw()
            fixation.draw()
            win.flip()
            
            k = ['wait']
            while k[0] not in ['q', 'space', 'left', 'right']:
                k = event.waitKeys()
            if k[0] in ['q']:
                abort = True
                break
            elif k[0] in ['space']:
                tracker.comment('manually aborted trial')
                position[which_stair] = position[which_stair] + [pos]
                increment = False
                resp = 'abort'
                targ_chosen = 'abort'
                reversal = 'abort'
            else:
                resp = 1 if k[0] == 'left' else 2
                tracker.comment('response %d'%(resp))
                
            fixation.ori -= 45
            
        else:
        
            ## dealing with auto-aborted trials
        
            # auto recalibrate if no initial fixation
            if recalibrate:
                recalibrate = False
                tracker.calibrate()
                win.flip()
                fixation.draw()
                win.flip()
                k = event.waitKeys()
                if k[0] in ['q']:
                    abort = True
                    break
            
            # changing fixation to signify gaze out, restart with 'up' possibily of break and manual recalibration 'r' 
            else:
                hiFusion.draw()
                loFusion.draw()
                visual.TextStim(win, '#', height = letter_height, color = col_both).draw()
                win.flip()
                k = ['wait']
                while k[0] not in ['q', 'up', 'r']:
                    k = event.waitKeys()
                if k[0] in ['q']:
                    abort = True
                    break
        
                # manual recalibrate
                if k[0] in ['r']:
                    tracker.calibrate()
                    win.flip()
                    fixation.draw()
                    win.flip()
                    k = event.waitKeys()
                    if k[0] in ['q']:
                        abort = True
                        break
                
            position[which_stair] = position[which_stair] + [pos]
            increment = False
            resp = 'auto_abort'
            targ_chosen = 'auto_abort'
            reversal = 'auto_abort'
        
        if increment:
            '''
            which_first == 'Targ'          => was target first? (True/False)
            dif > 0                        => was target smaller? (True/False)
            k[0] == 'left'                 => was first chosen? (True/False)
            target first == target smaller => was first smaller? (True/False)
            first smaller == first chosen  => was smaller chosen? (True/False)
            
            (which_first == 'Targ') == (k[0] == 'left') => was target chosen?
            '''
            
            targ_chosen = (which_first == 'Targ') == (k[0] == 'left')

            ## update staircase (which direction, is there a reversal?)
            reversal = False
            resps[which_stair] = resps[which_stair] + [targ_chosen]
            if  resps[which_stair][-2] != resps[which_stair][-1]:
                reversal = True
                direction[which_stair] *= -1
                revs[which_stair] += len(resps[which_stair]) > 2
                
            ## increment/update
            cur_int[which_stair] = max(min(cur_int[which_stair] + direction[which_stair], len(intervals) - 1), 0)
            trial_stair[which_stair] = trial_stair[which_stair] + 1
            stairs_ongoing[which_stair] = revs[which_stair] <= nRevs or trial_stair[which_stair] < nTrials

        ## print trial
        print(resp,
            pos[0],
            pos[1],
            tar,
            dif,
            which_first,
            targ_chosen,
            reversal,
            foil_type[which_stair],
            eye[which_stair],
            gaze_out,
            which_stair)
        respFile = open(data_path + filename + str(x) + '.txt','a')
        respFile.write('\t'.join(map(str, [resp,
                                        pos[0],
                                        pos[1],
                                        tar,
                                        dif,
                                        which_first,
                                        targ_chosen,
                                        reversal,
                                        foil_type[which_stair],
                                        eye[which_stair],
                                        gaze_out,
                                        which_stair,
                                        trial])) + "\n")
        respFile.close()
        trial += 1

    if abort:
        respFile = open(data_path + filename + str(x) + '.txt','a')
        respFile.write("Run manually ended at " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + "!")
        respFile.close()
        tracker.comment("Run manually ended at " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + "!")
    elif not any(stairs_ongoing):
        print('run ended properly!')
        tracker.comment('run ended properly!')
    else:
        print('something weird happened')

    print(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
    blindspot.autoDraw = False

    ## last screen
    visual.TextStim(win,'Run ended.', height = letter_height, color = 'black').draw()
    win.flip()
    k = event.waitKeys()

    tracker.shutdown()
    win.close()
    core.quit()

if __name__ == "__main__":
    doDistanceTask()