# -*- coding: utf-8 -*-
# this file contains all the functions needed for all experiments
# !!! Check the correct path for the code repository and correct dtb user first!
# you'll need custom module 'helpers' to import the dtb settings/connection

#-----------------imports---------------------------
  # so that 1/3=0.333 instead of 1/3=0
from psychopy import event,core,gui,visual
import numpy as np  # whole numpy lib is available, prepend 'np.'
import time, datetime, os, random, copy, math
import setup, newPoints, variables,doodle,platform, sys
import SQL_call as sql
import csv

# set working path in the computer so that relative packages could work
def setpath():
    if platform.system() == 'Windows': # set path in windows machines
        sys.path.append('/Users/user/repos') # !!! put in correct path first
        sys.path.append('C:\\python27\\Lib\\site-packages')
    else: # set path in mac machines
        sys.path.append('/Users/user/repos') # !!! put in correct path first
        sys.path.append('/usr/local/lib/python2.7/site-packages')

setpath()

#--------------import helper------------------------
import helpers.DBUtilsClass as db
import helpers.net as net
import json

mouse = event.Mouse(setup.mywin)

# connect to database
def dbconnect():
    dbc = db.Connection() # connect to database
    sql.select_user(dbc,'user') # !!! put in correct user first
    return dbc

# ask subject for netid from a window shown on the screen
def get_netid(var,doo,dbc,fN):
    expN, extN = os.path.splitext(fN)    
    st = datetime.datetime.now()
    expD = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
    host_ip=net.getIP()
    p_net = (var.expInfo['Net ID'])
    try:
        p_num = sql.r_subjid(dbc,p_net) # get subject id (p_num) given netid 
    except IndexError: # net_ID is not in the system
        print("net_ID is not in the system!")
        doo.mixNonInstruction.text = 'net_ID is not in the system'
        doo.mixNonInstruction.draw()
        setup.mywin.flip()
        core.wait(2)
        core.quit()
    return p_num, expD, st,expN, host_ip,p_net


# Risk task setups
def exp_setup_risk(var,doo,dbc,getName,sub_id,expName,expDate):
    stt = datetime.datetime.now()
    #-----------------data recording-----------------------------------
    if getName:
        dlg = gui.DlgFromDict(dictionary=var.expInfo, title=expName)
        if dlg.OK == False: 
            core.quit()  # user pressed cancel
        else:
            setup.mywin.winHandle.maximize()
            setup.mywin.winHandle.activate()
            setup.mywin.fullscr = True
            setup.mywin.winHandle.set_fullscreen(True)
            setup.mywin.flip()
        p_net = (var.expInfo['Net ID'])
        try:
            p_num = sql.r_subjid(dbc,p_net)
        except IndexError: # net_ID is not in the system
            print("net_ID is not in the system!")
            doo.instruction.text = 'net_ID is not in the system'
            doo.instruction.draw()
            setup.mywin.flip()
            core.wait(2)
            core.quit() 
    else:
        p_net = sub_id
        p_num = sql.r_subjid(dbc,p_net)
    if expName == 'Risk_Chn':
        print(expName)
        settingsdtb = 'risk_chn'
    else:
        settingsdtb = 'risk3' #changed from 'risk' and 'test risk'
    try:
        varsetdtb = sql.r_varset(dbc,settingsdtb)
        setiddtb = sql.r_settingsid(dbc,settingsdtb)
        var.probability = varsetdtb['probability']
        var.mag = varsetdtb['rewmag']
        var.shortmag = varsetdtb['surebet']
        #var.refresherNum = varsetdtb['refresherNum']
        var.blockTrial = varsetdtb['blockTrial']
    except IndexError: # settings_ID is not in the system
        print("settings_ID is not in the system!")
        
    fileName = 'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format("No.","block","total", "trial", 
        "bluePos", "yellowPos", "decisionRT","choice", "yellowRew", "rewMag", "probability", "pay_prob", "reward_give", 
        "lottery_draw","smag"))
    var.dataFile.flush()
    #remove test_ to save real data
    host_ip=net.getIP()
    sql.w_before_Risk(dbc,p_num, expDate, stt, expName, host_ip, setiddtb)
    sessid = sql.r_lastID(dbc)
    return sessid,p_num,p_net,setiddtb,host_ip,var,dbc


# Verbal experiment setups block by (probability)
def verbalSetup(totalTrialNumber,probList):
    blockInfoList = [] # this function requires that problist is ordered
    totalNum = 0 # number of probability blocks
    for prob in probList: # add all probabilities into blockInfoList as individual sublists
        blockInfoList.append([prob])
        totalNum += 1
    totalMean = round(totalTrialNumber/totalNum)# average trial num 
    for setNum in range(len(blockInfoList)):# loop over each sublist in blockInfoList
        if setNum == len(blockInfoList)-1:
            totalBeforeLastBigger = 0
            for i in range(setNum):
                    totalBeforeLastBigger+=blockInfoList[i][1]
            trialNum = int(totalTrialNumber- totalBeforeLastBigger)
            blockInfoList[setNum].append(trialNum)
        elif setNum < len(blockInfoList)-1:
                trialNum = random.randint(totalMean-2, totalMean+2)
                blockInfoList[setNum].append(trialNum)
    return blockInfoList
# this function generates the trial numbers for each block (by reward) and the overall structure of this session
def verbalSetup_rew(totalTrialNumber,magList,shortMag):
    blockInfoList = [] # this function requires that maglist is ordered
    smallerNum = 0 # number of rewardmag that's smaller than surebet
    biggerNum = 0 # number of rewardmag that is greater than surebet
    smallerTotal = totalTrialNumber * 0.05 # total number of trials to have bigger rewmag
    biggerTotal = totalTrialNumber - smallerTotal# total number of trials to have smaller rewmag
    for mag in magList: # add all rewmag into blockInfoList as individual sublists and set smallerNum/biggerNum
        blockInfoList.append([mag])
        if mag < shortMag:
            smallerNum += 1
        elif mag > shortMag:
            biggerNum += 1
    smallerMean = round(smallerTotal/smallerNum)# average trial num for each smaller/bigger rewmag
    biggerMean = round(biggerTotal/biggerNum)
    for setNum in range(len(blockInfoList)):# loop over each sublist in blockInfoList
        if blockInfoList[setNum][0] < shortMag:# if rewmag in this sublist is smaller than surebet
            if setNum == smallerNum-1:# if the current sublist is the last smaller rewmag
                totalBeforeLastSmaller = 0
                for i in range(setNum):# calculate the sum of trial numbers of all the other smaller rewmags before it
                    totalBeforeLastSmaller+=blockInfoList[i][1]
                trialNum = max(1,int(smallerTotal- totalBeforeLastSmaller))# subtract the sum above from the total smaller trial number
                blockInfoList[setNum].append(trialNum)# append the trial num of this last smaller rewmag to its sublist
            elif setNum < smallerNum-1:# if the current sublist is not the last smaller rewmag
                trialNum = max(1,random.randint(smallerMean-1,smallerMean+1))# set the trialNum within +1/-1 range from the smallerMean value
                blockInfoList[setNum].append(trialNum)
        elif blockInfoList[setNum][0] > shortMag:# if rewmag in this sublist is greater than surebet
            if setNum == len(blockInfoList)-1:
                totalBeforeLastBigger = 0
                for i in range(smallerNum,setNum):
                    totalBeforeLastBigger+=blockInfoList[i][1]
                trialNum = int(biggerTotal- totalBeforeLastBigger)
                blockInfoList[setNum].append(trialNum)
            elif setNum < len(blockInfoList)-1:
                trialNum = random.randint(biggerMean-2, biggerMean+2)
                blockInfoList[setNum].append(trialNum)
    return blockInfoList

# this function selects one trial to actually pay for the participant
def paymentSelection(totalTrialNumber):
    return random.randint(1,totalTrialNumber-1)

# show verbal instructions between each verbal block
def block_instruction(var,doo):
    doo.instruction.text = 'Block '+str(var.blockName)
    doo.instruction.height = 65 #30
    doo.instruction.pos=[0, 0]
    doo.instruction.draw()
    setup.mywin.flip()
    core.wait(3)

def block_instruction_Chn(var,doo):
    doo.chinese_instruction.text = '模块 '+str(var.blockName)
    doo.chinese_instruction.height = 65 #30
    doo.chinese_instruction.pos=[0, 0]
    doo.chinese_instruction.draw()
    setup.mywin.flip()
    core.wait(3)

# present a break between each verbal block. Show the clock and the instructions
def block_break(var,doo):
    doo.instruction.text = 'Please take a %r-second break.\n\nPress enter to stop the break and you will continue to the next stage.' % var.blockBreak
    doo.instruction.pos=[0,0]
    doo.instruction.height = 30
    delayStart = time.time()
    delayEnd = time.time()
    while delayEnd-delayStart<=var.blockBreak:
        var.secPos2 = 'TBD'
        var.secPos = np.floor(delayEnd-delayStart+60-var.oneRound)*360/60#NB floor will round down to previous second
        if not event.getKeys(keyList = "return"):
            if var.secPos != var.secPos2:
                delayCircle(var,doo)
                scales(var,doo)
                doo.clock.visibleWedge = (0, var.secPos*(60/var.blockBreak)+1)
                doo.clock.draw()
                scales(var,doo)
                doo.instruction.draw()
                setup.mywin.flip()
            var.secPos2 = copy.copy(var.secPos)
            delayEnd = time.time()
        else:
            breakCancel = time.time()
            var.blockBreakCancel = breakCancel-delayStart
            break
    doo.instruction.draw()
    setup.mywin.flip()
    core.wait(0.2)

def block_break_Chn(var,doo):
    doo.chinese_instruction.text = '请休息 %r 秒.\n\n或者您可以按下‘ENTER’直接进入下一模块.'% var.blockBreak
    doo.chinese_instruction.pos=[0,0]
    doo.chinese_instruction.height = 30
    delayStart = time.time()
    delayEnd = time.time()
    while delayEnd-delayStart<=var.blockBreak:
        var.secPos2 = 'TBD'
        var.secPos = np.floor(delayEnd-delayStart+60-var.oneRound)*360/60#NB floor will round down to previous second
        if not event.getKeys(keyList = "return"):
            if var.secPos != var.secPos2:
                delayCircle(var,doo)
                scales(var,doo)
                doo.clock.visibleWedge = (0, var.secPos*(60/var.blockBreak)+1)
                doo.clock.draw()
                scales(var,doo)
                doo.chinese_instruction.draw()
                setup.mywin.flip()
            var.secPos2 = copy.copy(var.secPos)
            delayEnd = time.time()
        else:
            breakCancel = time.time()
            var.blockBreakCancel = breakCancel-delayStart
            break
    doo.chinese_instruction.draw()
    setup.mywin.flip()
    core.wait(0.2)

# instruction before the experiment
def instruction(var,doo):
    event.Mouse(visible=False)
    var.DBRSoundDur = 2
    toneMag=doo.toneMag(var.blockRewMag)
    setup.mywin.flip()
    core.wait(1)
    toneMag.play()
    core.wait(2)
    var.DBRSoundDur = 0.48
    event.Mouse(visible=True)
    return var

# this function makes the survey
def survey(doo):
    questions = ['1. To what extent did you feel that you were out of money in the last two weeks?',
                 '2. To what extent did you feel that you were out of time in the last two weeks?',
                 '3. To what extent are you in a hurry today?']
    rate_ans = []
    dt_ans = []
    chhist_ans = []
    for question in questions:
        ratingScale = visual.RatingScale(setup.mywin,scale=None,acceptPreText='')
        doo.instruction.text = question
        doo.instruction.pos = [0,80]
        while ratingScale.noResponse:
            doo.instruction.draw()
            doo.survey_instr.text = '(Press a number to make your choice. Press enter to confirm your choice.)'
            doo.survey_instr.draw()
            ratingScale.draw()
            setup.mywin.flip()
        rating = ratingScale.getRating()
        decisionTime = ratingScale.getRT()
        choiceHistory = ratingScale.getHistory()
        rate_ans.append(rating)
        dt_ans.append(decisionTime)
        chhist_ans.append(choiceHistory)
    return rate_ans, dt_ans, chhist_ans

def survey_Chn(doo):
    questions = ['1.在过去的两周内，您在多大程度上觉得自己经济紧张？',
                 '2.在过去的两周内，您在多大程度上觉得自己缺少时间?',
                 '3.您在多大程度上觉得自己今天很匆忙？']
    rate_ans = []
    dt_ans = []
    chhist_ans = []
    for question in questions:
        ratingScale = visual.RatingScale(setup.mywin,scale=None,acceptPreText='') #suppress english text
        doo.chinese_instruction.text = question
        doo.chinese_instruction.pos = [0,80]
        while ratingScale.noResponse:
            doo.chinese_instruction.draw()
            doo.chinese_survey_instr.text = '(1=完全没有...非常地=7)'
            doo.chinese_survey_instr.draw()
            ratingScale.draw() 
            setup.mywin.flip()
        rating = ratingScale.getRating()
        decisionTime = ratingScale.getRT()
        choiceHistory = ratingScale.getHistory()
        rate_ans.append(rating)
        dt_ans.append(decisionTime)
        chhist_ans.append(choiceHistory)
    return rate_ans, dt_ans, chhist_ans

# this function is reminding the subject to focus. Experiment is about to start
def about_to_start(doo):
        doo.instruction.text = 'Experiment Starts Soon...'
        doo.instruction.pos = [0,0]
        doo.instruction.draw()
        setup.mywin.flip()
        core.wait(3)
        setup.mywin.flip()

def about_to_start_Chn(doo):
        doo.chinese_instruction.text = '实验即将开始...'
        doo.chinese_instruction.pos = [0,0]
        doo.chinese_instruction.draw()
        setup.mywin.flip()
        core.wait(3)
        setup.mywin.flip()

#this function generates the  instruction between nonverbal and verbal session
def break_instruction(doo):
    doo.instruction.text = 'You may take a short break now.\n\nPress enter if you are ready to start the decision stages.\n\nNote: Keep your headphones on, and if you don\'t hear any sound after pressing enter, please report to the experimenter.'
    doo.instruction.pos=[0,0]
    doo.instruction.height = 30
    doo.instruction.draw()
    setup.mywin.flip()
    press = event.waitKeys(keyList="return")
    while press[0]=="return":
        break

def break_instruction_Chn(doo):
    doo.instruction.text = '您现在可以稍作休息.\n\n如果您已准备好开始决策计分阶段，请按“Enter”.\n\n 注意：请带上耳机。如果您在按下“Enter”之后没有听到任何声音, 请立刻告知实验员.'
    doo.instruction.pos=[0,0]
    doo.instruction.height = 30
    doo.instruction.draw()
    setup.mywin.flip()
    press = event.waitKeys(keyList="return")
    while press[0]=="return":
        break

#this function generates the circle for the clock: we need the clock for the break
def delayCircle(var,doo):
    doo.circle.size = 150
    doo.circle.pos = [0,240]
    doo.circle.fillColor=var.purple
    doo.circle.draw()
    doo.circle.size=var.circle_fullSize


#this function generates the empty circle for the clock: we need the clock for the break
def delayCircleEmpty(var,doo):
    doo.circle.size = 150
    doo.circle.pos = [0,240]
    doo.circle.fillColor=var.gray2
    doo.circle.draw()
    doo.circle.size=var.circle_fullSize

#this function draws the scales on the clock: we need the clock for the break
def scales(var,doo):
    pi = math.pi
    for i in range(12):
        startX,startY = pol2cart(var,65,i*pi/6)
        endX,endY = pol2cart(var,75,i*pi/6)
        doo.scale.start = (startX,startY)
        doo.scale.end = (endX,endY)
        doo.scale.draw()

#this function transfers cart to polar for the clock
def cart2pol(var,x, y):
    rho = np.sqrt((x-var.clockX)**2 + (y-var.clockY)**2)
    phi = np.arctan2(y-var.clockY, x-var.clockX)
    return(rho, phi)

#this function transfers polar to cart for the clock
def pol2cart(var,rho, phi):
    x = rho * np.cos(phi)+var.clockX
    y = rho * np.sin(phi)+var.clockY
    return(x, y)

#this function gets randomized positions for L and R (jon)
def getRLpos(var):
    num = random.randint(0,1)
    if num == 0:
        var.Lpos = 1
        var.Rpos = 2
    else:
        var.Lpos = 2
        var.Rpos = 1

def getProb(var):
    random.shuffle(var.probability)
    var.probmag = var.probability[random.randint(0,len(var.probability)-1)] # Random prob
    return var

#this function redraws everything while waiting for choice (jon)
#draws initial choices (jon)
def initText(var,doo):
    doo.choice1.draw()
    doo.choice2.draw()

def reDrawInitText(var,doo,myPoints):
    initText(var,doo)
    if not var.Risk:
        myPoints.totalUpdate(var.points)
    setup.mywin.flip()

def reDrawInitText_Chn(var,doo,myPoints):
    doo.choice1_Chn.draw()
    doo.choice2_Chn.draw()
    if not var.Risk:
        myPoints.totalUpdate(var.points)
    setup.mywin.flip()

#Draws beginning of trial text choices (jon)
def draw_init(var,doo,myPoints):
    getRLpos(var)
    if var.Lpos == 1:
        doo.choice1.pos = [-240,30]
        doo.choice2.pos = [240,30]
        var.bluePos = 'L'
        var.yellowPos = 'R'
    else:
        doo.choice1.pos = [240,30]
        doo.choice2.pos = [-240,30]
        var.bluePos = 'R'
        var.yellowPos = 'L'
    doo.choice1.text = '%r coins\n100%%' % (var.shortmag)
    doo.choice1.text= format_text(doo.choice1.text)
    doo.choice1.draw()
    if var.rewmag == 1:
            doo.choice2.text = '%r coin \n%r%%' % (var.rewmag,int(100*var.probmag))
    else:
            doo.choice2.text = '%r coins \n%r%%' % (var.rewmag,int(100*var.probmag))
    doo.choice2.text= format_text(doo.choice2.text)
    doo.choice2.draw()
    if not var.Risk:
        myPoints.totalUpdate(var.points)
    setup.mywin.flip()
    var.timeStart1 = time.time()
    var.state = 'wait_for_choice'
    return var,doo,myPoints

def draw_init_Risk_Chn(var,doo,myPoints):
    getRLpos(var)
    if var.Lpos == 1:
        doo.choice1_Chn.pos = [-240,30]
        doo.choice2_Chn.pos = [240,30]
        var.bluePos = 'L'
        var.yellowPos = 'R'
    else:
        doo.choice1_Chn.pos = [240,30]
        doo.choice2_Chn.pos = [-240,30]
        var.bluePos = 'R'
        var.yellowPos = 'L'
    doo.choice1_Chn.text = '%r 金币\n100%%' % (var.shortmag)#u'%r coins\n100%%' % (var.shortmag)
    doo.choice1_Chn.text= format_text(doo.choice1_Chn.text)
    doo.choice1_Chn.draw()
    doo.choice2_Chn.text = '%r 金币\n%r%%' % (var.rewmag, int(100*var.probmag))
    doo.choice2_Chn.text= format_text(doo.choice2_Chn.text)
    doo.choice2_Chn.draw()
    if not var.Risk:
        myPoints.totalUpdate(var.points)
    setup.mywin.flip()
    var.timeStart1 = time.time()
    var.state = 'wait_for_choice_Chn'
    return var,doo,myPoints


#this function checks whether user inputs choice (jon)
def wait_for_choice(var,doo,myPoints):
    reDrawInitText(var,doo,myPoints)
    while True:
        presses = event.waitKeys()
        if presses[0] == 'a' or presses[0] == 'l':
            if presses[0] == 'a':
                if var.Lpos == 1:
                    var.rewmag = var.shortmag
                    var.choice = 'b'
                else:
                    var.choice = 'y'
            elif presses[0] == 'l':
                if var.Lpos == 2:
                    var.rewmag = var.shortmag
                    var.choice = 'b'
                else:
                    var.choice = 'y'
            timeEnd1 = time.time()
            var.wait_for_choice_time = timeEnd1-var.timeStart1
            var.trialsCorrect += 1 
            var.state = 'draw_reward'
            return var,doo,myPoints
        elif presses[0] != 'l' and presses[0] != 'a':
            doo.reminder.draw()
            return var,doo,myPoints

#this function checks whether user inputs choice (jon)
def wait_for_choice_Chn(var,doo,myPoints):
    reDrawInitText_Chn(var,doo,myPoints)
    while True:
        presses = event.waitKeys()
        if presses[0] == 'a' or presses[0] == 'l':
            if presses[0] == 'a':
                if var.Lpos == 1:
                    var.rewmag = var.shortmag
                    var.choice = 'b'
                else:
                    var.choice = 'y'
            elif presses[0] == 'l':
                if var.Lpos == 2:
                    var.rewmag = var.shortmag
                    var.choice = 'b'
                else:
                    var.choice = 'y'
            timeEnd1 = time.time()
            var.wait_for_choice_time = timeEnd1-var.timeStart1
            var.trialsCorrect += 1 
            var.state = 'draw_reward_Chn'
            return var,doo,myPoints
        elif presses[0] != 'l' and presses[0] != 'a':
            doo.reminder_Chn.draw()
            return var,doo,myPoints


# this function generates a high low (6 in total) reward list
def makeHighLowRew(var):
    for i in range(np.int(var.forcedTrialNum/2)-1):
        var.highLowRew.append(var.maxRewMag)
        var.highLowRew.append(var.minRewMag)
        random.shuffle(var.highLowRew)
    return var

#this function gets a random end rewmag
def getHighLowRew(var,index):
    var.rewmag = var.highLowRew[index]
    return var

# this functions gets the reward mag for the orderly block
def getRewmag(var):
    var.rewmag = var.mag[var.rewIndex]
    return var



# Show the reward chosen by the subject in verbal tasks
def draw_reward(var,doo,myPoints):
    setup.mywin.flip()
    if var.choice=='b':
        doo.instruction.text='Your choice:\n %r coins, \n for sure' %(var.shortmag)
    else:
        if var.rewmag == 1 :
            doo.instruction.text= '   Your choice:\n     %r coin, \na %r%% chance' %(var.rewmag,int(100*var.probmag))
        else:
            doo.instruction.text= '   Your choice:\n     %r coins, \na %r%% chance' %(var.rewmag,int(100*var.probmag))
    doo.instruction.text= format_text(doo.instruction.text)
    doo.instruction.height = 50
    doo.instruction.pos=[0, 0]
    doo.instruction.draw()
    setup.mywin.flip()
    core.wait(1.5)
    var.points+=var.rewmag
    var.state = 'none'
    return var,doo,myPoints

def draw_reward_Chn(var,doo,myPoints):
    setup.mywin.flip()
    if var.Risk:
        if var.choice=='b':
            doo.chinese_instruction.text='        您选择:\n 确定获得 %r 金币' %(var.rewmag)
        else:
            doo.chinese_instruction.text='       您的选择:\n %r%%的可能性获得\n          %r 金币' %(int(100*var.probmag),var.rewmag)
    #doo.chinese_instruction.text = format_text(doo.chinese_instruction.text)
    doo.chinese_instruction.height = 50
    doo.chinese_instruction.pos=[0, 0]
    doo.chinese_instruction.draw()
    setup.mywin.flip()
    core.wait(1.5)
    var.points+=var.rewmag
    var.state = 'none'
    return var,doo,myPoints


#this function check whether there should a block break. If so, it will give a break and show the next block name
def block_break_check(var):
    if var.blockTrialCounter%var.blockTrial==0 :
        if var.blockName>1:
            block_break()
        block_instruction()
        var.blockName+=1
    return var


# Set up probability in and rewmag in risk task.
def new_trial_setup_risk(var,problist):
    if var.blockTrialCounter==0 :
        var = getMag(var,problist)
        print('get Mag')
    var.rewmag = var.shmaglist[var.blockTrialCounter]
    var.probability = var.blockProb
    var.blockRewMag = var.rewmag # now block reward variable changes each trial
    return var

#create a shuffled list of reward of requested size
def getMag(var,problist):
    if len(var.mag)>=problist :
        random.shuffle(var.mag)
        maglist = var.mag[0:problist]
    else:
        multiplier = int(problist/len(var.mag))+1
        longlist = []
        longlist.extend(var.mag*multiplier)
        random.shuffle(longlist)
        maglist = longlist[0:problist]
        print(multiplier, longlist, maglist)
    random.shuffle(maglist)
    var.shmaglist = maglist
    print(var.shmaglist)
    #random.shuffle(var.mag)
    #var.rewmag = var.mag[random.randint(0,len(var.mag)-1)] # Random magnitude
    return var

# determine whether the subject has learned the task
def passStageTest(var):
    if var.goodPokesInARoll >= var.passThreshold: # if the number of correct trials in a roll exceed certain number, assume the subject has learned the task
        return 'pass'

#-----------------------------data recording after one trial-----------------------------------
def dataRecord_risk(var,dbc,sessid):
    var.dataFile.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(str(var.trialCounter), str(var.blockName), str(var.points), str(var.rewardGot),
     str(var.bluePos), str(var.yellowPos), str(var.wait_for_choice_time),
     str(var.choice), str(var.blockRewMag), str(var.rewmag), str(var.probmag), var.pay_prob, var.reward_give, var.GetaNum, var.shortmag))
    d = {'pay_prob':var.pay_prob, 'pay_num':var.pay_num,'trial_pay':var.pay,'trial': var.trialCounter, 'rewMag': var.rewmag,'points': var.points, 
        'trialsCorrect': var.rewardGot, 'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_choice_time, 
         'probability':var.probmag,'yellowRew':var.blockRewMag,'choice': var.choice, 'reward_give':var.reward_give, 'lottery_draw':var.GetaNum}
    sd = json.dumps(d)
    if var.choice == 'b':
        var.ychoice = 0
    elif var.choice =='y':
        var.ychoice = 1
    sql.w_after_Risktrial(dbc,var,sessid,sd)
    var.dataFile.flush()

#this function shows all the big coins at final
def show_totalScore(var):
    results = visual.TextStim(setup.mywin, units='pix', ori=0, name='Results',text='You got %r coins' % (var.points),    font='Arial',
    pos=[0, 0], height=18, wrapWidth=None,color='black', colorSpace='rgb', opacity=1,depth=-12.0)
    results.draw()
    setup.mywin.flip()
    core.wait(1.5)


def stage_instruction_risk(stageName,var,doo,pre_points):
    if pre_points==0:
        stnum = 1
    else:
        stnum = 2
    doo.instruction.text = format_text(str(stageName[:4])+' Stage'+' # %r' %(stnum))
    doo.instruction.height = 75 #30
    doo.instruction.pos=[0, 0]
    doo.instruction.draw()
    setup.mywin.flip()
    core.wait(1.5)
    
def stage_instruction_risk_Chn(stageName,var,doo):
    doo.chinese_instruction.text = '风险阶段'
    doo.chinese_instruction.height = 75 #30
    doo.chinese_instruction.pos=[0, 0]
    doo.chinese_instruction.draw()
    setup.mywin.flip()
    core.wait(1.5)


# show all the big coins at the end of a session/block
def show_bigCoins(var,myPoints):
    myPoints.stackAllbig(var.points) # draw all the big coins
    setup.mywin.flip() # show the drawings
    core.wait(2) # keep the drawings for 2 seconds
    var.dataFile.close() # close the data file


# get the total points and trial number of this stage
def total_Points_trialCounter(var):
    return var.points, var.trialCounter

# reset the total points and trial number to 0
def reset_Points_trialCounter(var):
    var.trialCounter = 0
    var.points = 0
    var.totalTrialCounter = 0

#  shows all the coins earned at the end of all learning stages
def show_bigCoins_total(totalProfits,myPoints):
    myPoints.stackAllbig(totalProfits) # draw all the big coins
    setup.mywin.flip() # show the drawings
    core.wait(2) # keep the drawings on the screen for 2 seconds

    
def end_instruction_risk(doo,trial_pay, session_pay,pay_num,pay_prob, lottery_pay, var):
    if lottery_pay:
        doo.instruction.text = 'This is the end of the experimental session.\n\nTrial # %r from Risk Stage # %r was randomly chosen to pay you.\n\nYour choice in that trial was: %r coin(s) with a %r %% chance.\n\nYou got %r coin(s). \n\nPlease wait...' % (trial_pay,session_pay,pay_num,int(100*pay_prob),pay_num)
    else:
        doo.instruction.text = 'This is the end of the experimental session.\n\nTrial # %r from Risk Stage # %r was randomly chosen to pay you.\n\nYour choice in that trial was: %r coin(s) with a %r %% chance.\n\nYou got 0 coin(s). \n\nPlease wait...' % (trial_pay,session_pay,pay_num,int(100*pay_prob))
    doo.instruction.pos=[0,0]
    doo.instruction.height = 30
    doo.instruction.draw()
    setup.mywin.flip()
    core.wait(20)

def end_instruction_risk2(doo,trial_pay, session_pay,pay_num,pay_prob, lottery_pay, var):
    if lottery_pay:
        doo.instruction.text = 'Trial # %r from Risk Stage # %r was randomly chosen to pay you.\n\nYour choice in that trial was: %r coin(s) with a %r %% chance.\n\nYou got %r coin(s).\n\nPlease report to the experimenter. Thank you very much for your participation!' % (trial_pay,session_pay,pay_num,int(100*pay_prob),pay_num)
    else:
        doo.instruction.text = 'Trial # %r from Risk Stage # %r was randomly chosen to pay you.\n\nYour choice in that trial was: %r coin(s) with a %r %% chance.\n\nYou got 0 coin(s).\n\nPlease report to the experimenter. Thank you very much for your participation!' % (trial_pay,session_pay,pay_num,int(100*pay_prob))
    doo.instruction.pos=[0,0]
    doo.instruction.height = 30
    doo.instruction.draw()
    setup.mywin.flip()
    core.wait(20)

def end_instruction_risk_Chn(doo,trial_pay,session_pay,pay_num,pay_prob, lottery_pay,var):
    if lottery_pay:
        doo.chinese_instruction.text = '本轮实验结束.\n\n系统随机选择了第 %r个<风险阶段>的第 %r号实验，您获得了该奖赏\n\n您在该次实验的选择是: \n\n有 %r %%几率获得 %r 金币.\n\n您获得 %r 金币.'% (session_pay,trial_pay,int(100*pay_prob),pay_num, pay_num)
    else:
        doo.chinese_instruction.text = '本轮实验结束.\n\n系统随机选择了第 %r个<风险阶段>的第 %r号实验，您没有获得该奖赏\n\n您在该次实验的选择是: n\n有 %r %%几率获得 %r 金币.\n\n您获得 0 金币.'% (session_pay,trial_pay,int(100*pay_prob))
    doo.chinese_instruction.pos=[0,0]
    doo.chinese_instruction.height = 30
    doo.chinese_instruction.draw()
    setup.mywin.flip()
    core.wait(20)

def end_instruction_risk2_Chn(doo,trial_pay,session_pay,pay_num,pay_prob, lottery_pay,var):
    if lottery_pay:
        doo.chinese_instruction.text = '系统随机选择了第 %r个<风险阶段>的第 %r号实验,您获得了该奖赏\n\n您在该次实验的选择是: \n\n有 %r %%几率获得 %r 金币.\n\n您获得 %r 金币. \n\n请向实验员报告. 非常感谢您前来参与本次实验!'% (session_pay,trial_pay,int(100*pay_prob),pay_num, pay_num)
    else:
        doo.chinese_instruction.text = '系统随机选择了第 %r个<风险阶段>的第 %r号实验，您没有获得该奖赏\n\n您在该次实验的选择是: n\n有 %r %%几率获得 %r 金币.\n\n您获得 0 金币. \n\n请向实验员报告. 非常感谢您前来参与本次实验!'% (session_pay,trial_pay,int(100*pay_prob))
    doo.chinese_instruction.pos=[0,0]
    doo.chinese_instruction.height = 30
    doo.chinese_instruction.draw()
    setup.mywin.flip()
    core.wait(20)

# this function randomly picks a trial from all long verbal trials to pay the subjects
def pick_pay(pick1,pick2):
    pay_session = random.choice([1,2])
    if pay_session == 1:
        return pay_session,pick1
    return pay_session,pick2

# this funcion assigns the final payment given the session selected to pay
def assign_riskpay(session_pay,pay_delay1,pay_delay2,pay_num1,pay_num2,lottery1,lottery2):
    if session_pay == 1:
        return pay_delay1, pay_num1, lottery1
    else:
        return pay_delay2, pay_num2, lottery2

# this function formats text to be center aligned
def format_text(text):
    text = text.splitlines()
    length = 0
    for i in range(len(text)):
        if len(text[i]) > length:
            length = len(text[i])
    text2 = ''
    for i in range(len(text)):
        text2 = text2 + '\n' + text[i].center(length)
    return text2


#-------------------Function Name Dictionary(for recursive state calling)------------------------
funcDic_risk = {'draw_init':draw_init, 'wait_for_choice':wait_for_choice, 'draw_reward':draw_reward}
funcDic_risk_Chn = {'draw_init_Risk_Chn':draw_init_Risk_Chn, 'wait_for_choice_Chn':wait_for_choice_Chn, 'draw_reward_Chn':draw_reward_Chn}