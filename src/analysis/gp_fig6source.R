# Setup -----------
library(dplyr)
library(corrplot)

table4 = function(data){
  res <- rcorr(as.matrix(data))
  return(res) # gives also total number of observations
}

fig6 = function(data){
  dataX1 = dplyr::select(data,c(profitS, RT_S, PL_S, waitS, profitS1, RT_S1, PL_S1,
                                waitS1, profitS2, RT_S2, PL_S2, waitS2,ls1,ls2,ls3,
                                lh1,lh2,lh3,pss,bepsi,lcu,ms,ts,PC1,PC2,PC3,PC4))
  dataX2 = dplyr::select(data,c(profitS, RT_S, PL_S, waitS, profitS1, RT_S1, PL_S1, 
                                waitS1, profitS2, RT_S2, PL_S2, waitS2,lds2,lds3,lds32,
                                lfs2,lfs3,lfs32,ldh2,ldh3,ldh32,lfh2,lfh3,lfh32))
  dfX1 = na.omit(dataX1)
  McX1 <- cor(dfX1)
  rescX1 <- cor.mtest(dfX1, conf.level = .95)
  #pdf(file = "../../figs/subj_figs/fig6l.pdf")
  p1 = corrplot(McX1, method = "color", type = "upper", p.mat = rescX1$p, 
               sig.level = 0.05, col = brewer.pal(n=10, name = "PuOr"), tl.col = "purple")
  #dev.off()
  dfX2 = na.omit(dataX2)
  McX2 <- cor(dfX2)
  rescX2 <- cor.mtest(dfX2, conf.level = .95)
  #pdf(file = "../../figs/subj_figs/fig6r.pdf")
  p2 = corrplot(McX2, method = "color", type = "upper", p.mat = rescX2$p, 
                sig.level = 0.05, col = brewer.pal(n=10, name = "PuOr"), tl.col = "purple")
  #dev.off()
  return(list(p1, p2))
}
