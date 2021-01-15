library("psych")
setwd("/home/aahowel3/Documents/scienceisfun_2020/likert")
data=read.csv("SIF_Likert_prepost_2020.csv",header=TRUE)
#reverse scoring formula is max(x) + 1 - x 
func = function(x) 5 + 1 - x
#scoring is converted high to low to make interperations easier for readers
#convert everything BUT the reverse scored items (items 7/11)
names=c("B1","B2","B3","B4","B5","B6","B8","B9","B10","B12","B13","B14","B15","B16","B17","B18","B19",
        "A1","A2","A3","A4","A5","A6","A8","A9","A10","A12","A13","A14","A15","A16","A17","A18","A19",
        "AA1","AA2","AA3","AA4","AA5","AA6","AA8","AA9","AA10","AA12","AA13","AA14","AA15","AA16","AA17","AA18","AA19")

data[names]=sapply(data[names],func)

#write.csv(data,"SIF_Likert_prepost_2020_revscore.csv")

#for pre/post/postpost analysis simple way to drop schools without a third entry 
#run this func then continue script as normal 
#drops observations from 490 to 335
###############################
completeFun <- function(data, desiredCols) {
  completeVec <- complete.cases(data[, desiredCols])
  return(data[completeVec, ])
}

data=completeFun(data, "AA19")

#write.csv(data,"SIF_Likert_prepost_2020_revscore_postpost.csv")

###############################

#original setup pre and post
#run this after EACH items
alpha(data[,items])
#some studies want a Cronbachs after pre and post
#and if we did decide to bring back post post thats outlined here too 
#sia
items = c("B1","B2","B3","B4","B5","B17","B18","B19")
items = c("A1","A2","A3","A4","A5","A17","A18","A19")
items = c("AA1","AA2","AA3","AA4","AA5","AA17","AA18","AA19")
#self efficacy 
items = c("B12","B13","B14","B15","B16")
items = c("A12","A13","A14","A15","A16")
items = c("AA12","AA13","AA14","AA15","AA16")
#additudes and values
items = c("B6","B7")
items = c("A6","A7")
items = c("AA6","AA7")
#expectancy
items = c("B8","B9","B10","B11")
items = c("A8","A9","A10","A11")
items = c("AA8","AA9","AA10","AA11")

#option 2 setup prepost
#sia=same
#no expectancy cat 
#self efficacy now including 8,11,9
items = c("B12","B13","B14","B15","B16","B8","B11","B9")
items = c("A12","A13","A14","A15","A16","A8","A11","A9")
items = c("AA12","AA13","AA14","AA15","AA16","AA8","AA11","AA9")
#additudes and values now including 10
items = c("B6","B7", "B10")
items = c("A6","A7","A10")
items = c("AA6","AA7","AA10")

#After michelle revisions playing around with self-efficacy combos
#sia and av finalized, expectancy scraped 
#self efficacy option 1 add 9 and 11 drop 12
items = c("B13","B14","B15","B16","B11","B9")
items = c("A13","A14","A15","A16","A11","A9")
items = c("AA13","AA14","AA15","AA16","AA11","AA9")

#self efficacy option 2 add 9 drop 12
items = c("B13","B14","B15","B16","B9")
items = c("A13","A14","A15","A16","A9")
items = c("AA13","AA14","AA15","AA16","AA9")

#self efficacy option 3 add 9 and 11 keep 12
items = c("B13","B14","B15","B16","B11","B9","B12")
items = c("A13","A14","A15","A16","A11","A9","A12")
items = c("AA13","AA14","AA15","AA16","AA11","AA9","AA12")

#self efficacy option 4 add 9 keep 12
items = c("B13","B14","B15","B16","B12","B9")
items = c("A13","A14","A15","A16","A12","A9")
items = c("AA13","AA14","AA15","AA16","AA12","AA9")

psych::alpha(data[,items])
#post meeting 1/6/20
#general science interest
items = c("B1","B4","B7","B5","B10","B3")
items = c("A1","A4","A7","A5","A10","A3")
pre_a=0.82
post_a=0.81
#beyond school science interest/value
items=c("B5","B3","B10")
items=c("A5","A3","A10")
pre_a=0.75
post_a=0.73
items=c("B10","B5","B3","B6") 
items=c("A10","A5","A3","A6") 
pre_a=0.73
post_a=0.71
#self-efficacy 
items = c("B13","B15","B14","B9","B16","B12")
items = c("A13","A15","A14","A9","A16","A12")
pre_a=0.72
post_a=0.78
items = c("B13","B15","B14","B9","B16")
items = c("A13","A15","A14","A9","A16")
pre_a=0.71
post_a=0.78
#energy science interest 
items = c("B17","B18","B19")
items = c("A17","A18","A19")
pre_a=0.79
post_a=0.81

#Factor Analysis supported categories
psych::alpha(data[,items])
#post meeting 1/6/20
#general science interest
items = c("B1","B4","B7","B5","B10","B3","B6","B11")

#self-efficacy 
items = c("B13","B15","B14","B9","B16","B12")

#energy science interest 
items = c("B17","B18","B19")


