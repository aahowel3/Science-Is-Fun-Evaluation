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

#for pre/post/postpost analysis simple way to drop schools without a third entry 
#run this func then continue script as normal 
#drops observations from 490 to 335
###############################
completeFun <- function(data, desiredCols) {
  completeVec <- complete.cases(data[, desiredCols])
  return(data[completeVec, ])
}

data=completeFun(data, "AA19")
###############################

#create composite score columns 
#general science interest
data$presia = (data$B1 + data$B4 + data$B7 + data$B5 + data$B10 + data$B3)/6
data$postsia = (data$A1 + data$A4 + data$A7 + data$A5 + data$A10 + data$A3)/6
data$postpostsia = (data$AA1 + data$AA4 + data$AA7 + data$AA5 + data$AA10 + data$AA3)/6
#self-efficacy
data$preSE = (data$B13 + data$B15 + data$B14 + data$B9 + data$B16 + data$B12)/6
data$postSE = (data$A13 + data$A15 + data$A14 + data$A9 + data$A16 + data$A12)/6
data$postpostSE = (data$AA13 + data$AA15 + data$AA14 + data$AA9 + data$AA16 + data$AA12)/6
#energy science interest
data$preenergy = (data$B17 + data$B18 + data$B19)/3
data$postenergy = (data$A17 + data$A18 + data$A19)/3
data$postpostenergy = (data$AA17 + data$AA18 + data$AA19)/3

write.csv(data,"SIF_Likert_prepost_2020_revscore_catcolumns_factoranalysis.csv")


###^^^these categories, while supported by factor analysis, do not give us a strong effect size
#testing with groupings supported by cronbachs if not factor analysis 
data$presia = (data$B1 + data$B2 + data$B3 + data$B4 + data$B5 + data$B17 + data$B18 + data$B19)/8
data$postsia = (data$A1 + data$A2 + data$A3 + data$A4 + data$A5 + data$A17 + data$A18 + data$A19)/8
#self-efficacy
data$preSE = (data$B13 + data$B14 + data$B15 + data$B16 + data$B9 + data$B11 + data$B12)/7
data$postSE = (data$A13 + data$A14 + data$A15 + data$A16 + data$A9 + data$A11 + data$A12 )/7
#additudes and values
data$preAV = (data$B6 + data$B7 + data$B10)/3
data$postAV = (data$A6 + data$A7 + data$A10)/3

write.csv(data,"SIF_Likert_prepost_2020_revscore_catcolumns_theorybased.csv")




