#!/usr/bin/env python
# coding: utf-8

# # Real-world Data Wrangling

# In this project, you will apply the skills you acquired in the course to gather and wrangle real-world data with two datasets of your choice.
# 
# You will retrieve and extract the data, assess the data programmatically and visually, accross elements of data quality and structure, and implement a cleaning strategy for the data. You will then store the updated data into your selected database/data store, combine the data, and answer a research question with the datasets.
# 
# Throughout the process, you are expected to:
# 
# 1. Explain your decisions towards methods used for gathering, assessing, cleaning, storing, and answering the research question
# 2. Write code comments so your code is more readable
# 
# Before you start, install the some of the required packages. 

# In[14]:


get_ipython().system('python -m pip install kaggle==1.6.12')


# In[15]:


get_ipython().system('pip install --target=/workspace ucimlrepo')


# **Note:** Restart the kernel to use updated package(s).

# ## 1. Gather data
# 
# In this section, you will extract data using two different data gathering methods and combine the data. Use at least two different types of data-gathering methods.

# ### **1.1.** Problem Statement
# In 2-4 sentences, explain the kind of problem you want to look at and the datasets you will be wrangling for this project.
# 
# I want to combine the adult and suicide datasets so I can see in more detail whether we can find interesting insights

# Finding the right datasets can be time-consuming. Here we provide you with a list of websites to start with. But we encourage you to explore more websites and find the data that interests you.
# 
# * Google Dataset Search https://datasetsearch.research.google.com/
# * The U.S. Government’s open data https://data.gov/
# * UCI Machine Learning Repository https://archive.ics.uci.edu/ml/index.php
# 

# ### **1.2.** Gather at least two datasets using two different data gathering methods
# 
# List of data gathering methods:
# 
# - Download data manually
# - Programmatically downloading files
# - Gather data by accessing APIs
# - Gather and extract data from HTML files using BeautifulSoup
# - Extract data from a SQL database
# 
# Each dataset must have at least two variables, and have greater than 500 data samples within each dataset.
# 
# For each dataset, briefly describe why you picked the dataset and the gathering method (2-3 full sentences), including the names and significance of the variables in the dataset. Show your work (e.g., if using an API to download the data, please include a snippet of your code). 
# 
# Load the dataset programmtically into this notebook.

# #### *UCI Adult*
# 
# Type: CSV File
# 
# Method: We downloaded a CSV file and names, and used pandas to load it into a dataframe.
# 
# Dataset variables:
# age, workclass, fnlwgt, education, education-num, marital-status, occupation,relationship, race, sex, capital-gain, capital-loss, hours-per-week, native-country, income

# In[2]:


#FILL IN 1st data gathering and loading method

import pandas as pd

# URLs of the dataset files
data_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data'
names_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.names'

# Column names (you can find these in the adult.names file or the dataset description)
column_names = [
    'age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 
    'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 
    'hours-per-week', 'native-country', 'income'
]

# Load the dataset into a pandas dataframe
df1 = pd.read_csv(data_url, names=column_names, sep=',\s', engine='python')

# Display the first few rows of the dataframe
print(df1.head())
print(df1.columns)


# #### Dataset 2
# 
# Type: *CSV File
# 
# Method: Loading the file into a dataframe
# 
# Dataset variables:
# 
# *INDICATOR', 'UNIT', 'UNIT_NUM', 'STUB_NAME', 'STUB_NAME_NUM',
#        'STUB_LABEL', 'STUB_LABEL_NUM', 'YEAR', 'YEAR_NUM', 'AGE', 'AGE_NUM',
#        'ESTIMATE', 'FLAG

# In[3]:


#FILL IN 2nd data gathering and loading method
import pandas as pd

# URL of the second dataset file
second_data_url = 'https://data.cdc.gov/api/views/9j2v-jamp/rows.csv?accessType=DOWNLOAD'

# Load the second dataset into a pandas dataframe
df2 = pd.read_csv(second_data_url)

# Display the first few rows of the second dataframe
print(df2.head())

print(df2.columns)


# Optional data storing step: You may save your raw dataset files to the local data store before moving to the next step.

# In[ ]:


#Optional: store the raw data in your local data store


# ## 2. Assess data - I did a lot to clean up this data. I'm going to break it down into what I did, the issue, and whether it was tidiness or cleanness related in each step. Generally, I 
# 
# Assess the data according to data quality and tidiness metrics using the report below.
# 
# List **two** data quality issues and **two** tidiness issues. Assess each data issue visually **and** programmatically, then briefly describe the issue you find.  **Make sure you include justifications for the methods you use for the assessment.**

# ### Quality Issues: Suicide Dataset Cleanup

# In[4]:


# Visual viewing
print(df2.head())

# I also went into Excel and looked at the data and saw a bunch of things I didn't like

# Programmatic 
print(df2.columns)
print(df2.describe())


# Observations: This data looks terrible and is really hard to use in this form. 

# Here are some of the problems with it. Tons of Unnecessary Columns, Unnecessary Entries (years, not enough indicators)


# In[5]:


# First, I'd like to only look at data that I can cross-apply to the adult data set. 
# I also wanted to look at only STUB_LABELS that had 3 columns so that I could more generally match to adult data set.

# Issue 1: Not enough data for some columns I'm trying to match on. Solution: Drop rows that don't have the data I'm looking for
# Step 1: Cleaning - Filter down to appropriate year and STUB_LABEL containing exactly three colons
df2adj = df2[(df2['YEAR'] == 1994) & (df2['STUB_LABEL'].str.count(':') == 3)]

# In it's current form the data is comma delimited when it should be its own separate columns to make it easier for it to merge with adult.

# Step 2: Tidying - Split 'STUB_LABEL' into 'GENDER', 'ETHNICITY', 'RACE', and 'AGE_RANGE'
df2adj[['GENDER', 'ETHNICITY', 'RACE', 'AGE_RANGE']] = df2['STUB_LABEL'].str.split(':', expand=True)

# I don't need all these other columns as they distract and make the data look messy.

# Step 3: Tidying - Keep only the columns 'GENDER', 'RACE', 'AGE_RANGE', and 'ESTIMATE'
df2adj = df2adj[['GENDER', 'RACE', 'AGE_RANGE', 'ESTIMATE']]

# Several of the entries lack the Estimate column, I want to only look at entries with values.

# Step 4: Cleaning - Drop rows with NaN values in the 'ESTIMATE' column
df2adj = df2adj.dropna(subset=['ESTIMATE'])

# Display the resulting DataFrame
print(df2adj)

# This data looks broadly able to be merged at this point.


# Issue and justification: I wrote out each issue for this throughout the coding

# ### Quality Issues: Adult DataSet Cleanup

# In[6]:


# Inspecting the dataframe visually

print(df1.head())

print(df1.columns)

# Inspecting the dataframe programmatically

print(df1.describe())

# Observation: Some missing values exist.

#Step 1 - Cleaning: Let's fill them in as unknown
df1.replace('?', pd.NA, inplace=True)
df1.fillna('Unknown', inplace=True)

# There are some spaces between delimiters, potentially leading to issues.

#Step 2 Cleaning - There are some spaces between the delimiters, potentially leading to data analysis problems in adult dataset

df1 = df1.applymap(lambda x: x.strip() if isinstance(x, str) else x)

df1 = df1.applymap(lambda x: x.lower() if isinstance(x, str) else x)

# Discrete ages is more specific than the suicide dataset. This will lead to a data tidiness issue

#Let's also make sure that we can tidy this data to combine with the suicide dataset. In this step, we'll break the ages into bins.

age_bins = [15, 24, 44, 64, float('inf')]
age_labels = ['15-24', '25-44', '45-64', '65+']
df1['age_category'] = pd.cut(df1['age'], bins=age_bins, labels=age_labels, right=True)

# Display the first few rows of the dataframe
print(df1.head())
print(df1[['age', 'age_category']].head())


# In[7]:


# This data is too hard to manage with all the extra columns. 

#Let's keep only a few more columns to really focus

columns_to_keep = [
    'age_category', 'occupation', 'race', 'sex'
]
df1adj = df1.loc[:, columns_to_keep]

# Confirming data is easy to read
print(df1adj.head())
print(df1adj.columns)


# Issue and justification: Now the data looks a lot easier to work with/wrangle because it's more manageable

# ### Now we gotta make the data able to be merged

# In[8]:


# We'll do a direct comparison of heads

print(df1adj.head())
print(df2adj.head())

# Notice similar concepts but have different column headings, values. We'll have to convert.


# In[9]:


print(df1adj.head())
print(df2adj.head())

#Tidying, let's make sure the columns are a 1-1 match in terms of names. Decided to capitalize occupation so it would look nice.

df1adj = df1adj.rename(columns={
    'sex': 'GENDER',
    'age_category': 'AGE_RANGE',
    'race': 'RACE',
    'occupation': 'OCCUPATION'
})
print(df1adj.head())

# Tidying -Convert values in the 'GENDER' column to lowercase
df2adj['GENDER'] = df2adj['GENDER'].str.lower()

# Tidying Convert values in the 'RACE' column to lowercase
df2adj['RACE'] = df2adj['RACE'].str.lower()

# Tidying data so that we're using the same naming conventions to be able to merge

df2adj['AGE_RANGE'] = df2adj['AGE_RANGE'].str.strip()

age_range_replacements = {
    '15-24 years': '15-24',
    '25-44 years': '25-44',
    '45-64 years': '45-64',
    '65 years and over': '65+'
}

# Now we're applying the replacements to the 'AGE_RANGE' column
df2adj['AGE_RANGE'] = df2adj['AGE_RANGE'].replace(age_range_replacements)

# Checking to see if it worked

print(df2adj.head())

# I tried merging in a different cell at this point. Noticed the dataframe was empty, had to troubleshoot. Checking datatypes to see if they match up.

print(df1adj.dtypes)
print(df2adj.dtypes)

# Tidying data so that datatypes match

df1adj['AGE_RANGE'] = df1adj['AGE_RANGE'].astype(object)
print(df1adj.dtypes)

# I was still running into issues having entries in my dataframe. At this point, I wanted to make sure there were no extraneous spaces.

# We're cleaning the data so it has no spaces

df1adj['GENDER'] = df1adj['GENDER'].str.strip()
df1adj['RACE'] = df1adj['RACE'].str.strip()
df1adj['AGE_RANGE'] = df1adj['AGE_RANGE'].str.strip()

df2adj['GENDER'] = df2adj['GENDER'].str.strip()
df2adj['RACE'] = df2adj['RACE'].str.strip()
df2adj['AGE_RANGE'] = df2adj['AGE_RANGE'].str.strip()


# Now we've got data that should work. (It should work because I've been trying to merge unsuccessfully for a while at this point

# ### Creating the merge

# In[10]:


# Now we're merging the datasets to verify that we're having entries that work

merged_df = pd.merge(df1adj, df2adj[['GENDER', 'RACE', 'AGE_RANGE', 'ESTIMATE']], 
                     on=['GENDER', 'RACE', 'AGE_RANGE'], 
                     how='inner')
print(merged_df.head(20))

# It looks good!


# In[ ]:





# Doesn't that look great?

# ## 3. Clean data
# Clean the data to solve the 4 issues corresponding to data quality and tidiness found in the assessing step. **Make sure you include justifications for your cleaning decisions.**
# 
# After the cleaning for each issue, please use **either** the visually or programatical method to validate the cleaning was succesful.
# 
# At this stage, you are also expected to remove variables that are unnecessary for your analysis and combine your datasets. Depending on your datasets, you may choose to perform variable combination and elimination before or after the cleaning stage. Your dataset must have **at least** 4 variables after combining the data.

# In[11]:


print(merged_df.dtypes)


# ### **Quality Issue 1: Completed Above**

# In[ ]:


# You may note that I've done this in detail above


# In[ ]:


# Observe the prior cleaning I've been doing


# Justification: I did a bunch of cleaning in the issues section, and noted what they were

# ### See above

# In[ ]:


See above


# In[ ]:


See above


# Justification: I explain why I do what I do above

# ### **See above

# In[ ]:





# In[ ]:


#See above


# See above

# ### See above

# In[ ]:


#See above


# In[ ]:


#See above


# Justification: See above

# ### **Remove unnecessary variables and combine datasets**
# 
# Depending on the datasets, you can also peform the combination before the cleaning steps.

# In[ ]:


# This has been done in an earlier step


# ## 4. Update your data store
# Update your local database/data store with the cleaned data, following best practices for storing your cleaned data:
# 
# - Must maintain different instances / versions of data (raw and cleaned data)
# - Must name the dataset files informatively
# - Ensure both the raw and cleaned data is saved to your database/data store

# In[12]:


# df1 is essentially uncleaned whereas df1adj has been modified signficantly. The same can be said for df2 and df2adj


# ## 5. Answer the research question
# 
# ### **5.1:** Define and answer the research question 
# Going back to the problem statement in step 1, use the cleaned data to answer the question you raised. Produce **at least** two visualizations using the cleaned data and explain how they help you answer the question.

# *Research question:* FILL IN from answer to Step 1

# In[13]:


import matplotlib.pyplot as plt
import seaborn as sns

# Calculate average estimate by occupation
occupation_avg_estimate = merged_df.groupby('OCCUPATION')['ESTIMATE'].mean().reset_index()

# Create a bar plot
plt.figure(figsize=(12, 6))
sns.barplot(data=occupation_avg_estimate, x='OCCUPATION', y='ESTIMATE', palette='viridis')
plt.xticks(rotation=45, ha='right')
plt.title('Average Estimate by Occupation')
plt.xlabel('Occupation')
plt.ylabel('Average Estimate')
plt.tight_layout()
plt.show()


# *Answer to research question:* FILL IN

# In[ ]:


#Visual 2 - FILL IN


# *Answer to research question:* FILL IN

# ### **5.2:** Reflection
# In 2-4 sentences, if you had more time to complete the project, what actions would you take? For example, which data quality and structural issues would you look into further, and what research questions would you further explore?

# *Answer:* FILL IN
