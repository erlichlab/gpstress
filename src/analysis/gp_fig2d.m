function gp_fig2d()
% file
load('../../data/gpstress.mat');
% prepare data
all_trials.treat_ind(:) = 'L';
all_trials.treat_ind(strcmp(all_trials.treatment,'Short_Verbal_Chn')) = 'S';
all_trials.treat_ind(strcmp(all_trials.treatment,'Weeks_Verbal_Chn')) = 'W';
dsfits.K_S = log(exp(dsfits.K_S)/86400);
dwfits.K_W = log(exp(dwfits.K_W)*7);
jfits.K_S = log(exp(jfits.K_S)/86400);
jfits.K_W = log(exp(jfits.K_W)*7);
treatment = 'DS';
dstrials = all_trials(ismember(all_trials.treatment,'Long_Verbal_Chn')|ismember(all_trials.treatment,'Short_Verbal_Chn'),:);
plot_fits_earlylate(dstrials,dsfits,treatment,4)
%treatment = 'DW';
%dwtrials = all_trials(ismember(all_trials.treatment,'Days_Verbal_Chn')|ismember(all_trials.treatment,'Weeks_Verbal_Chn'),:);
%dwtrials.treatment(ismember(dwtrials.treatment,'Days_Verbal_Chn'),:) = {'Long_Verbal_Chn'};
%plot_fits_earlylate(dwtrials,dwfits,treatment,4)
%treatment = 'SW';
%all_trials.treatment(ismember(all_trials.treatment,'Days_Verbal_Chn'),:) = {'Long_Verbal_Chn'};
%plot_fits_earlylate(all_trials,jfits,treatment,4)
