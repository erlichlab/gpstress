function gp_paper_perm_tests()
%% New Bootmean Tests
% +utils in path
%% Behavior
behdt = readtable('../data/ds12w_fits_imp.csv');
% DDD session 1 vs session 2
[p,ci] = bootmean(behdt.K_L_x-behdt.K_L_y,'boots',10000) 
% mean(behdt.K_L_x)
% Mk_DDD_s1 = -3.0020 Mk_DDD_s2 = -3.3334
% p = 0.2866 ci = -0.2465    0.9595

% DDD session 2 vs session 3 - significant
[p,ci] = bootmean(behdt.K_L_y-behdt.K_L,'boots',10000) 
% Mk_DDD_s2 = -3.3334 Mk_DDD_s3 = -4.5337 
% p = 2.0000e-04 ci = 0.7738    1.6262

% DDD session 1 vs session 3 - significant
[p,ci] = bootmean(behdt.K_L_x-behdt.K_L,'boots',10000) 
% Mk_DDD_s1 = -3.0020 Mk_DDD_s3 = -4.5337 
% p = 2.0000e-04 ci = 0.8032    2.2913

% SDD session 1 vs session 2
[p,ci] = bootmean(behdt.K_S_x-behdt.K_S_y,'boots',10000) 
% mean(log(exp(behdt.K_S_x)/86400))
% Mk_SDD_s1 = -2.2290 Mk_SDD_s2 = -2.0595
% p = 0.2944 ci = -0.4893    0.1447


%% Stress
strdt = readtable('../data/dfjstr.csv');

% Between Genders, only s1 was found before - not anymore
[p,ci] = bootmean(strdt(strcmp(strdt.sex,'f'),:).s1,strdt(strcmp(strdt.sex,'m'),:).s1,'boots',10000) 
% mean(strdt(strcmp(strdt.sex,'f'),:).s1)
% Mf = 0.8913 Mm = 1.5101
% old -  p = 0.0126, ci = 0.5710     4.6570
% new -  p = 0.0118, ci = 0.0960    1.9000

[p,ci] = bootmean(strdt(strcmp(strdt.sex,'f'),:).ls1,strdt(strcmp(strdt.sex,'m'),:).ls1,'boots',10000) 
% mean(strdt(strcmp(strdt.sex,'f'),:).ls1)
% Mf = -0.1789 Mm = 0.1488
% p = 0.0988, ci = -0.5604    1.0886

% Saliva across sessions - session 1 is different

[p,ci] = bootmean(strdt.ls1-strdt.ls2,'boots',10000) 
% mean(strdt.ls1)
% Ms1 = -0.0465 Ms2 = -0.3288
% p = 0.0212, ci =  0.0456    0.4981

[p,ci] = bootmean(strdt.ls2-strdt.ls3,'boots',10000) 
% Ms2 = -0.3288 Ms3 = -0.3300
% p = 0.9845, ci =  -0.1896    0.1979

[p,ci] = bootmean(strdt.ls1-strdt.ls3,'boots',10000) 
% Ms1 = -0.0465 Ms3 = -0.3300
% p = 0.0108, ci =  0.0680    0.4847

% Hair across sessions - not significantly different

[p,ci] = bootmean(strdt.lh1-strdt.lh2,'boots',10000) 
% nanmean(strdt.lh1)
% Mh1 = 2.8069 Mh2 = 2.6136
% p = 0.1618, ci =  -0.0781    0.4627

[p,ci] = bootmean(strdt.lh2-strdt.lh3,'boots',10000) 
% Mh2 = 2.6136 Mh3 = 2.6118
% p = 0.9817, ci =  -0.1927    0.2058

[p,ci] = bootmean(strdt.lh1-strdt.lh3,'boots',10000) 
% Mh1 = 2.8069 Mh3 = 2.6118
% p = 0.2080, ci =  -0.1030    0.4899