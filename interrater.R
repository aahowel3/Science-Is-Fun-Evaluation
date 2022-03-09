library(stringr)
#normal likert dataset format just subset for 35 examples 
#this data informs tables 1 and 2 in the manuscript under "Analysis - DAST"
setwd("~/Documents/scienceisfun_2020/inter_rater")
mydata=read.csv("interraterreliability_AbigailHowell.csv")
theirdata=read.csv("interraterreliability_ws.csv")

compare=as.matrix(mydata)==as.matrix(theirdata)
length(which(compare==TRUE))
length(which(compare==FALSE))
#minus 631 - 35 because of subject column 
#596/700 (35rowx20col - 21 with subject col)

#Percent agreement - Table 1
#by category 
#looked at every y/n box in each PC column and compared if they matched or didn't match = % agreement per category 
PC= c('lab.coat','eyeglasses','facial.hair','pencil.pen.in.pocket','unkempt.appearance') 
mydataPC=mydata[PC]
theirdataPC=theirdata[PC]
compare=as.matrix(mydataPC)==as.matrix(theirdataPC)
#numerator
length(which(compare==TRUE))
#denominator
length(compare)

ST= c('solutions.in.glassware','machines','other..signs.of.technology.')
mydataST=mydata[ST]
theirdataST=theirdata[ST]
compare=as.matrix(mydataST)==as.matrix(theirdataST)
#numerator
length(which(compare==TRUE))
#denominator
length(compare)

SK= c('books','filing.cabinets','other..symbols.of.knowledge.')
mydataSK=mydata[SK]
theirdataSK=theirdata[SK]
compare=as.matrix(mydataSK)==as.matrix(theirdataSK)
#numerator
length(which(compare==TRUE))
#denominator
length(compare)

SR= c('test.tubes','flasks','microscope','bunsen.burner','experimental.animals','other..symbols.of.research.') 
mydataSR=mydata[SR]
theirdataSR=theirdata[SR]
compare=as.matrix(mydataSR)==as.matrix(theirdataSR)
#numerator
length(which(compare==TRUE))
#denominator
length(compare)

#by gender 
gender= c('scientist.gender') 
mydata=mydata[gender]
theirdata=theirdata[gender]
compare=as.matrix(mydata)==as.matrix(theirdata)
#numerator
length(which(compare==TRUE))
#denominator
length(compare)

#by race
race= c('scientist.race') 
mydata=mydata[race]
theirdata=theirdata[race]
compare=as.matrix(mydata)==as.matrix(theirdata)
#numerator
length(which(compare==TRUE))
#denominator
length(compare)

#by PNES
app= c('overall.appearance.of.scientist') 
mydata=mydata[app]
theirdata=theirdata[app]
compare=as.matrix(mydata)==as.matrix(theirdata)
#numerator
length(which(compare==TRUE))
#denominator
length(compare)

#Pearson's product correlation - for scores that are cont. variables (PC, ST, SK, SR) - Table 2 
#correlation for score of student 1A PC score AH vs. PC score WS
#then t test for in text t value and p values 
mydata=read.csv("interraterreliability_AbigailHowell.csv")
theirdata=read.csv("interraterreliability_ws.csv")
#okay this turns EVERY column into 0 or 1, can just use subject lines from data, use binary values from data2
mydata2 <- ifelse(mydata == "y", 1, 0)
mydata2=as.data.frame(mydata2)

theirdata2 <- ifelse(theirdata == "y", 1, 0)
theirdata2=as.data.frame(theirdata2)

#Create PC quantitative column for each dataset then plot them against each other
mydata$AHPC = (mydata2$lab.coat + mydata2$eyeglasses + mydata2$facial.hair + 
  mydata2$pencil.pen.in.pocket + mydata2$unkempt.appearance)/5 
theirdata$HSPC = (theirdata2$lab.coat + theirdata2$eyeglasses + theirdata2$facial.hair + 
                    theirdata2$pencil.pen.in.pocket + theirdata2$unkempt.appearance)/5 
cor.test(mydata$AHPC,theirdata$HSPC, method="pearson")
t.test(mydata$AHPC,theirdata$HSPC,paired=TRUE)

#Create ST quantitative column for each dataset then plot them against each other
mydata$AHST = (mydata2$solutions.in.glassware + mydata2$machines + mydata2$other..signs.of.technology.)/ 3
theirdata$HSST = (theirdata2$solutions.in.glassware + theirdata2$machines + theirdata2$other..signs.of.technology.)/3
cor.test(mydata$AHST,theirdata$HSST, method="pearson")
t.test(mydata$AHST,theirdata$HSST,paired=TRUE)

#Create SK quantitative column for each dataset then plot them against each other
mydata$AHSK = (mydata2$books + mydata2$filing.cabinets + mydata2$other..symbols.of.knowledge.)/ 3
theirdata$HSSK = (theirdata2$books + theirdata2$filing.cabinets + theirdata2$other..symbols.of.knowledge.)/3
cor.test(mydata$AHSK,theirdata$HSSK, method="pearson")
t.test(mydata$AHSK,theirdata$HSSK,paired=TRUE)

#Create SR quantitative column for each dataset then plot them against each other
mydata$AHSR = (mydata2$test.tubes + mydata2$flasks + mydata2$microscope + 
               mydata2$bunsen.burner + mydata2$experimental.animals + mydata2$other..symbols.of.research.)/ 6

theirdata$HSSR = (theirdata2$test.tubes + theirdata2$flasks + theirdata2$microscope + 
                    theirdata2$bunsen.burner + theirdata2$experimental.animals + theirdata2$other..symbols.of.research.)/ 6
cor.test(mydata$AHSR,theirdata$HSSR, method="pearson")
t.test(mydata$AHSR,theirdata$HSSR,paired=TRUE)


#chi2 signifgance testing for gender 
x=toString(mydata$scientist.gender)
M_AH=str_count(x, "m")
F_AH=str_count(x, "f")
idk_AH=str_count(x, "don't know")

x=toString(theirdata$scientist.gender)
M_HS=str_count(x, "m")
F_HS=str_count(x, "f")
idk_HS=str_count(x, "don't know")

#matrix to test if theres any difference between pre/post/postpost scores 
scores=matrix(c(M_AH,F_AH,idk_AH,
                M_HS,F_HS,idk_HS),ncol=3,byrow = TRUE)
rownames(scores)=c("AH","HS")
colnames(scores)=c("male","female","unknown")
scores=as.table(scores)
chisq.test(scores,correct=TRUE)

#new stat requested IJSE
#kappa with only make and female no idk
#matrix to test if theres any difference between pre/post/postpost scores 
library("vcd")
#JESUSS have to just manually calculate males agreed 18 times so disagrreed 3 etc 
scores=matrix(c(18,1,
                3,10),ncol=2,byrow = TRUE)
scores=as.table(scores)
categories <- c("male", "female")
dimnames(scores) <- list(AH = categories, HS = categories)
scores
Kappa(scores)

#chi2 test for PNES signifigance testing
#can't just subset them and count lengths of the column with multi-tier responses (i.e P/S or N/E)
#have to use a count function 
#compare 
x=toString(mydata$overall.appearance.of.scientist)
N_AH=str_count(x, "N")
P_AH=str_count(x, "P")
E_AH=str_count(x, "E")
S_AH=str_count(x, "S")

x=toString(theirdata$overall.appearance.of.scientist)
N_HS=str_count(x, "N")
P_HS=str_count(x, "P")
E_HS=str_count(x, "E")
S_HS=str_count(x, "S")
#matrix to test if theres any difference between pre/post/postpost scores 
scores=matrix(c(N_AH,P_AH,E_AH,S_AH,
                N_HS,P_HS,E_HS,S_HS),ncol=4,byrow = TRUE)
rownames(scores)=c("AH","HS")
colnames(scores)=c("Neutral","Positive","Eccentric","Sinister")
scores=as.table(scores)
mosaicplot(scores,col=c("red","blue","darkgreen","gold"),ylab="Scientist Depiction",xlab = "Scorer",
           main="DAST Overall Scientist Depiction Ratios by Scorer")      

chisq.test(scores,correct=TRUE)




####Kappa test for PNES
#matrix to test if theres any difference between pre/post/postpost scores 
scores=matrix(c(10,2,1,0,
                2,16,1,0,
                2,0,4,0,
                0,0,0,4),ncol=4,byrow = TRUE)
rownames(scores)=c("AH","HS")
colnames(scores)=c("Neutral","Positive","Eccentric","Sinister")
scores=as.table(scores)

Kappa(scores)
