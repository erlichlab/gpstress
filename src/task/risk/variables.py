# this file defines all the common variables needed in the whole experiment
from psychopy import sound
#---------------variables/lists-----------------------------------
class Variables:
    def __init__(self):
        self.stg = 'tbd'
        self.secPos = 'tbd'
        self.secPos2 = 'TBD'
        self.expInfo = {'Net ID':''}
        self.expInfo_genpop = {'ID':''}
        self.gray2 = "#808080" #need colors for the break clock
        self.purple = "#800080" 
        self.white = "#FFFFFF"
        self.black = "#000000"
        self.cyan = "#00FFFF"
        self.yellow = "#FFFF00"
        self.mag = [1,2,5,8,10]
        self.elX = [0,0,0,-120,120,-240,-120,120,240] # [1]-reward, [2,3] - init, rest - symmetric for decisions !!!SWITCHED 2 and 3!!!
        self.elY = [-210, 30,-90,-90, -90,-210,-210,-210,-210,]
        self.clockX = 0
        self.clockY = 240
        self.shortmag = 2 #surebet value for risk
        self.maxRewMag = max(self.mag)
        self.minRewMag = min(self.mag)
        self.highLowRew = [self.maxRewMag,self.minRewMag] # 1 for reward minimum
        self.state = 'TBD'
        self.dataFile = 'TBD'
        self.rewPos= 0
        self.initPos = 'TBD'
        self.bluePos = 'TBD'
        self.yellowPos = 'TBD'
        self.choice = '/'
        self.ychoice = '/' #1 if chose yellow, 0 if blue
        self.pay = None
        self.circle_fullSize = 100 # need for the block break
        self.sameInitPos = False
        self.riskTotalTrial = 100 # for students 100, for GenPop 100
        self.verbalTotalTrial = 50 # (this num * percentage of smaller trials /number of smaller trials) >= 2; in current case has to >= 80
        self.verbalTotalTrial_dw = 100
        self.trial = 1000 # changed from 40, cannot proceed if fail 
        self.forcedTrialNum= 16 # changed from 16
        self.highLowTrialNum = 6 
        self.refresherNum = 20 # changed from 20
        self.blockTrial = 10 # changed from 10
        self.oneRound = 60 # changed from 60
        self.rewdelPair = 60 # force number of pairs
        self.rewIndex = 0
        self.trialCounter = 0
        self.trialsCorrect = 0
        self.blockTrialCounter = 0
        self.totalTrialCounter = 0
        self.pairNum = 0
        self.blockName = 1
        self.rewDelPairList = []
        self.initStimDis = 'TBD'
        self.magScale = 50
        self.rewardGot = 0
        self.fixDur = 2
        self.SF=41000
        self.points = 0
        self.rewmag = 1
        self.blockProb='/'
        self.blockRewMag='/'
        self.pay_num = []
        self.blockBreak = 20
        self.blockBreakCancel = '/'
        self.timeStart1 = '/'
        self.delayStart = '/'
        self.sessid = 0
        # new
        self.wait_for_choice_time = '/'
        self.Rpos = 'tbd'
        self.Lpos = 'tbd'
        # new vars for session data saving.
        self.rate_ans = []
        self.dt_ans = []
        self.chhist_ans = []
        self.quest = 'tbd'
        self.session1 = 0
        self.d = 'tbd'
        # new vars for risk task
        self.Risk = False 
        self.probability = [] 
        self.probmag = 0
        self.prob_clicks = []
        self.pay_prob = []
        self.sure_rwd = 1 #consider switching to 1
        self.reward_give = []
        self.RiskTotalTrial = 0
        self.GetaNum = []
        self.shmaglist = [] # shuffled magnitude list