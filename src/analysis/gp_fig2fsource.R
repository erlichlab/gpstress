# rho split by KS>KL

# Setup -------
library(ggplot2)
library(data.table)
require(latex2exp)
library(viridis)
library(RColorBrewer)

fig2f = function(ds_fits,risk_fits){
  ds_fits$K_S = log(exp(ds_fits$K_S)/86400) # change units to be comparable
  fits <- merge.data.table(ds_fits,risk_fits, by='subjid')
  p <- ggplot(data=fits, aes(x=r, group=K_S>K_L, fill=K_S>K_L)) +
    geom_density(adjust=1.5, alpha=.4) +
    #geom_histogram() +
    scale_fill_viridis(discrete = TRUE) +
    xlab(TeX('$\\rho$')) +
    labs(fill = TeX('$k_{SV} > k_{LV}$')) +
    xlim(-0.5,2.0)+
    #theme(element_text(size=15)) +
    theme_classic(base_size = 15)
  ggsave('../../figs/fig2f.pdf',
         units = 'in', width = 5, height = 3, scale = 1, plot = p)
  return(p)
}