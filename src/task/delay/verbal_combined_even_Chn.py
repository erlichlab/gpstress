# Run this file for combined verbal experiment (longVerbal+shortverbal+longVerbal+shortVerbal) 
# Chinese Version
#-------------------imports--------------------------------------------------------------------
import Short_Verbal_Chn, Long_Verbal_Chn, doodle, setup, variables,newPoints
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
def verbal_even_Chn(var,doo,mouse,myPoints,dbc):
    expName = os.path.basename(__file__)[:-3] # get expName of this file
    expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S") # get expDate
    [rate_ans, dt_ans, chhist_ans]=fc.survey_Chn(doo) # survey subjects' recent time and money scarcity
    d = {'answer': rate_ans, 'decisionTime': dt_ans, 'choiceHistory': chhist_ans} # record the survey result to database
    quest = json.dumps(d)
    fc.about_to_start_Chn(doo) # show the get ready instruction
    p_net,pick1,pay_delay1,pay_num1,trials_long1,points_long1 = Long_Verbal_Chn.LongVerbal(var,doo,myPoints,dbc,mouse) # run the first long verbal session and record the returned info
    p_num = sql.r_subjid(dbc,p_net)
    ses1id = sql.r_sessid(dbc,p_num)
    numl1 = sql.r_countChoice(dbc,ses1id)
    fc.block_break_Chn(var,doo) # show the break instruction to subject
    var.points = 0 # set total points to 0 for short verbal experiments
    p_net,points_short1,trials_short1,trialsCorrect_short1 = Short_Verbal_Chn.ShortVerbal(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net) # run short verbal session #1
    fc.block_break_Chn(var,doo)  # show the break instruction to subject
    longResult2 = Long_Verbal_Chn.LongVerbal(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net,pre_points=points_long1,gettrialn=numl1,pre_trials=trials_long1) # run the second long verbal session
    pick2 = longResult2[1]-numl1 # record the number of trial picked to pay in the second session
    pay_delay2 = longResult2[2] # delay of selected payment from long delay session #2
    pay_num2 = longResult2[3] # reward of selected payment from long delay session #2
    fc.block_break_Chn(var,doo) # show the break instruction to subject
    Short_Verbal_Chn.ShortVerbal(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net,pre_points=points_short1,pre_trials=trials_short1,pre_trialsCorrect=trialsCorrect_short1) # run short verbal session #2
    session_pay,trial_pay = fc.pick_pay(pick1,pick2) # pick one from the two selected trials(in the two long verbal session) to pay the subject
    pay_delay,pay_num = fc. assign_pay(session_pay,pay_delay1,pay_delay2,pay_num1,pay_num2) # assign the final payment based on the picked trial 
    endt = datetime.datetime.now() # record end time
    id = sql.r_sessid(dbc,p_num)
    sql.w_after_verbalCombined(dbc,var,id,p_num, expDate, endt, expName, session_pay, trial_pay,pay_num,pay_delay,rate_ans, quest)
    fc.end_instruction_verbal_Chn(doo,trial_pay,session_pay,pay_num,pay_delay) # show the ending instruction and picked pay trial to subject
    dbc.close() #close connection to db

if __name__ == "__main__":
    verbal_even_Chn(var,doo,mouse,myPoints,dbc) # call main function
