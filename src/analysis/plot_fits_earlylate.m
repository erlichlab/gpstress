function plot_fits_earlylate(data1_m,full,treat,varargin)
% varargin # of early trials
earlyn = varargin{1};
    if treat == 'DS'
        treatment = {'L' 'S'};
        tid = 'LS';
        tnum = 1;
    elseif treat == 'DW'
        treatment = {'L' 'W'};
        tid = 'LW';
        tnum = 2;
    else
        treatment = {'L' 'S' 'W'};
        tid = 'LSW';
        tnum = 3;
    end
   
% all trials
figure(1); clf;
ax = draw.jaxes
cl1 = colormap(parula(6));
hold on;
for tx3=1:numel(treatment)
    noisetxt = sprintf('noise_%s',treatment{tx3});
    logtxt = sprintf('K_%s',treatment{tx3});
    rtxt = sprintf('rews_%s',treatment{tx3});
    noise_idx = find(strcmpi(full.Properties.VariableNames,noisetxt));
    logk_idx = find(strcmpi(full.Properties.VariableNames,logtxt));
    rews_idx = find(strcmpi(full.Properties.VariableNames,rtxt));
    id_idx = find(strcmpi(full.Properties.VariableNames,'subjid'));
    fullar = table2array(full(:,[id_idx,logk_idx,noise_idx,rews_idx])); 
    data1_ses = data1_m(ismember(data1_m.treat_ind,tid(tx3)),:);
    % join with logk and noise per each subject
    data1_ses = join(data1_ses,full(:,[logk_idx,noise_idx,rews_idx,id_idx]));
    full_all = fullar; % all participants
    tout_all = data1_ses(ismember(data1_ses.subjid,full_all(:,1)),:);
    choice = tout_all.choice;
    logk_idx2 = find(ismember(tout_all.Properties.VariableNames,sprintf('K_%s',treatment{tx3})));
    logk = table2array(tout_all(:,logk_idx2));
    rews_idx2 = find(ismember(tout_all.Properties.VariableNames,sprintf('rews_%s',treatment{tx3})));
    rews = table2array(tout_all(:,rews_idx2));
    v1 = tout_all.rewmag; 
    t1 = tout_all.unitdelay;
    v2 = tout_all.smag;
    xhat = exp(rews).*v1./(1 + exp(logk).*t1) - v2;
    [bx,by,be]=stats.binned(xhat, choice==1, 'n_bins', 10); % Jeff prefers stats.binned
    if tx3<=2
        if tnum ~=2
            h1 = draw.errorplot(ax,bx,by,be,'Color',(cl1(2*tx3,:)));
        else
            if tx3==1
                h1 = draw.errorplot(ax,bx,by,be,'Color',(cl1(2*tx3,:)));
            else
                h2 = draw.errorplot(ax,bx,by,be,'Color',(cl1(3*tx3-1,:)));
            end
        end
    else
        h2 = draw.errorplot(ax,bx,by,be,'Color',(cl1(2*tx3-1,:)));
    end
    [gB,gDEV,gSTATS] = glmfit(xhat, choice ==1, 'binomial','link','probit');
    xfit = -6:0.1:6;  
    yfit = glmval(gB, xfit, 'probit');
    if tx3==1
        h3 = plot(ax,xfit,yfit,'Color',(cl1(2*tx3,:)),'LineWidth',2,'LineStyle','--');
        treatment1 = treatment{tx3};
    else
        if numel(treatment)==2 && tnum ~=2
                h4 = plot(ax,xfit,yfit,'Color',(cl1(2*tx3,:)),'LineWidth',2,'LineStyle','-.');
        
        elseif numel(treatment)==2 && tnum ==2
                h4 = plot(ax,xfit,yfit,'Color',(cl1(3*tx3-1,:)),'LineWidth',2,'LineStyle','-.');
        else
            if tx3==2
                h4 = plot(ax,xfit,yfit,'Color',(cl1(2*tx3,:)),'LineWidth',2,'LineStyle','-.');
                treatment2 = treatment{tx3};
            else
                h43 = plot(ax,xfit,yfit,'Color',(cl1(2*tx3-1,:)),'LineWidth',2,'LineStyle',':');
            end
        end
    end
    hold on;
end
ax.XLim = [-6 6];
ax.YLim = [0 1];
ax.YTick = [0 0.5 1];
if numel(treatment)==2
    legend ([h3 h4],{sprintf('%sV',treatment1),sprintf('%sV',treatment{tx3})},'Location','southeast');
else
    legend ([h3 h4 h43],{sprintf('%sV',treatment1),sprintf('%sV',treatment2),sprintf('%sV',treatment{tx3})},'Location','northwest');
end
legend boxoff                   % Hides the legend's axes
ylabel(ax, 'P(later)');
xlabel(ax, 'U(later) - U(sooner)');
set(ax,'FontSize',16);
fsave = sprintf('~/Library/Mobile Documents/com~apple~CloudDocs/GP_Analysis/F3_matlab_%s_%d_rs0.pdf',treat,earlyn);
outpos = get(gca,'OuterPosition');
set(gca,'OuterPosition',[outpos(1) outpos(2) + 0.005 outpos(3) outpos(4)])
set(gcf,'PaperPosition',[0 0 3 5]);
%set(gcf,'PaperPosition',[0 0 5 4]);
set(gcf, 'PaperSize', [3 5]);
%set(gcf, 'PaperSize', [5 4]);
saveas(gcf, fsave,'pdf')

% early
figure(2); clf;
ax = draw.jaxes;
cl1 = colormap(parula(6));
hold on;
for tx3=1:numel(treatment)
    noisetxt = sprintf('noise_%s',treatment{tx3});
    logtxt = sprintf('K_%s',treatment{tx3});
    rtxt = sprintf('rews_%s',treatment{tx3});
    noise_idx = find(strcmpi(full.Properties.VariableNames,noisetxt));
    logk_idx = find(strcmpi(full.Properties.VariableNames,logtxt));
    rews_idx = find(strcmpi(full.Properties.VariableNames,rtxt));
    id_idx = find(strcmpi(full.Properties.VariableNames,'subjid'));
    fullar = table2array(full(:,[id_idx,logk_idx,noise_idx,rews_idx])); 
    data1_ses = data1_m(ismember(data1_m.treat_ind,tid(tx3)),:);
    % join with logk and noise per each subject
    data1_ses = join(data1_ses,full(:,[logk_idx,noise_idx,rews_idx,id_idx]));
    full_all = fullar; % all participants
    tout_all = data1_ses(ismember(data1_ses.subjid,full_all(:,1)),:);
    tout_early = tout_all(tout_all.trialnum<earlyn+1,:); % just early 
    choice = tout_early.choice;
    logk_idx2 = find(ismember(tout_all.Properties.VariableNames,sprintf('K_%s',treatment{tx3})));
    logk = table2array(tout_early(:,logk_idx2));
    rews_idx2 = find(ismember(tout_all.Properties.VariableNames,sprintf('rews_%s',treatment{tx3})));
    rews = table2array(tout_early(:,rews_idx2));
    v1 = tout_early.rewmag;
    t1 = tout_early.unitdelay;
    v2 = tout_early.smag;
    xhat = exp(rews).*v1./(1 + exp(logk).*t1) - v2;
    [bx,by,be]=stats.binned(xhat, choice==1, 'n_bins', 10); % Jeff prefers stats.binned
    if tx3<=2
        if tnum ~=2
            h1 = draw.errorplot(ax,bx,by,be,'Color',(cl1(2*tx3,:)));
        else
            if tx3==1
                h1 = draw.errorplot(ax,bx,by,be,'Color',(cl1(2*tx3,:)));
            else
                h2 = draw.errorplot(ax,bx,by,be,'Color',(cl1(3*tx3-1,:)));
            end
        end
    else
        h2 = draw.errorplot(ax,bx,by,be,'Color',(cl1(2*tx3-1,:)));
    end
    [gB,gDEV,gSTATS] = glmfit(xhat, choice ==1, 'binomial','link','probit');
    xfit = -6:0.1:6;  
    yfit = glmval(gB, xfit, 'probit');
    if tx3==1
        h3 = plot(ax,xfit,yfit,'Color',(cl1(2*tx3,:)),'LineWidth',2,'LineStyle','--');
        treatment1 = treatment{tx3};
    else
        if numel(treatment)==2 && tnum ~=2
                h4 = plot(ax,xfit,yfit,'Color',(cl1(2*tx3,:)),'LineWidth',2,'LineStyle','-.');
        
        elseif numel(treatment)==2 && tnum ==2
                h4 = plot(ax,xfit,yfit,'Color',(cl1(3*tx3-1,:)),'LineWidth',2,'LineStyle','-.');
        else
            if tx3==2
                h4 = plot(ax,xfit,yfit,'Color',(cl1(2*tx3,:)),'LineWidth',2,'LineStyle','-.');
                treatment2 = treatment{tx3};
            else
                h43 = plot(ax,xfit,yfit,'Color',(cl1(2*tx3-1,:)),'LineWidth',2,'LineStyle',':');
            end
        end
    end
    hold on;
end
ax.XLim = [-6 6];
ax.YLim = [0 1];
ax.YTick = [0 0.5 1];
if numel(treatment)==2
    legend ([h3 h4],{sprintf('%sV',treatment1),sprintf('%sV',treatment{tx3})},'Location','southeast');
else
    legend ([h3 h4 h43],{sprintf('%sV',treatment1),sprintf('%sV',treatment2),sprintf('%sV',treatment{tx3})},'Location','northwest');
end
legend boxoff                   % Hides the legend's axes
ylabel(ax, 'P(later)');
xlabel(ax, 'U(later) - U(sooner)');
set(ax,'FontSize',16);
fsave = sprintf('~/Library/Mobile Documents/com~apple~CloudDocs/GP_Analysis/F3_matlab_%s_%d_early_rs0.pdf',treat,earlyn);
outpos = get(gca,'OuterPosition');
set(gca,'OuterPosition',[outpos(1) outpos(2) + 0.005 outpos(3) outpos(4)])
set(gcf,'PaperPosition',[0 0 3 5]);
%set(gcf,'PaperPosition',[0 0 5 4]);
set(gcf, 'PaperSize', [3 5]);
%set(gcf, 'PaperSize', [5 4]);
saveas(gcf, fsave,'pdf')