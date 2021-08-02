function gp_fig3d()
% dbc can be removed after all subjects renamed and data stored in one .mat
dbc = db.labdb.getConnection();
dbc.use('jenya');
% rs_bi
qr = 'select * from stanfits_gp_delay_rs0_bi';
params_dtb = dbc.query(qr);
% prepare data
params_a = table2array(params_dtb(:,:)); % followup group
s_idx = find(strcmpi(params_dtb.Properties.VariableNames,'K_S'));
se_idx = find(strcmpi(params_dtb.Properties.VariableNames,'K_S_sd'));
l_idx = find(strcmpi(params_dtb.Properties.VariableNames,'K_L'));
le_idx = find(strcmpi(params_dtb.Properties.VariableNames,'K_L_sd'));
x(:,1) = log(exp(params_a(:,s_idx))/86400);
x(:,2) = params_a(:,se_idx);
x(:,3) = x(:,2);
y(:,1) = params_a(:,l_idx);
y(:,2) = params_a(:,le_idx);
y(:,3) = y(:,2);
% Fig 2A
figure;
cl1 = colormap(parula(10));
e = errbar(x(:,1),y(:,1),y(:,2),y(:,3),'Color', [0.6 0.6 0.6]);
hold on;
ex = errbar(x(:,1),y(:,1),x(:,2),x(:,3),'horiz','Color', [0.6 0.6 0.6]);
b  = deming(x(:,1), y(:,1));
h3 = plot([-10; x(:,1); 4],b(1) + b(2).*[-10; x(:,1); 4],'Color',cl1(1,:));
draw.unity;
s = scatter(x(:,1),y(:,1),[],cl1(1,:),'filled','MarkerEdgeColor',[0.3 0.3 0.3]);
hold on;
ylabel('log(k_{LV}), k_{LV} ~ 1/day');
xlabel('log(k_{SV}), k_{SV} ~ 1/sec');
set (gca,'FontSize', 16);
set(gca,'Xtick',[-8 -4 0]);
set(gca,'Ytick',[-8 -4 0]);
[tau_k1,tau_k_p1] = corr(y(:,1),x(:,1));
if tau_k_p1<0.01
starp1='**';
elseif tau_k_p1<0.05
starp1='*';
else
starp1='';
end
txt1 = sprintf('Pearson r = %5.2f %s',tau_k1,starp1);
text(-9,3,txt1,'FontSize', 16,'Color',cl1(1,:));
ylim([-10,4]);
xlim([-10,4]);
set(gcf,'PaperPosition',[0 0 5 4]);
set(gcf, 'PaperSize', [5 4]);
saveas(gcf, '~/Library/Mobile Documents/com~apple~CloudDocs/GP_Analysis/F3d_rs0.pdf')