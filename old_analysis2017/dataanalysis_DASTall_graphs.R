setwd("/home/aahowel3/Documents/scienceisfun/analysis/SIF_finalanalysis_July2018/SIF_analysis_postpst_December_2018")


data1=read.csv("df_allDAST_melt.csv",header=TRUE)
data1$factor=factor(data1$condition,levels=c("Pre PC","Post PC","Pre SR","Post SR","Pre ST","Post ST","Pre SK","Post SK"))
boxplot(score ~ factor, data=data1, 
        col=c("darkgreen","gold","darkgreen","gold","darkgreen","gold","darkgreen","gold"),
        main="DAST Categorical Scores Per Assessment Period",
        xlab="",ylab="",ylim=c(0.0,0.45),outline=FALSE,whisklty=0,staplelty=0)
        
legend("topright",legend=c("Pre","Post"),fill=c("darkgreen","gold")) ### Remove legend box
