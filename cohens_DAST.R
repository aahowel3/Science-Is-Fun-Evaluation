setwd("/home/aahowel3/Documents/scienceisfun_2020/dast")

data=read.csv("DAST_catcolumns.csv")

PCdf=data[,c("Subjects","prePC","postPC")]
PCdf=gather(PCdf, PC, PCscore, prePC:postPC, factor_key=TRUE)

cohensD(PCscore ~ PC, data = PCdf, method = "paired")
