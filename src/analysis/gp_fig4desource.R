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

fig4d = function(posterior){
  r = sprintf('$\\rho$')
  beta1 = sprintf('$1/\\beta$')
  pb = plot_each(1/posterior$beta, TeX(beta1)) + scale_x_continuous(breaks = c(0.3,0.5),labels = c('0.3','0.5'))
  pr = plot_each(posterior$rho, TeX(r))  + scale_x_continuous(breaks = c(0.6,0.7,0.8),labels = c('0.6','0.7','0.8'))
  pg = bayesplot_grid(pr,pb, grid_args = c(ncol=2))
  #ggsave('../../figs/fig4d.pdf',
  #       units = 'in', width = 3, height = 3, scale = 1, plot = pg)
  return(pg)
}

fig4e = function(posterior){
  k = sprintf('$\\kappa$')
  beta1 = sprintf('$1/\\beta$')
  pb = plot_each(1/posterior$beta, TeX(beta1)) + scale_x_continuous(breaks = c(0.6,0.8,1.0),labels = c('0.6','0.8','1.0'))
  pr = plot_each(posterior$kappa, TeX(k)) + scale_x_continuous(breaks = c(0.2,0.3,0.4),labels = c('0.2','0.3','0.4'))
  pg = bayesplot_grid(pr,pb, grid_args = c(ncol=2))
  #ggsave('../../figs/fig4e.pdf',
  #       units = 'in', width = 3, height = 3, scale = 1, plot = pg)
  return(pg)
}
