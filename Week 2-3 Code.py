
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#load in datasets
agg_listings = pd.read_csv(r'C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Week 1\agg_filtered_listings.csv')
agg_solds = pd.read_csv(r'C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Week 1\agg_filtered_solds.csv')
'''
#check the database was loaded correctly
print(agg_listings.head())
print(agg_solds.head())

#Check that there are no duplicate columns
print(agg_listings.columns.duplicated().any())
print(new_solds.columns.duplicated().any())

#identify the number of rows and columns for each dataset
print(agg_listings.info())
print(agg_solds.info())

#The agg_listings dataset has 547162 rows and 84 columns.
#The agg_solds dataset has 414054 rows and 84 columns

#Since we are using the already filtered dataset, we know all the property types are 'Residential'
#The rows in the listing dataset after the filtering is 547162 and the rows in the sold dataset after the filtering in 414054. The filter excluded ~36% of rows for listing and ~33% of rows for sold. 

summary_null_listings = agg_listings.isnull().sum().reset_index()
summary_null_listings.columns = ['Column Name', "Null Count"]
print(summary_null_listings)

summary_null_solds = agg_listings.isnull().sum().reset_index()
summary_null_solds.columns = ['Column Name', 'Null Count']
print(summary_null_solds)
'''

count_null = 0
listings_null = []
null_listings = agg_listings.isnull().sum()
for column, count in null_listings.items():
    percentage = count / len(agg_listings) * 100
    #print(f'The percentage of null values in Column "{column}" is {percentage}%')
    if percentage >= 90:
        #print(f'The Column "{column}" has a high percentage of null values of "{percentage}"%')
        count_null = count_null + 1
        listings_null = listings_null + [f'{column}']
print(f'The number of columns in the listings dataset exceeding 50% null values is: {count_null} and the columns are:')
print(listings_null)

count_null = 0 
solds_null = []
null_solds = agg_solds.isnull().sum()
for column, count in null_solds.items():
    percentage = count / len(agg_solds) * 100
    #print(f'The percentage of null values in Column "{column}" is {percentage}%')
    if percentage >= 90:
        #print(f'The Column "{column}" has a high percentage of null values of "{percentage}"%')
        count_null = count_null + 1
        solds_null = solds_null + [f'{column}']

print(f'The number of columns in the solds dataset exceeding 90% null values is: {count_null} and the columns are:')
print(solds_null) 


#Generate Histograms, Boxplots, percentile summaries and identify outliers for the given columns
#Since there are such extreme outliers, we need to log the values to adjust the data

target_dir = "C:/Users/famil/OneDrive/Desktop/Python Workspace/IDX Exchange/Week 2-3/Week 2-3 Output/Listings"
list_col = ['ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea', 'LotSizeAcres', 'BedroomsTotal', 'DaysOnMarket', 'YearBuilt']
for i in list_col:
    agg_listings[i] = pd.to_numeric(agg_listings[i], errors='coerce')
    print(agg_listings[i].describe())
    outliers = agg_listings[agg_listings[i] > agg_listings[i].quantile(0.95)]
    print(outliers)

    clean = agg_listings[i].replace([np.inf, -np.inf], np.nan)
    clean = clean[clean >= 0].dropna()
    logged = np.log1p(clean)

    plt.figure()
    logged.dropna().plot(kind = 'hist', bins = 50, edgecolor = 'black', title = f"{i} Histogram")
    plt.xlabel(f'log(1 + {i})')
    plt.savefig(f"{target_dir}/{i}_listings_histogram.png", dpi = 300, bbox_inches = 'tight')
    plt.close()

    plt.figure()
    logged.plot(kind = 'box', title = f"{i} Boxplot")
    plt.xlabel(f'log(1 + {i})')
    plt.savefig(f"{target_dir}/{i}_listings_boxplot.png", dpi = 300, bbox_inches = 'tight')
    plt.close()

target_dir = "C:/Users/famil/OneDrive/Desktop/Python Workspace/IDX Exchange/Week 2-3/Week 2-3 Output/Solds"
for i in list_col:
    agg_solds[i] = pd.to_numeric(agg_solds[i], errors='coerce')
    print(agg_solds[i].describe())
    outliers = agg_solds[agg_solds[i] > agg_solds[i].quantile(0.95)]
    print(outliers)

    clean = agg_solds[i].replace([np.inf, -np.inf], np.nan)
    clean = clean[clean >= 0].dropna()
    logged = np.log1p(clean)

    plt.figure()
    logged.dropna().plot(kind = 'hist', bins = 50, edgecolor = 'black', title = f"{i} Histogram")
    plt.xlabel(f'log(1 + {i})')
    plt.savefig(f"{target_dir}/{i}_solds_histogram.png", dpi = 300, bbox_inches = 'tight')
    plt.close()

    plt.figure()
    logged.plot(kind = 'box', title = f"{i} Boxplot")
    plt.xlabel(f'log(1 + {i})')
    plt.savefig(f"{target_dir}/{i}_solds_boxplot.png", dpi = 300, bbox_inches = 'tight')
    plt.close()