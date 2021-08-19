# GP_posterior

# Setup -------

library(bayesplot)
library(brms)
#library(ggthemes)
library(ggplot2)

plot_each = function(x, xl){
  p = mcmc_areas(x, prob=.8, prob_outer = 0.9999, point_est = 'mean') +  
    vline_at(x, colMeans, size=.1, color='gray') +
    theme(text = element_text(family = 'sans')) +
    scale_y_discrete(expand = expand_scale(add = c(.5,1.2))) + 
    xlab(xl)
  return(p)
}

fig2b = function(posterior){
  logtau= sprintf('$log(\\tau)$')
  pn = plot_each(posterior$noise, TeX(logtau)) + scale_x_continuous(limits=c(-0.3,0.7), breaks = c(-0.2,0.2,0.6),labels = c('-0.2','0.2','0.6'))
  pk = plot_each(posterior$logk, 'log(k)') 
  pr = plot_each(posterior$rews, 'rews') + scale_x_continuous(limits=c(0.3,1), breaks = c(0.5,0.7),labels = c('0.5','1'))
  pg = bayesplot_grid(pk,pn,pr, grid_args = c(ncol=3))
  #ggsave('../../figs/fig2b.pdf',
  #       units = 'in', width = 3, height = 3, scale = 1, plot = pg)
  return(pg)
}

fig2d = function(posterior){
  logtau= sprintf('$log(\\tau)$')
  pn = plot_each(posterior$noise, TeX(logtau)) #+ scale_x_continuous(limits=c(-0.,0.7), breaks = c(-0.2,0.2,0.6),labels = c('-0.2','0.2','0.6'))
  pk = plot_each(posterior$logk, 'log(k)') 
  pr = plot_each(posterior$rews, 'rews') #+ scale_x_continuous(limits=c(0.3,1), breaks = c(0.5,0.7),labels = c('0.5','1'))
  pg = bayesplot_grid(pk,pn,pr, grid_args = c(ncol=3))
  #ggsave('../../figs/fig2d.pdf',
  #       units = 'in', width = 3, height = 3, scale = 1, plot = pg)
  return(pg)
}
