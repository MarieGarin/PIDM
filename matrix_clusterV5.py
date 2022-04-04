import scipy.stats
import pandas as pd
all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_human_GL.csv', header=0, index_col=0) 

import seaborn as sns
import matplotlib.pyplot as plt
#f, ax = plt.subplots(figsize=(7, 5))
#ax = sns.heatmap(corr, mask=mask, square=True, vmax=.3, square=True)

masktranspose = all_data_clean_transpose.notna()
all_data_clean_transpose.set_axis(all_data_clean_transpose.index, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.dropna(how = 'all')
orwname = list(all_data_clean_transpose.index)

all_data_clean_transpose = all_data_clean_transpose[orwname]
rownameclean = []
for string in orwname:
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean.append(new_string)

all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose_mean_index = all_data_clean_transpose.mean(axis=1).sort_values(ascending=False).index
all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))

orwname = list(all_data_clean_transpose.index)
rownameclean = []
for string in orwname:
    rownameclean.append(string)

score_pos = pd.DataFrame()
score_neg = pd.DataFrame()
for region in rownameclean:
    mask1 = all_data_clean_transpose.loc[region, :]>0
    mask2 = all_data_clean_transpose.loc[region, :]<0
    if mask1.sum() > mask2.sum():
        CACA = pd.DataFrame([mask1.sum()], index=[region])
        score_pos = score_pos.append(CACA)
    elif mask1.sum() <= mask2.sum():
        CACA = pd.DataFrame([mask2.sum()], index=[region])
        score_neg = score_neg.append(CACA)
    else:
        print(mask1.sum())
        print(mask2.sum())

good_order = score_pos.sort_values(by=0, ascending=False).append(score_neg.sort_values(by=0, ascending=True))

rownameclean = list(good_order.index)

newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)

mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

# xticklabels=False,
plt.close('all')
with sns.axes_style('darkgrid'):
	plt.figure(figsize=(25, 25))
	sns.set(font_scale=3, rc={'font.weight':'normal'})
	ax = sns.heatmap(newmatrix, cmap="bwr", vmin=-3, vmax=3, mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=True,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('blue')
plt.savefig("testspeices.png", dpi=400, bbox_inches='tight')

###################################


all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_slope_GL.csv', header=0, index_col=0)

all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

# xticklabels=False,
plt.close('all')
with sns.axes_style('darkgrid'):
	plt.figure(figsize=(25, 25))
	sns.set(font_scale=3, rc={'font.weight':'normal'})
	ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('blue')
    text =  lab.get_text()
plt.savefig("testspeices_GL_Matrix_slope.png", dpi=400, bbox_inches='tight')



###################################


all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_lambda_GL.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]

all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

# xticklabels=False,
plt.close('all')
with sns.axes_style('darkgrid'):
	plt.figure(figsize=(25, 25))
	sns.set(font_scale=3, rc={'font.weight':'normal'})
	ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('blue')
plt.savefig("testspeices_GL_Matrix_lambda.png", dpi=400, bbox_inches='tight')



###################################


all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_intercept_GL.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

# xticklabels=False,
plt.close('all')
with sns.axes_style('darkgrid'):
	plt.figure(figsize=(25, 25))
	sns.set(font_scale=3, rc={'font.weight':'normal'})
	ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('blue')
plt.savefig("testspeices_GL_Matrix_intercept.png", dpi=400, bbox_inches='tight')


####################################################################################################BN


import scipy.stats
import pandas as pd
all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_human_BN.csv', header=0, index_col=0) 
masktranspose = all_data_clean_transpose.notna()
import seaborn as sns
import matplotlib.pyplot as plt
#f, ax = plt.subplots(figsize=(7, 5))
#ax = sns.heatmap(corr, mask=mask, square=True, vmax=.3, square=True)

all_data_clean_transpose.set_axis(all_data_clean_transpose.index, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.dropna(how = 'all')
orwname = list(all_data_clean_transpose.index)

all_data_clean_transpose = all_data_clean_transpose[orwname]
rownameclean = []
for string in orwname:
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean.append(new_string)

all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose_mean_index = all_data_clean_transpose.mean(axis=1).sort_values(ascending=False).index
all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))

orwname = list(all_data_clean_transpose.index)
rownameclean = []
for string in orwname:
    rownameclean.append(string)

score_pos = pd.DataFrame()
score_neg = pd.DataFrame()
for region in rownameclean:
    mask1 = all_data_clean_transpose.loc[region, :]>0
    mask2 = all_data_clean_transpose.loc[region, :]<0
    if mask1.sum() > mask2.sum():
        CACA = pd.DataFrame([mask1.sum()], index=[region])
        score_pos = score_pos.append(CACA)
    elif mask1.sum() <= mask2.sum():
        CACA = pd.DataFrame([mask2.sum()], index=[region])
        score_neg = score_neg.append(CACA)
    else:
        print(mask1.sum())
        print(mask2.sum())


good_order = score_pos.sort_values(by=0, ascending=False).append(score_neg.sort_values(by=0, ascending=True))

rownameclean = list(good_order.index)

newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)

mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

# xticklabels=False,
plt.close('all')
with sns.axes_style('darkgrid'):
	plt.figure(figsize=(30, 30))
	sns.set(font_scale=3, rc={'font.weight':'normal'})
	ax = sns.heatmap(newmatrix, cmap="bwr", vmin=-3, vmax=3, mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=True,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('blue')
plt.savefig("testspeices_BN.png", dpi=400, bbox_inches='tight')





all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_slope_BN.csv', header=0, index_col=0)
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

# xticklabels=False,
plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=3, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('blue')
plt.savefig("testspeices_BN_Matrix_slope.png", dpi=400, bbox_inches='tight')



all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_lambda_BN.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

# xticklabels=False,
plt.close('all')
with sns.axes_style('darkgrid'):
	plt.figure(figsize=(30, 30))
	sns.set(font_scale=3, rc={'font.weight':'normal'})
	ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('blue')
plt.savefig("testspeices_BN_Matrix_lambda.png", dpi=400, bbox_inches='tight')




all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_intercept_BN.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

# xticklabels=False,
plt.close('all')
with sns.axes_style('darkgrid'):
	plt.figure(figsize=(30, 30))
	sns.set(font_scale=3, rc={'font.weight':'normal'})
	ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('blue')
plt.savefig("testspeices_BN_Matrix_intercept.png", dpi=400, bbox_inches='tight')

####################################################################################################BA2


import scipy.stats
import pandas as pd
all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_human_BA2.csv', header=0, index_col=0) 
masktranspose = all_data_clean_transpose.notna()

import seaborn as sns
import matplotlib.pyplot as plt
#f, ax = plt.subplots(figsize=(7, 5))
#ax = sns.heatmap(corr, mask=mask, square=True, vmax=.3, square=True)

all_data_clean_transpose.set_axis(all_data_clean_transpose.index, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.dropna(how = 'all')
orwname = list(all_data_clean_transpose.index)

all_data_clean_transpose = all_data_clean_transpose[orwname]
rownameclean = []
for string in orwname:
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean.append(new_string)

all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose_mean_index = all_data_clean_transpose.mean(axis=1).sort_values(ascending=False).index
all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))

orwname = list(all_data_clean_transpose.index)
rownameclean = []
for string in orwname:
    rownameclean.append(string)

score_pos = pd.DataFrame()
score_neg = pd.DataFrame()
for region in rownameclean:
    mask1 = all_data_clean_transpose.loc[region, :]>0
    mask2 = all_data_clean_transpose.loc[region, :]<0
    if mask1.sum() > mask2.sum():
        CACA = pd.DataFrame([mask1.sum()], index=[region])
        score_pos = score_pos.append(CACA)
    elif mask1.sum() <= mask2.sum():
        CACA = pd.DataFrame([mask2.sum()], index=[region])
        score_neg = score_neg.append(CACA)
    else:
        print(mask1.sum())
        print(mask2.sum())


good_order = score_pos.sort_values(by=0, ascending=False).append(score_neg.sort_values(by=0, ascending=True))

rownameclean = list(good_order.index)

newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)

mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(25, 25))
    sns.set(font_scale=3, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", vmin=-3, vmax=3, mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=True,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('blue')
plt.savefig("testspeices_BA2.png", dpi=400, bbox_inches='tight')




all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_slope_BA2.csv', header=0, index_col=0)
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

# xticklabels=False,
plt.close('all')
with sns.axes_style('darkgrid'):
	plt.figure(figsize=(25, 25))
	sns.set(font_scale=3, rc={'font.weight':'normal'})
	ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('blue')
plt.savefig("testspeices_BA2_Matrix_slope.png", dpi=400, bbox_inches='tight')



all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_lambda_BA2.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

# xticklabels=False,
plt.close('all')
with sns.axes_style('darkgrid'):
	plt.figure(figsize=(25, 25))
	sns.set(font_scale=3, rc={'font.weight':'normal'})
	ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('blue')
plt.savefig("testspeices_BA2_Matrix_lambda.png", dpi=400, bbox_inches='tight')




all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_intercept_BA2.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

# xticklabels=False,
plt.close('all')
with sns.axes_style('darkgrid'):
	plt.figure(figsize=(25, 25))
	sns.set(font_scale=3, rc={'font.weight':'normal'})
	ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('blue')
plt.savefig("testspeices_BA2_Matrix_intercept.png", dpi=400, bbox_inches='tight')


####################################################################################################Chimpanzee


import scipy.stats
import pandas as pd
all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_chimanzee2.csv', header=0, index_col=0) 
masktranspose = all_data_clean_transpose.notna()

import seaborn as sns
import matplotlib.pyplot as plt
#f, ax = plt.subplots(figsize=(7, 5))
#ax = sns.heatmap(corr, mask=mask, square=True, vmax=.3, square=True)

all_data_clean_transpose.set_axis(all_data_clean_transpose.index, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.dropna(how = 'all')
orwname = list(all_data_clean_transpose.index)

all_data_clean_transpose = all_data_clean_transpose[orwname]
rownameclean = []
for string in orwname:
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean.append(new_string)

all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose_mean_index = all_data_clean_transpose.mean(axis=1).sort_values(ascending=False).index
all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))

orwname = list(all_data_clean_transpose.index)
rownameclean = []
for string in orwname:
    rownameclean.append(string)

score_pos = pd.DataFrame()
score_neg = pd.DataFrame()
for region in rownameclean:
    mask1 = all_data_clean_transpose.loc[region, :]>0
    mask2 = all_data_clean_transpose.loc[region, :]<0
    if mask1.sum() > mask2.sum():
        CACA = pd.DataFrame([mask1.sum()], index=[region])
        score_pos = score_pos.append(CACA)
    elif mask1.sum() <= mask2.sum():
        CACA = pd.DataFrame([mask2.sum()], index=[region])
        score_neg = score_neg.append(CACA)
    else:
        print(mask1.sum())
        print(mask2.sum())


good_order = score_pos.sort_values(by=0, ascending=False).append(score_neg.sort_values(by=0, ascending=True))

rownameclean = list(good_order.index)

newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)

mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(33, 33))
    sns.set(font_scale=3, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", vmin=-3, vmax=3, mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=True,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('blue')
plt.savefig("testspeices_Matrix_chimanzee2.png", dpi=400, bbox_inches='tight')




all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_slope_chimanzee.csv', header=0, index_col=0)
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

# xticklabels=False,
plt.close('all')
with sns.axes_style('darkgrid'):
	plt.figure(figsize=(34, 34))
	sns.set(font_scale=3, rc={'font.weight':'normal'})
	ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('blue')
plt.savefig("testspeices_chimanzee_Matrix_slope.png", dpi=400, bbox_inches='tight')



all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_lambda_chimanzee.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

# xticklabels=False,
plt.close('all')
with sns.axes_style('darkgrid'):
	plt.figure(figsize=(34, 34))
	sns.set(font_scale=3, rc={'font.weight':'normal'})
	ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('blue')
plt.savefig("testspeices_chimanzee_Matrix_lambda.png", dpi=400, bbox_inches='tight')




all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_intercept_chimanzee.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

# xticklabels=False,
plt.close('all')
with sns.axes_style('darkgrid'):
	plt.figure(figsize=(34, 34))
	sns.set(font_scale=3, rc={'font.weight':'normal'})
	ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('blue')
plt.savefig("testspeices_chimanzee_Matrix_intercept.png", dpi=400, bbox_inches='tight')





####################################################################################################Macaque


import scipy.stats
import pandas as pd
all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_Macaque2.csv', header=0, index_col=0) 
masktranspose = all_data_clean_transpose.notna()

import seaborn as sns
import matplotlib.pyplot as plt
#f, ax = plt.subplots(figsize=(7, 5))
#ax = sns.heatmap(corr, mask=mask, square=True, vmax=.3, square=True)

all_data_clean_transpose.set_axis(all_data_clean_transpose.index, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.dropna(how = 'all')
orwname = list(all_data_clean_transpose.index)

all_data_clean_transpose = all_data_clean_transpose[orwname]


rownameclean = []
for string in orwname:
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean.append(new_string)

all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose_mean_index = all_data_clean_transpose.mean(axis=1).sort_values(ascending=False).index
all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))

orwname = list(all_data_clean_transpose.index)
rownameclean = []
for string in orwname:
    rownameclean.append(string)

score_pos = pd.DataFrame()
score_neg = pd.DataFrame()
for region in rownameclean:
    mask1 = all_data_clean_transpose.loc[region, :]>0
    mask2 = all_data_clean_transpose.loc[region, :]<0
    if mask1.sum() > mask2.sum():
        CACA = pd.DataFrame([mask1.sum()], index=[region])
        score_pos = score_pos.append(CACA)
    elif mask1.sum() <= mask2.sum():
        CACA = pd.DataFrame([mask2.sum()], index=[region])
        score_neg = score_neg.append(CACA)
    else:
        print(mask1.sum())
        print(mask2.sum())


good_order = score_pos.sort_values(by=0, ascending=False).append(score_neg.sort_values(by=0, ascending=True))

rownameclean = list(good_order.index)

newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)

mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(25, 25))
    sns.set(font_scale=2, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", vmin=-3, vmax=3, mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=True,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('blue')
plt.savefig("testspeices_Matrix_Macaque2.png", dpi=400, bbox_inches='tight')




all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_slope_Macaque.csv', header=0, index_col=0)
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=2, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('blue')
plt.savefig("testspeices_Macaque_Matrix_slope.png", dpi=400, bbox_inches='tight')



all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_lambda_Macaque.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=2, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('blue')
plt.savefig("testspeices_Macaque_Matrix_lambda.png", dpi=400, bbox_inches='tight')




all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_intercept_Macaque.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=2, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('blue')
plt.savefig("testspeices_Macaque_Matrix_intercept.png", dpi=400, bbox_inches='tight')


####################################################################################################Vervet


import scipy.stats
import pandas as pd
all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_Vervet2.csv', header=0, index_col=0) 
masktranspose = all_data_clean_transpose.notna()

import seaborn as sns
import matplotlib.pyplot as plt
#f, ax = plt.subplots(figsize=(7, 5))
#ax = sns.heatmap(corr, mask=mask, square=True, vmax=.3, square=True)

all_data_clean_transpose.set_axis(all_data_clean_transpose.index, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.dropna(how = 'all')
orwname = list(all_data_clean_transpose.index)

all_data_clean_transpose = all_data_clean_transpose[orwname]


rownameclean = []
for string in orwname:
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean.append(new_string)

all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose_mean_index = all_data_clean_transpose.mean(axis=1).sort_values(ascending=False).index
all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))

orwname = list(all_data_clean_transpose.index)
rownameclean = []
for string in orwname:
    rownameclean.append(string)

score_pos = pd.DataFrame()
score_neg = pd.DataFrame()
for region in rownameclean:
    mask1 = all_data_clean_transpose.loc[region, :]>0
    mask2 = all_data_clean_transpose.loc[region, :]<0
    if mask1.sum() > mask2.sum():
        CACA = pd.DataFrame([mask1.sum()], index=[region])
        score_pos = score_pos.append(CACA)
    elif mask1.sum() <= mask2.sum():
        CACA = pd.DataFrame([mask2.sum()], index=[region])
        score_neg = score_neg.append(CACA)
    else:
        print(mask1.sum())
        print(mask2.sum())


good_order = score_pos.sort_values(by=0, ascending=False).append(score_neg.sort_values(by=0, ascending=True))

rownameclean = list(good_order.index)

newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)

mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(25, 25))
    sns.set(font_scale=2, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", vmin=-3, vmax=3, mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=True,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('blue')
plt.savefig("testspeices_Matrix_Vervet2.png", dpi=400, bbox_inches='tight')




all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_slope_Vervet.csv', header=0, index_col=0)
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=2, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('blue')
plt.savefig("testspeices_Vervet_Matrix_slope.png", dpi=400, bbox_inches='tight')



all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_lambda_Vervet.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=2, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('blue')
plt.savefig("testspeices_Vervet_Matrix_lambda.png", dpi=400, bbox_inches='tight')




all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_intercept_Vervet.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=2, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(27)
        lab.set_color('blue')
plt.savefig("testspeices_Macaque_Vervet_intercept.png", dpi=400, bbox_inches='tight')


####################################################################################################Marmoset


import scipy.stats
import pandas as pd
all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_Marmoset2.csv', header=0, index_col=0) 
masktranspose = all_data_clean_transpose.notna()

import seaborn as sns
import matplotlib.pyplot as plt
#f, ax = plt.subplots(figsize=(7, 5))
#ax = sns.heatmap(corr, mask=mask, square=True, vmax=.3, square=True)

all_data_clean_transpose.set_axis(all_data_clean_transpose.index, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.dropna(how = 'all')
orwname = list(all_data_clean_transpose.index)

all_data_clean_transpose = all_data_clean_transpose[orwname]


rownameclean = []
for string in orwname:
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean.append(new_string)

all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose_mean_index = all_data_clean_transpose.mean(axis=1).sort_values(ascending=False).index
all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))

orwname = list(all_data_clean_transpose.index)
rownameclean = []
for string in orwname:
    rownameclean.append(string)

score_pos = pd.DataFrame()
score_neg = pd.DataFrame()
for region in rownameclean:
    mask1 = all_data_clean_transpose.loc[region, :]>0
    mask2 = all_data_clean_transpose.loc[region, :]<0
    if mask1.sum() > mask2.sum():
        CACA = pd.DataFrame([mask1.sum()], index=[region])
        score_pos = score_pos.append(CACA)
    elif mask1.sum() <= mask2.sum():
        CACA = pd.DataFrame([mask2.sum()], index=[region])
        score_neg = score_neg.append(CACA)
    else:
        print(mask1.sum())
        print(mask2.sum())


good_order = score_pos.sort_values(by=0, ascending=False).append(score_neg.sort_values(by=0, ascending=True))

rownameclean = list(good_order.index)

newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)

mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=3, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", vmin=-3, vmax=3, mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=True,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('blue')
plt.savefig("testspeices_Matrix_Marmoset2.png", dpi=400, bbox_inches='tight')




all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_slope_Marmoset.csv', header=0, index_col=0)
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=2, rc={'font.weight':'bold'})
    ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6},
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()
plt.savefig("testspeices_marmoset_Matrix_slope.png", dpi=400, bbox_inches='tight')



all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_lambda_Marmoset.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=3, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('blue')
plt.savefig("testspeices_marmoset_Matrix_lambda.png", dpi=400, bbox_inches='tight')




all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_intercept_Marmoset.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=3, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('blue')
plt.savefig("testspeices_marmoset_Matrix_intercept.png", dpi=400, bbox_inches='tight')


import scipy.stats
import pandas as pd
all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_Marmoset2_k5.csv', header=0, index_col=0) 
masktranspose = all_data_clean_transpose.notna()

import seaborn as sns
import matplotlib.pyplot as plt
#f, ax = plt.subplots(figsize=(7, 5))
#ax = sns.heatmap(corr, mask=mask, square=True, vmax=.3, square=True)

all_data_clean_transpose.set_axis(all_data_clean_transpose.index, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.dropna(how = 'all')
orwname = list(all_data_clean_transpose.index)

all_data_clean_transpose = all_data_clean_transpose[orwname]


rownameclean = []
for string in orwname:
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean.append(new_string)

all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose_mean_index = all_data_clean_transpose.mean(axis=1).sort_values(ascending=False).index
all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))

orwname = list(all_data_clean_transpose.index)
rownameclean = []
for string in orwname:
    rownameclean.append(string)

score_pos = pd.DataFrame()
score_neg = pd.DataFrame()
for region in rownameclean:
    mask1 = all_data_clean_transpose.loc[region, :]>0
    mask2 = all_data_clean_transpose.loc[region, :]<0
    if mask1.sum() > mask2.sum():
        CACA = pd.DataFrame([mask1.sum()], index=[region])
        score_pos = score_pos.append(CACA)
    elif mask1.sum() <= mask2.sum():
        CACA = pd.DataFrame([mask2.sum()], index=[region])
        score_neg = score_neg.append(CACA)
    else:
        print(mask1.sum())
        print(mask2.sum())


good_order = score_pos.sort_values(by=0, ascending=False).append(score_neg.sort_values(by=0, ascending=True))

rownameclean = list(good_order.index)

newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)

mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=3, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", vmin=-3, vmax=3, mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=True,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(35)
        lab.set_color('blue')
plt.savefig("testspeices_Matrix_Marmoset2_k5.png", dpi=400, bbox_inches='tight')

####################################################################################################Microcebe


import scipy.stats
import pandas as pd
all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_Microcebe2.csv', header=0, index_col=0) 
masktranspose = all_data_clean_transpose.notna()

import seaborn as sns
import matplotlib.pyplot as plt
#f, ax = plt.subplots(figsize=(7, 5))
#ax = sns.heatmap(corr, mask=mask, square=True, vmax=.3, square=True)

all_data_clean_transpose.set_axis(all_data_clean_transpose.index, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.dropna(how = 'all')
orwname = list(all_data_clean_transpose.index)

all_data_clean_transpose = all_data_clean_transpose[orwname]


rownameclean = []
for string in orwname:
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean.append(new_string)

all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose_mean_index = all_data_clean_transpose.mean(axis=1).sort_values(ascending=False).index
all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))

orwname = list(all_data_clean_transpose.index)
rownameclean = []
for string in orwname:
    rownameclean.append(string)

score_pos = pd.DataFrame()
score_neg = pd.DataFrame()
for region in rownameclean:
    mask1 = all_data_clean_transpose.loc[region, :]>0
    mask2 = all_data_clean_transpose.loc[region, :]<0
    if mask1.sum() > mask2.sum():
        CACA = pd.DataFrame([mask1.sum()], index=[region])
        score_pos = score_pos.append(CACA)
    elif mask1.sum() <= mask2.sum():
        CACA = pd.DataFrame([mask2.sum()], index=[region])
        score_neg = score_neg.append(CACA)
    else:
        print(mask1.sum())
        print(mask2.sum())


good_order = score_pos.sort_values(by=0, ascending=False).append(score_neg.sort_values(by=0, ascending=True))

rownameclean = list(good_order.index)

newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)

mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=3, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", vmin=-3, vmax=3, mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=True,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('blue')
plt.savefig("testspeices_Matrix_Microcebe2.png", dpi=400, bbox_inches='tight')




all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_slope_Microcebe.csv', header=0, index_col=0)
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=3, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('blue')
plt.savefig("testspeices_Microcebe_Matrix_slope.png", dpi=400, bbox_inches='tight')



all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_lambda_Microcebe.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=3, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('blue')
plt.savefig("testspeices_Microcebe_Matrix_lambda.png", dpi=400, bbox_inches='tight')




all_data_clean_transpose =  pd.read_csv('/home/cgarin/Matrix_intercept_Microcebe.csv', header=0, index_col=0) 
all_data_clean_transpose = all_data_clean_transpose.where(masktranspose)

rownameclean_all = []
for string in list(all_data_clean_transpose.index):
    new_string = string.replace(".", "/")
    new_string = new_string.replace("__", "-")
    new_string = new_string.replace("_", " ")
    rownameclean_all.append(new_string)

all_data_clean_transpose.set_axis(rownameclean_all, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean_all, axis=1, inplace=True)
all_data_clean_transpose = all_data_clean_transpose.loc[orwname]
all_data_clean_transpose = all_data_clean_transpose[orwname]


all_data_clean_transpose.set_axis(rownameclean, axis=0, inplace=True)
all_data_clean_transpose.set_axis(rownameclean, axis=1, inplace=True)

all_data_clean_transpose = all_data_clean_transpose.reindex(list(all_data_clean_transpose_mean_index))
all_data_clean_transpose = all_data_clean_transpose.reindex(columns=list(all_data_clean_transpose_mean_index))


newmatrix = all_data_clean_transpose.reindex(rownameclean)
newmatrix = newmatrix.reindex(columns=rownameclean)


mask = newmatrix.isnull()
newmatrix = newmatrix.fillna(int(0.000000))

plt.close('all')
with sns.axes_style('darkgrid'):
    plt.figure(figsize=(30, 30))
    sns.set(font_scale=3, rc={'font.weight':'normal'})
    ax = sns.heatmap(newmatrix, cmap="bwr", mask=mask, square=True, robust=False, center=0, cbar_kws={"shrink": .6}, annot=False,
            fmt='.1g',annot_kws={"size":13, "fontweight":"bold"})

for t in ax.texts:
    if float(t.get_text())>=0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    elif float(t.get_text())<=-0.00000000000000000000000000000000000000000001:
        t.set_text(t.get_text()) #if the value is greater than 0.4 then I set the text 
    else:
        t.set_text("") # if not it sets an empty text

# ADDED: Remove labels.
ax.set_ylabel('')    
ax.set_xlabel('')
plt.tight_layout()

for i, (lab, annot) in enumerate(zip(ax.get_yticklabels(), ax.texts)):
    totalnumber = len(ax.get_yticklabels())
    listfin = list(range(totalnumber))[:5]
    listfin2 = list(range(totalnumber))[-5:]
    if i in listfin: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('red')
    if i in listfin2: # lets highlight row 2
        # set the properties of the ticklabel
        lab.set_weight('bold')
        lab.set_size(40)
        lab.set_color('blue')
plt.savefig("testspeices_Microcebe_Matrix_intercept.png", dpi=400, bbox_inches='tight')
