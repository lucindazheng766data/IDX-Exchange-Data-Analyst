import pandas as pd

listing1 = pd.read_csv("csv/CRMLSListing202401.csv")
listing2 = pd.read_csv("csv/CRMLSListing202402.csv")
listing3 = pd.read_csv("csv/CRMLSListing202403.csv")
listing4 = pd.read_csv("csv/CRMLSListing202404.csv")
listing5 = pd.read_csv("csv/CRMLSListing202405.csv")
listing6 = pd.read_csv("csv/CRMLSListing202406.csv")
listing7 = pd.read_csv("csv/CRMLSListing202407.csv")
listing8 = pd.read_csv("csv/CRMLSListing202408.csv")
listing9 = pd.read_csv("csv/CRMLSListing202409.csv")
listing10 = pd.read_csv("csv/CRMLSListing202410.csv")
listing11 = pd.read_csv("csv/CRMLSListing202411.csv")
listing12 = pd.read_csv("csv/CRMLSListing202412.csv")
listing13 = pd.read_csv("csv/CRMLSListing202501.csv")
listing14 = pd.read_csv("csv/CRMLSListing202502.csv")
listing15 = pd.read_csv("csv/CRMLSListing202503.csv")
listing16 = pd.read_csv("csv/CRMLSListing202504.csv")
listing17 = pd.read_csv("csv/CRMLSListing202505.csv")
listing18 = pd.read_csv("csv/CRMLSListing202506.csv")
listing19 = pd.read_csv("csv/CRMLSListing202507.csv")
listing20 = pd.read_csv("csv/CRMLSListing202508.csv")
listing21 = pd.read_csv("csv/CRMLSListing202509.csv")
listing22 = pd.read_csv("csv/CRMLSListing202510.csv")
listing23 = pd.read_csv("csv/CRMLSListing202511.csv")
listing24 = pd.read_csv("csv/CRMLSListing202512.csv")
listing25 = pd.read_csv("csv/CRMLSListing202601.csv")
listing26 = pd.read_csv("csv/CRMLSListing202602.csv")
listing27 = pd.read_csv("csv/CRMLSListing202603.csv")
listing28 = pd.read_csv("csv/CRMLSListing202604.csv")
sold1 = pd.read_csv("csv/CRMLSSold202401_filled.csv")
sold2 = pd.read_csv("csv/CRMLSSold202402.csv")
sold3 = pd.read_csv("csv/CRMLSSold202403_filled.csv")
sold4 = pd.read_csv("csv/CRMLSSold202404_filled.csv")
sold5 = pd.read_csv("csv/CRMLSSold202405_filled.csv")
sold6 = pd.read_csv("csv/CRMLSSold202406_filled.csv")
sold7 = pd.read_csv("csv/CRMLSSold202407_filled.csv")
sold8 = pd.read_csv("csv/CRMLSSold202408.csv")
sold9 = pd.read_csv("csv/CRMLSSold202409.csv")
sold10 = pd.read_csv("csv/CRMLSSold202410.csv")
sold11 = pd.read_csv("csv/CRMLSSold202411.csv")
sold12 = pd.read_csv("csv/CRMLSSold202412.csv")
sold13 = pd.read_csv("csv/CRMLSSold202501_filled.csv")
sold14 = pd.read_csv("csv/CRMLSSold202502.csv")
sold15 = pd.read_csv("csv/CRMLSSold202503.csv")
sold16 = pd.read_csv("csv/CRMLSSold202504.csv")
sold17 = pd.read_csv("csv/CRMLSSold202505.csv")
sold18 = pd.read_csv("csv/CRMLSSold202506.csv")
sold19 = pd.read_csv("csv/CRMLSSold202507.csv")
sold20 = pd.read_csv("csv/CRMLSSold202508.csv")
sold21 = pd.read_csv("csv/CRMLSSold202509.csv")
sold22 = pd.read_csv("csv/CRMLSSold202510.csv")
sold23 = pd.read_csv("csv/CRMLSSold202511.csv")
sold24 = pd.read_csv("csv/CRMLSSold202512.csv")
sold25 = pd.read_csv("csv/CRMLSSold202601.csv")
sold26 = pd.read_csv("csv/CRMLSSold202602.csv")
sold27 = pd.read_csv("csv/CRMLSSold202603.csv")
sold28 = pd.read_csv("csv/CRMLSSold202604.csv")

listings = [listing1, listing2, listing3, listing4, listing5, listing6, listing7, listing8, listing9, listing10, listing11, listing12, listing13, listing14, listing15, listing16, listing17, listing18, listing19, listing20, listing21, listing22, listing23, listing24, listing25, listing26, listing27, listing28]

listing_before_concat = 0
for i in listings:
    listing_before_concat = listing_before_concat + len(i)

print(listing_before_concat)

listing_concat = pd.concat([listing1, listing2, listing3, listing4, listing5, listing6, listing7, listing8, listing9, listing10, listing11, listing12, listing13, listing14, listing15, listing16, listing17, listing18, listing19, listing20, listing21, listing22, listing23, listing24, listing25, listing26, listing27, listing28])

listing_after_concat = len(listing_concat)
print(listing_after_concat)
#row count for listing is 860898 before and after concatenation

solds = [sold1, sold2, sold3, sold4, sold5, sold6, sold7, sold8, sold9, sold10, sold11, sold12, sold13, sold14, sold15, sold16, sold17, sold18, sold19, sold20, sold21, sold22, sold23, sold24, sold25, sold26, sold27, sold28]

sold_before_concat = 0

for i in solds:
    sold_before_concat = sold_before_concat + len(i)

print(sold_before_concat)

sold_concat = pd.concat([sold1, sold2, sold3, sold4, sold5, sold6, sold7, sold8, sold9, sold10, sold11, sold12, sold13, sold14, sold15, sold16, sold17, sold18, sold19, sold20, sold21, sold22, sold23, sold24, sold25, sold26, sold27, sold28])

sold_after_concat = len(sold_concat)
print(sold_after_concat)
#Row count for solds is 615707 for before and after concatenation

 #We have verified that the row count matches before and after concatenation for both the listings and sold databases. Yippee!

#Run to see what categories are under PropertyType and if there's any typos
print(listing_concat['PropertyType'].unique())
print(sold_concat['PropertyType'].unique())


listing_residential = listing_concat[listing_concat['PropertyType'] == 'Residential']

sold_residential = sold_concat[sold_concat['PropertyType'] == 'Residential']

print(len(listing_residential))
print(len(sold_residential))

#The rows in the listing dataset after the filtering is 547162 and the rows in the sold dataset after the filtering in 414054. The filter excluded ~36% of rows for listing and ~33% of rows for sold. 

listing_residential.to_csv('agg_filtered_listings.csv', index = False)

sold_residential.to_csv('agg_filtered_solds.csv', index = False)