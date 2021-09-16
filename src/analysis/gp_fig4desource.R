# GP_posterior

# Setup -------

library(bayesplot)
library(brms)
#library(ggthemes)
library(ggplot2)
require(latex2exp)

plot_each_n = function(x, xl){
  p = mcmc_areas(x, prob=.8, prob_outer = 0.9999, point_est = 'mean') +  
    vline_at(x, colMeans, size=.1, color='gray') +
    theme(text = element_text(family = 'sans')) +
    scale_y_discrete(expand = expansion(add = c(.5,1.2)),
                     labels = xl)
  return(p)
}

fig4d = function(posterior){
  rbl = c("1/beta" = expression(paste("1/",beta)),
    "rho" = expression(paste(rho)))
  p = plot_each_n(posterior,rbl)
  #ggsave('../../figs/fig4d.pdf',
  #       units = 'in', width = 3, height = 3, scale = 1, plot = p)
  return(p)
}

fig4e = function(posterior){
  kbl = c("1/beta" = expression(paste("1/",beta)),
          "kappa" = expression(paste(kappa)))
  p = plot_each_n(posterior,kbl)
  #ggsave('../../figs/fig4e.pdf',
  #       units = 'in', width = 3, height = 3, scale = 1, plot = p)
  return(p)
}
