# Setup -----------
library(ggplot2)
library(dplyr)
library(data.table)
#library(ggbiplot)
library(lattice)
library(corrplot)
library(RColorBrewer)

impute_merge = function (ds_fits, ds12_fits, dw_fits, mf, dfjstr){
  # impute
  k33= as.numeric(ds_fits[ds_fits$subjid==33,])
  rk33 = rep(k33[-1],2)
  crk33 = c(33, rk33)
  ds12_impfits <- rbind(ds12_fits, crk33)
  # merge fits
  ds12w_impfits = dw_fits %>% left_join(ds12_impfits, by="subjid")
  # merge model free
  ds12w_impfits_mf = ds12w_impfits %>% left_join(mf, by="subjid")
  # merge stress
  data = ds12w_impfits_mf %>% left_join(dfjstr, by="subjid")
  return(data)
}

corpl_bs = function(ds_fits, ds12_fits, dw_fits, mf, dfjstr){
  data = impute_merge(ds_fits, ds12_fits, dw_fits, mf, dfjstr)
  # select data
  data1 = dplyr::select(data,c(K_S.x,K_S.y,K_L.x,K_L.y,K_L,PL_S1,PL_S2,PL_L1,PL_L2,PL_D,pss,bepsi,lcu,ls1,ls2,ls3,lh1,lh2,lh3,PC1,PC2,PC3,PC4))
  df = na.omit(data1)
  #df = data
  Mc <- cor(df)
  resc <- cor.mtest(df, conf.level = .95)
  #pdf(file = "../../figs/cor_bs.pdf")
  p = corrplot(Mc, method = "color", type = "upper", p.mat = resc$p, 
               sig.level = 0.05, col = brewer.pal(n=10, name = "YlGnBu"), tl.col = "purple", 
               tl.cex = 0.5, cl.cex = 0.5, pch.cex = 0.5) 
  # tl.cex = 0.4, cl.cex = 0.4, number.cex = 0.4
  #dev.off()
  return(p)
}

corpl_ws = function(ds_fits, ds12_fits, dw_fits, mf, dfjstr){
  data = impute_merge(ds_fits, ds12_fits, dw_fits, mf, dfjstr)
  data$K_Sd2 = data$K_S.y-data$K_S.x
  data$K_Ld2 = data$K_L.y-data$K_L.x
  data$K_Ld3 = data$K_L-data$K_L.x
  data$K_Ld32 = data$K_L-data$K_L.y
  data$PL_Sd2 = data$PL_S2-data$PL_S1
  data$PL_Ld2 = data$PL_L2-data$PL_L1
  data$PL_Ld3 = data$PL_D-data$PL_L1
  data$PL_Ld32 = data$PL_D-data$PL_L2
  # select data
  data2 = dplyr::select(data,c(K_Sd2,K_Ld2,K_Ld3,K_Ld32,PL_Sd2,PL_Ld2,PL_Ld3,PL_Ld32,lds2,lds3,lds32,ldh2,ldh3,ldh32))
  df = na.omit(data2)
  #df = data
  Mc <- cor(df)
  resc <- cor.mtest(df, conf.level = .95)
  #pdf(file = "../../figs/cor_ws.pdf")
  p = corrplot(Mc, method = "color", type = "upper", p.mat = resc$p, 
               sig.level = 0.05, col = brewer.pal(n=10, name = "YlGnBu"), tl.col = "purple", 
               tl.cex = 0.5, cl.cex = 0.5, pch.cex = 0.5) 
  # tl.cex = 0.4, cl.cex = 0.4, number.cex = 0.4
  #dev.off()
  return(p)
}