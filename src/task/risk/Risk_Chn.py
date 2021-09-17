# -*- coding: utf-8 -*-
# Risk task in Chinese
#--------------import stuff----------------------------------------
import os, datetime, copy, random
import newPoints,setup,variables,doodle
from psychopy import event
import functions as fc
import SQL_call as sql
#------------make objects----------------------
# these objects won't be made if the file is called from another file
myPoints = newPoints.NewPoints()
var = variables.Variables()
doo = doodle.Doodle()
dbc = fc.dbconnect()
mouse = event.Mouse(setup.mywin)
#--------------------------Main Code--------------------------------
def Risk_Chn(var,doo,myPoints,dbc,mouse,getName=True,sub_id=None,pre_points=0,gettrialn=0,pre_trials=0):
    var.trialCounter = pre_trials
    var.rewardGot = gettrialn
    var.points = pre_points # if it's the second risk session in the experiment, points are accumulated from the first long verbal session
    var.Risk = True # specify risk task for specific functions
    fc.setpath() # set up directory
    fN = os.path.basename(__file__) # get expName of this file
    expName, extN = os.path.splitext(fN) # get expName and extN
    stageName = expName[:8] # get stageName
    expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")# get expDate
    sessid,p_num,p_net,setiddtb,host_ip, var,dbc = fc.exp_setup_risk(var,doo,dbc,getName,sub_id,expName,expDate) # database setup and data start recording
    var.pay = fc.paymentSelection(var.riskTotalTrial)+gettrialn # select one trial(number) to actually pay the subject 
    setupList = fc.verbalSetup(var.riskTotalTrial,var.probability)  # setup the blocks of probability for the whole experiment
    shuffledSetupList = copy.copy(setupList)# shuffle the reward list
    random.shuffle(shuffledSetupList)
    fc.stage_instruction_risk_Chn(stageName,var,doo) # show subjects stage name (Chinese risk task)
    for i in range(len(shuffledSetupList)): # apply a probability for each block
        var.blockProb = shuffledSetupList[i][0] # assign probability for this block
        var.blockName = i+1 # assign blockName
        var.probmag = var.blockProb # assign probability
        fc.block_instruction_Chn(var,doo) # show block instruction to the subject
        while var.blockTrialCounter < shuffledSetupList[i][1]: # run pre-determined number of trials in each block 
            var = fc.new_trial_setup_risk(var,shuffledSetupList[i][1]) # get random reward
            var,doo,myPoints = fc.draw_init_Risk_Chn(var,doo,myPoints) # start the first state
            while var.state != 'none': # go through all connected states in one trial
                var,doo,myPoints = fc.funcDic_risk_Chn[var.state](var,doo,myPoints)           
            var.rewardGot += 1  # plus 1 in rewardGot 
            var.trialCounter+=1 # plus 1 in trialCounter (total trial num)
            var.blockTrialCounter += 1  # plus 1 in blockTrialCounter (trial num in current block)
            var.pairNum+=1 # proceed to next pair
            if var.rewardGot == var.pay: # assign pay_prob and pay_num if the current trial is the one picked to be actually paid
                if var.choice!='b':
                    var.pay_prob = var.probmag
                else:
                    var.pay_prob = var.sure_rwd
                var.pay_num = var.rewmag
                var.GetaNum = random.random()# get a random number between 0 and 1
                print(var.GetaNum)
                if var.GetaNum <= var.pay_prob: #decide to if give reward based on given probability
                    var.reward_give = True
                print(var.pay_prob, var.reward_give)
            fc.dataRecord_risk(var,dbc,sessid) # record data for this trial
        var.blockTrialCounter = 0 # reset blockTrialCounter
    var.dataFile.close() # close the data file
    var.Risk = False # reset longVerbal boolean to be False
    endt = datetime.datetime.now() # record end time
    sql.w_after_Risk(dbc,var,sessid, p_num, expDate, endt, expName, host_ip, setiddtb) # save data of this session in database
    return p_net, var.pay, var.pay_prob, var.pay_num, var.trialCounter,var.points, var.reward_give


if __name__ == "__main__":
    Risk_Chn(var,doo,myPoints,dbc,mouse) # run main function
    trial_pay = var.pay
    session_pay = 1
    fc.end_instruction_risk_Chn(doo,trial_pay,session_pay,var.pay_num,var.pay_prob,var.reward_give,var)