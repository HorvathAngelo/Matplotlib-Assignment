#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib
matplotlib.__version__


# In[3]:


# Import necessary packages and dependencies
import pandas as pd

# Read the mouse metadata and study results files
mouse_metadata = pd.read_csv('C:/Users/Horva/Downloads/Starter_Code (8)/Starter_Code/Pymaceuticals/data/Mouse_metadata.csv')
study_results = pd.read_csv('C:/Users/Horva/Downloads/Starter_Code (8)/Starter_Code/Pymaceuticals/data/Study_results.csv')

# Merge the mouse metadata and study results dataframes
merged_data = pd.merge(mouse_metadata, study_results, on='Mouse ID')

# Display the number of unique mice IDs
unique_mice = merged_data['Mouse ID'].nunique()
print(f"Number of unique mice IDs: {unique_mice}")

# Check for any mouse ID with duplicate time points
duplicate_mouse = merged_data.loc[merged_data.duplicated(subset=['Mouse ID', 'Timepoint']), 'Mouse ID'].unique()

# Display the data associated with the mouse ID with duplicate time points
print("Data associated with duplicate mouse ID:")
print(merged_data.loc[merged_data['Mouse ID'] == duplicate_mouse[0]])

# Create a new DataFrame with the data removed for the mouse ID with duplicate time points
cleaned_data = merged_data.loc[merged_data['Mouse ID'] != duplicate_mouse[0]]

# Display the updated number of unique mice IDs
updated_unique_mice = cleaned_data['Mouse ID'].nunique()
print(f"Updated number of unique mice IDs: {updated_unique_mice}")


# In[4]:


# Group the data by drug regimen and calculate the statistics
summary_stats = cleaned_data.groupby('Drug Regimen')['Tumor Volume (mm3)'].agg(['mean', 'median', 'var', 'std', 'sem'])

# Rename the columns for better readability
summary_stats = summary_stats.rename(columns={
    'mean': 'Mean',
    'median': 'Median',
    'var': 'Variance',
    'std': 'Standard Deviation',
    'sem': 'SEM'
})

# Display the summary statistics DataFrame
print(summary_stats)


# In[5]:


import matplotlib.pyplot as plt

# Bar chart using Pandas DataFrame.plot()
bar_chart_pandas = cleaned_data['Drug Regimen'].value_counts().plot(kind='bar', color='blue', alpha=0.7)
bar_chart_pandas.set_xlabel('Drug Regimen')
bar_chart_pandas.set_ylabel('Number of Mice')
bar_chart_pandas.set_title('Number of Mice per Drug Regimen (Pandas)')

# Bar chart using Matplotlib's pyplot
bar_chart_matplotlib = cleaned_data['Drug Regimen'].value_counts()
plt.bar(bar_chart_matplotlib.index, bar_chart_matplotlib.values, color='blue', alpha=0.7)
plt.xlabel('Drug Regimen')
plt.ylabel('Number of Mice')
plt.title('Number of Mice per Drug Regimen (Matplotlib)')
plt.xticks(rotation=45)
plt.show()

# Pie chart using Pandas DataFrame.plot()
pie_chart_pandas = cleaned_data['Sex'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['lightblue', 'lightpink'])
pie_chart_pandas.set_ylabel('')
pie_chart_pandas.set_title('Distribution of Mice by Sex (Pandas)')

# Pie chart using Matplotlib's pyplot
pie_chart_matplotlib = cleaned_data['Sex'].value_counts()
plt.pie(pie_chart_matplotlib.values, labels=pie_chart_matplotlib.index, autopct='%1.1f%%', colors=['lightblue', 'lightpink'])
plt.axis('equal')
plt.title('Distribution of Mice by Sex (Matplotlib)')
plt.show()


# In[6]:


# Create a grouped DataFrame to find the last (greatest) time point for each mouse
max_timepoint = cleaned_data.groupby('Mouse ID')['Timepoint'].max().reset_index()

# Merge the grouped DataFrame with the original cleaned DataFrame to get the final tumor volume
final_tumor_volume = pd.merge(max_timepoint, cleaned_data, on=['Mouse ID', 'Timepoint'])

# Create a list to hold the treatment names and an empty list to hold the tumor volume data
treatment_list = ['Capomulin', 'Ramicane', 'Infubinol', 'Ceftamin']
tumor_volume_data = []

# Loop through each treatment and append the final tumor volumes to the list
for treatment in treatment_list:
    tumor_volume = final_tumor_volume.loc[final_tumor_volume['Drug Regimen'] == treatment, 'Tumor Volume (mm3)']
    tumor_volume_data.append(tumor_volume)

# Determine outliers using the upper and lower bounds
outliers = []
for tumor_volume in tumor_volume_data:
    quartiles = tumor_volume.quantile([0.25, 0.5, 0.75])
    lower_quartile = quartiles[0.25]
    upper_quartile = quartiles[0.75]
    iqr = upper_quartile - lower_quartile
    lower_bound = lower_quartile - (1.5 * iqr)
    upper_bound = upper_quartile + (1.5 * iqr)
    outliers.append(tumor_volume.loc[(tumor_volume < lower_bound) | (tumor_volume > upper_bound)])

# Print the potential outliers
for i, treatment in enumerate(treatment_list):
    if not outliers[i].empty:
        print(f"Potential outliers for {treatment}:")
        print(outliers[i])
        print()

# Generate a box plot to show the distribution of the final tumor volume for each treatment
plt.boxplot(tumor_volume_data, labels=treatment_list, flierprops={'marker': 'o', 'markerfacecolor': 'red', 'markersize': 8})
plt.xlabel('Drug Regimen')
plt.ylabel('Final Tumor Volume (mm3)')
plt.title('Distribution of Final Tumor Volume by Treatment')
plt.show()


# In[7]:


import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Select a single mouse treated with Capomulin
capomulin_data = cleaned_data.loc[cleaned_data['Drug Regimen'] == 'Capomulin']
mouse_id = capomulin_data['Mouse ID'].unique()[0]
mouse_data = capomulin_data.loc[capomulin_data['Mouse ID'] == mouse_id]

# Generate a line plot of tumor volume versus time point for the selected mouse
plt.plot(mouse_data['Timepoint'], mouse_data['Tumor Volume (mm3)'], marker='o')
plt.xlabel('Timepoint (Days)')
plt.ylabel('Tumor Volume (mm3)')
plt.title(f'Tumor Volume vs Timepoint for Mouse {mouse_id} (Capomulin)')
plt.grid(True)
plt.show()

# Generate a scatter plot of mouse weight versus average observed tumor volume for the entire Capomulin treatment regimen
average_tumor_volume = capomulin_data.groupby('Mouse ID')['Tumor Volume (mm3)'].mean()
mouse_weight = capomulin_data.groupby('Mouse ID')['Weight (g)'].mean()

plt.scatter(mouse_weight, average_tumor_volume)
plt.xlabel('Weight (g)')
plt.ylabel('Average Tumor Volume (mm3)')
plt.title('Mouse Weight vs Average Tumor Volume (Capomulin)')
plt.grid(True)
plt.show()

# Calculate correlation coefficient and linear regression model
correlation = np.corrcoef(mouse_weight, average_tumor_volume)[0, 1]
slope, intercept, rvalue, pvalue, stderr = linregress(mouse_weight, average_tumor_volume)

# Print correlation coefficient
print(f"Correlation Coefficient: {correlation}")

# Print linear regression model
print(f"Linear Regression Model: y = {slope:.2f}x + {intercept:.2f}")
print(f"R-squared Value: {rvalue**2:.2f}")


# In[9]:


import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Group the Capomulin data by mouse ID and calculate the average tumor volume and mouse weight
capomulin_data = cleaned_data.loc[cleaned_data['Drug Regimen'] == 'Capomulin']
average_tumor_volume = capomulin_data.groupby('Mouse ID')['Tumor Volume (mm3)'].mean()
mouse_weight = capomulin_data.groupby('Mouse ID')['Weight (g)'].mean()

# Calculate the correlation coefficient between mouse weight and average tumor volume
correlation = np.corrcoef(mouse_weight, average_tumor_volume)[0, 1]

# Perform linear regression to obtain the slope and intercept of the regression line
slope, intercept, rvalue, pvalue, stderr = linregress(mouse_weight, average_tumor_volume)

# Generate the scatter plot of mouse weight versus average tumor volume
plt.scatter(mouse_weight, average_tumor_volume)
plt.xlabel('Weight (g)')
plt.ylabel('Average Tumor Volume (mm3)')
plt.title('Mouse Weight vs Average Tumor Volume (Capomulin)')
plt.grid(True)

# Plot the linear regression line
regression_line = slope * mouse_weight + intercept
plt.plot(mouse_weight, regression_line, color='red')

# Add equation and R-squared value to the plot
equation = f'y = {slope:.2f}x + {intercept:.2f}'
r_squared = f'R-squared = {rvalue**2:.2f}'
plt.text(20, 36, equation, color='red')
plt.text(20, 34, r_squared, color='red')

# Display the plot
plt.show()

# Print the correlation coefficient and linear regression equation
print(f"Correlation Coefficient: {correlation}")
print(f"Linear Regression Equation: y = {slope:.2f}x + {intercept:.2f}")
print(f"R-squared Value: {rvalue**2:.2f}")


# In[ ]:




