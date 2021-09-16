# Data

This folder contains 

- `.mat` files that are required for generating the figures in Matlab;
- `.Rdata` files that are required for generating the figures in R; 
- [brms](https://github.com/paul-buerkner/brms) model input and output.

File            		| Description
-----           		|------------
gpstress\_all_trials.RData | all trials in an R dataframe
gpfitsstress.RData         | fits, model-free and stress data for main figures in R
gpstress.mat			| fits and stress data for main figures in Matlab
ds_posterior.RData  | posteriors from brms fits for DS sessions
dw_posterior.RData  | posteriors from brms fits for DW sessions
risk_posterior.RData  | posteriors from brms fits (power utility, rho-beta model) for risk task
kapparisk_posterior.RData  | posteriors from brms fits (kappa-beta model) for risk task
ds\_subj.RData, dw\_subj.RData,  risk_subj.RData,       | example subject fitted draws
ds\_r2.RData, dw\_r2.RData, risk_r2.RData       | Bayesian r2