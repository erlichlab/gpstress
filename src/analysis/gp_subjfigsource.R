# Setup -----------
library(magrittr)
library(dplyr)
library(forcats)
library(tidyr)
library(modelr)
library(tidybayes)
library(ggplot2)
library(ggstance)
library(ggridges)
library(cowplot)
library(rstan)
library(brms)
library(latex2exp)
library(data.table)
theme_set(theme_tidybayes() +  background_grid())
bino = function(x){
  out = binom.test(sum(x), length(x))
  df = data.frame(y = mean(x), ymin=out$conf.int[1], ymax=out$conf.int[2])
  return(df)
}

plot_subject_ds = function(sind,fits,these_trials){
  sr = ds_r2 %>% filter(subjid==subjids[sind], unit=='1') %>% select(r2) %>% as.double()
  lr = ds_r2 %>% filter(subjid==subjids[sind], unit=='0') %>% select(r2) %>% as.double()
  fitstr1 = sprintf('log(k)\\[SDD,DDD\\]=\\[$%.1f, %.1f$\\]',
                    log((exp(fits$K_S[sind]))/86400), fits$K_L[sind])
  fitstr2= sprintf('log($\\tau$)\\[SDD,DDD\\]=\\[$%.1f, %.1f$\\]',
                   fits$noise_S[sind],fits$noise_L[sind])
  fitstr3= sprintf('rews\\[SDD,DDD\\]=\\[$%.1f, %.1f$\\]',
                   fits$rews_S[sind],fits$rews_L[sind])
  fitstr4 =  sprintf('$r^2$\\[SDD,DDD\\]=\\[$%0.2f,%0.2f$\\]', sr, lr)
  unit_names <- as_labeller(
    c('SV'="SDD",'LV'="DDD",
    '3'='3','6.5'='6.5','14'='14','30'='30','64'='64')
  )
  p = ds.subj %>%
    ggplot(aes(x = rewmag, y = .value/n_trials, color = ordered(delaybin), fill = ordered(delaybin))) + 
    facet_grid(unit ~ delaybin, labeller = unit_names, drop=TRUE) +
    stat_lineribbon(aes(y = .value/n_trials), .width = c(.99, .80, .50), alpha = 1/4, size = 0.1) + 
    stat_summary_bin(aes(y = .value), bins = 4, size = .05, fun.data = bino, data = these_trials %>% mutate(.value=choice) ) +
    labs(y='P(Delayed Option)', x='Reward Magnitude', color='Delay') + 
    guides(fill='none', color='none') +
    scale_y_continuous(breaks=c(0,0.5,1)) +
    scale_x_continuous(breaks = c(0,5,10)) +
    theme(
      plot.margin = margin(30,1,1,1),
      text = element_text(size=7),
      strip.text = element_text(color = "black", 
                                margin = margin(1, 1, 1, 1))
    )
  q = ggdraw(p) +
    draw_label(TeX(fitstr1), x = 0.05,y = 0.98, hjust = 0, vjust = 1,size=6) +
    draw_label(TeX(fitstr2), x = 0.05,y = 0.94, hjust = 0, vjust = 1,size=6) +
    draw_label(TeX(fitstr3), x = 0.05,y = 0.90, hjust = 0, vjust = 1,size=6) +
    draw_label(TeX(fitstr4), x = 0.55,y = 0.94, hjust = 0, vjust = 1,size=6)
  
  ggsave(paste0('../../figs/ds.pdf'),plot=q, units = 'in', width=2.5, height =2.5)
  return(q)
}

plot_subject_dw = function(sind,fits,these_trials){
wr = dw_r2 %>% filter(subjid==subjids[sind], unit=='2') %>% select(r2) %>% as.double()
dr = dw_r2 %>% filter(subjid==subjids[sind], unit=='0') %>% select(r2) %>% as.double()
fitstr1 = sprintf('log(k)\\[WDD,DDD\\]=\\[$%.1f, %.1f$\\]',
                  log((exp(fits$K_W[sind]))*7), fits$K_L[sind])
fitstr2= sprintf('log($\\tau$)\\[WDD,DDD\\]=\\[$%.1f, %.1f$\\]',
                 fits$noise_W[sind],fits$noise_L[sind])
fitstr3= sprintf('rews\\[WDD,DDD\\]=\\[$%.1f, %.1f$\\]',
                 fits$rews_W[sind],fits$rews_L[sind])
fitstr4 =  sprintf('$r^2$\\[WDD,DDD\\]=\\[$%0.2f,%0.2f$\\]', wr, dr)
unit_names_dw <- as_labeller(
  c('DV'="DDD",'WV'="WDD",
    '1'='1','3'='3','7'='7','14'='14','28'='28','35'='35','64'='64')
)
p=dw.subj %>%  
  ggplot(aes(x = rewmag, y = .value/n_trials, color = ordered(delaybin), fill = ordered(delaybin))) + 
  facet_grid(unit~delaybin, labeller = unit_names_dw, drop=TRUE) +
  stat_lineribbon(aes(y = .value/n_trials), .width = c(.99, .80, .50), alpha = 1/4, size = 0.1) + 
  stat_summary_bin(aes(y = .value), bins = 4, size = .05, fun.data = bino, data = these_trials %>% mutate(.value=choice)) +
  labs(y='P(Delayed Option)', x='Reward Magnitude', color='Delay') + #, title=TeX(fitstr1), subtitle = TeX(fitstr2)) +
  guides(fill='none', color='none') +
  scale_y_continuous(breaks=c(0,0.5,1)) +
  scale_x_continuous(breaks = c(0,5,10)) +
  theme( # plot.subtitle = element_text(hjust=0, size=8,margin=margin(1,1,1,1)), plot.title = element_text(hjust=0, size=8,margin=margin(1,1,1,1)),
    plot.margin = margin(30,1,1,1),
    text = element_text(size=7),
    strip.text = element_text(color = "black", 
                              margin = margin(1, 1, 1, 1))
  )
q = ggdraw(p) +
  draw_label(TeX(fitstr1), x = 0.05,y = 0.98, hjust = 0, vjust = 1,size=6) +
  draw_label(TeX(fitstr2), x = 0.05,y = 0.94, hjust = 0, vjust = 1,size=6) +
  draw_label(TeX(fitstr3), x = 0.05,y = 0.90, hjust = 0, vjust = 1,size=6) +
  draw_label(TeX(fitstr4), x = 0.55,y = 0.94, hjust = 0, vjust = 1,size=6)
ggsave(paste0('../../figs/','dw.pdf'),plot=q, units = 'in', width=2.5, height =2.5)
return(q)
}

plot_subject_risk = function(sind,fitsgp,these_trials){
rr = risk_r2 %>% filter(subjid==subjids[sind]) %>% select(r2) %>% as.double()
#fitss = fits  %>% filter(subjid == subjids[sind])
fitstr1 = sprintf('$\\rho$ = $%.1f$',
                  fitsgp$r[sind])

fitstr2= sprintf('1/$\\beta$ = $%.1f$',
                 1/(fitsgp$beta[sind]))

fitstr3 =  sprintf('$r^2$ = $%0.2f$', rr)

p=risk.subj %>%  
  ggplot(aes(x = rewmag, y = .value, color = ordered(probability), fill = ordered(probability))) + 
  facet_grid(.~probability, labeller = labeller(.multi_line = FALSE), drop=TRUE) +
  stat_lineribbon(aes(y = .value), .width = c(.99, .80, .50), alpha = 1/4, size = 0.1) + 
  stat_summary(size = .05, fun.data = bino, data = these_trials %>% mutate(.value=choice)) +
  labs(y='P(Chose Lottery)', x='Reward Magnitude', color='Probability') + #, title=TeX(fitstr1), subtitle = TeX(fitstr2)) +
  guides(fill='none', color='none') +
  scale_y_continuous(breaks=c(0,0.5,1)) +
  scale_x_continuous(breaks = c(0,25,50)) +
  theme( # plot.subtitle = element_text(hjust=0, size=8,margin=margin(1,1,1,1)), plot.title = element_text(hjust=0, size=8,margin=margin(1,1,1,1)),
    plot.margin = margin(30,1,1,1),
    text = element_text(size=7),
    strip.text = element_text(color = "black", 
                              margin = margin(1, 1, 1, 1))
  )
q = ggdraw(p) +
  draw_label(TeX(fitstr1), x = 0.05,y = 0.98, hjust = 0, vjust = 1,size=6) +
  draw_label(TeX(fitstr2), x = 0.05,y = 0.94, hjust = 0, vjust = 1,size=6) +
  draw_label(TeX(fitstr3), x = 0.05,y = 0.90, hjust = 0, vjust = 1,size=6)

#ggsave(paste0('../../figs/subj_figs/','risk_',sind,'.pdf'),plot=q, units = 'in', width=2.5, height =2.5)
return(q)
}

#-----

fig2b = function(ds_trials,fits,ds_r2){
  these_fits = fits %>% filter(subjid == 14)
  breaksL <- c(2,6,13,29,62,65)
  breaksS <- c(2/86400,6/86400,13/86400,29/86400,62/86400,65/86400)
  # specify interval/bin labels
  tags <- c("3","6.5", "14", "30", "64")
  # bucketing values into bins
  ds_trials$delaybin <- cut(ds_trials$delay,
                                breaks=breaksL,
                                include.lowest=TRUE,
                                right=FALSE,
                                labels=tags)
  ds_trials$delaybin[ds_trials$unit == "1"] = cut(ds_trials$delay[ds_trials$unit == "1"], breaks=breaksS,include.lowest=TRUE,right=FALSE,labels=tags)
  these_trials = ds_trials %>% filter(subjid == 14)
  these_trials$unit = factor(these_trials$unit, levels=c('1','0'), labels=c('SV','LV'))
  p = plot_subject_ds(1,these_fits,these_trials)
  return(p)
}

fig_dw = function(dw_trials,fits,dw_r2){
  these_fits = fits %>% filter(subjid == 40)
  # bin delays ahead of time
  # set up cut-off values
  breaksL <- c(0,2,6,13,20,29,62,65)
  breaksW <- c(0,2*7,6*7,13*7,20*7,29*7,62*7,65*7)
  # specify interval/bin labels
  tags <- c("1","3","7", "14","28", "35", "64")
  # bucketing values into bins
  dw_trials$delaybin <- cut(dw_trials$delay,
                                breaks=breaksL,
                                include.lowest=TRUE,
                                right=FALSE,
                                labels=tags)
  dw_trials$delaybin[dw_trials$unit == "2"] = cut(dw_trials$delay[dw_trials$unit == "2"], breaks=breaksW,include.lowest=TRUE,right=FALSE,labels=tags)
  these_trials = dw_trials %>% filter(subjid == 40)
  these_trials$unit = factor(these_trials$unit, levels=c('2','0'), labels=c('WV','DV'))
  p = plot_subject_dw(1,these_fits,these_trials)
  return(p)
}

fig_risk = function(risk_trials,fits,risk_r2){
  these_fits = fits %>% filter(subjid == 16)
  these_trials = risk_trials %>% filter(subjid == 16)
  p = plot_subject_risk(1,these_fits,these_trials)
  return(p)
}