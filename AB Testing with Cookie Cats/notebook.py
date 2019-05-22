#!/usr/bin/env python
# coding: utf-8

# Importing pandas
import pandas as pd

# Reading in the data
df = pd.read_csv('datasets/cookie_cats.csv')

# Showing the first few rows
df.head()

# Counting the number of players in each AB group.
df.groupby(by='version').count()

# This command makes plots appear in the notebook
get_ipython().run_line_magic('matplotlib', 'inline')

# Counting the number of players for each number of gamerounds 
plot_df = df.groupby(df['sum_gamerounds']).count()

# Plotting the distribution of players that played 0 to 100 game rounds
ax = plot_df.head(100).plot()
ax.set_xlabel("game round")
ax.set_ylabel("user count")


# The % of users that came back the day after they installed
# df['retention_1'].sum()/df['retention_1'].count()
df['retention_1'].mean()

# Calculating 1-day retention for each AB-group
df.groupby('version')['retention_1'].mean()

# Creating an list with bootstrapped means for each AB-group
boot_1d = []
for i in range(500):
    boot_mean = df.sample(frac=1, replace=True).groupby('version')['retention_1'].mean()
    boot_1d.append(boot_mean)
    
# Transforming the list to a DataFrame
boot_1d = pd.DataFrame(boot_1d)
    
# A Kernel Density Estimate plot of the bootstrap distributions
boot_1d.plot()


# Adding a column with the % difference between the two AB-groups
boot_1d['diff'] = ((boot_1d['gate_30']-boot_1d['gate_40'])/boot_1d['gate_40']*100)

# Ploting the bootstrap % difference
ax = boot_1d['diff'].plot()
ax.set_xlabel('bootstrap %')


# Calculating the probability that 1-day retention is greater when the gate is at level 30
prob = (boot_1d['diff'] > 0.0).sum()/len(boot_1d['diff'])

# Pretty printing the probability
print(prob)


# Calculating 7-day retention for both AB-groups
df.groupby('version')['retention_7'].mean()


# Creating a list with bootstrapped means for each AB-group
boot_7d = []
for i in range(500):
    boot_mean = df.sample(frac=1,replace=True).groupby('version')['retention_7'].mean()
    boot_7d.append(boot_mean)
    
# Transforming the list to a DataFrame
boot_7d = pd.DataFrame(boot_7d)

# Adding a column with the % difference between the two AB-groups
boot_7d['diff'] = ((boot_7d['gate_30']-boot_7d['gate_40'])/boot_7d['gate_40'])

# Ploting the bootstrap % difference
ax = boot_7d['diff'].plot()
ax.set_xlabel("% difference in means")

# Calculating the probability that 7-day retention is greater when the gate is at level 30
prob = (boot_7d['diff'] > 0.0).sum()/len(boot_7d['diff'])

# Pretty printing the probability
print(prob)

# So, given the data and the bootstrap analysis
# Should we move the gate from level 30 to level 40 ?
move_to_level_40 = False 

