#using pre/post data only
#dropping unpaired classes 
#paired t-test, nonparametric = wilcoxon signed rank test PAIRED
library("ez")
library("nlme") 
library("rmarkdown")
library("PMCMR")
require("multcomp")
library("gplots")
#dev.off() 
#run to clear plot environment 
#link to pdftex installation for knitting document, install in terminal not in Rstudio
#https://tex.stackexchange.com/questions/112734/is-it-possible-to-install-only-the-required-latex-tool-pdflatex-in-ubuntu
#use Sys.which("package") to make sure its there 
#using pre/post/postpost data
setwd("/home/aahowel3/Documents/scienceisfun/analysis/SIF_finalanalysis_July2018/SIF_analysis_postpst_December_2018/January_2019/")
data1=read.csv("df_all_melt_t.csv",header=TRUE)
datapre= subset(data1,data1$condition=="Pre All")
datapost= subset(data1,data1$condition=="Post All")

#general statistics: mean, standard deviation, standard error, confidence intervals 
mean_pre=mean(datapre$score)
print(mean_pre)
mean_post=mean(datapost$score)
print(mean_post)
std_dev_pre=sd(datapre$score)
std_dev_post=sd(datapost$score)
sem_pre=std_dev_pre/sqrt(length(datapre$score))
sem_post=std_dev_post/sqrt(length(datapost$score))
CI_upper_pre=mean_pre + (2*sem_pre)
CI_lower_pre=mean_pre - (2*sem_pre)
CI_upper_post=mean_post + (2*sem_post)
CI_lower_post=mean_post - (2*sem_post)

library("gplots")
plotCI(1:2, c(mean_pre,mean_post), uiw = c(2*sem_pre,2*sem_post), lty = 2, xaxt ="n", 
       gap = 0,xlim=c(0.5,2.5),xlab="", ylab="Mean Total Scores", 
       main = "95% CI Mean Total Scores")

axis(side=1, at=1:2,label=c("95% CI Pre Total","95% CI Post Total"))

wilcox.test(datapre$score, datapost$score,paired=TRUE)

medianpre_post=wilcox.test(datapre$score, datapost$score,paired=TRUE, p.adj="bonferroni", conf.int = TRUE)
CIpre_post=(wilcox.test(datapre$score, datapost$score,paired=TRUE, p.adj="bonferroni", conf.int = TRUE)$conf.int)[2] -
  medianpre_post[[9]]

#effect size
#for each combination, not corrected for pairwise comparisons
z_prepost=qnorm(medianpre_post$p.value)
Es_prepost=abs(z_prepost)/sqrt(length(datapre$score)+length(datapost$score))
Es_prepost
#power analysis 
#not a clear cut way to do power analysis with pairwise wilcox nonparametric - reported is parametric version 
n=length(datapre$score)
pwr.t.test(n=n,d=Es_prepost,sig.level=0.05,type="paired")


