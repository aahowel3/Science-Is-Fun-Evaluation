#all graphs and signifigance values for DAST data
#ONLY script you need for DAST data 
#!/usr/bin/python 

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
from statsmodels.stats.proportion import proportions_ztest
 
#removes scientific notation from pandas.sum()
pd.set_option('display.float_format', lambda x: '%.3f' % x)


df=pd.read_csv("SIF_DAST_prepost_AUG2018_postpost.csv", header=None, encoding="ISO-8859-1") 
#have to specify header=None to have pd read in first column
 
df.columns = df.iloc[0]

df=df.reindex(df.index.drop(0))

#with "other" categorical answers don't care about nuiances rn so converting everything with addtional info into simple "yes" 
category=[]
for x in df["other (symbols of research)"]:
    if x == "n" or x=="N":
        category.append("n")
    else: 
        category.append("y") 
df["corrected other (symbols of research)"]=category

category=[]
for x in df["other (symbols of knowledge)"]:
    if x == "n" or x=="N":
        category.append("n")
    else: 
        category.append("y") 
df["corrected other (symbols of knowledge)"]=category

category=[]
for x in df["machines"]:
    if x == "n" or x=="N":
        category.append("n")
    else: 
        category.append("y") 
df["corrected machines"]=category

category=[]
for x in df["other (signs of technology)"]:
    if x == "n" or x=="N":
        category.append("n")
    else: 
        category.append("y") 
df["corrected other (signs of technology)"]=category

category=[]
for x in df["pother (symbols of research)"]:
    if x == "n" or x=="N":
        category.append("n")
    else: 
        category.append("y") 
df["pcorrected other (symbols of research)"]=category

category=[]
for x in df["pother (symbols of knowledge)"]:
    if x == "n" or x=="N":
        category.append("n")
    else: 
        category.append("y") 
df["pcorrected other (symbols of knowledge)"]=category

category=[]
for x in df["pmachines"]:
    if x == "n" or x=="N":
        category.append("n")
    else: 
        category.append("y") 
df["pcorrected machines"]=category

category=[]
for x in df["pother (signs of technology)"]:
    if x == "n" or x=="N":
        category.append("n")
    else: 
        category.append("y") 
df["pcorrected other (signs of technology)"]=category

category=[]
for x in df["ppother (symbols of research)"]:
    if x == "n" or x=="N":
        category.append("n")
    else: 
        category.append("y") 
df["ppcorrected other (symbols of research)"]=category

category=[]
for x in df["ppother (symbols of knowledge)"]:
    if x == "n" or x=="N":
        category.append("n")
    else: 
        category.append("y") 
df["ppcorrected other (symbols of knowledge)"]=category

category=[]
for x in df["ppmachines"]:
    if x == "n" or x=="N":
        category.append("n")
    else: 
        category.append("y") 
df["ppcorrected machines"]=category

category=[]
for x in df["ppother (signs of technology)"]:
    if x == "n" or x=="N":
        category.append("n")
    else: 
        category.append("y") 
df["ppcorrected other (signs of technology)"]=category

df.drop(['other (symbols of research)', 'other (symbols of knowledge)','machines','other (signs of technology)','pother (symbols of research)', 'pother (symbols of knowledge)','pmachines','pother (signs of technology)','ppother (symbols of research)', 'ppother (symbols of knowledge)','ppmachines','ppother (signs of technology)'], axis=1,inplace=True)

#print(df.columns)

df.fillna("NA", inplace=True)
cols = ['lab coat','eyeglasses','facial hair','pencil/pen in pocket','unkempt appearance','test tubes',	\
'flasks','microscope','bunsen burner','experimental animals','corrected other (symbols of research)','books',	\
'filing cabinets','corrected other (symbols of knowledge)','solutions in glassware','corrected machines','corrected other (signs of technology)', \
'plab coat','peyeglasses','pfacial hair','ppencil/pen in pocket','punkempt appearance','ptest tubes',	\
'pflasks','pmicroscope','pbunsen burner','pexperimental animals','pcorrected other (symbols of research)','pbooks',	\
'pfiling cabinets','pcorrected other (symbols of knowledge)','psolutions in glassware','pcorrected machines','pcorrected other (signs of technology)', \
'pplab coat','ppeyeglasses','ppfacial hair','pppencil/pen in pocket','ppunkempt appearance','pptest tubes',	\
'ppflasks','ppmicroscope','ppbunsen burner','ppexperimental animals','ppcorrected other (symbols of research)','ppbooks',	\
'ppfiling cabinets','ppcorrected other (symbols of knowledge)','ppsolutions in glassware','ppcorrected machines','ppcorrected other (signs of technology)']
df[cols]= df[cols].replace({'n':'0'})
df[cols]= df[cols].replace({'N':'0'})
df[cols]= df[cols].replace({'y':'1'})
df[cols]= df[cols].replace({'Y':'1'})

#df.to_csv("DAST_int.csv") 

df=pd.read_csv("DAST_int.csv", encoding="ISO-8859-1")

df.replace("NaN", np.nan)
#some columns you will still have to go in and manually edit, nbd
#df=df[df["pplab coat"] != "no secondary post data "]
df.loc[:, 'lab coat':'solutions in glassware']=df.loc[:,'lab coat':'solutions in glassware'].apply(pd.to_numeric)
df.loc[:, 'plab coat':'psolutions in glassware']=df.loc[:,'plab coat':'psolutions in glassware'].apply(pd.to_numeric)
#df.loc[:, 'pplab coat':'ppsolutions in glassware']=df.loc[:,'pplab coat':'ppsolutions in glassware'].apply(pd.to_numeric)
df.loc[:, 'corrected other (symbols of research)':'pcorrected other (signs of technology)']=df.loc[:,'corrected other (symbols of research)':'pcorrected other (signs of technology)'].apply(pd.to_numeric)


df['Pre PC'] = df['lab coat'] + df['eyeglasses'] + df['facial hair'] + df['pencil/pen in pocket'] \
+ df['unkempt appearance'] 
presia=[]
for row in df["Pre PC"]:
    x=row/5
    presia.append(x)
df['Pre PC'] = presia

df['Post PC'] = df['plab coat'] + df['peyeglasses'] + df['pfacial hair'] + df['ppencil/pen in pocket'] + df['punkempt appearance'] 
presia=[]
for row in df["Post PC"]:
    x=row/5
    presia.append(x)
df['Post PC'] = presia


df['Pre SR'] = df['test tubes'] + df['flasks'] + df['microscope'] + df['bunsen burner'] \
+ df['experimental animals'] + df['corrected other (symbols of research)'] 
presia=[]
for row in df["Pre SR"]:
    x=row/6
    presia.append(x)
df['Pre SR'] = presia

df['Post SR'] = df['ptest tubes'] + df['pflasks'] + df['pmicroscope'] + df['pbunsen burner'] \
+ df['pexperimental animals'] + df['pcorrected other (symbols of research)'] 
presia=[]
for row in df["Post SR"]:
    x=row/6
    presia.append(x)
df['Post SR'] = presia


df['Pre SK'] = df['books'] + df['filing cabinets'] + df['corrected other (symbols of knowledge)'] 
presia=[]
for row in df["Pre SK"]:
    x=row/3
    presia.append(x)
df['Pre SK'] = presia

df['Post SK'] = df['pbooks'] + df['pfiling cabinets'] + df['pcorrected other (symbols of knowledge)'] 
presia=[]
for row in df["Post SK"]:
    x=row/3
    presia.append(x)
df['Post SK'] = presia

df['Pre ST'] = df['solutions in glassware'] + df['corrected machines'] + df['corrected other (signs of technology)'] 
presia=[]
for row in df["Pre ST"]:
    x=row/3
    presia.append(x)
df['Pre ST'] = presia

df['Post ST'] = df['psolutions in glassware'] + df['pcorrected machines'] + df['pcorrected other (signs of technology)'] 
presia=[]
for row in df["Post ST"]:
    x=row/3
    presia.append(x)
df['Post ST'] = presia


#df=df[df["Pre PC"] != "np.nan"]
#df=df[df["Post PC"] != "np.nan"]

#use following section of code if doing a rmANOVA either with pre/post/postpost data or pre/post only
#treating DAST data as continuous 

#create melt columns for all students for pre/post data 
#postpost is listed but will not be used in analysis 
#wilcox analysis will be done here 
'''
df=df[(df["scientist gender"] == "m") | (df["scientist gender"] == "f")]
df=df[(df["pscientist gender"] == "m") | (df["pscientist gender"] == "f")]
#df=df[(df["ppscientist gender"] == "m") | (df["ppscientist gender"] == "f")]
####for m/f count specifically, have to remove lines with idk and both
df_sia=df[["Subjects",'scientist gender','pscientist gender']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_gender_melt_t.csv") 
'''

df_sia=df[["Subjects",'Pre SK','Post SK']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_SK_melt_t.csv")
'''
df_sia=df[["Subjects",'Pre PC','Post PC']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_PC_melt_t.csv") 

df_sia=df[["Subjects",'Pre SR','Post SR']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_SR_melt_t.csv") 

 

df_sia=df[["Subjects",'Pre ST','Post ST']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_ST_melt_t.csv") 
'''
#friedman's analysis will be done here 
#remove schools with no post-post data
df=df[df["School "] != "Patterson"]
df=df[df["School "] != "Patterson "]
df=df[df["School "] != "CTA"]
df=df[df["Subjects"] != "H2 (drawings averaged) "]
df=df[df["Subjects"] != "H3 (drawings averaged) "]
df=df[df["Subjects"] != "H5 (drawings averaged) "]
df=df[df["Subjects"] != "H3 (drawings averaged)"]
df=df[df["Subjects"] != "H5 (drawings averaged)"]
df=df[df["Subjects"] != "H5(drawings averaged)"]

#df.to_csv("check.csv") 

#remove single entries without post-post data
df=df[df["pplab coat"] != "no secondary post data "]


df.replace("NaN", 0)

df.loc[:, 'pplab coat':'ppsolutions in glassware']=df.loc[:,'pplab coat':'ppsolutions in glassware'].apply(pd.to_numeric)
df.loc[:, 'corrected other (symbols of research)':'ppcorrected other (signs of technology)']=df.loc[:,'corrected other (symbols of research)':'ppcorrected other (signs of technology)'].apply(pd.to_numeric)


df['PostPost PC'] = df['pplab coat'] + df['ppeyeglasses'] + df['ppfacial hair'] + df['pppencil/pen in pocket'] \
+ df['ppunkempt appearance'] 
presia=[]
for row in df["PostPost PC"]:
    x=row/5
    presia.append(x)
df['PostPost PC'] = presia

df['PostPost SR'] = df['pptest tubes'] + df['ppflasks'] + df['ppmicroscope'] + df['ppbunsen burner'] \
+ df['ppexperimental animals'] + df['ppcorrected other (symbols of research)'] 
presia=[]
for row in df["PostPost SR"]:
    x=row/6
    presia.append(x)
df['PostPost SR'] = presia

df['PostPost ST'] = df['ppsolutions in glassware'] + df['ppcorrected machines'] + df['ppcorrected other (signs of technology)'] 
presia=[]
for row in df["PostPost ST"]:
    x=row/3
    presia.append(x)
df['PostPost ST'] = presia

df['PostPost SK'] = df['ppbooks'] + df['ppfiling cabinets'] + df['ppcorrected other (symbols of knowledge)'] 
presia=[]
for row in df["PostPost SK"]:
    x=row/3
    presia.append(x)
df['PostPost SK'] = presia

'''
#have to filter chi2 datasets by t test first (leave in all subjects with complete pre/post) then by friedmans (remove subjects without complete pre/post/postpost)
df=df[(df["scientist gender"] == "m") | (df["scientist gender"] == "f")]
df=df[(df["pscientist gender"] == "m") | (df["pscientist gender"] == "f")]
df=df[(df["ppscientist gender"] == "m") | (df["ppscientist gender"] == "f")]
####for m/f count specifically, have to remove lines with idk and both
df_sia=df[["Subjects",'scientist gender','pscientist gender','ppscientist gender']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_gender_melt_f.csv") 
'''
df_sia=df[["Subjects",'Pre SK','Post SK','PostPost SK']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_SK_melt_f.csv") 
'''
df_sia=df[["Subjects",'Pre PC','Post PC','PostPost PC']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_PC_melt_f.csv") 

df_sia=df[["Subjects",'Pre SR','Post SR','PostPost SR']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_SR_melt_f.csv") 

df_sia=df[["Subjects",'Pre SK','Post SK','PostPost SK']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_SK_melt_f.csv") 

df_sia=df[["Subjects",'Pre ST','Post ST','PostPost ST']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_ST_melt_f.csv") 
'''
#use following section of code if doing a chi2 analysis in which you need binary answers, all entries without a postpost response dropped 
'''
#remove schools with no post-post data
df=df[df["School "] != "Patterson"]
df=df[df["School "] != "Patterson "]
df=df[df["School "] != "CTA"]
df=df[df["Subjects"] != "H2 (drawings averaged) "]
df=df[df["Subjects"] != "H3 (drawings averaged) "]
df=df[df["Subjects"] != "H5 (drawings averaged) "]
df=df[df["Subjects"] != "H3 (drawings averaged)"]
df=df[df["Subjects"] != "H5 (drawings averaged)"]
df=df[df["Subjects"] != "H5(drawings averaged)"]

#remove single entries without post-post data
df=df[df["pplab coat"] != "no secondary post data "]
#if one entry has a both or idk instead of m/f delete all entries of it 
df=df[(df["scientist gender"] == "m") | (df["scientist gender"] == "f")]
df=df[(df["pscientist gender"] == "m") | (df["pscientist gender"] == "f")]
df=df[(df["ppscientist gender"] == "m") | (df["ppscientist gender"] == "f")]
####for m/f count specifically, have to remove lines with idk and both
df_sia=df[["Subjects",'scientist gender','pscientist gender','ppscientist gender']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_gender_melt.csv") 

####for general characteristics 
df_sia=df[["Subjects",'lab coat','plab coat','pplab coat']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_labcoat_melt.csv") 
'''

###################nothing below this line used for analysis - exported to R 
'''
#statistics for DAST categorical valvues 
#len() function does not skip NA values but aggregate functions like .mean .std .sem do, so no worries,=
#changed len function to count for accurate N calculation
print("Personal Characteristics")
print("Pre PC Descriptive Statistics")
lengthx=(df['Pre PC'].count()) 
mean1=(df['Pre PC'].mean())
sd1=(df['Pre PC'].std())
sem1=(df['Pre PC'].sem())
print("N:", lengthx, "Mean:", mean1, "SD:", sd1, "SE:", sem1)

print("Post PC Descriptive Statistics")
lengthx=(df['Post PC'].count())
mean2=(df['Post PC'].mean())
sd2=(df['Post PC'].std())
sem2=(df['Post PC'].sem())
print("N:", lengthx, "Mean:", mean2, "SD:", sd2, "SE:", sem2)

print(scipy.stats.mannwhitneyu(df['Pre PC'], df['Post PC']))
cohens_pc = (   (df['Pre PC'].mean()) - (df['Post PC'].mean()) )/ (  np.sqrt( ((df['Pre PC'].std()) ** 2) + (df['Post PC'].std()) ** 2) / 2)
print("Cohen's D PC", cohens_pc)

df_sia=df[["Subjects",'Pre PC','Post PC','PostPost PC']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_PC_melt.csv") 


print("Symbols of Research")
print("Pre SR Descriptive Statistics")
lengthx=(df['Pre SR']).count() 
meann1=(df['Pre SR'].mean())
sdd1=(df['Pre SR'].std())
semm1=(df['Pre SR'].sem())
print("N:", lengthx, "Mean:", meann1, "SD:", sdd1, "SE:", semm1)

print("Post SR Descriptive Statistics")
lengthx=(df['Post SR']).count()
meann2=(df['Post SR'].mean())
sdd2=(df['Post SR'].std())
semm2=(df['Post SR'].sem())
print("N:", lengthx, "Mean:", meann2, "SD:", sdd2, "SE:", semm2)

print(scipy.stats.mannwhitneyu(df['Pre SR'], df['Post SR']))
cohens_pc = (   (df['Pre SR'].mean()) - (df['Post SR'].mean()) )/ (  np.sqrt( ((df['Pre SR'].std()) ** 2) + (df['Post SR'].std()) ** 2) / 2)
print("Cohen's D SR", cohens_pc)

df_sia=df[["Subjects",'Pre SR','Post SR','PostPost SR']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_SR_melt.csv") 


print("Symbols of Knowledge")
print("Pre SK Descriptive Statistics")
lengthx=(df['Pre SK']).count() 
meannn1=(df['Pre SK'].mean())
sddd1=(df['Pre SK'].std())
semmm1=(df['Pre SK'].sem())
print("N:", lengthx, "Mean:", meannn1, "SD:", sddd1, "SE:", semmm1)

print("Post SK Descriptive Statistics")
lengthx=(df['Post SK']).count() 
meannn2=(df['Post SK'].mean())
sddd2=(df['Post SK'].std())
semmm2=(df['Post SK'].sem())
print("N:", lengthx, "Mean:", meannn2, "SD:", sddd2, "SE:", semmm2)
print(scipy.stats.mannwhitneyu(df['Pre SK'], df['Post SK']))
cohens_pc = (   (df['Pre SK'].mean()) - (df['Post SK'].mean()) )/ (  np.sqrt( ((df['Pre SK'].std()) ** 2) + (df['Post SK'].std()) ** 2) / 2)
print("Cohen's D SK", cohens_pc)

df_sia=df[["Subjects",'Pre SK','Post SK','PostPost SK']]
df_sia_melt=pd.melt(df_sia, id_vars=["Subjects"], var_name="condition", value_name="score")
df_sia_melt.to_csv("df_SK_melt.csv") 

print("Signs of Technology") 
print("Pre ST Descriptive Statistics")
lengthx=(df['Pre ST']).count()
meannnn1=(df['Pre ST'].mean())
sdddd1=(df['Pre ST'].std())
semmmm1=(df['Pre ST'].sem())
print("N:", lengthx, "Mean:", meannnn1, "SD:", sdddd1, "SE:", semmmm1)

print("Post ST Descriptive Statistics")
lengthx=(df['Post ST']).count()
meannnn2=(df['Post ST'].mean())
sdddd2=(df['Post ST'].std())
semmmm2=(df['Post ST'].sem())
print("N:", lengthx, "Mean:", meannnn2, "SD:", sdddd2, "SE:", semmmm2)

print(scipy.stats.mannwhitneyu(df['Pre ST'], df['Post ST']))
cohens_pc = (   (df['Pre ST'].mean()) - (df['Post ST'].mean()) )/ (  np.sqrt( ((df['Pre ST'].std()) ** 2) + (df['Post ST'].std()) ** 2) / 2)
print("Cohen's D ST", cohens_pc)
'''
'''
#df.to_csv("DAST_all.csv")
#bar graph comparing means of DAST categorical values 

mns_pre=(mean1, meann1, meannn1, meannnn1)
mns_post=(mean2, meann2, meannn2, meannnn2)

std_pre=(sem1, semm1, semmm1,semmmm1)
std_post=(sem2, semm2, semmm2, semmmm2)

N=4
ind = np.arange(N)  # the x locations for the group

width=0.35
fig, ax = plt.subplots()
rects1 = ax.bar(ind, mns_pre, width, color='r', yerr=std_pre)

rects2 = ax.bar(ind + width, mns_post, width, color='y', yerr=std_post)

# add some text for labels, title and axes ticks
ax.set_ylabel('Categorical Score')
ax.set_title('DAST Categorical Scores Pre and Post')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('Personal Characteristics', 'Symbols of Research', 'Symbols of Knowledge', 'Symbols of Technology'))
plt.xticks(rotation=45)
fig.savefig('DAST_cat.png', bbox_inches='tight')
ax.legend((rects1[0], rects2[0]), ('Pre', 'Post'))
#https://matplotlib.org/examples/api/barchart_demo.html
#https://onlinecourses.science.psu.edu/stat500/node/55

#plt.show()


#for pie charts have to manually change pre and post, for sig stats both present 
#pie chart for scientist gender

females=0
males=0

for x in df["pscientist gender"]: 
    if x=="m" or x=="M":
        males +=1 
    if x=="f" or x=="F":
        females +=1 

fem=(females)/(df["pscientist gender"]).count()*100
mem=(males)/(df["pscientist gender"]).count()*100
print(fem)
print(mem)

leftover=100 - (mem + fem)
labels = ("Female", "Male", "Ambiguous") 
sizes = [fem, mem, leftover]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('DAST Post Gender Depiction Ratios')
fig1.savefig('DAST_postgender.png', bbox_inches='tight')
#plt.show()

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

###racial demographics pie chart 

df_new=df[df['pscientist race'].notnull()]
a=df_new['pscientist race'].values.tolist()
b=split1(a)
c=split2(b)

unknown=0
white=0
hispanic=0
asian=0
africanamerican=0

for x in c: 
    if x=="don't know":
        unknown +=1 
    if x=="white":
        white +=1
    if x=="asian" or x=="Asian":
        asian +=1
    if x=="hispanic" or x=="Hispanic":
        hispanic +=1
    if x=="african-american" or x=="African american" or x== "African American" or x== "African-american" or x== "Black or african american":
        africanamerican +=1
    else: 
        pass 

r=(unknown)/(df["pscientist race"]).count() * 100
w=(white)/(df["pscientist race"]).count() *100 
a=(asian)/(df["pscientist race"]).count() *100 
h=(hispanic)/(df["pscientist race"]).count() *100 
aa=(africanamerican)/(df["pscientist race"]).count() *100 

sizes = [r,w,a,h,aa]

labelz = ("Ambiguous", "White", "Asian", "Hispanic","African-American")

patches, texts = plt.pie(sizes, startangle=90, radius=1.2)
labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labelz, sizes)]

sort_legend = True
if sort_legend:
    patches, labels, dummy =  zip(*sorted(zip(patches, labels, sizes),
                                          key=lambda x: x[2],
                                          reverse=True))

plt.legend(patches, labels, fontsize=10)
plt.title("DAST Post Race Depiction Ratios")
plt.savefig('DAST_postrace.png', bbox_inches='tight')           


###scientist depiction categories pie chart
df_new=df[df['poverall appearance of scientist'].notnull()]
a=df_new['poverall appearance of scientist'].values.tolist()
b=split1(a)
c=split2(b)

E=0
N=0
P=0
S=0

for x in c: 
    if x=="E" or x=="e":
        E +=1 
    if x=="N" or x=="n":
        N +=1 
    if x=="S" or x=="s":
        S +=1 
    if x=="P" or x=="p":
        P +=1 
    else:
        pass
        
r=(E)/(df["poverall appearance of scientist"]).count() * 100
w=(S)/(df["poverall appearance of scientist"]).count() *100 
a=(P)/(df["poverall appearance of scientist"]).count() *100 
h=(N)/(df["poverall appearance of scientist"]).count() *100 

sizes=[r,w,a,h]

labels=("Eccentric", "Sinister", "Positive", "Neutral") 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('DAST Post Overall Appearance of Scientist Ratios')
plt.savefig('DAST_postapp.png', bbox_inches='tight')
#plt.show()

#Overall appearance of scientits signifigance stats
df_new=df[df['overall appearance of scientist'].notnull()]
a=df_new['overall appearance of scientist'].values.tolist()
b=split1(a)
c=split2(b)

E1=0
N1=0
P1=0
S1=0

for x in c: 
    if x=="E" or x=="e":
        E1 +=1 
    if x=="N" or x=="n":
        N1 +=1 
    if x=="S" or x=="s":
        S1 +=1 
    if x=="P" or x=="p":
        P1 +=1 
    else:
        pass
E2=0
N2=0
P2=0
S2=0        

df_new=df[df['poverall appearance of scientist'].notnull()]
a=df_new['poverall appearance of scientist'].values.tolist()
b=split1(a)
c=split2(b)

for x in c: 
    if x=="E" or x=="e":
        E2 +=1 
    if x=="N" or x=="n":
        N2 +=1 
    if x=="S" or x=="s":
        S2 +=1 
    if x=="P" or x=="p":
        P2 +=1 
    else:
        pass
        
n1=(df["overall appearance of scientist"]).count()
n2=(df["poverall appearance of scientist"]).count()

#counts=(E of pre test, E of post test)
#nobs=(n samples of pre test, n samples of post test)
#E value
counts=(E1, E2)
nobs=(n1, n2)
print(counts)
print(nobs)
stat, pval = proportions_ztest(counts, nobs)
r=('{0:0.3f}'.format(pval))
print("Signifigance for DAST E Category:", r) 

#N value
counts=(N1, N2)
nobs=(n1, n2)

stat, pval = proportions_ztest(counts, nobs)
r=('{0:0.3f}'.format(pval))
print("Signifigance for DAST N Category:", r) 

#P value
counts=(P1, P2)
nobs=(n1, n2)

stat, pval = proportions_ztest(counts, nobs)
r=('{0:0.3f}'.format(pval))
print("Signifigance for DAST P Category:", r) 

#S value
counts=(S1, S2)
nobs=(n1, n2)

stat, pval = proportions_ztest(counts, nobs)
r=('{0:0.3f}'.format(pval))
print("Signifigance for DAST S Category:", r) 

###Signifigance for racial cateories
df_new=df[df['scientist race'].notnull()] 
a=df_new['scientist race'].values.tolist()
b=split1(a)
c=split2(b)

unknown1=0
white1=0
hispanic1=0
asian1=0
africanamerican1=0

for x in c: 
    if x=="don't know":
        unknown1 +=1 
    if x=="white":
        white1 +=1
    if x=="asian" or x=="Asian":
        asian1 +=1
    if x=="hispanic" or x=="Hispanic":
        hispanic1 +=1
    if x=="african-american" or x=="African american" or x== "African American" or x== "African-american" or x== "Black or african american":
        africanamerican1 +=1
    else: 
        pass

unknown2=0
white2=0
hispanic2=0
asian2=0
africanamerican2=0
df_new=df[df['pscientist race'].notnull()]
a=df_new['pscientist race'].values.tolist()
b=split1(a)
c=split2(b)

for x in c: 
    if x=="don't know":
        unknown2 +=1 
    if x=="white":
        white2 +=1
    if x=="asian" or x=="Asian":
        asian2 +=1
    if x=="hispanic" or x=="Hispanic":
        hispanic2 +=1
    if x=="african-american" or x=="African american" or x== "African American" or x== "African-american" or x== "Black or african american":
        africanamerican2 +=1
    else: 
        pass
        
n1=(df["scientist race"]).count()
n2=(df["pscientist race"]).count()

#counts=(E of pre test, E of post test)
#nobs=(n samples of pre test, n samples of post test)
#unknown value
counts=(unknown1, unknown2)
nobs=(n1, n2)

stat, pval = proportions_ztest(counts, nobs)
r=('{0:0.3f}'.format(pval))
print("Signifigance for DAST Race Category Ambiguous:", r) 

#N value
counts=(asian1, asian2)
nobs=(n1, n2)

stat, pval = proportions_ztest(counts, nobs)
r=('{0:0.3f}'.format(pval))
print("Signifigance for DAST Race Category Asian:", r) 

#P value
counts=(hispanic1, hispanic2)
nobs=(n1, n2)

stat, pval = proportions_ztest(counts, nobs)
r=('{0:0.3f}'.format(pval))
print("Signifigance for DAST Race Category Hispanic:", r) 

#S value
counts=(white1, white2)
nobs=(n1, n2)

stat, pval = proportions_ztest(counts, nobs)
r=('{0:0.3f}'.format(pval))
print("Signifigance for DAST Race Category White:", r)

#S value
counts=(africanamerican1, africanamerican2)
nobs=(n1, n2)

stat, pval = proportions_ztest(counts, nobs)
r=('{0:0.3f}'.format(pval))
print("Signifigance for DAST Race Category African-American:", r) 

###Signifigance of gender categories

females1=0
males1=0

for x in df["scientist gender"]:  
    if x=="m" or x=="M":
        males1 +=1 
    if x=="f" or x=="F":
        females1 +=1 

females2=0
males2=0

for x in df["pscientist gender"]: 
    if x=="m" or x=="M":
        males2 +=1 
    if x=="f" or x=="F":
        females2 +=1 
        
n1=(df["scientist gender"]).count()
n2=(df["pscientist gender"]).count()
        
counts=(females1, females2)
nobs=(n1, n2)

stat, pval = proportions_ztest(counts, nobs)
r=('{0:0.3f}'.format(pval))

print("Signifigance for DAST Gender Category Women:", r) 

counts=(males1, males2)
nobs=(n1, n2)

stat, pval = proportions_ztest(counts, nobs)
r=('{0:0.3f}'.format(pval))

print("Signifigance for DAST Gender Category Men:", r)

'''
