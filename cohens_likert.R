library("tidyr")
library("psych")
library("lsr")
setwd("/home/aahowel3/Documents/scienceisfun_2020/likert")

data=read.csv("SIF_Likert_prepost_2020_revscore_catcolumns_factoranalysis.csv")
#interest
siadf=data[,c("Subjects","presia","postsia")]
siadf=gather(siadf, SIA, SIAscore, presia:postsia, factor_key=TRUE)
cohensD(SIAscore ~ SIA, data = siadf, method = "paired")
#expectancy 
sedf=data[,c("Subjects","preSE","postSE")]
sedf=gather(sedf, SE, SEscore, preSE:postSE, factor_key=TRUE)
cohensD(SEscore ~ SE, data = sedf, method = "paired")
#energy
endf=data[,c("Subjects","preenergy","postenergy")]
endf=gather(endf, energy, energy_score, preenergy:postenergy, factor_key=TRUE)
cohensD(energy_score ~ energy, data =endf, method = "paired")

data=read.csv("SIF_Likert_prepost_2020_revscore_catcolumns_theorybased.csv")
#interest
siadf=data[,c("Subjects","presia","postsia")]
siadf=gather(siadf, SIA, SIAscore, presia:postsia, factor_key=TRUE)
cohensD(SIAscore ~ SIA, data = siadf, method = "paired")
#expectancy 
sedf=data[,c("Subjects","preSE","postSE")]
sedf=gather(sedf, SE, SEscore, preSE:postSE, factor_key=TRUE)
cohensD(SEscore ~ SE, data = sedf, method = "paired")
#additudesandvalues
avdf=data[,c("Subjects","preAV","postAV")]
avdf=gather(avdf, AV, AVscore, preAV:postAV, factor_key=TRUE)
cohensD(AVscore ~ AV, data =avdf, method = "paired")



