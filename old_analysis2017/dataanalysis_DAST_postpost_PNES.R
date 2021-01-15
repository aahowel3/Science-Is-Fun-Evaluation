library("ez")
library("nlme") 
library("rmarkdown")
library("PMCMR")
require("multcomp")
library("gplots")
library("pwr")
library("vcd")
library("rcompanion")
library("lsr")
library("fifer")
#dev.off() 
#run to clear plot environment 
#link to pdftex installation for knitting document, install in terminal not in Rstudio
#https://tex.stackexchange.com/questions/112734/is-it-possible-to-install-only-the-required-latex-tool-pdflatex-in-ubuntu
#use Sys.which("package") to make sure its there 

#using pre/post/postpost data
#used only paired responses, no H3/H5/P3etc 
setwd("/home/aahowel3/Documents/scienceisfun/analysis/SIF_finalanalysis_July2018/SIF_analysis_postpst_December_2018/January_2019/")
#####DID NOT USE THESE TEST, NOT REAPEATED MEASURES, NOT TEASED OUT BY 
data=read.csv("df_PNES_melt_f.csv",header=TRUE)

datapre= subset(data,data$condition=="overall appearance of scientist")
datapost= subset(data,data$condition=="poverall appearance of scientist")
datapostpost= subset(data,data$condition=="ppoverall appearance of scientist")

Ppre=subset(datapre,datapre$score == "P" | datapre$score == "p") 
Epre=subset(datapre,datapre$score == "E" | datapre$score == "e") 
Spre=subset(datapre,datapre$score == "S" | datapre$score == "s") 
Npre=subset(datapre,datapre$score == "N" | datapre$score == "n") 
Ppost=subset(datapost,datapost$score == "P" | datapost$score == "p") 
Epost=subset(datapost,datapost$score == "E" | datapost$score == "e") 
Spost=subset(datapost,datapost$score == "S" | datapost$score == "s") 
Npost=subset(datapost,datapost$score == "N" | datapost$score == "n") 
Pppost=subset(datapostpost,datapostpost$score == "P" | datapostpost$score == "p") 
Eppost=subset(datapostpost,datapostpost$score == "E" | datapostpost$score == "e") 
Sppost=subset(datapostpost,datapostpost$score == "S" | datapostpost$score == "s") 
Nppost=subset(datapostpost,datapostpost$score == "N" | datapostpost$score == "n") 

#matrix to test if theres any difference between pre/post/postpost scores 
scores=matrix(c(length(Ppre$score),length(Epre$score),length(Spre$score),length(Npre$score),
                length(Ppost$score),length(Epost$score),length(Spost$score),length(Npost$score),
                length(Pppost$score),length(Eppost$score),length(Sppost$score),length(Nppost$score)),ncol=4,byrow = TRUE)
rownames(scores)=c("pre","post","postpost")
colnames(scores)=c("P","E","S","N")
scores=as.table(scores)
chisq.test(scores,correct=TRUE)
chisq.post.hoc(scores,test="fisher.test", popsInRows=TRUE, control="bonferroni")

#matrix just to get nice plotting grouped by condition, not for analysis 
scores=matrix(c(length(Ppre$score),length(Ppost$score),length(Pppost$score),
                length(Epre$score),length(Epost$score),length(Eppost$score),
                length(Spre$score),length(Spost$score),length(Sppost$score),
                length(Npre$score),length(Npost$score),length(Nppost$score)),ncol=3,byrow = TRUE)
colnames(scores)=c("pre","post","postpost")
rownames(scores)=c("P","E","S","N")
scores=as.table(scores)
barplot(scores, beside=TRUE,legend=TRUE,args.legend = list(x   = "topright",   ### Legend location
                                                          cex = 0.8,          ### Legend text size
                                                          bty = "n"))         ### Remove legend box

#single category chi squared test 
scores=matrix(c(length(Ppre$score),length(Ppost$score),length(Pppost$score)),ncol=1,byrow = FALSE)
rownames(scores)=c("pre","post","postpost")
colnames(scores)=c("P")
scores=as.table(scores)
chisq.test(scores,correct=TRUE)

#single category chi squared test 
scores=matrix(c(length(Epre$score),length(Epost$score),length(Eppost$score)),ncol=1,byrow = FALSE)
rownames(scores)=c("pre","post","postpost")
colnames(scores)=c("E")
scores=as.table(scores)
chisq.test(scores,correct=TRUE)

#single category chi squared test 
scores=matrix(c(length(Spre$score),length(Spost$score),length(Sppost$score)),ncol=1,byrow = FALSE)
rownames(scores)=c("pre","post","postpost")
colnames(scores)=c("S")
scores=as.table(scores)
chisq.test(scores,correct=TRUE)

#single category chi squared test 
scores=matrix(c(length(Npre$score),length(Npost$score),length(Nppost$score)),ncol=1,byrow = FALSE)
rownames(scores)=c("pre","post","postpost")
colnames(scores)=c("N")
scores=as.table(scores)
chisq.test(scores,correct=TRUE)

######################################################################################################################
#only pre post data now - more datapoints
data=read.csv("df_PNES_melt_t.csv",header=TRUE)

datapre= subset(data,data$condition=="overall appearance of scientist")
datapost= subset(data,data$condition=="poverall appearance of scientist")

Ppre=subset(datapre,datapre$score == "P" | datapre$score == "p") 
Epre=subset(datapre,datapre$score == "E" | datapre$score == "e") 
Spre=subset(datapre,datapre$score == "S" | datapre$score == "s") 
Npre=subset(datapre,datapre$score == "N" | datapre$score == "n") 
Ppost=subset(datapost,datapost$score == "P" | datapost$score == "p") 
Epost=subset(datapost,datapost$score == "E" | datapost$score == "e") 
Spost=subset(datapost,datapost$score == "S" | datapost$score == "s") 
Npost=subset(datapost,datapost$score == "N" | datapost$score == "n") 

#matrix to test if theres any difference between pre/post/postpost scores 
scores=matrix(c(length(Ppre$score),length(Npre$score),length(Epre$score),length(Spre$score),
                length(Ppost$score),length(Npost$score),length(Epost$score),length(Spost$score)),ncol=4,byrow = TRUE)
rownames(scores)=c("Pre","Post")
colnames(scores)=c("Positive","Neutral","Eccentric","Sinister")
scores=as.table(scores)
mosaicplot(scores,col=c("red","blue","darkgreen","gold"),ylab="Scientist Depiction",xlab = "Timepoint",
           main="DAST Overall Scientist Depiction Ratios Pre/Post")      

chisq.test(scores,correct=TRUE)

mosaicplot(scores, col=c("red","blue"), ylab="Scientist Gender",xlab="Timepoint",
           main="DAST Gender Depiction Ratios Pre/Post")
legend("topright",legend=c("male","female"),fill=c("red","blue")) ### Remove legend box

#matrix just to get nice plotting grouped by condition, not for analysis 
scores=matrix(c(length(Ppre$score),length(Ppost$score),
                length(Epre$score),length(Epost$score),
                length(Spre$score),length(Spost$score),
                length(Npre$score),length(Npost$score)),ncol=2,byrow = TRUE)
colnames(scores)=c("Pre","Post")
rownames(scores)=c("Positive","Eccentric","Sinister","Neutral")
scores=as.table(scores)
mosaicplot(scores, beside=TRUE,col=c("red","blue"))      
### Remove legend box
