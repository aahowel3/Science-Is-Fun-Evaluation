setwd("/home/aahowel3/Documents/scienceisfun_2020/dast")
data=read.csv("SIF_DAST_prepost_2020.csv",header=TRUE)

data2 <- ifelse(data == "y", 1, 0)
#okay this turns EVERY column into 0 or 1, can just use subject lines from data, use binary values from data2
data2=as.data.frame(data2)

#Create 4 category columns 
data$prePC = (data2$PC1 + data2$PC2 + data2$PC3 + data2$PC4 + data2$PC5)/5
data$postPC = (data2$postPC1 + data2$postPC2 + data2$postPC3 + data2$postPC4 + data2$postPC5)/5

data$preSR = (data2$SR1 + data2$SR2 + data2$SR3 + data2$SR4 + data2$SR5+data2$SR6)/6
data$postSR = (data2$postSR1 + data2$postSR2 + data2$postSR3 + data2$postSR4 + data2$postSR5 + data2$postSR6)/6

data$preSK = (data2$SK1 + data2$SK2 + data2$SK3)/3
data$postSK = (data2$postSK1 + data2$postSK2 + data2$postSK3)/3 

data$preST = (data2$ST1 + data2$ST2 + data2$ST3)/3
data$postST = (data2$postST1 + data2$postST2 + data2$postST3)/3 

finaldata=data[,c("Subjects","prePC","postPC","preSR","postSR","preSK","postSK","preST","postST")]

finaldata <- finaldata[order(finaldata$Subjects),]
#organize columns alphabetically to just cp/paste new racial designations

#add gender and race columns from Likert to DAST dataset
#have to delete select rows, n likert = 490 while n DAST = 418 
#then go in and delete the NA gender entries 
setwd("/home/aahowel3/Documents/scienceisfun_2020/likert/Spring2020")
datalik=read.csv("SIF_Likert_prepost_2020_revscore.csv",header=TRUE)
datalik <- datalik[order(datalik$Subjects),]

#cut down likert rows 
#if Subject id is not present in dast dataset (data$subjects) remove it from datalikert
datalik=datalik[datalik$Subjects %in% finaldata$Subjects,]
#now that its trimmed we can append THIS dataframes race and gender data onto this frame

finaldata2=data.frame(finaldata$Subjects, datalik$D1pre, datalik$Race, 
                      finaldata$prePC, finaldata$postPC, finaldata$preSR, finaldata$postSR,
                      finaldata$preSK,finaldata$postSK,finaldata$preST,finaldata$postST) 
colnames(finaldata2)=c("Subjects", "gender", "race","prePC",
                       "postPC","preSR","postSR","preSK","postSK","preST","postST")


setwd("/home/aahowel3/Documents/scienceisfun_2020/dast")
write.csv(finaldata2,"DAST_catcolumns.csv")
