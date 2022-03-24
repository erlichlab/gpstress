%% master.m
% master script that calls individual functions to generate each figure.
% These functions use shared lab code that are a submodule included here:
% https://github.com/erlichlab/elutils/git

addpath elutils; % This adds the helper functions that are used for the figures.

%% Fig 2 D
gp_fig2d()

%% Fig 2 E left
gp_fig2el()

%% Fig 2 E right
gp_fig2er()
