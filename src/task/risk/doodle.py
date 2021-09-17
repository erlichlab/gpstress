# -*- coding: utf-8 -*-
# a class that does most of the drawing in the experiment
from psychopy import visual,sound
import setup, variables
import numpy as np  # whole numpy lib is available, prepend 'np.'
var = variables.Variables()
class Doodle:
    def __init__(self):
        self.circle = visual.Circle(setup.mywin, units='pix', size = var.circle_fullSize, 
            ori=0, pos=np.array([var.elX[0],var.elY[0]]), fillColor=var.gray2, fillColorSpace='rgb',
            opacity =1, interpolate=True)
        self.scale = visual.Line(setup.mywin, start=(0,0), end=(0,0))
        self.clock = visual.RadialStim(setup.mywin,tex='sqrXsqr', mask='none', units='pix', 
                    pos=(0, 240), size=(148, 148), radialCycles=1, angularCycles=1, 
                    radialPhase=0, angularPhase=0, ori=0.0, texRes=64, angularRes=100, 
                    visibleWedge=(0, 0), rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', 
                    dkl=None, lms=None, contrast=0.0, opacity=1.0, depth=10, rgbPedestal=(1.0, 1.0, 1.0), 
                    interpolate=False, name=None, autoLog=None, maskParams=None)
        self.instruction = visual.TextStim(setup.mywin, units='pix', ori=0, name='Instructions',text='Block Name',    font='Arial Monospaced',
            pos=[0, 0], height=30, wrapWidth=None,color='black', colorSpace='rgb', opacity=1,depth=-12.0,alignVert='center',alignHoriz='center')
        self.chinese_instruction = visual.TextStim(setup.mywin, units='pix', ori=0, name='Instructions',text='',    font='Songti SC',
            pos=[0, 240], height=40, wrapWidth=None,color='black', colorSpace='rgb', opacity=1,depth=-12.0,alignVert='center',alignHoriz='center')
        self.survey_instr = visual.TextStim(setup.mywin, units='pix', ori=0, name='Instructions',text='Block Name',    font='Arial',
            pos=[0, 0], height=20, wrapWidth=None,color='black', colorSpace='rgb', opacity=1,depth=-12.0,alignVert='center',alignHoriz='center')
        self.chinese_survey_instr = visual.TextStim(setup.mywin, units='pix', ori=0, name='Instructions',text='',    font='Songti SC',
            pos=[0, 0], height=20, wrapWidth=None,color='black', colorSpace='rgb', opacity=1,depth=-12.0,alignVert='center',alignHoriz='center')
        #Doodle var for text choices 
        self.choice1 = visual.TextStim(setup.mywin, units='pix', ori=0, name='Instructions',text='',    font='Arial Monospaced',
            pos=[-240, 30], height=50, wrapWidth=None,color='black', colorSpace='rgb', opacity=1,depth=-12.0,alignVert='center',alignHoriz='center')
        self.choice2 = visual.TextStim(setup.mywin, units='pix', ori=0, name='Instructions',text='',    font='Arial Monospaced',
            pos=[240, 30], height=50, wrapWidth=None,color='black', colorSpace='rgb', opacity=1,depth=-12.0,alignVert='center',alignHoriz='center')
        self.choice1_Chn = visual.TextStim(setup.mywin, units='pix', ori=0, name='Instructions',text='',    font='Songti SC',
            pos=[-240, 30], height=50, wrapWidth=None,color='black', colorSpace='rgb', opacity=1,depth=-12.0,alignVert='center',alignHoriz='center')
        self.choice2_Chn = visual.TextStim(setup.mywin, units='pix', ori=0, name='Instructions',text='',    font='Songti SC',
            pos=[240, 30], height=50, wrapWidth=None,color='black', colorSpace='rgb', opacity=1,depth=-12.0,alignVert='center',alignHoriz='center')
        self.reminder = visual.TextStim(setup.mywin, units='pix', ori=0, name='Instructions',text='Reminder: Press \'a\' for the left choice and \'l\' for the right choice. Please do not press any other buttons.',    font='Arial',
            pos=[0, -240], height=20, wrapWidth=None,color='black', colorSpace='rgb', opacity=1,depth=-12.0,alignVert='center',alignHoriz='center')
        self.reminder_Chn = visual.TextStim(setup.mywin, units='pix', ori=0, name='Instructions',text='提示：请按下‘a’选择左侧选项，‘l’选择右侧选项，请不要误按其它按键。',    font='Songti SC',
            pos=[0, -240], height=20, wrapWidth=None,color='black', colorSpace='rgb', opacity=1,depth=-12.0,alignVert='center',alignHoriz='center')
        
