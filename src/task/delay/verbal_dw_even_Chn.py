# Run this file for combined verbal experiment (longVerbal+shortverbal+longVerbal+shortVerbal) 
#-------------------imports--------------------------------------------------------------------
import Days_Verbal_Chn, Weeks_Verbal_Chn, doodle, setup, variables,newPoints
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
def verbal_dw_even(var,doo,mouse,myPoints,dbc):
    expName = os.path.basename(__file__)[:-3] # get expName of this file
    expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S") # get expDate
    [rate_ans, dt_ans, chhist_ans]=fc.survey_Chn(doo) # survey subjects' recent time and money scarcity
    d = {'answer': rate_ans, 'decisionTime': dt_ans, 'choiceHistory': chhist_ans} # record the survey result to database
    quest = json.dumps(d)
    fc.about_to_start_Chn(doo) # show the get ready instruction
    p_net,pick1,pay_delay1,pay_num1,trials_long1,points_long1 = Weeks_Verbal_Chn.WeeksVerbal_Chn(var,doo,myPoints,dbc,mouse) # run the first long verbal session and record the returned info
    p_num = sql.r_subjid(dbc,p_net)
    ses1id = sql.r_sessid(dbc,p_num)
    numl1 = sql.r_countChoice(dbc,ses1id)
    fc.block_break_Chn(var,doo) # show the break instruction to subject
    var.points = 0 # set total points to 0 for short verbal experiments
    var.weekVerbal = False
    p_net,pick2,pay_delay2,pay_num2,trials_short1,points_short1 = Days_Verbal_Chn.DaysVerbal_Chn(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net) # run short verbal session #1
    ses2id = sql.r_sessid(dbc,p_num)
    numl2 = sql.r_countChoice(dbc,ses2id)
    fc.block_break_Chn(var,doo)  # show the break instruction to subject
    longResult2 = Weeks_Verbal_Chn.WeeksVerbal_Chn(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net,pre_points=points_long1,gettrialn=numl1,pre_trials=trials_long1) # run the second long verbal session
    pick3 = longResult2[1]-numl1 # record the number of trial picked to pay in the second session
    pay_delay3 = longResult2[2] # delay of selected payment from long delay session #2
    pay_num3 = longResult2[3] # reward of selected payment from long delay session #2
    fc.block_break_Chn(var,doo) # show the break instruction to subject
    var.weekVerbal = False
    shortResult2 = Days_Verbal_Chn.DaysVerbal_Chn(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net,pre_points=points_short1,gettrialn=numl2,pre_trials=trials_short1) # run the second long verbal session
    pick4 = shortResult2[1]-numl1 # record the number of trial picked to pay in the second session
    pay_delay4 = shortResult2[2] # delay of selected payment from short delay session #2
    pay_num4 = shortResult2[3] # reward of selected payment from short delay session #2   
    session_pay_l,trial_pay_l = fc.pick_pay(pick1,pick3) # pick one from the two selected trials(in the two long verbal sessions) to pay the subject
    pay_delay_l,pay_num_l = fc. assign_pay(session_pay_l,pay_delay1,pay_delay3,pay_num1,pay_num3) # assign the final payment based on the picked trial 
    session_pay_s,trial_pay_s = fc.pick_pay(pick2,pick4) # pick one from the two selected trials(in the two short verbal sessions) to pay the subject
    pay_delay_s,pay_num_s = fc. assign_pay(session_pay_s,pay_delay2,pay_delay4,pay_num2,pay_num4) # assign the final payment based on the picked trial 
    endt = datetime.datetime.now() # record end time
    id = sql.r_sessid(dbc,p_num)
    sql.w_after_verbalCombined_dw_Chn(dbc,var,id,p_num, expDate, endt, expName, session_pay_s, trial_pay_s,pay_num_s,pay_delay_s, session_pay_l, trial_pay_l,pay_num_l,pay_delay_l,rate_ans, quest)
    # Days first then Weeks both for data recording and display on the screen
    fc.end_instruction_verbal2_Chn(doo,trial_pay_s,session_pay_s,pay_num_s,pay_delay_s,trial_pay_l,session_pay_l,pay_num_l,pay_delay_l) # show the ending instruction and picked pay trial to subject
    dbc.close() #close connection to db

if __name__ == "__main__":
    verbal_dw_even(var,doo,mouse,myPoints,dbc) # call main function
