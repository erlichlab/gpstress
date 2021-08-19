# rho split by KS>KL

# Setup -------
library(ggplot2)
library(data.table)

fig4f = function(ds_fits,risk_fits){
  ds_fits$K_S = log(exp(ds_fits$K_S)/86400) # change units to be comparable
  fits <- merge.data.table(ds_fits,risk_fits, by='subjid')
  p <- ggplot(data=fits, aes(x=r, group=K_S>K_L, fill=K_S>K_L)) +
    geom_density(adjust=1.5, alpha=.4) +
    #geom_histogram() +
    scale_fill_viridis(discrete = TRUE) +
    xlab(TeX('$\\rho$')) +
    labs(fill = TeX('$log(k_{SV})>log(k_{LV})$')) +
    xlim(-0.5,2.0)+
    theme(text = element_text(size=15)) +
    theme_bw()
  #ggsave('../../figs/fig4f.pdf',
  #       units = 'in', width = 4, height = 2, scale = 1, plot = p)
  return(p)
}