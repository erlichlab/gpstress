# Setup -----------
library(ggplot2)
library(dplyr)
library(data.table)
library(ggbiplot)
library(lattice)
library(corrplot)
library(RColorBrewer)
library(ggpubr)

figs6 = function(data,x1){
  data1 = dplyr::select(data,c(ls1,ls2,ls3,lh1,lh2,lh3,pss,bepsi,lcu,sex))
  dataX = na.omit(data1)
  gr <- factor(dataX$sex)
  dataX <- subset(dataX, select = -c(sex))
  dataX.pca <- prcomp(dataX, center = TRUE,scale. = TRUE)
  p1 <- ggbiplot(dataX.pca, ellipse=TRUE, groups=gr)+
    scale_colour_manual(name="Gender", values= c("#542788","#E08214","#B2ABD2"), labels = c('female','male','na'))+
    geom_hline(yintercept = 0) +
    geom_vline(xintercept = 0) +
    theme(text = element_text(size=15)) +
    theme_bw()
  #ggsave('../../figs/figS6u.pdf',plot=p1, units = 'in', width = 4, height = 4)
  p2 <- ggbiplot(dataX.pca, choices = 2:3, ellipse=TRUE, groups=gr)+
    scale_colour_manual(name="Gender", values= c("#542788","#E08214","#B2ABD2"), labels = c('female','male','na'))+
    geom_hline(yintercept = 0) +
    geom_vline(xintercept = 0) +
    theme(text = element_text(size=15)) +
    theme_bw()
  #ggsave('../../figs/figS6d.pdf',plot=p2, units = 'in', width = 4, height = 4)
  cumpro <- cumsum(dataX.pca$sdev^2 / sum(dataX.pca$sdev^2))
  #pdf(file = "../../figs/figS6cu.pdf", width = 4, height = 3)
  p3 <- plot(cumpro[0:9], xlab = "PC #", ylab = "Amount of explained variance", main = "Cumulative variance plot")
  abline(v = x1, col="purple", lty=5)
  abline(h = cumpro[x1], col="purple", lty=5)
  #dev.off()
  #pdf(file = "../../figs/figS6cd.pdf", width = 4, height = 3)
  p4 <- screeplot(dataX.pca, type = "l", npcs = 9, main = "Screeplot of the first PCs")
  abline(h = 1, col="orange", lty=5)
  #dev.off()
  return(list(dataX.pca,p1, p2, p3, p4))
}

table2 = function(data,choices) {
    data1 = dplyr::select(data,c(ls1,ls2,ls3,lh1,lh2,lh3,pss,bepsi,lcu,sex))
    dataX = na.omit(data1)
    gr <- factor(dataX$sex)
    dataX <- subset(dataX, select = -c(sex))
    dataX.pca <- prcomp(dataX, center = TRUE,scale. = TRUE)
    nobs.factor <- sqrt(nrow(dataX.pca$x) - 1)
    d <- dataX.pca$sdev
    u <- sweep(dataX.pca$x, 2, 1 / (d * nobs.factor), FUN = '*')
    v <- dataX.pca$rotation
    # Scores
    choices <- pmin(choices, ncol(u))
    df.u <- as.data.frame(sweep(u[,choices], 2, d[choices]^0, FUN='*'))
    # Directions
    v <- sweep(v, 2, d^1, FUN='*')
    df.v <- as.data.frame(v[, choices])
    names(df.u) <- c('xvar', 'yvar')
    names(df.v) <- names(df.u)
    df.u <- df.u * nobs.factor
    # Scale the radius of the correlation circle so that it corresponds to 
    # a data ellipse for the standardized PC scores
    r <- sqrt(qchisq(0.69, df = 2)) * prod(colMeans(df.u^2))^(1/4) 
    # circle.prob = 0.69 from biplot
    # Scale directions
    v.scale <- rowSums(v^2)
    df.v <- r * df.v / sqrt(max(v.scale))
    df.v$angle <- with(df.v, (180/pi) * atan(yvar / xvar))
    return(df.v)
}

pca_loads = function(data,choices) {
  data1 = dplyr::select(data,c(ls1,ls2,ls3,lh1,lh2,lh3,pss,bepsi,lcu,sex))
  dataX = na.omit(data1)
  gr <- factor(dataX$sex)
  dataX <- subset(dataX, select = -c(sex))
  dataX.pca <- prcomp(dataX, center = TRUE,scale. = TRUE)
  return(dataX.pca$rotation)
}

plot_pc4 = function(data) {
  # need to sort for highest absolute value and report the variable and loading for the best five for four first PCs
  dpc1 = data.frame(data[sort(abs(data[,1]),decreasing=T,index.return=T)[[2]],])
  dpc1$name <- factor(rownames(dpc1), levels = rownames(dpc1))
  pc1 <- ggplot(dpc1[1:5,], aes(x = name, y = PC1)) +
    geom_bar(stat = "identity") +
    coord_flip() + xlab('stress var') + theme_bw()
  dpc2 = data.frame(data[sort(abs(data[,2]),decreasing=T,index.return=T)[[2]],])
  dpc2$name <- factor(rownames(dpc2), levels = rownames(dpc2))
  pc2 <- ggplot(dpc2[1:5,], aes(x = name, y = PC2)) +
    geom_bar(stat = "identity") +
    coord_flip() + xlab('stress var') + theme_bw()
  dpc3 = data.frame(data[sort(abs(data[,3]),decreasing=T,index.return=T)[[2]],])
  dpc3$name <- factor(rownames(dpc3), levels = rownames(dpc3))
  pc3 <- ggplot(dpc3[1:5,], aes(x = name, y = PC3)) +
    geom_bar(stat = "identity") +
    coord_flip() + xlab('stress var') + theme_bw()
  dpc4 = data.frame(data[sort(abs(data[,4]),decreasing=T,index.return=T)[[2]],])
  dpc4$name <- factor(rownames(dpc4), levels = rownames(dpc4))
  pc4 <- ggplot(dpc4[1:5,], aes(x = name, y = PC4)) +
    geom_bar(stat = "identity") +
    coord_flip() + xlab('stress var') + theme_bw()
  ggarrange(pc1, pc2, pc3, pc4, ncol = 2, nrow = 2)
}