library("ez")
library("nlme") 
library("rmarkdown")
library("PMCMR")
require("multcomp")
library("gplots")
library("pwr")
library("vcd")
library("rcompanion")
library("fifer")
library("lsr")
#dev.off() 
#run to clear plot environment 
#link to pdftex installation for knitting document, install in terminal not in Rstudio
#https://tex.stackexchange.com/questions/112734/is-it-possible-to-install-only-the-required-latex-tool-pdflatex-in-ubuntu
#use Sys.which("package") to make sure its there 
#using pre/post/postpost data
setwd("/home/aahowel3/Documents/scienceisfun/analysis/SIF_finalanalysis_July2018/SIF_analysis_postpst_December_2018/January_2019/")
#####DID NOT USE THESE TEST, NOT REAPEATED MEASURES, NOT TEASED OUT BY 
data=read.csv("df_PC_melt_f.csv",header=TRUE)
data1=read.csv("df_SK_melt_f.csv",header=TRUE)
data2=read.csv("df_SR_melt_f.csv",header=TRUE)
data3=read.csv("df_ST_melt_f.csv",header=TRUE)

datapre= subset(data,data$condition=="Pre PC")
datapost= subset(data,data$condition=="Post PC")
datapostpost= subset(data,data$condition=="PostPost PC")
datapre1= subset(data1,data1$condition=="Pre SK")
datapost1= subset(data1,data1$condition=="Post SK")
datapostpost1= subset(data1,data1$condition=="PostPost SK")
datapre2= subset(data2,data2$condition=="Pre SR")
datapost2= subset(data2,data2$condition=="Post SR")
datapostpost2= subset(data2,data2$condition=="PostPost SR")
datapre3= subset(data3,data3$condition=="Pre ST")
datapost3= subset(data3,data3$condition=="Post ST")
datapostpost3= subset(data3,data3$condition=="PostPost ST")

scores=matrix(c(sum(datapre$score),sum(datapost$score),sum(datapostpost$score),
                sum(datapre1$score),sum(datapost1$score),sum(datapostpost1$score),
                sum(datapre2$score),sum(datapost2$score),sum(datapostpost2$score),
                sum(datapre3$score),sum(datapost3$score),sum(datapostpost3$score)),ncol=4,byrow = FALSE)
rownames(scores)=c("pre","post","postpost")
colnames(scores)=c("PC","SK","SR","ST")
scores=as.table(scores)
#is there a difference between pre/post/postpost across all 4 categories?
chisq.test(scores,correct=TRUE)
chisq.post.hoc(scores,test="fisher.test", popsInRows=TRUE, control="bonferroni")
pairwiseNominalIndependence(scores, chisq = TRUE, method="fdr")
Es=cramersV(scores)
Es
n=sum(scores)
pwr.chisq.test(w=Es,N=n, df=6,sig.level = 0.05)

#is there a difference between pre/post/postpost in PC scores?
#chisq then post hoc each combo 
#example if you want to make no 0-2 or 0-1, etc
#norespre=subset(datapre,datapre$score == 0 | datapre$score == 1) 
#####DID NOT USE THIS TEST - NOT REAPTED MEASURES
norespre=subset(datapre,datapre$score == 0)
norespost=subset(datapost,datapost$score == 0) 
norespostpost=subset(datapostpost,datapostpost$score == 0) 

scores=matrix(c(length(datapre$score)-length(norespre$score),length(norespre$score),
                length(datapost$score)-length(norespost$score),length(norespost$score),
                length(datapostpost$score)-length(norespostpost$score),length(norespostpost$score)),ncol=2,byrow = TRUE)

rownames(scores)=c("pre","post","postpost")
colnames(scores)=c("PC_yes","PC_no")
scores=as.table(scores)
chisq.test(scores,correct=TRUE)
chisq.post.hoc(scores,test="fisher.test", popsInRows=TRUE, control="bonferroni")


#####THIS IS THE TEST YOU USED, MOST APPROPRIATE FOR REAPEATED TESTS 
#################################################################PC DAST CATEGORY
Data=read.csv("df_PC_melt_f.csv",header=TRUE)
Data$presencePC= ifelse(Data$score == 0, "No", "Yes")

Data$Practice = factor(Data$condition,
                       levels=unique(Data$condition))
Data$Response = factor(Data$presencePC,
                       levels=c("No","Yes"))

Data$Response.n = as.numeric(Data$Response) - 1   ### Creates a new numeric variable
###  that is Response as a 0 or 1

Table = xtabs(Response.n ~ Subjects + Practice,
              data=Data)

xtabs( ~ Practice + Response,
       data=Data)

Table = xtabs( ~ Response + Practice,
               data=Data)
barplot(Table, beside=TRUE,legend=TRUE,args.legend = list(x   = "topright",   ### Legend location
                                                          cex = 0.8,          ### Legend text size
                                                          bty = "n"))         ### Remove legend box

library("coin")
symmetry_test(Response ~ Practice | Subjects,
              data = Data,
              teststat = "quad")

### Order groups

Data$Practice = factor(Data$Practice,
                       levels = c("Pre PC", "Post PC",
                                  "PostPost PC"))

### Pairwise McNemar tests
library(rcompanion)

PT = pairwiseMcnemar(Response ~ Practice | Subjects,
                     data   = Data,
                     test   = "permutation",
                     method = "fdr",
                     digits = 3)
PT = PT$Pairwise
cldList(p.adjust ~ Comparison,
        data       = PT,
        threshold  = 0.05)


Es=cramersV(Table)
Es
n=sum(Table)
pwr.chisq.test(w=Es,N=n, df=2,sig.level = 0.05)

#################################################################SK DAST CATEGORY
Data=read.csv("df_SK_melt_f.csv",header=TRUE)
Data$presencePC= ifelse(Data$score == 0, "No", "Yes")

Data$Practice = factor(Data$condition,
                       levels=unique(Data$condition))
Data$Response = factor(Data$presencePC,
                       levels=c("No","Yes"))

Data$Response.n = as.numeric(Data$Response) - 1   ### Creates a new numeric variable
###  that is Response as a 0 or 1

Table = xtabs(Response.n ~ Subjects + Practice,
              data=Data)

xtabs( ~ Practice + Response,
       data=Data)

Table = xtabs( ~ Response + Practice,
               data=Data)
barplot(Table, beside=TRUE,legend=TRUE,args.legend = list(x   = "topright",   ### Legend location
                                                          cex = 0.8,          ### Legend text size
                                                          bty = "n"))         ### Remove legend box

library("coin")
symmetry_test(Response ~ Practice | Subjects,
              data = Data,
              teststat = "quad")

### Order groups

Data$Practice = factor(Data$Practice,
                       levels = c("Pre SK", "Post SK",
                                  "PostPost SK"))

### Pairwise McNemar tests
library(rcompanion)

PT = pairwiseMcnemar(Response ~ Practice | Subjects,
                     data   = Data,
                     test   = "permutation",
                     method = "fdr",
                     digits = 3)
PT = PT$Pairwise
#cldList(p.adjust ~ Comparison,
#        data       = PT,
#        threshold  = 0.05)


Es=cramersV(Table)
Es
n=sum(Table)
pwr.chisq.test(w=Es,N=n, df=2,sig.level = 0.05)

#################################################################ST DAST CATEGORY
Data=read.csv("df_ST_melt_f.csv",header=TRUE)
Data$presencePC= ifelse(Data$score == 0, "No", "Yes")

Data$Practice = factor(Data$condition,
                       levels=unique(Data$condition))
Data$Response = factor(Data$presencePC,
                       levels=c("No","Yes"))

Data$Response.n = as.numeric(Data$Response) - 1   ### Creates a new numeric variable
###  that is Response as a 0 or 1

Table = xtabs(Response.n ~ Subjects + Practice,
              data=Data)

xtabs( ~ Practice + Response,
       data=Data)

Table = xtabs( ~ Response + Practice,
               data=Data)
barplot(Table, beside=TRUE,legend=TRUE,args.legend = list(x   = "topright",   ### Legend location
                                                          cex = 0.8,          ### Legend text size
                                                          bty = "n"))         ### Remove legend box

library("coin")
symmetry_test(Response ~ Practice | Subjects,
              data = Data,
              teststat = "quad")

### Order groups

Data$Practice = factor(Data$Practice,
                       levels = c("Pre ST", "Post ST",
                                  "PostPost ST"))

### Pairwise McNemar tests
library(rcompanion)

PT = pairwiseMcnemar(Response ~ Practice | Subjects,
                     data   = Data,
                     test   = "permutation",
                     method = "fdr",
                     digits = 3)
PT = PT$Pairwise
#cldList(p.adjust ~ Comparison,
#        data       = PT,
#        threshold  = 0.05)


Es=cramersV(Table)
Es
n=sum(Table)
pwr.chisq.test(w=Es,N=n, df=2,sig.level = 0.05)


#################################################################Sr DAST CATEGORY
Data=read.csv("df_SR_melt_f.csv",header=TRUE)
Data$presencePC= ifelse(Data$score == 0, "No", "Yes")

Data$Practice = factor(Data$condition,
                       levels=unique(Data$condition))
Data$Response = factor(Data$presencePC,
                       levels=c("No","Yes"))

Data$Response.n = as.numeric(Data$Response) - 1   ### Creates a new numeric variable
###  that is Response as a 0 or 1

Table = xtabs(Response.n ~ Subjects + Practice,
              data=Data)

xtabs( ~ Practice + Response,
       data=Data)

Table = xtabs( ~ Response + Practice,
               data=Data)
barplot(Table, beside=TRUE,legend=TRUE,args.legend = list(x   = "topright",   ### Legend location
                                                          cex = 0.8,          ### Legend text size
                                                          bty = "n"))         ### Remove legend box

library("coin")
symmetry_test(Response ~ Practice | Subjects,
              data = Data,
              teststat = "quad")

### Order groups

Data$Practice = factor(Data$Practice,
                       levels = c("Pre SR", "Post SR",
                                  "PostPost SR"))

### Pairwise McNemar tests
library(rcompanion)

PT = pairwiseMcnemar(Response ~ Practice | Subjects,
                     data   = Data,
                     test   = "permutation",
                     method = "fdr",
                     digits = 3)
PT = PT$Pairwise
cldList(p.adjust ~ Comparison,
        data       = PT,
        threshold  = 0.05)


Es=cramersV(Table)
Es
n=sum(Table)
pwr.chisq.test(w=Es,N=n, df=2,sig.level = 0.05)

#####################################################################################################
#pre/post ONLY - single McNamer test
setwd("/home/aahowel3/Documents/scienceisfun/analysis/SIF_finalanalysis_July2018/SIF_analysis_postpst_December_2018")
Data=read.csv("df_PC_melt_t (copy).csv",header=TRUE)
Data$presencePC= ifelse(Data$score == 0, "No", "Yes")

Data$Practice = factor(Data$condition,
                       levels=unique(Data$condition))

Data$Response = factor(Data$presencePC,
                       levels=c("No", "Yes"))

Data$Response.n = as.numeric(Data$Response) - 1   ### Creates a new numeric variable
###  that is Response as a 0 or 1

Table = xtabs(Response.n ~ Subjects + Practice,
              data=Data)

xtabs( ~ Practice + Response,
       data=Data)

Table = xtabs( ~ Response + Practice,
               data=Data)
barplot(Table, beside=TRUE,legend=TRUE,args.legend = list(x   = "topright",   ### Legend location
                                                          cex = 0.8,          ### Legend text size
                                                          bty = "n"))         ### Remove legend box


### Pairwise McNemar tests
library(rcompanion)

PT = pairwiseMcnemar(Response ~ Practice | Subjects,
                     data   = Data,
                     test   = "permutation",
                     method = "fdr",
                     digits = 3)
PT = PT$Pairwise
#cldList(p.adjust ~ Comparison,
#        data       = PT,
#        threshold  = 0.05)

Es=cramersV(Table)
Es
n=sum(Table)
pwr.chisq.test(w=Es,N=n, df=2,sig.level = 0.05)

#####################################################################################################
#pre/post ONLY - single McNamer test
setwd("/home/aahowel3/Documents/scienceisfun/analysis/SIF_finalanalysis_July2018/SIF_analysis_postpst_December_2018")
Data=read.csv("df_SK_melt_t (copy).csv",header=TRUE)
Data$presencePC= ifelse(Data$score == 0, "No", "Yes")

Data$Practice = factor(Data$condition,
                       levels=unique(Data$condition))

Data$Response = factor(Data$presencePC,
                       levels=c("No", "Yes"))

Data$Response.n = as.numeric(Data$Response) - 1   ### Creates a new numeric variable
###  that is Response as a 0 or 1

Table = xtabs(Response.n ~ Subjects + Practice,
              data=Data)

xtabs( ~ Practice + Response,
       data=Data)

Table = xtabs( ~ Response + Practice,
               data=Data)
barplot(Table, beside=TRUE,legend=TRUE,args.legend = list(x   = "topright",   ### Legend location
                                                          cex = 0.8,          ### Legend text size
                                                          bty = "n"))         ### Remove legend box


### Pairwise McNemar tests
library(rcompanion)

PT = pairwiseMcnemar(Response ~ Practice | Subjects,
                     data   = Data,
                     test   = "permutation",
                     method = "fdr",
                     digits = 3)
PT = PT$Pairwise
#cldList(p.adjust ~ Comparison,
#        data       = PT,
#        threshold  = 0.05)

Es=cramersV(Table)
Es
n=sum(Table)
pwr.chisq.test(w=Es,N=n, df=2,sig.level = 0.05)

#####################################################################################################
#pre/post ONLY - single McNamer test
setwd("/home/aahowel3/Documents/scienceisfun/analysis/SIF_finalanalysis_July2018/SIF_analysis_postpst_December_2018")
Data=read.csv("df_ST_melt_t (copy).csv",header=TRUE)
Data$presencePC= ifelse(Data$score == 0, "No", "Yes")

Data$Practice = factor(Data$condition,
                       levels=unique(Data$condition))

Data$Response = factor(Data$presencePC,
                       levels=c("No", "Yes"))

Data$Response.n = as.numeric(Data$Response) - 1   ### Creates a new numeric variable
###  that is Response as a 0 or 1

Table = xtabs(Response.n ~ Subjects + Practice,
              data=Data)

xtabs( ~ Practice + Response,
       data=Data)

Table = xtabs( ~ Response + Practice,
               data=Data)
barplot(Table, beside=TRUE,legend=TRUE,args.legend = list(x   = "topright",   ### Legend location
                                                          cex = 0.8,          ### Legend text size
                                                          bty = "n"))         ### Remove legend box


### Pairwise McNemar tests
library(rcompanion)

PT = pairwiseMcnemar(Response ~ Practice | Subjects,
                     data   = Data,
                     test   = "permutation",
                     method = "fdr",
                     digits = 3)
PT = PT$Pairwise
#cldList(p.adjust ~ Comparison,
#        data       = PT,
#        threshold  = 0.05)

Es=cramersV(Table)
Es
n=sum(Table)
pwr.chisq.test(w=Es,N=n, df=2,sig.level = 0.05)

#####################################################################################################
#pre/post ONLY - single McNamer test
setwd("/home/aahowel3/Documents/scienceisfun/analysis/SIF_finalanalysis_July2018/SIF_analysis_postpst_December_2018")
Data=read.csv("df_SR_melt_t (copy).csv",header=TRUE)
Data$presencePC= ifelse(Data$score == 0, "No", "Yes")

Data$Practice = factor(Data$condition,
                       levels=unique(Data$condition))

Data$Response = factor(Data$presencePC,
                       levels=c("No", "Yes"))

Data$Response.n = as.numeric(Data$Response) - 1   ### Creates a new numeric variable
###  that is Response as a 0 or 1

Table = xtabs(Response.n ~ Subjects + Practice,
              data=Data)

xtabs( ~ Practice + Response,
       data=Data)

Table = xtabs( ~ Response + Practice,
               data=Data)
barplot(Table, beside=TRUE,legend=TRUE,args.legend = list(x   = "topright",   ### Legend location
                                                          cex = 0.8,          ### Legend text size
                                                          bty = "n"))         ### Remove legend box


### Pairwise McNemar tests
library(rcompanion)

PT = pairwiseMcnemar(Response ~ Practice | Subjects,
                     data   = Data,
                     test   = "permutation",
                     method = "fdr",
                     digits = 3)
PT = PT$Pairwise
cldList(p.adjust ~ Comparison,
        data       = PT,
        threshold  = 0.05)

Es=cramersV(Table)
Es
n=sum(Table)
pwr.chisq.test(w=Es,N=n, df=2,sig.level = 0.05)