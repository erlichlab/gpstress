[email *jlukinova@nyu.edu* for further explanations]
## Necessary setups before delay discounting or risk experiment

**Computer setup:**

    1. Python 2.7 needs to be installed in your computer
    2. Download and install PsychoPy 1.83.04
    3. Download and install any MySQL user interface
    4. git clone repos/ folder (with helpers/ folder and code/ folder in it)
    'helpers' is custom module needed to access dtb
    5. Setup working path
        - In repos/code/functions.py, find setpath() function
        - sys.path.append('directory where you git cloned repos folder')
        - sys.path.append('directory where your /Python/2.7/site-packages is')
    6. Setup MySQL database
        6.1. Setup all tables(and column names) needed in our code
            -sessions: sessid/subjid/sessiondate/starttime/treatment/hostip/settingsid/startts
            -sessions_end: sessid/subjid/sessiondate/endtime/treatment/hostip/num_trials/total_profit/settingsid/sessionpay/trialpay/payrew/paydelay/endts/moneyscarcity/timescarcity/hurry/questionnaire/sessionpay_w/trialpay_w/payrew_w/paydelay_w
            -settings: settingid/expgroupid/data/description
            -subjinfo: subjid/netid/firstname/fullname
            -trials: trialid/sessid/trialtime/trialnum/trialdata/stage/rewmag/delay/probability/choice/points/smag/sdelay/short_delay/long_delay
        6.2. Set database user name
            - In repos/code/functions, find dbconnect() function
            - Input your database user name in sql.select_user(dbc,'your user name')
        6.3. Setup a subjects pool in your database
            - In 'subjinfo' table, input information of all subjects
            - There needs to be an ID(netid) for each subject to input at the beginning of each program that will lead a unique subjid saved in the 'subjinfo' table
        6.4. Create two necessary settings
            - You can input whatever fits your need in the n/a's 
            - In 'settings' table, create two rows of necessary settings for the experiment:
| settingsid | expgroupid | data                                                                                                                             | description |
|-----------:|------------|----------------------------------------------------------------------------------------------------------------------------------|-------------|
| n/a        | n/a        | {"delay": [ 3 , 7, 14, 30, 64], "refresherNum": 10, "blockTrial": 2, "passThreshold": 2, "rewdelpair": 10, "ddiscounter": 1.2} | delay    |   
| n/a        | n/a        | {"probability": [ 0.25, 0.5, 0.75], "rewmag": [ 2, 4, 6, 6, 6, 12, 12, 12, 18, 18, 18, 50], "surebet": 4, "refresherNum": 10, "blockTrial": 2, "passThreshold": 2, "rewdelpair": 10, "ddiscounter": 1.2} | risk   |          

**Subject data saving preparation**
    
    1. Once the subject gave his consent, add his data to subjinfo table. 
    2. He will be given a subjid (manual entry in the dtb).
    3. Participant will be instructed to insert his netID (linked to subjid). 
    4. If netID is not in the database, PsychoPy will display an error message.

**Run the following code:**

    1. For [odd subjid] delay d (DS: days and seconds) -> run verbal_combined_odd_Chn.py
    2. For [even subjid] delay d (DS: days and seconds) -> run verbal_combined_even_Chn.py
    3. For [odd subjid] delay d (DW: days and weeks) -> run verbal_dw_odd_Chn.py
    4. For [even subjid] delay d (DW: days and weeks) -> run verbal_dw_even_Chn.py
    5. For risk task -> run risk_combined_Chn.py

**Auxiliary files catalog**
    
    1. functions.py: file which contains all functions needed for other scripts
    2. SQL_call.py: all database related commands(read and write) needed for other scripts
    3. Short_Verbal_Chn.py: short-delay session (imported by verbal_combined_odd/even_Chn.py)
    4. Long_Verbal_Chn.py: long-delay session (imported by verbal_combined_odd/even_Chn.py)
    5. Days_Verbal_Chn.py: day-delay experiment (imported by verbal_dw_odd/even_Chn.py)
    6. Weeks_Verbal_Chn.py: week-delay experiment (imported by verbal_dw_odd/even_CHn.py)
    7. Risk_Chn.py: risk experiment (imported by risk_combined_Chn.py)
    5. doodle.py: defines class Doodle which creates circle/text/sound objects and modifies their properties (important file that decreases memory use)
    6. newPoints.py: defines class NewPoins which creates coin objects and modifies their properties (imported by all files that need to draw coins)
    7. setup.py: defines the window that displays stimuli and other setups (imported by all files for experiments)
    8. variables.py: defines class Variables which defines all the variables needed (imported by all files for experiments)
    9. coin_echo5.wav: the sound stimuli when getting a coin in the short delay task
    
