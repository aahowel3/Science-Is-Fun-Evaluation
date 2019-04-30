library("ez")
library("nlme") 
library("rmarkdown")
library("PMCMR")
require("multcomp")
library("gplots")
library("coin")
library("psych")
library("pwr")
#dev.off() 
#run to clear plot environment 
#link to pdftex installation for knitting document, install in terminal not in Rstudio
#https://tex.stackexchange.com/questions/112734/is-it-possible-to-install-only-the-required-latex-tool-pdflatex-in-ubuntu
#use Sys.which("package") to make sure its there 
#using pre/post/postpost data
setwd("/home/aahowel3/Documents/scienceisfun/analysis/SIF_finalanalysis_July2018/SIF_analysis_postpst_December_2018/January_2019")
data=read.csv("df_sia_melt_f.csv",header=TRUE)

#checking Chronbach's alpha reliability 
data_a=read.csv("sia.csv",header=TRUE)
r=alpha(data_a)
r
#only use complete entries for 3 timepoint testing 
data=data[complete.cases(data), ]
#get residuals to test for normality
m = aov(score ~ condition + (Error(Subjects/condition)), 
        data=data) 
res=proj(m)
data$res=res[[3]][,"Residuals"]
#normality testing 
qqnorm(data$res)
qqline(data$res)
shapiro.test(data$res)
summary(m)

#try transformation 
data$score_trans=log(data$score)
#get residuals from transformed data
#http://coltekin.net/cagri/R/r-exercisesse5.html
m2 = aov(score_trans ~ condition + Error(Subjects/condition), 
         data=data) 
summary(m2)
res2=proj(m2)
data$res2=res2[[3]][,"Residuals"]
#normality testing 
qqnorm(data$res2)
qqline(data$res2)
shapiro.test(data$res2)

#general statistics: mean, standard deviation, standard error
datapre= subset(data,data$condition=="Pre SI-a")
datapost= subset(data,data$condition=="Post SI-a")
datapostpost= subset(data,data$condition=="PostPost SI-a")
mean_pre=mean(datapre$score)
print(mean_pre)
mean_post=mean(datapost$score)
print(mean_post)
mean_postpost=mean(datapostpost$score)
print(mean_postpost)
std_dev_pre=sd(datapre$score)
std_dev_post=sd(datapost$score)
std_dev_postpost=sd(datapostpost$score)
sem_pre=std_dev_pre/sqrt(length(datapre$score))
sem_post=std_dev_post/sqrt(length(datapost$score))
sem_postpost=std_dev_postpost/sqrt(length(datapostpost$score))


#non-parametric test 
friedman.test(score ~ condition|Subjects,data=data)
#posthoc friedman
posthoc.friedman.nemenyi.test(score ~ condition|Subjects,data=data)
#additional posthoc with pairwise wilcoxon with corrections
pairwise.wilcox.test(data$score, data$condition, p.adj="bonferroni",exact=F,paired=T)

#boxplot no CIs
#plot nonparametric data with boxplot not CI 
data$factor=factor(data$condition,levels=c("Pre SI-a","Post SI-a","PostPost SI-a"))
boxplot(score ~ factor, data=data, main="SI-a Scores Per Assessment Period",xlab="",ylab="",ylim=c(1,5),outline=FALSE)
#text(1:3, labels=c("a","b","c"),pos=3)
text(tapply(data$score,data$condition) - 1.95, labels=c("a","a","b"),pos=3)

#mean difference between groups (wilcoxon signed rank) with true CIs
#wilcoxon CIs
medianpre_post=wilcox.test(datapre$score, datapost$score,paired=TRUE, p.adj="bonferroni", conf.int = TRUE)
CIpre_post=(wilcox.test(datapre$score, datapost$score,paired=TRUE, p.adj="bonferroni", conf.int = TRUE)$conf.int)[2] -
  medianpre_post[[9]]
medianpost_postpost=wilcox.test(datapost$score, datapostpost$score,paired=TRUE, p.adj="bonferroni", conf.int = TRUE)
CIpost_postpost=(wilcox.test(datapost$score, datapostpost$score,paired=TRUE, p.adj="bonferroni", conf.int = TRUE)$conf.int)[2] -
  medianpost_postpost[[9]]
medianpre_postpost=wilcox.test(datapre$score, datapostpost$score,paired=TRUE, p.adj="bonferroni", conf.int = TRUE)
CIpre_postpost=(wilcox.test(datapre$score, datapostpost$score,paired=TRUE, p.adj="bonferroni", conf.int = TRUE)$conf.int)[2] -
  medianpre_postpost[[9]]

library("gplots")
plotCI(1:3, c(medianpre_post[[9]],medianpost_postpost[[9]],medianpre_postpost[[9]]), 
       uiw = c(CIpre_post,CIpost_postpost,CIpre_postpost), lty = 2, xaxt ="n",
       xlab="", ylab="Median Difference SI-a Scores", 
       main = "95% CI Median Difference SI-a Scores")
axis(side=1, at=1:3,label=c("95% CI Pre-Post SI-a","95% CI Post-PostPost SI-a","95% CI Pre-PostPost SI-a"))

#mean of each group with 2SD CIs 
#more representative of data, easily interperted 
plotCI(1:3, c(mean_pre,mean_post,mean_postpost), uiw = c(2*std_dev_pre,2*std_dev_post,2*std_dev_postpost), lty = 2, xaxt ="n", 
       gap = 0,ylim=c(1,5),xlab="", ylab="Mean SI-a Scores", 
       main = "95% CI Mean SI-a Scores")

axis(side=1, at=1:3,label=c("95% CI Pre SI-a","95% CI Post SI-a","95% CI PostPost SI-a"))

#effect size
#for each combination, not corrected for pairwise comparisons
z_prepost=qnorm(medianpre_post$p.value)
Es_prepost=abs(z_prepost)/sqrt(length(datapre$score)+length(datapost$score))
Es_prepost
z_postpostpost=qnorm(medianpost_postpost$p.value)
Es_postpostpost=abs(z_postpostpost)/sqrt(length(datapost$score)+length(datapostpost$score))
Es_postpostpost
z_prepostpost=qnorm(medianpre_postpost$p.value)
Es_prepostpost=abs(z_prepostpost)/sqrt(length(datapre$score)+length(datapostpost$score))
Es_prepostpost
#power analysis 
#not a clear cut way to do power analysis with pairwise wilcox nonparametric - reported is parametric version 
n=length(datapre$score)
pwr.t.test(n=n,d=Es_prepost,sig.level=0.05,type="paired")
pwr.t.test(n=n,d=Es_postpostpost,sig.level=0.05,type="paired")
pwr.t.test(n=n,d=Es_prepostpost,sig.level=0.05,type="paired")
###################################################################################
#using pre/post data only 
#paired t-test, nonparametric = wilcoxon signed rank test
data1=read.csv("df_sia_melt_t.csv",header=TRUE)
datapre= subset(data1,data1$condition=="Pre SI-a")
datapost= subset(data1,data1$condition=="Post SI-a")

#general statistics: mean, standard deviation, standard error
mean_pre=mean(datapre$score)
print(mean_pre)
mean_post=mean(datapost$score)
print(mean_post)
datadiff=datapre$score-datapost$score
mean_diff=mean(datadiff)
print(mean_diff)
std_dev_pre=sd(datapre$score)
std_dev_post=sd(datapost$score)
std_dev_diff=sd(datadiff)
sem_pre=std_dev_pre/sqrt(length(datapre$score))
sem_post=std_dev_post/sqrt(length(datapost$score))
sem_diff=std_dev_diff/sqrt(length(datadiff))

#test for normality
qqnorm(datadiff)
qqline(datadiff)
shapiro.test(datadiff)

data1$factor=factor(data1$condition,levels=c("Pre SI-a","Post SI-a"))
boxplot(score ~ factor, data=data1, main="SI-a Scores Per Assessment Period",xlab="",ylab="",ylim=c(1,5),outline=FALSE)
#text(1:3, labels=c("a","b","c"),pos=3)
text(tapply(data1$score,data1$condition) - 2.22, labels=c("a","a"),pos=3)

#mean difference between groups (wilcoxon signed rank) with true CIs
#wilcoxon CIs
medianpre_post=wilcox.test(datapre$score, datapost$score,paired=TRUE, p.adj="bonferroni", conf.int = TRUE)
CIpre_post=(wilcox.test(datapre$score, datapost$score,paired=TRUE, p.adj="bonferroni", conf.int = TRUE)$conf.int)[2] -
  medianpre_post[[9]]


library("gplots")
plotCI(1:1, medianpre_post[[9]], 
       uiw = CIpre_post, lty = 2, xaxt ="n",
       xlab="", ylab="Median Difference SI-a Scores", 
       main = "95% CI Median Difference SI-a Scores")
axis(side=1, at=1:1,label="95% CI Pre-Post SI-a")

#mean of each group with 2SD CIs 
#more representative of data, easily interperted 
library("gplots")
plotCI(1:2, c(mean_pre,mean_post), uiw = c(2*std_dev_pre,2*std_dev_post), lty = 2, xaxt ="n", 
       gap = 0,xlim=c(0.8,2),ylim=c(1,5),xlab="", ylab="Mean SI-a Scores", 
       main = "95% CI Mean SI-a Scores")

axis(side=1, at=1:2,label=c("95% CI Pre SI-a","95% CI Post SI-a"))

#effect size
#for each combination, not corrected for pairwise comparisons
z_prepost=qnorm(medianpre_post$p.value)
Es_prepost=abs(z_prepost)/sqrt(length(datapre$score)+length(datapost$score))
Es_prepost
#power analysis 
#not a clear cut way to do power analysis with pairwise wilcox nonparametric - reported is parametric version 
n=length(datapre$score)
pwr.t.test(n=n,d=Es_prepost,sig.level=0.05,type="paired")

