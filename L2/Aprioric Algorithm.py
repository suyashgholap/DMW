
# coding: utf-8

# In[11]:


import pandas as pd
import numpy as np
import math


# In[12]:


transaction_df = pd.read_csv('GroceryStoreDataSet.csv')
transaction_df


# In[14]:


transaction_df.shape


# In[15]:


transaction_df.info()


# In[17]:


transaction_df.index.rename('TID', inplace=True)
transaction_df.rename(columns={'MILK,BREAD,BISCUIT' : 'item_list'}, inplace=True)


# In[18]:


trans_df = transaction_df.item_list.str.split(',')
trans_df


# In[19]:


def prune(data,supp):
    
    df = data[data.supp_count >= supp] 
    return df
    
def count_itemset(transaction_df, itemsets):
    
    count_item = {}
    for item_set in itemsets:
        set_A = set(item_set)
        for row in trans_df:
            set_B = set(row)
            if set_B.intersection(set_A) == set_A: 
                if item_set in count_item.keys():
                    count_item[item_set] += 1
                
                else:
                    count_item[item_set] = 1
                
    data = pd.DataFrame()
    data['item_sets'] = count_item.keys()
    data['supp_count'] = count_item.values()
    
    return data
def count_item(trans_items):
    
    count_ind_item = {}
    for row in trans_items:
        for i in range(len(row)):
            if row[i] in count_ind_item.keys():
                count_ind_item[row[i]] += 1
            else:
                count_ind_item[row[i]] = 1
                data = pd.DataFrame()
    data['item_sets'] = count_ind_item.keys()
    data['supp_count'] = count_ind_item.values()
    data = data.sort_values('item_sets')
    return data


def join(list_of_items):
    itemsets = []
    i = 1
    for entry in list_of_items:
        proceding_items = list_of_items[i:]
        for item in proceding_items:
            if(type(item) is str):
                if entry != item:
                    tuples = (entry, item)
                    itemsets.append(tuples)
            else:
                if entry[0:-1] == item[0:-1]:
                    tuples = entry+item[1:]
                    itemsets.append(tuples)
        i = i+1
    if(len(itemsets) == 0):
        return None
    return itemsets


# In[20]:


def apriori(trans_data,supp=3, con=0.5):
    freq = pd.DataFrame()
    
    df = count_item(trans_data)
   
    while(len(df) != 0):
        
        df = prune(df, supp)
    
        if len(df) > 1 or (len(df) == 1 and int(df.supp_count >= supp)):
            freq = df
        
        itemsets = join(df.item_sets)
        if(itemsets is None):
            return freq
    
        df = count_itemset(trans_data, itemsets)
    return df


# In[21]:


freq_item_sets = apriori(trans_df, 4)
freq_item_sets


# In[22]:


def calculate_conf(value1, value2):
    return round(int(value1)/int(value2) * 100, 2)


# In[23]:


def strong_rules(freq_item_sets, threshold):

    confidences = {}
    for row in freq_item_sets.item_sets:
        for i in range(len(row)):
            for j in range(len(row)):
                 if i != j:
                    tuples = (row[i], row[j])
                    conf = calculate_conf(freq_item_sets[freq_item_sets.item_sets == row].supp_count, count_item(trans_df)[count_item(trans_df).item_sets == row[i]].supp_count)
                    confidences[tuples] = conf
                    conf_df = pd.DataFrame()
    conf_df['item_set'] = confidences.keys()
    conf_df['confidence'] = confidences.values()

    return conf_df[conf_df.confidence >= threshold]


# In[15]:


strong_rules(freq_item_sets, 50.0)


# In[16]:


from functools import reduce # Valid in Python 2.6+, required in Python 3
import operator

def interesting_rules(freq_item_sets):
    
    lifts = {}
    prob_of_items = []
  
    for row in freq_item_sets.item_sets:
        num_of_items = len(row)
        
        prob_all = freq_item_sets[freq_item_sets.item_sets == row].supp_count / 18
        for i in range(num_of_items):
            prob_of_items.append(count_item(trans_df)[count_item(trans_df).item_sets == row[i]].supp_count / 18)


# In[19]:


def strong_rules(freq_item_sets, threshold):

    confidences = {}
    for row in freq_item_sets.item_sets:
        for i in range(len(row)):
            for j in range(len(row)):
                 if i != j:
                    tuples = (row[i], row[j])
                    conf = calculate_conf(freq_item_sets[freq_item_sets.item_sets == row].supp_count, count_item(trans_df)[count_item(trans_df).item_sets == row[i]].supp_count)
                    confidences[tuples] = conf
    conf_df = pd.DataFrame()
    conf_df['item_set'] = confidences.keys()
    conf_df['confidence'] = confidences.values()

    return conf_df[conf_df.confidence >= threshold]


# In[20]:


strong_rules(freq_item_sets, 50.0)

