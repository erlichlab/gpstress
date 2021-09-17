# -*- coding: utf-8 -*-
# Run this file for combined risk verbal experiment  (set # of stages you want to run: 2,4)
#-------------------imports--------------------------------------------------------------------
import Risk_Chn, doodle, setup, variables, newPoints
import os, datetime, json
from psychopy import event
import functions as fc
import SQL_call as sql

#-------------make necessary objects------------------------------
myPoints = newPoints.NewPoints()
var = variables.Variables()
doo = doodle.Doodle()
dbc = fc.dbconnect()
mouse = event.Mouse(setup.mywin)

#---------------Main Function-------------------------------------
def risk_combined_chn(var,doo,mouse,myPoints,dbc):
    expName = os.path.basename(__file__)[:-3] # get expName of this file
    expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S") # get expDate
    #[rate_ans, dt_ans, chhist_ans]=fc.survey_Chn(doo) # survey subjects' recent time and money scarcity
    #d = {'answer': rate_ans, 'decisionTime': dt_ans, 'choiceHistory': chhist_ans} # record the survey result to database
    #quest = json.dumps(d)
    #fc.about_to_start_Chn(doo) # show the get ready instruction
    p_net,pick1,pay_prob1,pay_num1,trials_risk1,points_risk1,lottery1 = Risk_Chn.Risk_Chn(var,doo,myPoints,dbc,mouse,getName=True,sub_id=None,pre_points=0,gettrialn=0,pre_trials=0) # run the risk stage and record the returned info
    if lottery1:
        lottery1_pay = pay_num1
    else:
        lottery1_pay = 0    
    p_num = sql.r_subjid(dbc,p_net)
    ses1id = sql.r_sessid(dbc,p_num)
    numr1 = sql.r_countChoice(dbc,ses1id)
    var.pay_prob = []
    var.reward_give = []
    var.GetaNum = []
    fc.block_break_Chn(var,doo)  # show the break instruction to subject
    riskResult2 = Risk_Chn.Risk_Chn(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net,pre_points=points_risk1,gettrialn=numr1,pre_trials=trials_risk1) # run the second long verbal session
    pick2 = riskResult2[1]-numr1 # record the number of trial picked to pay in the second session
    pay_prob2 = riskResult2[2] # prob of selected payment from risk stage #2
    pay_num2 = riskResult2[3] # reward of selected payment from risk stage #2
    lottery2 = riskResult2[6] # lottery results from risk stage #2
    if lottery2:
        lottery2_pay = pay_num2
    else:
        lottery2_pay = 0
    #session_pay,trial_pay = fc.pick_pay(pick1,pick2) # pick one from the two selected trials(in the two risk stages) to pay the subject
    #pay_prob,pay_num,lottery = fc.assign_riskpay(session_pay,pay_prob1,pay_prob2,pay_num1,pay_num2,lottery1,lottery2) # assign the final payment based on the picked trial 
    endt = datetime.datetime.now() # record end time
    #id = sql.r_sessid(dbc,p_num)
    #sql.w_after_riskCombined2(dbc,var,id,p_num, expDate, endt, expName, rate_ans, quest)
    fc.end_instruction_risk_Chn(doo,pick1,1,pay_num1,pay_prob1,lottery1_pay,var)
    fc.end_instruction_risk2_Chn(doo,pick2,2,pay_num2,pay_prob2,lottery2_pay,var)
    #fc.end_instruction_risk_Chn(doo,trial_pay,session_pay,pay_num,pay_prob,lottery_pay,var) # show the ending instruction and picked pay trial to subject
    dbc.close() #close connection to db
    
if __name__ == "__main__":
    risk_combined_chn(var,doo,mouse,myPoints,dbc) # call main function