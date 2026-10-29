import pandas as pd
import numpy as np

listings = pd.read_csv(r'C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Week 2-3\Week 3 Output\listings_with_rates.csv')
solds = pd.read_csv(r'C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Week 2-3\Week 3 Output\sold_with_rates.csv')
#===========================To Fix========================
##Print out columns removed and number of rows removed
##Remove columns with more than 90% null
##Change the drop numeric to not drop nulls

print("Number of columns before cleaning:", f'listings: {len(listings.columns)}, solds: {len(solds.columns)}')
print("Number of rows before cleaning:", f'listings: {len(listings)}, solds: {len(solds)}')

#change date columns to datetime 
dates = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']
for col in dates:
    if col in solds.columns:
        solds[col] = pd.to_datetime(solds[col], errors='coerce', format='mixed')
    if col in listings.columns:
        listings[col] = pd.to_datetime(listings[col], errors='coerce', format='mixed')

#find columns with more than 90% null values and remove them
def drop_high_null(df, threshold=0.9):
    threshold = 0.9
    high_null_cols = df.columns[df.isnull().mean() > threshold].tolist()
    print(f'Columns with more than {threshold*100}% null values in {df.name if hasattr(df, "name") else "DataFrame"}: {high_null_cols}')
    
    if not high_null_cols:
        return df
    
    return df.drop(columns=high_null_cols)
drop_high_null(listings)
drop_high_null(solds)

#find the redudant columns and remove them
def drop_identical_data_columns(df):
    #Sample only the first 10000 rows to check for identical columns
    sample_df = df.sample(n=10000, random_state = 42)
    
    full_dups_mask = sample_df.T.duplicated(keep = 'first')
    actual_dups = sample_df.columns[full_dups_mask].tolist()
    print(f'Identical columns found in {df.name if hasattr(df, "name") else "DataFrame"}: {actual_dups}')

    if not actual_dups:
        return df
    
    return df.drop(columns=actual_dups)

listings_cleaned = drop_identical_data_columns(listings)
solds_cleaned = drop_identical_data_columns(solds)

print("Listings still have duplicates?", listings_cleaned.sample(10000, random_state=42).T.duplicated().any())
print("Solds still have duplicates?", solds_cleaned.sample(10000, random_state=42).T.duplicated().any())

#find columns that are completely empty and remove them
def drop_empty_columns(df):
    empty_cols = df.columns[df.isnull().all()].tolist()
    print(f'Empty columns found in {df.name if hasattr(df, "name") else "DataFrame"}: {empty_cols}')
    if not empty_cols:
        return df

    return df.drop(columns=empty_cols)

listings_cleaned = drop_empty_columns(listings_cleaned)
solds_cleaned = drop_empty_columns(solds_cleaned)

print("Listings still have empty columns?", listings_cleaned.isnull().all().any())
print("Solds still have empty columns?", solds_cleaned.isnull().all().any())

#remove negative values from columns
def remove_negatives(df, Close, Living, Days, Bedrooms, Bathrooms):
    if Close in df.columns:
        df = df[(df[Close] > 0) | df[Close].isnull()]
    if Living in df.columns:
        df = df[(df[Living] > 0) | df[Living].isnull()]
    if Days in df.columns:
        df = df[(df[Days] >= 0) | df[Days].isnull()]
    if Bedrooms in df.columns:
        df = df[(df[Bedrooms] >= 0) | df[Bedrooms].isnull()]
    if Bathrooms in df.columns:
        df = df[(df[Bathrooms] >= 0) | df[Bathrooms].isnull()]
    return df

#dont remove nulls
listings_cleaned = remove_negatives(listings_cleaned, 'ClosePrice', 'LivingArea', 'DaysOnMarket', 'BedroomsTotal', 'BathroomsTotalInteger')
solds_cleaned = remove_negatives(solds_cleaned, 'ClosePrice', 'LivingArea', 'DaysOnMarket', 'BedroomsTotal', 'BathroomsTotalInteger')

def add_date_flags(df):
    # Only run checks if the needed columns exist
    has_all = all(c in df.columns for c in ['ListingContractDate', 'PurchaseContractDate', 'CloseDate'])
    if not has_all:
        print("Skipping: missing one or more date columns")
        return df

    df['listing_after_close_flag'] = df['ListingContractDate'] > df['CloseDate']

    df['purchase_after_close_flag'] = df['PurchaseContractDate'] > df['CloseDate']

    # 3. Negative timeline: the sequence Listing -> Purchase -> Close is broken anywhere
    df['negative_timeline_flag'] = (
        (df['ListingContractDate'] > df['PurchaseContractDate']) |
        (df['PurchaseContractDate'] > df['CloseDate']) |
        (df['ListingContractDate'] > df['CloseDate']))

    return df

solds_cleaned = add_date_flags(solds_cleaned)
listings_cleaned = add_date_flags(listings_cleaned)

def geog_data(df):
    df['missing_long_or_lat'] = df['Longitude'].isnull() | df['Latitude'].isnull()
    df['zero_long_or_lat'] = (df['Longitude'] == 0) | (df['Latitude'] == 0)
    df['negative_long'] = df['Longitude'] < 0
    CA_LAT_MIN, CA_LAT_MAX = 32.5, 42.0
    CA_LON_MIN, CA_LON_MAX = -124.5, -114.1
    outside_box = ~df['Latitude'].between(CA_LAT_MIN, CA_LAT_MAX) | ~df['Longitude'].between(CA_LON_MIN, CA_LON_MAX)
    df['out_of_state_flag'] = outside_box & ~df['missing_long_or_lat'] & ~df['zero_long_or_lat'] & ~df['negative_long']
    return df

listings_cleaned_and_flagged = geog_data(listings_cleaned)
solds_cleaned_and_flagged = geog_data(solds_cleaned)

total_geog_flags1 = sum([listings_cleaned_and_flagged['missing_long_or_lat'].sum(), listings_cleaned_and_flagged['zero_long_or_lat'].sum(), listings_cleaned_and_flagged['negative_long'].sum(), listings_cleaned_and_flagged['out_of_state_flag'].sum()])
print("Total geographic flags in listings:", total_geog_flags1)
total_geog_flags2 = sum([solds_cleaned_and_flagged['missing_long_or_lat'].sum(), solds_cleaned_and_flagged['zero_long_or_lat'].sum(), solds_cleaned_and_flagged['negative_long'].sum(), solds_cleaned_and_flagged['out_of_state_flag'].sum()])
print("Total geographic flags in solds:", total_geog_flags2)

listings_cleaned_and_flagged.to_csv('C:/Users/famil/OneDrive/Desktop/Python Workspace/IDX Exchange/Week 4-5/Week 4 Output/listings_cleaned_and_flagged.csv', index = False)
solds_cleaned_and_flagged.to_csv('C:/Users/famil/OneDrive/Desktop/Python Workspace/IDX Exchange/Week 4-5/Week 4 Output/solds_cleaned_and_flagged.csv', index = False)

print("Number of columns after cleaning:", f'listings: {len(listings_cleaned_and_flagged.columns)}, solds: {len(solds_cleaned_and_flagged.columns)}')
print("Number of rows after cleaning:", f'listings: {len(listings_cleaned_and_flagged)}, solds: {len(solds_cleaned_and_flagged)}')