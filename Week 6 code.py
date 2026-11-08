import pandas as pd
import geopandas as gpd
import numpy as np

listings = pd.read_csv(r"C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Week 4-5\Week 4 Output\listings_cleaned.csv")
solds = pd.read_csv(r"C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Week 4-5\Week 4 Output\solds_cleaned.csv")

def populate_metrics(df,):
    for col in ['CloseDate', 'PurchaseContractDate', 'ListingContractDate']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    if 'ClosePrice' in df.columns and 'OriginalListPrice' in df.columns:
        orig_list = df['OriginalListPrice'].replace(0, np.nan)
        df['Close to Original List Ratio'] = df['ClosePrice'] / orig_list

    if 'ClosePrice' in df.columns and 'LivingArea' in df.columns:
        living_area = df['LivingArea'].replace(0,np.nan)
        df['Price Per Sq Ft'] = df['ClosePrice'] / living_area

    if 'CloseDate' in df.columns:
        df['Year'] = df["CloseDate"].dt.year
        df['Month'] = df['CloseDate'].dt.month
        df['YrMo'] = df['CloseDate'].dt.to_period('M').astype(str)

    if 'PurchaseContractDate' in df.columns and 'ListingContractDate' in df.columns:
        df['Listing to Contract Days'] = (df['PurchaseContractDate'] - df['ListingContractDate']).dt.days

    if 'CloseDate' in df.columns and 'PurchaseContractDate' in df.columns:
        df['Contract to Close Days'] = (df['CloseDate'] - df['PurchaseContractDate']).dt.days

    return df

listings_metrics = populate_metrics(listings)
solds_metrics = populate_metrics(solds)

#check values of metrics
new_cols = ['Close to Original List Ratio', 'Price Per Sq Ft', 'Year', "Month", 'YrMo', 'Listing to Contract Days', 'Contract to Close Days']
print(listings_metrics[new_cols].head())
print(solds_metrics[new_cols].head())


#add school districts
districts = gpd.read_file(r'C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Long Lat Folder\DistrictAreas2425.shp')
districts = districts.to_crs('EPSG:4326')
districts = districts[['DistrictNa', 'DistrictTy', 'geometry']]

def add_school_districts(df):
    valid_mask = (df['Latitude'].notnull() & df['Longitude'].notnull() & (df['Latitude'] !=0) & (df['Longitude'] < 0))
    valid = df[valid_mask]

    points = gpd.GeoDataFrame(valid[[]], geometry = gpd.points_from_xy(valid['Longitude'], valid['Latitude']), crs = "EPSG:4326")

    joined = gpd.sjoin(points, districts, how = 'left', predicate = 'within')
    #stops overlapped districts
    joined = joined[~joined.index.duplicated(keep = 'first')]
    #merge back into original dfs
    df = df.join(joined[['DistrictNa', 'DistrictTy', ]])
    df = df.rename(columns = {'DistrictNa': "SchoolDistrict", 'DistrictTy': 'SchoolDistrictType'})

    return df

solds_metrics = add_school_districts(solds_metrics)
listings_metrics = add_school_districts(listings_metrics)

solds_metrics.to_csv('Solds_metrics.csv', index = False)
listings_metrics.to_csv('Listings_metrics.csv', index = False)

#independent metrics based on different categorical factors for solds 
def segment_summary(df, by):
    return (
        df.groupby(by)
        .agg(
            sales_count=('ClosePrice', 'count'),
            median_close_price=('ClosePrice', 'median'),
            avg_close_price=('ClosePrice', 'mean'),
            median_ppsf=('Price Per Sq Ft', 'median'),
            avg_close_to_orig_ratio=('Close to Original List Ratio', 'mean'),
            avg_days_on_market=('DaysOnMarket', 'mean'),
            avg_listing_to_contract=('Listing to Contract Days', 'mean'),
            avg_contract_to_close=('Contract to Close Days', 'mean'),
        )
        .round(2)
        .sort_values('sales_count', ascending=False)
        .reset_index()
    )

# Run it on the sold dataset, one dimension at a time
by_type = segment_summary(solds_metrics, 'PropertyType')
by_subtype = segment_summary(solds_metrics, 'PropertySubType')
by_county = segment_summary(solds_metrics, 'CountyOrParish')
by_area = segment_summary(solds_metrics, 'MLSAreaMajor')
by_list_office = segment_summary(solds_metrics, 'ListOfficeName')

print(by_county.head(10))
print(by_type.head(10))
print(by_subtype.head(10))
print(by_area.head(10))
print(by_list_office.head(10))

by_county.to_html('Solds_by_county.html', index = False)
by_type.to_html('Solds_by_type.html', index = False)
by_subtype.to_html("Solds_by_subtype.html", index = False)
by_area.to_html('Solds_by_area.html', index = False)
by_list_office.to_html('Solds_by_list_office.html', index = False)