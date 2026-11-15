import numpy as np
import pandas as pd

listings = pd.read_csv(r"C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Week 6\Week 6 Output\Listings_metrics.csv")
solds = pd.read_csv(r"C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Week 6\Week 6 Output\Solds_metrics.csv")

#remove outliers within CLosePrice, LivingArea, DaysOnMarket

#first check how many entries are in both 
print(f'Listings dimensions before filtering: {listings.shape}')
print(f'Solds dimesions before filtering: {solds.shape}')

#write function to flag entries beyong the 1.5 * IQR boundary
def flag_outliers(df):
    targ_cols = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
    cols = [c for c in targ_cols if c in df.columns]
    if cols:
        Q1 = df[cols].quantile(0.25)
        Q3 = df[cols].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df['All_outliers'] = ((df[cols] < lower) | (df[cols] > upper)).any(axis = 1)
    return df

flag_listings = flag_outliers(listings)
flag_solds = flag_outliers(solds)
print(flag_listings['All_outliers'].sum())
print(flag_solds['All_outliers'].sum())
flag_listings.to_csv(r"C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Week 7\Week 7 Output\flagged_listings.csv")
flag_solds.to_csv(r'C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Week 7\Week 7 Output\flagged_solds.csv')

#write function to remove entries beyond the 1.5 * IQR boundary
def remove_outliers(df):
    if 'ClosePrice' in df.columns:
        Q1 = df['ClosePrice'].quantile(0.25)
        Q3 = df['ClosePrice'].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df = df[(df['ClosePrice'] >= lower) & (df['ClosePrice'] <= upper)]
    if 'LivingArea' in df.columns:
        Q1 = df['LivingArea'].quantile(0.25)
        Q3 = df['LivingArea'].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df = df[(df['LivingArea'] >= lower) & (df['LivingArea'] <= upper)]
    if 'DaysOnMarket' in df.columns:
        Q1 = df['DaysOnMarket'].quantile(0.25)
        Q3 = df['DaysOnMarket'].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df = df[(df['DaysOnMarket'] >= lower) & (df['DaysOnMarket'] <= upper)]
    return df

listings_cleaned = remove_outliers(listings)
solds_cleaned = remove_outliers(solds)
print(f'Listings dimensions after filtering: {listings_cleaned.shape}')
print(f'Solds dimesions after filtering: {solds_cleaned.shape}')

#print the median with and without filtering
def print_median(df, name):
    print(f"----{name}----")
    cols = ['ClosePrice', 'LivingArea', "DaysOnMarket"]
    for i in cols:
        print(f'Median {i}: {df[i].median():,.2f}')
    return
print_median(flag_listings, "Flagged Listings")
print_median(flag_solds, "Flagged Solds")
print_median(listings_cleaned, "Cleaned Listings")
print_median(solds_cleaned, "Cleaned Solds")

listings_cleaned.to_csv(r"C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Week 7\Week 7 Output\listings_no_outliers.csv")
solds_cleaned.to_csv(r'C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Week 7\Week 7 Output\solds_no_outliers.csv')