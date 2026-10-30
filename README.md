Week 1:  
Goal: Aggregate all listing datasets and sold datasets into respective csv's  
Tasks: Check entries before and after to ensure successful concatenation, filter PropertyType column to Residential only, output results as csv's  
Note: Some of the sold datasets have filled in the name. They have two extra columns called longitude filled and latitude filled. The datasets with filled in the title were saved instead of the non-filled  

Week 2:
Goal: Gain a deeper understanding of the data by gathering percentile information and deviated outliers
Tasks: Check the dataset was correctly loaded in, check that there are no duplicate columns, identify the number of columns for listings and solds, output total null entries for each column in each dataset, loop through datasets to find the percentage of null columns in each dataset, flag columns with more than 90% null entries, generate histograms and boxplots of the given columns for both datasets and save resulting plots into their respective folders.
Note: Values of columns were logged before plotted into histograms to account for inaccurate graphs due to outstanding outliers.

Week 3:
Goal: Upload live data from public API FRED into the spreadsheet as weekly averages
Tasks: Obtain data from from FRED using a url and averaging it by month
Note: Two new columns added year_month and rate_30yr_fixed into both listings and solds spreadsheet

Week 4-5:
Goal: Clean data and flag invalid columns
Tasks: Convert date column to datetime format, remove columns with over 90% null entries, remove columns duplicate columns, remove invalid numeric values such as negatives, make sure dates of transaction follow the correct timeline, and remove incorrect geographical data. 
Note: The listings dataset went from 86 columns and 547162 rows to 69 columns to 65 columns and 466239 rows. The solds dataset went from 86 columns and 414054 rows to 72 columns and 409661 rows. 
