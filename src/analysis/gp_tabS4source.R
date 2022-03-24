# Setup -----------
library(dplyr)
library(corrplot)

table4 = function(data){
  res <- rcorr(as.matrix(data))
  return(res) # gives also total number of observations
}