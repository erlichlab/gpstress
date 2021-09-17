# this file contains all the SQL request calls
# functions starting with 'w' are executing/writing data into dtb
# functions starting with 'r' are query/reading data from dtb
import json

# select username in the database
def select_user(dbc,name):
    dbc.use(name)

# get subject id (p_num) given netid 
def r_subjid(dbc,p_net):
    return int(dbc.query("select subjid from subjinfo where netid = '%s'" %p_net)[0][0])

# record data of one trial after the trial for risk sessions
def w_after_Risktrial(dbc,var,sessid,sd):
    dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, probability, choice, points, smag) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter, sd, var.blockName, var.blockRewMag, var.probmag, var.ychoice, var.points, var.shortmag))

# get the last inserted sessid
def r_lastID(dbc):
    return dbc.query('select last_insert_id()')[0][0]# added [0][0] here

# get settingsid with given info
def r_settingsid(dbc,settingsdtb):
    return int(dbc.query("select settingsid from settings where description = '%s'" %settingsdtb)[0][0])

# get variables from given setting
def r_varset(dbc,settingsdtb):
    return json.loads(dbc.query("select data from settings where description = '%s'" %settingsdtb)[0][0])

# get max sessid(id) from sessions_end table giv given subjid
def r_sessid(dbc,p_num):
    return int(dbc.query("select max(sessid) from sessions_end where subjid = '%s'" %p_num)[0][0])

#record serssion before a risk session in the sessions table
def w_before_Risk(dbc,p_num, expDate, stt, expName, host_ip, setiddtb):
    dbc.execute('insert into sessions (subjid, sessiondate, starttime, treatment, hostip, settingsid) values (%s, %s, %s, %s, %s, %s)',(p_num, expDate, stt, expName, host_ip, setiddtb))

#record session info after a risk session in the sessions_end table
def w_after_Risk(dbc,var,sessid, p_num, expDate, endt, expName, host_ip, setiddtb):
    if var.reward_give:
        lottery_pay = var.pay_num
    else:
        lottery_pay = 0
    dbc.execute('insert into sessions_end (sessid, subjid, sessiondate, endtime, treatment, hostip, num_trials, total_profit, settingsid, trialpay, payrew) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',\
                (sessid, p_num, expDate, endt, expName, host_ip, var.trialCounter, var.points, setiddtb, var.pay, lottery_pay))

# risk_combined
# count the number of trials in the first risk session
def r_countChoice(dbc,ses1id):
    return int(dbc.query("select count(choice) from trials where sessid = '%s' and choice is not NULL" %ses1id)[0][0]) 

# record the final info of this whole experiment in sessions_end table in database
def w_after_riskCombined(dbc,var,id,p_num, expDate, endt, expName, session_pay, trial_pay,lottery_pay,rate_ans, quest):
    dbc.execute('insert into sessions_end (sessid, subjid, sessiondate, endtime, treatment, sessionpay, trialpay,payrew,moneyscarcity, timescarcity, hurry, questionnaire) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',\
                (id+1,p_num, expDate, endt, expName, session_pay, trial_pay,lottery_pay,rate_ans[0], rate_ans[1], rate_ans[2], quest)) 

def w_after_riskCombined2(dbc,var,id,p_num, expDate, endt, expName, rate_ans, quest):
    dbc.execute('insert into sessions_end (sessid, subjid, sessiondate, endtime, treatment, moneyscarcity, timescarcity, hurry, questionnaire) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',\
                (id+1,p_num, expDate, endt, expName, rate_ans[0], rate_ans[1], rate_ans[2], quest)) 
