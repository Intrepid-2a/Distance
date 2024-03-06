 #!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Distance comparison across blind spot
TWCF IIT vs PP experiment 2a piloting
Authors: Clement Abbatecola, Belén María Montabes de la Cruz
    Code version:
        2.1 # 2024/02/16    Common code for LH and RH
        2.0 # 2024/02/12    Final common version before eye tracking
"""


import psychopy
from psychopy import core, visual, gui, data, event, monitors
from psychopy.tools.coordinatetools import pol2cart, cart2pol
import numpy as np
import random, datetime, os
from glob import glob
from itertools import compress
# from fusion_stim import fusionStim

#!!# import eye tracking dependencies

import sys, os
sys.path.append(os.path.join('..', 'EyeTracking'))
from EyeTracking import localizeSetup, EyeTracker

# the following two imports are used when participants are to hold down a button... might not be necessary here
from psychopy.hardware import keyboard
from pyglet.window import key

######
#### Initialize experiment
######

def doDistanceTask(ID=None, hemifield=None):

    ## parameters
    nRevs   = 10   #
    nTrials = 30  # at least 10 reversals and 30 trials for each staircase (~ 30*8 staircases = 250 trials)
    letter_height = 40

    ## path
    # main_path = 'C:/Users/clementa/Nextcloud/project_blindspot/blindspot_eye_tracker/'
    main_path = ''
    data_path = main_path + '../data/distance/'
    os.makedirs(data_path, exist_ok=True)

    ## files
    expInfo = {}
    askQuestions = False
    if ID == None:
        expInfo['ID'] = ''
        askQuestions = True
    if hemifield == None:
        expInfo['hemifield'] = ['left','right']
        askQuestions = True
    # expInfo = {'ID':'test', 'hemifield':['left','right']}
    if askQuestions:
        dlg = gui.DlgFromDict(expInfo, title='Infos', screen=0)

    if ID == None:
        ID = expInfo['ID'].lower()
    if hemifield == None:
        hemifield = expInfo['hemifield']
        
    x = 1
    filename = 'dist_' + ('LH' if hemifield == 'left' else 'RH') + '_' + ID + '_'
    while (filename + str(x) + '.txt') in os.listdir(data_path):
        x += 1
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

    ## blindspot parameters
    # bs_file = open(glob(main_path + 'mapping_data/' + ID + '_LH_blindspot*.txt')[-1], 'r')
    bs_file = open(glob('../data/mapping/' + ID + '_LH_blindspot*.txt')[-1], 'r')
    bs_param = bs_file.read().replace('\t','\n').split('\n')
    bs_file.close()
    spot_left_cart = eval(bs_param[1])
    spot_left = cart2pol(spot_left_cart[0], spot_left_cart[1])
    spot_left_size = eval(bs_param[3])

    # bs_file = open(glob(main_path + 'mapping_data/' + ID + '_RH_blindspot*.txt')[-1],'r')
    bs_file = open(glob('../data/mapping/' + ID + '_RH_blindspot*.txt')[-1],'r')
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

    ## colour (eye) parameters
    # col_file = open(glob(main_path + 'mapping_data/' + ID + '_col_cal*.txt')[-1],'r')
    col_file = open(glob('../data/color/' + ID + '_col_cal*.txt')[-1],'r')
    col_param = col_file.read().replace('\t','\n').split('\n')
    col_file.close()
    col_ipsi = eval(col_param[3]) if hemifield == 'left' else eval(col_param[5]) # left or right
    col_cont = eval(col_param[5]) if hemifield == 'left' else eval(col_param[3]) # right or left
    # col_back = [ 0.5, 0.5,  -1.0]
    # col_both = [-0.7, -0.7, -0.7] 




    ## window & elements
    # win = visual.Window([1500,800],allowGUI=True, monitor='ExpMon',screen=1, units='pix', viewPos = [0,0], fullscr = True, color= col_back)
    # win.mouseVisible = False # this should not be invisible when the dummy mouse tracker is used?
    # fixation = visual.ShapeStim(win, vertices = ((0, -2), (0, 2), (0,0), (-2, 0), (2, 0)), lineWidth = 4, units = 'pix', size = (10, 10), closeShape = False, lineColor = col_both)

    # hiFusion = fusionStim(win=win, pos=[0, 0.7], units = 'norm', col = [col_back, col_both])
    # loFusion = fusionStim(win=win, pos=[0,-0.7], units = 'norm', col = [col_back, col_both])


    if os.sys.platform == 'linux':
        location = 'toronto'
    else:
        location = 'glasgow'


    glasses = 'RG'
    trackEyes = [True, True]


    setup = localizeSetup(location=location, glasses=glasses, trackEyes=trackEyes, filefolder=None) # data path is for the mapping data, not the eye-tracker data!

    cfg = {}
    cfg['hw'] = setup



    ## instructions
    visual.TextStim(cfg['hw']['win'],'Troughout the experiment you will fixate at a white cross that will be located at the center of the screen.   \
    It is important that you fixate on this cross at all times.\n\n You will be presented with pairs of dots. You will have to indicate which dots were closer together.\n\n Left arrow = first pair of dots were closer together.\
    \n\n Right arrow = second pair of dots were closer together.\n\n\n Press the space bar to start the experiment.', height = letter_height,wrapWidth=1200, color = 'black').draw()
    cfg['hw']['win'].flip()
    k = ['wait']
    while k[0] not in ['q','space']:
        k = event.waitKeys()
    if k[0] in ['q']:

        # put message in response file that the experiment was quitted?

        respFile.close()

        # send quit comment
        # stop tracking
        # close file
        # shutdown eye-tracker

        cfg['hw']['win'].close()
        core.quit()

        return(False) # since this is now a function


    ######
    #### Prepare stimulation
    ######

    ## stimuli
    # point_1 = visual.Circle(cfg['hw']['win'], radius = .5, pos = pol2cart(00, 3), units = 'deg', fillColor = col_both, lineColor = None)
    # point_2 = visual.Circle(cfg['hw']['win'], radius = .5, pos = pol2cart(00, 6), units = 'deg', fillColor = col_both, lineColor = None)
    # point_3 = visual.Circle(cfg['hw']['win'], radius = .5, pos = pol2cart(45, 3), units = 'deg', fillColor = col_both, lineColor = None)
    # point_4 = visual.Circle(cfg['hw']['win'], radius = .5, pos = pol2cart(45, 6), units = 'deg', fillColor = col_both, lineColor = None)
    point_1 = visual.Circle(cfg['hw']['win'], radius = .5, lineColor = None)
    point_2 = visual.Circle(cfg['hw']['win'], radius = .5, lineColor = None)
    point_3 = visual.Circle(cfg['hw']['win'], radius = .5, lineColor = None)
    point_4 = visual.Circle(cfg['hw']['win'], radius = .5, lineColor = None)

    blindspot = visual.Circle(cfg['hw']['win'], radius = .5, pos = [7,0], units = 'deg', fillColor=col_ipsi, lineColor = None)
    blindspot.pos = spot_cart
    blindspot.size = spot_size
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

    ## setup and initialize eye-tracker + gaze ok region etc.
    #!!#


    # first calibration

    # it seems to me that this wait routine is not necessary, and with the quit option in there, it also does need a lot of extra code

    # visual.TextStim(cfg['hw']['win'],'Press any key to start calibration', color = col_both, units = 'deg', pos = (0,-2)).draw()
    visual.TextStim(cfg['hw']['win'],'Press any key to start calibration', color = [-1, -1, -1], units = 'deg', pos = (0,-2)).draw()
    fixation.draw()
    cfg['hw']['win'].flip()
    k = event.waitKeys()
    if k[0] in ['q']:
        # put message in response file that the experiment was quitted?

        respFile.close()

        # send quit message
        # stop tracking
        # close files
        # shutdown eye-tracker

        cfg['hw']['win'].close()
        core.quit()

        return(False) # since this is now a function
        
    #!!# calibrate
    cfg['hw']['tracker'].initialize()
    cfg['hw']['tracker'].calibrate()
    cfg['hw']['tracker'].startcollecting()

    # I don't know what the next wait does, other than stop the experiment for no apparent reason?

    fixation.draw()
    cfg['hw']['win'].flip()

    k = event.waitKeys()
    if k[0] in ['q']:
        # put message in response file that the experiment was quitted?

        respFile.close()

        # send quit message
        # stop tracking
        # close files
        # shutdown eye-tracker

        cfg['hw']['win'].close()
        core.quit()

        return(False) # since this is now a function

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
    reversal = [False] * 8
    resps = [[]] * 8
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

        shift = random.sample([-1, -.5, 0, .5, .1], 2) # why have a 0 offset? if we use: [-1., -2/3, -1/3, 1/3, 2/3, 1.] or maybe some round values, there is always some offset
        dif = intervals[cur_int[which_stair]] * foil_type[which_stair]
        which_first = random.choice(['Targ', 'Foil'])

        if which_first == 'Targ':
            point_1.pos = pol2cart(positions[pos[0]][0][0], positions[pos[0]][0][1]       + shift[0])
            point_2.pos = pol2cart(positions[pos[0]][1][0], positions[pos[0]][1][1]       + shift[0])
            point_3.pos = pol2cart(positions[pos[1]][0][0], positions[pos[1]][0][1]       + shift[1])
            point_4.pos = pol2cart(positions[pos[1]][1][0], positions[pos[1]][1][1] + dif + shift[1])

            if eye[which_stair] == hemifield:
                point_1.fillColor = col_ipsi
                point_2.fillColor = col_ipsi
                point_3.fillColor = col_cont
                point_4.fillColor = col_cont
            else:
                point_1.fillColor = col_cont
                point_2.fillColor = col_cont
                point_3.fillColor = col_ipsi
                point_4.fillColor = col_ipsi
            # point_3.fillColor = col_both
            # point_4.fillColor = col_both

        else:
            point_3.pos = pol2cart(positions[pos[0]][0][0], positions[pos[0]][0][1]       + shift[0])
            point_4.pos = pol2cart(positions[pos[0]][1][0], positions[pos[0]][1][1]       + shift[0])
            point_1.pos = pol2cart(positions[pos[1]][0][0], positions[pos[1]][0][1]       + shift[1])
            point_2.pos = pol2cart(positions[pos[1]][1][0], positions[pos[1]][1][1] + dif + shift[1])

            if eye[which_stair] == hemifield:
                point_1.fillColor = col_cont
                point_2.fillColor = col_cont
                point_3.fillColor = col_ipsi
                point_4.fillColor = col_ipsi
            else:
                point_1.fillColor = col_ipsi
                point_2.fillColor = col_ipsi
                point_3.fillColor = col_cont
                point_4.fillColor = col_cont
            # point_1.fillColor = col_both
            # point_2.fillColor = col_both
        
        # hiFusion.resetProperties()
        # loFusion.resetProperties()
        cfg['hw']['fusion']['hi'].resetProperties()
        cfg['hw']['fusion']['lo'].resetProperties()


        ## pre trial fixation
        cfg['hw']['tracker'].waitForFixation()


        trial_clock.reset()
        #!!# setup / start recording

        cfg['hw']['tracker'].startcollecting()

        # gaze_out = False # unnecessary variable?
        # while True and not abort:
        #     # Start detecting time
        #     t = trial_clock.getTime()
            
        #     #!!# get position at each t
        #     #!!# every 100 ms, check that positions were on average <2 dva from center
        #     #!!# after 5 consecutive intervals (500 ms) with correct fixation, break to start trial
        #     #!!# for now we break automatically:
        #     if t > .5:
        #         break
        #     #!!#

        #     # hiFusion.draw()
        #     # loFusion.draw()
        #     cfg['hw']['fusion']['hi'].draw()
        #     cfg['hw']['fusion']['lo'].draw()
        #     fixation.draw()
        #     cfg['hw']['win'].flip()

        #     k = event.getKeys(['q'])
        #     if k:
        #         if 'q' in k:
        #             abort = True
        #             break
            
        #     # set up auto recalibrate after 5s
        #     if t > 5:
        #         recalibrate = True
        #         gaze_out = True
        #         break

        #!!# stop recording/clear events
        
        # if not gaze_out:
        if cfg['hw']['tracker'].gazeInFixationWindow():
            ## trial
            
            #!!# start recording
            
            # hiFusion.draw()
            # loFusion.draw()
            cfg['hw']['fusion']['hi'].draw()
            cfg['hw']['fusion']['lo'].draw()
            fixation.draw()
            cfg['hw']['win'].flip()
            trial_clock.reset()
            gaze_in_region = True # unnecessary variable?
        
            while trial_clock.getTime() < 1.3 and not abort:
                t = trial_clock.getTime()
                
                #!!# get position at each t
                #!!# if position is invalid or >2 dva, set gaze in region to False
                #!!# may also record gazes in file here and do stuff like showing gaze position if simulating with mouse
                
                if not gaze_in_region:
                    gaze_out = True
                    break
                    
                # hiFusion.draw()
                # loFusion.draw()
                cfg['hw']['fusion']['hi'].draw()
                cfg['hw']['fusion']['lo'].draw()

                fixation.draw()
        
                if .1 <= trial_clock.getTime() < .5:
                    point_1.draw()
                    point_2.draw()
                elif .5 <= trial_clock.getTime() < 0.9:
                    point_1.draw()
                    point_2.draw()
                    point_3.draw()
                    point_4.draw()
                elif 0.9 <= trial_clock.getTime() < 1.3:
                    point_3.draw()
                    point_4.draw()
        
                cfg['hw']['win'].flip()
                
                k = event.getKeys(['q'])
                if k and 'q' in k:
                    abort = True
                    break
                    
            #!!# stop recording/clear events

        if abort:
            respFile.write("Run manually ended at " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + "!")
            break
        
        if not gaze_out:
        
            ## response
            fixation.ori += 45
            fixation.color = 'black'
            # hiFusion.draw()
            # loFusion.draw()
            cfg['hw']['fusion']['hi'].draw()
            cfg['hw']['fusion']['lo'].draw()

            fixation.draw()
            cfg['hw']['win'].flip()
            
            k = ['wait']
            while k[0] not in ['q', 'space', 'left', 'right']:
                k = event.waitKeys()
            if k[0] in ['q']:
                respFile.write("Run manually ended at " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + "!")
                break
            elif k[0] in ['space']:
                position[which_stair] = position[which_stair] + [pos]
                increment = False
                resp = 'abort'
                targ_chosen = 'abort'
                reversal = 'abort'
            else:
                resp = 1 if k[0] == 'left' else 2
                
            fixation.ori -= 45
            
        else:
        
            ## dealing with auto-aborted trials
        
            # auto recalibrate if no initial fixation
            if recalibrate:
                recalibrate = False
                cfg['hw']['tracker'].stopcollecting() # do we even have to stop/start collecting?
                cfg['hw']['tracker'].calibrate()
                cfg['hw']['tracker'].startcollecting()

                # visual.TextStim(cfg['hw']['win'],'Calibration...', color = col_both, units = 'deg', pos = (0,-2)).draw()
                # fixation.draw()
                # cfg['hw']['win'].flip()
                # k = event.waitKeys()
                # if k[0] in ['q']:
                #     respFile.write("Run manually ended at " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + "!")
                #     break
                    
                # #!!# calibrate
                
                # fixation.draw()
                # cfg['hw']['win'].flip()
                # k = event.waitKeys()
                # if k[0] in ['q']:
                #     respFile.write("Run manually ended at " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + "!")
                #     break
            
            # changing fixation to signify gaze out, restart with 'up' possibily of break and manual recalibration 'r' 

            # can't we just skip this whole part? in 99% of trials we'd just need to recalibrate... but now you have to press a button, and not the wrong one

            else:
                # hiFusion.draw()
                # loFusion.draw()
                cfg['hw']['fusion']['hi'].draw()
                cfg['hw']['fusion']['lo'].draw()
                # this is the fourth (?) time these are drawn... that should have been only 1... it's such complicated code for such a simple experiment

                # visual.TextStim(cfg['hw']['win'], '#', height = letter_height, color = col_both).draw()
                visual.TextStim(cfg['hw']['win'], '#', height = letter_height, color = [-1, -1, -1]).draw()
                cfg['hw']['win'].flip()
                k = ['wait']
                while k[0] not in ['q', 'up', 'r']:
                    k = event.waitKeys()
                if k[0] in ['q']:
                    respFile.write("Run manually ended at " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + "!")
                    break
        
                # manual recalibrate
                if k[0] in ['r']:
                    cfg['hw']['tracker'].stopcollecting() # do we even have to stop/start collecting?
                    cfg['hw']['tracker'].calibrate()
                    cfg['hw']['tracker'].startcollecting()

                    # visual.TextStim(cfg['hw']['win'],'Calibration...', color = col_both, units = 'deg', pos = (0,-2)).draw()
                    # fixation.draw()
                    # cfg['hw']['win'].flip()
                    # k = event.waitKeys()
                    # if k[0] in ['q']:
                    #     respFile.write("Run manually ended at " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + "!")
                    #     break

                    # #!!# calibrate

                    # fixation.draw()
                    # cfg['hw']['win'].flip()
                    # k = event.waitKeys()
                    # if k[0] in ['q']:
                    #     respFile.write("Run manually ended at " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + "!")
                    #     break
                
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
            if (len(resps[which_stair]) > 1) and (resps[which_stair][-2] != resps[which_stair][-1]):
                reversal = True
                revs[which_stair] = revs[which_stair] + 1
                direction[which_stair] *= -1
            
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
        trial += 1

    if not any(stairs_ongoing):
        print('run ended properly!')

    respFile.close()
    print(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
    blindspot.autoDraw = False # no stimulus should be on autodraw? that feature was a mistake in psychopy

    ## last screen
    visual.TextStim(cfg['hw']['win'],'Run ended.', height = letter_height, color = 'black').draw()
    cfg['hw']['win'].flip()
    k = event.waitKeys()

    #!!# close eye-tracker

    cfg['hw']['tracker'].closefile()
    cfg['hw']['tracker'].stopcollecting()
    cfg['hw']['tracker'].shutdown() # this should download the EyeLink edf file
    cfg['hw']['win'].close()
    core.quit()

