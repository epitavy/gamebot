#!/usr/bin/env python
# coding: utf-8

# <center><h1>Algorithm evolution visualizer</h1></center>
# 
# ***

# In[2]:


import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# ### Plotting functions

# In[3]:


def plot_metric_by_generation(*data, metric='Score'):
    fig, ax = plt.subplots()
    ax.set_xlabel('Generation')
    ax.set_ylabel(metric)
    
    for name, serie in data:
        ax.plot(range(len(serie)), serie, label=name)
    ax.legend()


# In[4]:


def plot_distribution(*data):
    fig, ax = plt.subplots(len(data))
    
    if type(ax) != np.ndarray:
        ax = [ax]
    
    for (name, (ticks, serie)), axis in zip(data, ax):
        axis.plot(ticks, serie, label=name)
        axis.set_xlabel("Parameter value")
        axis.set_ylabel('Count')
        axis.legend()


# ### Functions to cleanup data from log files

# In[5]:


def clean_raw_scores(raw_data):
    data = []
    for line in raw_data:
        line = line.split(' ')
        line = line[1:]   # Remove generation number
        line = list(map(lambda x : float(x), line))
        data.append(line)
    return data


# In[33]:


def clean_raw_params(raw_params):
    data = []
    
    head = raw_params[0].split(' ')
    try:
        pop_size = int(head[0])
    except Exception:
        raise Exception("File has bad format, the first line should be the population size")
        
    all_params = []
    for i, line in enumerate(raw_params[1:]):
        if i % pop_size == 0:
            data.append(all_params) # A whole generation
            all_params = []
        line = list(map(lambda x : float(x), line.split(' ')))
        all_params.append(line)
            
        
    return data[1:]


# ### Functions to compute useful stats

# #### For scores

# In[7]:


def scores_to_avg_by_gen(data):
    avg_by_gen = []
    for gen in data:
        avg_by_gen.append(sum(gen) / len(gen))
    return ('avg', avg_by_gen)


# In[8]:


def scores_to_best_by_gen(data):
    best_by_gen = []
    for gen in data:
        best_by_gen.append(gen[0])
    return ('best', best_by_gen)


# #### For algo parameters

# In[9]:


def build_histogram(ticks, values):
    # Build intervals
    intervals = []
    for i in range(len(ticks) - 1):
        intervals.append((ticks[i], ticks[i + 1]))
        
    histogram = []
    for inf, sup in intervals:
        count = 0
        for v in values:
            if inf <= v < sup:
                count += 1
        histogram.append(count)
    
    return (ticks[:-1], histogram)


# In[10]:


from numpy import arange

def params_to_distrib_over_pop(params, gen=0, param_index=0):
    # Select the generation
    gen_params = params[gen]
    # Select the parameter
    param = [params[param_index] for params in gen_params]
    
    min_val = min(param)
    max_val = max(param)
    
    interval = (max_val - min_val) / 40
    if interval == 0:      # Fuck that shit
        raise ValueError("No distribution, every parameter has the same value.")
    ticks = arange(min_val, max_val + interval, interval)
    return (f'gen {gen}\nparam{param_index}', build_histogram(ticks, param))
    


# In[11]:


def params_to_avg_by_gen(params, param_index=0):
    # Select the parameter
    param_by_gen = []
    nb_gen = len(params)
    for gen in params:
        all_gen_param = []
        for algo_param in gen:
            all_gen_param.append(algo_param[param_index])
        param_by_gen.append(all_gen_param)
    
    avg_by_gen = list(map(lambda arr : sum(arr) / len(arr), param_by_gen))
    return ('avg', avg_by_gen)


# ----
# ----
# ----

# In[51]:


with open('test_one_param-scores.log.raw', 'r') as file:
    raw_scores = file.readlines()
    
scores = clean_raw_scores(raw_scores)
scores_avg = scores_to_avg_by_gen(scores)
scores_best = scores_to_best_by_gen(scores)
plot_metric_by_generation(scores_best, scores_avg)

gen_size = len(scores[0])
print(gen_size)


# In[50]:


with open('test_one_param-params.log.raw', 'r') as file:
    raw_params = file.readlines()
    
params = clean_raw_params(raw_params)
param_distrib1 = params_to_distrib_over_pop(params, gen=1, param_index=0)
param_distrib3 = params_to_distrib_over_pop(params, gen=45, param_index=0)
param_distrib4 = params_to_distrib_over_pop(params, gen=198, param_index=0)

plot_distribution(param_distrib1, param_distrib3, param_distrib4)


gen_size = len(params[0])
print(gen_size)


# In[ ]:


avg_param = params_to_avg_by_gen(params)
plot_metric_by_generation(avg_param, metric='Parameter')


# In[ ]:


print()


# In[ ]:




