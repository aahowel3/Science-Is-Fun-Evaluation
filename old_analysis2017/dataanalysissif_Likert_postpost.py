#descriptive statistics for Likert data
#!/usr/bin/python
#run in python3 
import re
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
import scipy
from scipy import stats, integrate
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import trim_mean, kurtosis
from scipy.stats.mstats import mode, gmean, hmean
from statsmodels.stats.anova import AnovaRM
import scipy.stats as stats
import statsmodels.stats.multicomp as multi 

#since scores are cumulative (PreAV = B6 + flipB7), having zeros instead of NaN is ok
#NaNs won't go through the flip_values function 

#removes scientific notation from pandas.sum()
pd.set_option('display.float_format', lambda x: '%.3f' % x)

df=pd.read_csv("SIF_Likert_prepost_AUG2018_postpost.csv", header=None) 
#have to specify header=None to have pd read in first column

#inverted (negatively worded) scoring for questions 7 and 11     
df.columns = df.iloc[0]
df=df.reindex(df.index.drop(0))
df.fillna("0", inplace=True)

def flip_values(x): 
    for row in x:
        if row == "1": 
            return("5") 
        if row == "2": 
            return("4") 
        if row == "4": 
            return("2") 
        if row == "5": 
            return("1") 
        if row == "3": 
            return("3")
        if row == "0": 
            return("0")
        if row == "2.5": 
            return("3.5")
        if row == "4.5": 
            return("1.5")
        if row == "1.5": 
            return("4.5")
        if row == "4.5": 
            return("1.5")
        if row == "3.5": 
           return("2.5") 

#inverted (negatively worded) scoring for questions 7 and 11       
flip_B7=[]
for row in df["B7"]:
    flip_B7.append(flip_values(row))
df['flip_B7'] = flip_B7
df['flip_B7']=df['flip_B7'].apply(pd.to_numeric)

flip_B11=[]
for row in df["B11"]:
    flip_B11.append(flip_values(row))
df['flip_B11'] = flip_B11
df['flip_B11']=df['flip_B11'].apply(pd.to_numeric)

flip_A7=[]
for row in df["A7"]:
    flip_A7.append(flip_values(row))
df['flip_A7'] = flip_A7
df['flip_A7']=df['flip_A7'].apply(pd.to_numeric)

flip_A11=[]
for row in df["A11"]:
    flip_A11.append(flip_values(row))
df['flip_A11'] = flip_A11
df['flip_A11']=df['flip_A11'].apply(pd.to_numeric)

flip_AA7=[]
for row in df["AA7"]:
    flip_AA7.append(flip_values(row))
df['flip_AA7'] = flip_AA7
df['flip_AA7']=df['flip_AA7'].apply(pd.to_numeric)

flip_AA11=[]
for row in df["AA11"]:
    flip_AA11.append(flip_values(row))
df['flip_AA11'] = flip_AA11
df['flip_AA11']=df['flip_AA11'].apply(pd.to_numeric)


#convert numeric columns to numbers (not including free response questions) 
df.loc[:, 'B1':'B19']=df.loc[:,'B1':'B19'].apply(pd.to_numeric)
df.loc[:, 'A1':'A19']=df.loc[:,'A1':'A19'].apply(pd.to_numeric)
df.loc[:, 'AA1':'AA19']=df.loc[:,'AA1':'AA19'].apply(pd.to_numeric)


#divide by number of questions in the category so all are standardized 
df['Pre SI-a'] = df['B1'] + df['B2'] + df['B3'] + df['B4'] + df['B5'] + df['B17'] + df['B18'] + df['B19']
presia=[]
for row in df["Pre SI-a"]:
    x=row/8 
    presia.append(x)
df['Pre SI-a'] = presia

df['Pre AV'] = df['B6'] + df['flip_B7'] 
presia=[]
for row in df["Pre AV"]:
    x=row/2
    presia.append(x)
df['Pre AV'] = presia

df['Pre E'] = df['B8'] + df['B9'] + df['B10'] + df['flip_B11'] 
presia=[]
for row in df["Pre E"]:
    x=row/4
    presia.append(x)
df['Pre E'] = presia

df['Pre NGSS'] = df['B12'] + df['B13'] + df['B14'] + df['B15'] + df['B16'] 
presia=[]
for row in df["Pre NGSS"]:
    x=row/5
    presia.append(x)
df['Pre NGSS'] = presia

df['Post SI-a'] = df['A1'] + df['A2'] + df['A3'] + df['A4'] + df['A5'] + df['A17'] + df['A18'] + df['A19']
postsia=[]
for row in df["Post SI-a"]:
    x=row/8 
    postsia.append(x)
df['Post SI-a'] = postsia

df['Post AV'] = df['A6'] + df['flip_A7'] 
presia=[]
for row in df["Post AV"]:
    x=row/2
    presia.append(x)
df['Post AV'] = presia

df['Post E'] = df['A8'] + df['A9'] + df['A10'] + df['flip_A11'] 
presia=[]
for row in df["Post E"]:
    x=row/4
    presia.append(x)
df['Post E'] = presia

df['Post NGSS'] = df['A12'] + df['A13'] + df['A14'] + df['A15'] + df['A16']
presia=[]
for row in df["Post NGSS"]:
    x=row/5
    presia.append(x)
df['Post NGSS'] = presia

df['PostPost SI-a'] = df['AA1'] + df['AA2'] + df['AA3'] + df['AA4'] + df['AA5'] + df['AA17'] + df['AA18'] + df['AA19']
postsia=[]
for row in df["PostPost SI-a"]:
    x=row/8 
    postsia.append(x)
df['PostPost SI-a'] = postsia

df['PostPost AV'] = df['AA6'] + df['flip_AA7'] 
presia=[]
for row in df["PostPost AV"]:
    x=row/2
    presia.append(x)
df['PostPost AV'] = presia

df['PostPost E'] = df['AA8'] + df['AA9'] + df['AA10'] + df['flip_AA11'] 
presia=[]
for row in df["PostPost E"]:
    x=row/4
    presia.append(x)
df['PostPost E'] = presia

df['PostPost NGSS'] = df['AA12'] + df['AA13'] + df['AA14'] + df['AA15'] + df['AA16']
presia=[]
for row in df["PostPost NGSS"]:
    x=row/5
    presia.append(x)
df['PostPost NGSS'] = presia

df['Cumulative']="Cumulative"

#create intermediate file with data from all schools, will only compare pre and post for ttest in R 
df.replace(to_replace=0, value="NaN", inplace=True)
df.to_csv("intermediatecheck_test.csv")
#damn you statsmodels having no corrections or updates - export to R
df_sia=df[["Subjects",'Pre SI-a','Post SI-a','PostPost SI-a']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_sia_melt_t.csv") 

df_sia=df[["Subjects",'Pre E','Post E','PostPost E']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_e_melt_t.csv") 

df_sia=df[["Subjects",'Pre AV','Post AV','PostPost AV']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_av_melt_t.csv") 

df_sia=df[["Subjects",'Pre NGSS','Post NGSS','PostPost NGSS']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_ngss_melt_t.csv") 


#remove schools with no post-post data
df=df[df["School"] != "Patterson"]
df=df[df["School"] != "CTA"]
#remove single entries without post-post data
df=df[df["D1postpost"] != "no secondary post data "]
#create intermediate file with data from only complete schools for friedmans test in R
df.replace(to_replace=0, value="NaN", inplace=True)
df.to_csv("intermediatecheck_friedmans.csv") 

#damn you statsmodels having no corrections or updates - export to R
df_sia=df[["Subjects",'Pre SI-a','Post SI-a','PostPost SI-a']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_sia_melt_f.csv") 

df_sia=df[["Subjects",'Pre E','Post E','PostPost E']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_e_melt_f.csv") 

df_sia=df[["Subjects",'Pre AV','Post AV','PostPost AV']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_av_melt_f.csv") 

df_sia=df[["Subjects",'Pre NGSS','Post NGSS','PostPost NGSS']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_ngss_melt_f.csv") 


'''
print("Pre SI-a Descriptive Statistics")
lengthx=(df['Pre SI-a']).count()
print(lengthx)

#SI-a 
#ttest_rel is a PAIRED t-test, ok for likert not DAST data 
#really should have been using repeated measures ANOVA each time 
print("Pre SI-a Descriptive Statistics")
lengthx=(df['Pre SI-a']).count()
meann=(df['Pre SI-a'].mean())
sdd=(df['Pre SI-a'].std())
semm=(df['Pre SI-a'].sem())
print("N:", lengthx, "Mean:", meann, "SD total:", sdd, "SE total:", semm)
df["Pre SI-a"].plot(kind="hist",title="Pre SI-a Histogram")
plt.show()
stats.probplot(df["Pre SI-a"], plot=plt)
plt.show()
a=stats.shapiro(df['Pre SI-a'])
print("SW Normality of Pre SI-a data:", a) 
#try transformation
df["Pre SI-a_trans"]=np.cbrt(df["Pre SI-a"])
df["Pre SI-a_trans"].plot(kind="hist",title="Pre SI-a_trans Histogram")
plt.show()
stats.probplot(df["Pre SI-a_trans"], plot=plt)
plt.show()
a=stats.shapiro(df['Pre SI-a_trans'])
print("SW Normality of Pre SI-a_trans data:", a)


print("Post SI-a Descriptive Statistics")
lengthx=(df['Post SI-a']).count()
meann=(df['Post SI-a'].mean())
sdd=(df['Post SI-a'].std())
semm=(df['Post SI-a'].sem())
print("N:", lengthx, "Mean:", meann, "SD:", sdd, "SE:", semm)
df["Post SI-a"].plot(kind="hist",title="Post SI-a Histogram")
plt.show()
stats.probplot(df["Post SI-a"], plot=plt)
plt.show()
a=stats.shapiro(df['Post SI-a'])
print("SW Normality of Post SI-a data:", a)
#try transformation
df["Post SI-a_trans"]=np.cbrt(df["Post SI-a"])
df["Post SI-a_trans"].plot(kind="hist",title="Post SI-a_trans Histogram")
plt.show()
stats.probplot(df["Post SI-a_trans"], plot=plt)
plt.show()
a=stats.shapiro(df['Post SI-a_trans'])
print("SW Normality of Pre SI-a_trans data:", a)

#pre/post only Levene's Test
sia_lev=stats.levene(df['Pre SI-a'],df['Post SI-a'])
print(sia_lev)

sia_barlett=stats.bartlett(df['Pre SI-a'],df['Post SI-a'])
print(sia_barlett)
#pre/post/postpost Sphericity 


#pre and post signifigance paired t-test
#normal t-test
print("SI-a Significance")
y=scipy.stats.ttest_rel(df['Pre SI-a'], df['Post SI-a']) 
print(y)
#non-parametric test
r=scipy.stats.wilcoxon(df['Pre SI-a'], df['Post SI-a'])
print(r)
#transformed data with t-test 
#y=scipy.stats.ttest_rel(df['Pre SI-a_trans'], df['Post SI-a_trans']) 
print(y)


cohens_sia = (   (df['Pre SI-a'].mean()) - (df['Post SI-a'].mean()) )/ (  np.sqrt( ((df['Pre SI-a'].std()) ** 2) + (df['Post SI-a'].std()) ** 2) / 2)
print("Cohen's D SI-a", cohens_sia)

#pre/post/postpost Repeated measures ANOVA 
#first transform data wide to long with df.unstack, subset each category so you're not shifting entire dataset 
df_sia=df[["Subjects",'Pre SI-a','Post SI-a']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
print(df_sia_melt)

aovrm=AnovaRM(df_sia_melt, "score","Subjects",within=["condition"])
res=aovrm.fit()
print(res) 
'''
'''
#tukeyHSD test multicomparison 
test=multi.MultiComparison(df_sia_melt["score"],df_sia_melt["condition"])
res=test.tukeyhsd()
print(res.summary()) 

#Beferroni correction mulitple comparison 
MultiComp=multi.MultiComparison(df_sia_melt["score"],df_sia_melt["condition"])
res=MultiComp.allpairtest(stats.ttest_rel, method="Holm")
print(res[0])


#E
print("Pre E Descriptive Statistics")
lengthx=(df['Pre E']).count()
meann=(df['Pre E'].mean())
sdd=(df['Pre E'].std())
semm=(df['Pre E'].sem())
print("N:", lengthx, "Mean:", meann, "SD:", sdd, "SE:", semm)
df["Pre E"].plot(kind="hist",title="Pre E Histogram")
plt.show()
a=stats.shapiro(df['Pre E'])
print("SW Normality of Pre E data:", a)

print("Post E Descriptive Statistics")
lengthx=(df['Post E']).count()
meann=(df['Post E'].mean())
sdd=(df['Post E'].std())
semm=(df['Post E'].sem())
print("N:", lengthx, "Mean:", meann, "SD:", sdd, "SE:", semm)
df["Post E"].plot(kind="hist",title="Post E Histogram")
plt.show()
a=stats.shapiro(df['Post E'])
print("SW Normality of Post E data:", a)


print("E Significance")
y=scipy.stats.ttest_rel(df['Pre E'], df['Post E']) 
print(y)
r=scipy.stats.wilcoxon(df['Pre E'], df['Post E'])
print(r)

cohens_e = (   (df['Pre E'].mean()) - (df['Post E'].mean()) )/ (  np.sqrt( ((df['Pre E'].std()) ** 2) + (df['Post E'].std()) ** 2) / 2)
print("Cohen's D E:", cohens_e)

#AV
print("Pre AV Descriptive Statistics")
lengthx=len(df['Pre AV']) 
meann=(df['Pre AV'].mean())
sdd=(df['Pre AV'].std())
semm=(df['Pre AV'].sem())
print("N:", lengthx, "Mean:", meann, "SD:", sdd, "SE:", semm)
a=stats.shapiro(df['Pre AV'])
print("SW Normality of Pre AV data:", a)

print("Post AV Descriptive Statistics")
lengthx=len(df['Post AV']) 
meann=(df['Post AV'].mean())
sdd=(df['Post AV'].std())
semm=(df['Post AV'].sem())
print("N:", lengthx, "Mean:", meann, "SD:", sdd, "SE:", semm)
a=stats.shapiro(df['Post AV'])
print("SW Normality of Post AV data:", a)


print("AV Significance")
y=scipy.stats.ttest_rel(df['Pre AV'], df['Post AV']) 
print(y)
r=scipy.stats.wilcoxon(df['Pre AV'], df['Post AV'])
print(r)

cohens_av = (   (df['Pre AV'].mean()) - (df['Post AV'].mean()) )/ (  np.sqrt( ((df['Pre AV'].std()) ** 2) + (df['Post AV'].std()) ** 2) / 2)
print("Cohen's D AV:", cohens_av)

#NGSS
print("Pre NGSS Descriptive Statistics")
lengthx=len(df['Pre NGSS']) 
meann=(df['Pre NGSS'].mean())
sdd=(df['Pre NGSS'].std())
semm=(df['Pre NGSS'].sem())
print("N:", lengthx, "Mean:", meann, "SD:", sdd, "SE:", semm)
a=stats.shapiro(df['Pre NGSS'])
print("SW Normality of Pre NGSS data:", a)

print("Post NGSS Descriptive Statistics")
lengthx=len(df['Post NGSS']) 
meann=(df['Post NGSS'].mean())
sdd=(df['Post NGSS'].std())
semm=(df['Post NGSS'].sem())
print("N:", lengthx, "Mean:", meann, "SD:", sdd, "SE:", semm)
a=stats.shapiro(df['Post NGSS'])
print("SW Normality of Post NGSS data:", a)


print("NGSS Significance")
y=scipy.stats.ttest_rel(df['Pre NGSS'], df['Post NGSS']) 
print(y)
r=scipy.stats.wilcoxon(df['Pre NGSS'], df['Post NGSS'])
print(r)

cohens_ngss = (   (df['Pre NGSS'].mean()) - (df['Post NGSS'].mean()) )/ (  np.sqrt( ((df['Pre NGSS'].std()) ** 2) + (df['Post NGSS'].std()) ** 2) / 2)
print("Cohen's D NGSS", cohens_ngss)

#Dot plot figures are in sif_cumulative_graphs.py
#uses new_siflikert.csv data 

####Descriptive stats for each school for each category (SIa, EV,A,NGSS) 
schools=['Auxier', 'Bologna','CTA','Hartford','Hull','Navarrete', 'Patterson','Weinberg'] 

#SIA descriptive stats by school
df['Pre SI-a'] = df['Pre SI-a'].astype(int)
presiamean=df.groupby('School')['Pre SI-a'].mean().round(2)
df['Post SI-a'] = df['Post SI-a'].astype(int)
postsiamean=df.groupby('School')['Post SI-a'].mean().round(2)
df['Pre SI-a'] = df['Pre SI-a'].astype(int)
presiasd=df.groupby('School')['Pre SI-a'].std().round(2)
df['Post SI-a'] = df['Post SI-a'].astype(int)
postsiasd=df.groupby('School')['Post SI-a'].std().round(2)
df['Pre SI-a'] = df['Pre SI-a'].astype(int)
presiase=df.groupby('School')['Pre SI-a'].sem().round(2)
df['Post SI-a'] = df['Post SI-a'].astype(int)
postsiase=df.groupby('School')['Post SI-a'].sem().round(2)

presiamean=presiamean.tolist()
postsiamean=postsiamean.tolist()
presiasd=presiasd.tolist()
postsiasd=postsiasd.tolist()
presiase=presiase.tolist()
postsiase=postsiase.tolist()

pre_sia_ds=[]
pre_sia_ds.append(schools)
pre_sia_ds.append(presiamean)
pre_sia_ds.append(postsiamean)
pre_sia_ds.append(presiasd)
pre_sia_ds.append(postsiasd)
pre_sia_ds.append(presiase)
pre_sia_ds.append(postsiase)

headers = pre_sia_ds.pop(0)
df1 = pd.DataFrame(pre_sia_ds,columns=headers)
df1=df1[["Hartford","Patterson","CTA","Bologna","Hull","Weinberg","Navarrete","Auxier"]]
df1.to_csv("descriptive_stat1.csv") 
df1 = pd.DataFrame(pre_sia_ds,columns=headers)

#E descriptive stats by school
df['Pre E'] = df['Pre E'].astype(int)
presiamean=df.groupby('School')['Pre E'].mean().round(2)
df['Post E'] = df['Post E'].astype(int)
postsiamean=df.groupby('School')['Post E'].mean().round(2)
df['Pre E'] = df['Pre E'].astype(int)
presiasd=df.groupby('School')['Pre E'].std().round(2)
df['Post E'] = df['Post E'].astype(int)
postsiasd=df.groupby('School')['Post E'].std().round(2)
df['Pre E'] = df['Pre E'].astype(int)
presiase=df.groupby('School')['Pre E'].sem().round(2)
df['Post E'] = df['Post E'].astype(int)
postsiase=df.groupby('School')['Post E'].sem().round(2)

presiamean=presiamean.tolist()
postsiamean=postsiamean.tolist()
presiasd=presiasd.tolist()
postsiasd=postsiasd.tolist()
presiase=presiase.tolist()
postsiase=postsiase.tolist()

pre_sia_ds=[]
pre_sia_ds.append(schools)
pre_sia_ds.append(presiamean)
pre_sia_ds.append(postsiamean)
pre_sia_ds.append(presiasd)
pre_sia_ds.append(postsiasd)
pre_sia_ds.append(presiase)
pre_sia_ds.append(postsiase)

headers = pre_sia_ds.pop(0)
df1 = pd.DataFrame(pre_sia_ds, columns=headers)
df1=df1[["Hartford","Patterson","CTA","Bologna","Hull","Weinberg","Navarrete","Auxier"]]
df1.to_csv("descriptive_stat2.csv") 
df1 = pd.DataFrame(pre_sia_ds, columns=headers)

#AV descriptive stats by school
df['Pre AV'] = df['Pre AV'].astype(int)
presiamean=df.groupby('School')['Pre AV'].mean().round(2)
df['Post AV'] = df['Post AV'].astype(int)
postsiamean=df.groupby('School')['Post AV'].mean().round(2)
df['Pre AV'] = df['Pre AV'].astype(int)
presiasd=df.groupby('School')['Pre AV'].std().round(2)
df['Post AV'] = df['Post AV'].astype(int)
postsiasd=df.groupby('School')['Post AV'].std().round(2)
df['Pre AV'] = df['Pre AV'].astype(int)
presiase=df.groupby('School')['Pre AV'].sem().round(2)
df['Post AV'] = df['Post AV'].astype(int)
postsiase=df.groupby('School')['Post AV'].sem().round(2)

presiamean=presiamean.tolist()
postsiamean=postsiamean.tolist()
presiasd=presiasd.tolist()
postsiasd=postsiasd.tolist()
presiase=presiase.tolist()
postsiase=postsiase.tolist()

pre_sia_ds=[]
pre_sia_ds.append(schools)
pre_sia_ds.append(presiamean)
pre_sia_ds.append(postsiamean)
pre_sia_ds.append(presiasd)
pre_sia_ds.append(postsiasd)
pre_sia_ds.append(presiase)
pre_sia_ds.append(postsiase)

headers = pre_sia_ds.pop(0)
df1 = pd.DataFrame(pre_sia_ds, columns=headers)
df1=df1[["Hartford","Patterson","CTA","Bologna","Hull","Weinberg","Navarrete","Auxier"]]
df1.to_csv("descriptive_stat3.csv") 
df1 = pd.DataFrame(pre_sia_ds, columns=headers)

#NGSS descriptive stats by school
df['Pre NGSS'] = df['Pre NGSS'].astype(int)
presiamean=df.groupby('School')['Pre NGSS'].mean().round(2)
df['Post NGSS'] = df['Post NGSS'].astype(int)
postsiamean=df.groupby('School')['Post NGSS'].mean().round(2)
df['Pre NGSS'] = df['Pre NGSS'].astype(int)
presiasd=df.groupby('School')['Pre NGSS'].std().round(2)
df['Post NGSS'] = df['Post NGSS'].astype(int)
postsiasd=df.groupby('School')['Post NGSS'].std().round(2)
df['Pre NGSS'] = df['Pre NGSS'].astype(int)
presiase=df.groupby('School')['Pre NGSS'].sem().round(2)
df['Post NGSS'] = df['Post NGSS'].astype(int)
postsiase=df.groupby('School')['Post NGSS'].sem().round(2)

presiamean=presiamean.tolist()
postsiamean=postsiamean.tolist()
presiasd=presiasd.tolist()
postsiasd=postsiasd.tolist()
presiase=presiase.tolist()
postsiase=postsiase.tolist()

pre_sia_ds=[]
pre_sia_ds.append(schools)
pre_sia_ds.append(presiamean)
pre_sia_ds.append(postsiamean)
pre_sia_ds.append(presiasd)
pre_sia_ds.append(postsiasd)
pre_sia_ds.append(presiase)
pre_sia_ds.append(postsiase)

headers = pre_sia_ds.pop(0)
df1 = pd.DataFrame(pre_sia_ds, columns=headers)
df1=df1[["Hartford","Patterson","CTA","Bologna","Hull","Weinberg","Navarrete","Auxier"]]
df1.to_csv("descriptive_stat4.csv") 
df1 = pd.DataFrame(pre_sia_ds, columns=headers)

#result.to_csv("descriptivestats.csv")

###listing signifigance as 0.1 rather than 0.05
###Si-a is signifigant regardless of Wilcoxin or paired t-test 
###E is only signifigant using paired-t 
###However, we really can't justify using paired-t bc we have non-normal data 
###Try AD instead of Sharpiro normality to see if we can better justify using parametric test 

#General demographic pie chart 
#these 2 functions take the entries from the racial, hispanic, and gender categories and split them on , (split fucntion 1) and / (split fucntion 2)
#for responses with multiple answers, really only applicable for race I guess
def split1(a):
    b=[]
    for i in a:
        b.extend(i.split(','))
    return(b)
def split2(b):
    c=[]
    for i in b:
        c.extend(i.split('/'))
    return(c)

#gender response categories
a=df['D1pre'].values.tolist()
b=split1(a)
c=split2(b)
females=0
males=0
idk=0

for x in c: 
    if x=="male" or x== "Male"or x=="M" or x=="m":
        males +=1 
    if x=="female" or x=="Female" or x=="F" or x=="f":
        females +=1 
    if x=="decline to state": 
        idk +=1

labels = ("Female", "Male", "Decline to State") 

men=(males)/len(df["D1pre"]) * 100
women=(females)/len(df["D1pre"]) * 100
decline=(idk)/len(df["D1pre"]) * 100

sizes = [women, men, decline]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('Participant Gender Demographics')
fig1.savefig("likertgenderdemo.png")


#Likert racial categories 
a=df['D2pre '].values.tolist()
b=split1(a)
c=split2(b)
other=0
white=0
asian=0
africanamerican=0
decline=0
pacific=0

for x in c: 
    if x=="other":
        other +=1 
    if x=="white" or x=="white/other" or x=="white,other" or x=="White":
        white +=1
    if x=="Asian" or x=="asian":
        asian +=1
    if x=="Black or African American" or x=="black or african american" or x=="african-american":
        africanamerican +=1
    if x=="Native Hawaiian or Other Pacific Islander":
        pacific +=1
    if x=="decline to state":
        decline +=1 
        

r=(other)/len(df["D2pre "]) * 100
w=(white)/len(df["D2pre "]) *100 
a=(asian)/len(df["D2pre "]) *100 
h=(pacific)/len(df["D2pre "]) *100 
aa=(africanamerican)/len(df["D2pre "]) *100 
aar=(decline)/len(df["D2pre "]) *100 

sizes = [r,w, a, h,aa, aar]

labelz = ("Other", "White", "Asian", "Native Hawaiian or Other Pacific Islander", "Black or African American", "Decline to State")

patches,  texts = plt.pie(sizes, startangle=90, radius=1.2)
labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labelz, sizes)]

sort_legend = True
if sort_legend:
    patches, labels, dummy =  zip(*sorted(zip(patches, labels, sizes),
                                          key=lambda x: x[2],
                                          reverse=True))

plt.legend(patches, labels, fontsize=10)
plt.title("Participant Racial Demographics")
plt.savefig("likertracialdemo.png")

###Likert Hispanic demograpihcs 
yes=0
no=0
idk=0

for x in df["D3pre"]: 
    if x=="y" or x=="yes (spanish)"or x=="yes (Spanish)" or x=="Yes" or x=="yes" or x=="Y":
        yes +=1 
    if x=="n" or x=="N" or x=="No" or x=="no":
        no +=1 
    if x=="decline to state": 
        idk +=1

labels = ("Yes", "No", "Decline to State") 

Yes=(yes)/len(df["D3pre"]) * 100
No=(no)/len(df["D3pre"]) * 100
decline=(idk)/len(df["D3pre"]) * 100

sizes = [Yes, No, decline]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('Participant Hispanic Demographics')
fig1.savefig("likerhisnpanicdemo.png")

#post questionaire count graph responses
ax = sns.countplot(x="A21", data=df)
plt.title("I enjoyed the presentation.")
ax.set(xlabel='responses')

ax = sns.countplot(x="A22", data=df)
plt.title("The presentation made me think about new things.")
ax.set(xlabel='responses')

ax = sns.countplot(x="A23", data=df)
plt.title("The presentation kept my attention.")
ax.set(xlabel='responses')

ax = sns.countplot(x="A24", data=df)
plt.title("The presentation made me curious about science.")
ax.set(xlabel='responses')
#plt.show()
'''
