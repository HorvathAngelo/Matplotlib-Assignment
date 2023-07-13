Data Preparation:

I started by importing the necessary packages and dependencies.
Then, I loaded the "mouse_metadata.csv" and "study_results.csv" files into pandas DataFrames.
I merged the mouse metadata and study results DataFrames into a single DataFrame using the "Mouse ID" column as the common key.

Summary Statistics:

I calculated summary statistics for each drug regimen in the merged DataFrame.
The summary statistics included the mean, median, variance, standard deviation, and standard error of the mean (SEM) of the tumor volume for each drug regimen.
I organized the statistics into a DataFrame for easy analysis and interpretation.

Bar Charts and Pie Charts:

I created two bar charts to visualize the total number of rows (Mouse ID/Timepoints) for each drug regimen throughout the study.
The first bar chart was generated using the Pandas DataFrame.plot() method, and the second one using Matplotlib's pyplot methods.
Similarly, I created two pie charts to display the distribution of female versus male mice in the study.
The first pie chart was created using the Pandas DataFrame.plot() method, and the second one using Matplotlib's pyplot methods.

Quartiles, Outliers, and Box Plot:

I identified the four most promising treatment regimens: Capomulin, Ramicane, Infubinol, and Ceftamin.
For each of these treatment regimens, I calculated the final tumor volume of each mouse.
Then, I determined the quartiles, interquartile range (IQR), and potential outliers for each treatment regimen.
Finally, I visualized the distribution of the final tumor volume for all mice in each treatment group using a box plot, highlighting any potential outliers.

Line Plot and Scatter Plot:

I selected a single mouse that was treated with Capomulin and created a line plot of tumor volume versus time point for that mouse.
Additionally, I generated a scatter plot to show the relationship between mouse weight and average observed tumor volume for the entire Capomulin treatment regimen.

Correlation and Regression:

I calculated the correlation coefficient between mouse weight and average observed tumor volume for the Capomulin treatment regimen.
Furthermore, I performed linear regression to model the relationship between mouse weight and average observed tumor volume.
I plotted the linear regression model on top of the scatter plot to visualize the relationship between the variables.

Final Analysis:

I provided a summary of the study results based on the findings from the data analysis tasks.
This analysis included insights such as the performance of different treatment regimens, distribution of mice by sex, and correlations between mouse weight and tumor volume.
Overall, I successfully performed data analysis and visualization tasks to analyze the efficacy of different treatment regimens for squamous cell carcinoma (SCC) and gained valuable insights into the dataset provided.

