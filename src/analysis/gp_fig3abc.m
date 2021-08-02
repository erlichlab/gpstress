function gp_fig3abc()
% dbc can be removed after all subjects renamed and data stored in one .mat
dbc = db.labdb.getConnection();
dbc.use('jenya');
all_trials = readtable('~/repos/human_stress/Analysis/data/genpop_trials_all.csv');
all_trials.treat_ind(:) = 'L';
all_trials.treat_ind(strcmp(all_trials.treatment,'Short_Verbal_Chn')) = 'S';
all_trials.treat_ind(strcmp(all_trials.treatment,'Weeks_Verbal_Chn')) = 'W';
% file
% params = readtable('~/Library/Mobile Documents/com~apple~CloudDocs/GP_Analysis/gp_dw_rs_stan_3e.csv');
%load('../../data/delaytp.mat');
% prepare data
ds = 'select * from stanfits_gp_nc_rs0_bi order by subjid';
dsfits = dbc.query(ds);
dsfits.K_S = log(exp(dsfits.K_S)/86400);
dw = 'select * from stanfits_gp_dw_rs0_bi order by subjid';
dwfits = dbc.query(dw);
dwfits.K_W = log(exp(dwfits.K_W)*7);
dsdw = 'select * from stanfits_gp_delay_rs0_bi order by subjid';
jfits = dbc.query(dsdw);
jfits.K_S = log(exp(jfits.K_S)/86400);
jfits.K_W = log(exp(jfits.K_W)*7);
treatment = 'DS';
dstrials = all_trials(ismember(all_trials.treatment,'Long_Verbal_Chn')|ismember(all_trials.treatment,'Short_Verbal_Chn'),:);
plot_fits_earlylate(dstrials,dsfits,treatment,4)
treatment = 'DW';
dwtrials = all_trials(ismember(all_trials.treatment,'Days_Verbal_Chn')|ismember(all_trials.treatment,'Weeks_Verbal_Chn'),:);
dwtrials.treatment(ismember(dwtrials.treatment,'Days_Verbal_Chn'),:) = {'Long_Verbal_Chn'};
plot_fits_earlylate(dwtrials,dwfits,treatment,4)
treatment = 'SW';
all_trials.treatment(ismember(all_trials.treatment,'Days_Verbal_Chn'),:) = {'Long_Verbal_Chn'};
plot_fits_earlylate(all_trials,jfits,treatment,4)
