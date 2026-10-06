Week 1:  
Goal: Aggregate all listing datasets and sold datasets into respective csv's  
Tasks: Check entries before and after to ensure successful concatenation, filter PropertyType column to Residential only, output results as csv's  
Note: Some of the sold datasets have filled in the name. They have two extra columns called longitude filled and latitude filled. The datasets with filled in the title were saved instead of the non-filled  

Week 2:
Goal: Gain a deeper understanding of the data by gathering percentile information and deviated outliers
Tasks: Check the dataset was correctly loaded in, check that there are no duplicate columns, identify the number of columns for listings and solds, output total null entries for each column in each dataset, loop through datasets to find the percentage of null columns in each dataset, flag columns with more than 90% null entries, generate histograms and boxplots of the given columns for both datasets and save resulting plots into their respective folders.
Note: Values of columns were logged before plotted into histograms to account for inaccurate graphs due to outstanding outliers.
