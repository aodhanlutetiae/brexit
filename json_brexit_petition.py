
# coding: utf-8

# In[ ]:


# ********* GENERAL **********


# Location of website in question
# 
# https://petition.parliament.uk/petitions/235821

# In[ ]:


# TIME STAMP THE DOWNLOAD OF THE JSON DATA so you can compare them

# Monday 05.23 -- 1807 sigs
# Monday 14.12 -- 2045 sigs
# Tuesday 10.24 -- 2509 sigs


# JAVASCRIPT OBJECT NOTATION
# 
# json.load()
# -- load from a file
# 
# json.loads()
# -- load from a string - that's the S in loads
# 
# json.dump()
# -- output the file
# 
# json.dumps
# -- output the file as a string

# In[1]:


import json
import pandas as pd
from pandas.io.json import json_normalize #package for flattening json in pandas df

import matplotlib as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# IMPORTS FOR PLOTLY

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
init_notebook_mode(connected=True)

# Using plotly + cufflinks in offline mode
import cufflinks
cufflinks.go_offline(connected=True)
init_notebook_mode(connected=True)


# In[3]:


json_file = open ("/Users/aidanairuser/Desktop/petition_14.13_04022019.json", "r", encoding = "utf-8")


# In[4]:


pet = json.load (json_file)


# In[5]:


json_file.close()


# In[6]:


pet


# In[7]:


type (pet)

# so since it's a dictionary you access the info by key....


# In[8]:


# the main top level branch is 'data'

pet["data"]


# In[9]:


# the other top level branch (of 2)

pet ["links"]


# In[10]:


# how does a dictionary work again?

thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
x = thisdict["model"]
x


# In[ ]:


# ***** COUNTRIES WHERE PEOPLE ARE SIGNING *******


# In[11]:


#pull out part of the PET dictionary: drill down into PET/DATA/ATTRIBUTES to get to 
# SIGNATURES_BY_COUNTRY

sign = pet["data"]['attributes']['signatures_by_country']
sign


# In[12]:


# build a df from this info

sig_df = pd.DataFrame.from_dict(sign)


# In[13]:


sig_df.head(4)


# In[14]:


# check the total number of entries against the petition figure - 2045 on Monday afternoon

sig_df.signature_count.sum()


# In[15]:


# signatures from how many countries?

sig_df.name.count()


# In[16]:


# alternatively....

sig_df.shape


# In[17]:


sig_df = sig_df[['name', 'signature_count', 'code']]


# In[18]:


sig_df.rename(columns = {'signature_count':'signatures'}, inplace = True)
sig_df.rename(columns = {'name':'country'}, inplace = True)


# In[19]:


sig_df.sort_values(by = "signatures", ascending = False)


# In[20]:


sig_df2 = sig_df


# In[21]:


sig_df2.set_index("country",drop=True,inplace=True)


# In[22]:


# DROP ONE COLUMN 

sig_df2.drop('code', axis=1, inplace=True)


# In[23]:


sig_df2.sort_values(by = "signatures", ascending = False).head(10)


# In[24]:


sig_df2.sort_values(by = "signatures", ascending = False).head(10).plot(kind = 'barh')


# In[ ]:


# ****** MOVING ONTO CONSTITUENCIES *********


# In[25]:


# Drilling down to one top branch (data) then down to attributes then to sigs

const = pet["data"]['attributes']['signatures_by_constituency']
const


# In[26]:


con_df = pd.DataFrame.from_dict(const)


# In[27]:


con_df = con_df[['name', 'signature_count', 'ons_code', 'mp']]


# In[28]:


con_df.rename(columns = {'signature_count':'signatures'}, inplace = True)
con_df.rename(columns = {'name':'Constituency'}, inplace = True)


# In[29]:


con_df


# In[30]:


con_df.Constituency.shape

# so that's 585 constituencies out of the 650


# In[31]:


con_df.Constituency.count()

# that's out of 650 constituencies


# In[32]:


con_df.signatures.mean()

# with an average of just over three people signing per constituency.
# since the only requirement is to be British or UK-resident these numbers are out of 
# a very large pool.


# In[33]:


585 * 3.28


# In[34]:


con_df.signatures.value_counts().head()

# here we see there were 156 constituencies where 2 people signed,
# 130 where 3 people signed, etc.


# In[35]:


pulled = con_df[['Constituency', 'signatures']]

checking_df = pd.DataFrame(pulled)


# In[36]:


checking_df.signatures.sum()


# In[37]:


con_df.sort_values(by = "signatures", ascending = False)


# In[38]:


con_df.sort_values(by = "signatures", ascending = False).head(20)


# List of NI constituencies for info
# 
# Belfast East
# Belfast North
# Belfast South
# Belfast West
# East Antrim
# East Londonderry
# Fermanagh & South Tyrone
# Foyle
# Lagan Valley
# Mid Ulster
# Newry & Armagh
# North Antrim
# North Down
# South Antrim
# South Down
# Strangford
# Upper Bann
# West Tyrone

# In[39]:


con_df2 = con_df


# In[40]:


# can't rerun this code, obviously

con_df2.set_index("Constituency",drop=True,inplace=True)


# In[41]:


con_df2.sort_values(by = "signatures", ascending = False).head(20)


# In[42]:


con_df2.sort_values(by = "signatures", ascending = False).head(20).plot(kind = 'barh')

# if you plot this now it will have the highest bars on the bottom, not the top


# In[43]:


flipped = con_df2.sort_values(by = "signatures", ascending = False).head(20)
flipped2 = flipped.sort_values(by = "signatures", ascending = True)
flipped2.plot(kind = 'barh', figsize = (25, 14))


# In[44]:


flipped2.columns


# In[45]:


flipped2.drop('ons_code', axis=1, inplace=True)
flipped2.drop('mp', axis=1, inplace=True)


# In[46]:


flipped2.iplot(kind='barh', opacity = 1)


# In[ ]:


# NOTE Now GENERATE 'BREXITERS' BEFORE GOING ANY FURTHER


# In[ ]:


# **** SCRAPING RESULTS OF BREXIT VOTE IN NIRE *****


# In[49]:


# import, pull from url, print 'result', declare pulled as 'soup'

from bs4 import BeautifulSoup as bs
import requests
import re

url = ("https://en.wikipedia.org/wiki/Results_of_the_2016_United_Kingdom_European_Union_membership_referendum#Northern_Ireland")
results = requests.get(url)
print (results)
soup = bs(results.text, 'html.parser')


# In[50]:


soup


# In[51]:


# how many tables in this page?

len (soup('table'))


# In[52]:


# select the 18th table from the end

nire = soup.find_all("table")[-18]
print (nire)


# In[53]:


# how many rows in this selected table?

len (nire("tr"))


# In[54]:


# declare variable for all the rows found

rows = nire.findAll("tr")
rows


# In[55]:


# cycle through the cells

list_rows = []

for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)

print(clean2)


# In[56]:


# build pandas df from the rows collected

ni_df = pd.DataFrame(list_rows)
ni_df.head(3)


# In[57]:


# check what I've built ...

type (ni_df)


# In[58]:


# pull out from single column into several columns

nire_df = ni_df[0].str.split(',', expand=True)
nire = pd.DataFrame(nire_df)
nire.head(4)


# In[59]:


# check I've got a df

type (nire)


# In[60]:


# strip out the odd characters

nire[0] = nire[0].str.strip('[')
nire[7] = nire[7].str.strip(']')
nire[7] = nire[7].str.strip('\n')    


# In[61]:


nire.head(4)


# In[62]:


# drop the first two rows

nire.drop(nire.index[0: 2], inplace=True)
nire


# In[63]:


# declare column names

nire.columns = ["Constituency", "Voter_turnout", "Votes_remain_inK", "x", "Votes_leave_inK", "y", "Remain_pc", "Brexit vote (%)"]


# In[64]:


# drop two columns by name

nire.drop(['x', 'y'], axis=1, inplace=True)


# In[65]:


nire.head(4)


# In[66]:


# push 'constituency' column into the index column

nire.set_index("Constituency",drop=True,inplace=True)


# In[67]:


nire.head(4)


# In[68]:


nire.dtypes


# In[69]:


# changing the 'integers' into real integers

nire.Votes_remain_inK = nire.Votes_remain_inK.astype(int)
nire.Votes_leave_inK = nire.Votes_leave_inK.astype(int)


# In[70]:


# check they are now integers

nire.dtypes


# In[71]:


# strip out the % sign and convert Brexit vote results from string to float
# this means we can run a coefficient calculation on the two columns

nire["Brexit vote (%)"] = nire["Brexit vote (%)"].str.strip('%')
nire["Brexit vote (%)"] = nire["Brexit vote (%)"].astype(float)
nire["Brexit vote (%)"].dtypes


# In[72]:


nire.info()


# In[73]:


nire


# In[74]:


brexiters = nire.sort_values(by = "Brexit vote (%)", ascending = False)
brexiters


# In[ ]:


# ****NOW BACK TO THE GRAPHING


# In[78]:


#flipped2

both = pd.concat([flipped2, brexiters], axis = 1, sort = True)
both.fillna("NA")
both_final = both[['signatures', 'Brexit vote (%)']].sort_values(by = "signatures", ascending = True)
both_final


# In[79]:


both_final.signatures.iplot(kind='barh', opacity = 1)


# In[ ]:


# checking for correlation between brexit support and signatures



# In[80]:


# calculate the 0 - 1 correlation value for the two columns

both_final['signatures'].corr(both_final['Brexit vote (%)'])


# In[81]:


# pull a selection of just those constituencies that voted Leave

out = both_final[both_final['Brexit vote (%)'] > 50]
out


# In[82]:


# with just Leave constituencies the corr is higher, but is negative
# presumably because a 62% vote has only 11 signatures suggesting (erroneously) 'more votes, fewer signatures'

out['signatures'].corr(out['Brexit vote (%)'])


# In[83]:


out_test = out[out['signatures']>17]
out_test
#out = both_final[both_final['Brexit vote (%)'] > 50]


# In[84]:


# this only suggests a very weak correlation however, and still negative
# negative because 51% gives 30 sigs, while 55% gives 20 sigs.

out_test['signatures'].corr(out_test['Brexit vote (%)'])


# In[87]:


brexiters['Brexit vote (%)']

# here, for comparaison


# In[ ]:


# test scrape on the petition page


# In[75]:


url = ("https://petition.parliament.uk/petitions/235821")
results = requests.get(url)
print (results)


# In[76]:


soup = bs(results.text, 'html.parser')


# In[77]:


soup

