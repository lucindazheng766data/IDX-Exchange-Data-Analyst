import pandas as pd

agg_listings = pd.read_csv(r'C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Week 1\agg_filtered_listings.csv')
agg_solds = pd.read_csv(r'C:\Users\famil\OneDrive\Desktop\Python Workspace\IDX Exchange\Week 1\agg_filtered_solds.csv')
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']

mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (
 mortgage.groupby('year_month')['rate_30yr_fixed']
 .mean()
 .reset_index()
)

# Sold dataset — key off CloseDate
agg_solds['year_month'] = pd.to_datetime(agg_solds['CloseDate']).dt.to_period('M')

# Listings dataset — key off ListingContractDate
agg_listings['year_month'] = pd.to_datetime(agg_listings['ListingContractDate']).dt.to_period('M')

sold_with_rates = agg_solds.merge(mortgage_monthly, on='year_month', how='left')
listings_with_rates = agg_listings.merge(mortgage_monthly, on='year_month', how='left')

# Check for any unmatched rows (rate should not be null)
print(sold_with_rates['rate_30yr_fixed'].isnull().sum())
print(listings_with_rates['rate_30yr_fixed'].isnull().sum())

print(
 sold_with_rates[
 ['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']
 ].head()
 )

print(
 listings_with_rates[
 ['ListingContractDate', 'year_month', 'ListPrice', 'rate_30yr_fixed']
 ].head()
 )

sold_with_rates.to_csv('sold_with_rates.csv', index = False)
listings_with_rates.to_csv('listings_with_rates.csv', index = False)