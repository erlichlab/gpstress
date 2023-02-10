# Setup -----------
library(ggplot2)
library(dplyr)
library(data.table)
#library(ggbiplot)
library(lattice)
library(corrplot)
library(RColorBrewer)

fig3b = function(data){
  data1 = dplyr::select(data,c(pss,bepsi,lcu,ls1,ls2,ls3,lh1,lh2,lh3))
  df = na.omit(data1)
  #df = data
  Mc <- cor(df)
  resc <- cor.mtest(df, conf.level = .95)
  #pdf(file = "../../figs/fig3b.pdf")
  p = corrplot(Mc, method = "color", type = "upper", p.mat = resc$p, 
               sig.level = 0.05, col = brewer.pal(n=10, name = "PuOr"), tl.col = "purple", 
               tl.cex = 1.8, cl.cex = 1.4) 
  #dev.off()
  return(p)
}