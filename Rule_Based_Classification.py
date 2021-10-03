import pandas as pd

# add the absolute path here
df = pd.read_csv("...\persona.csv")


def check_df(dataframe, head=5):
    print("##################### Info #####################")
    print(dataframe.info())
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.25, 0.50, 0.75, 0.95, 1]).T)


check_df(df)

# How many unique Sources are there? What are their frequencies?
print(len(df['SOURCE'].unique()))
print(df['SOURCE'].value_counts())

# How many unique Prices are there?
print(len(df['PRICE'].unique()))

# How many sales were made from which PRICE?
print(df['PRICE'].value_counts())

# How many sales were made from which Country?
print(df['COUNTRY'].value_counts())

# How much was earned in total from sales by country?
print(df.groupby('COUNTRY')['PRICE'].sum())

# What are the sales numbers by Source types?
print(df['SOURCE'].value_counts())

# What are the Price averages by country?
print(df.groupby('COUNTRY')['PRICE'].mean())

# What are the Price averages by Sources?
print(df.groupby('SOURCE')['PRICE'].mean())

# What are the Price averages in the Country-Source breakdown?
print(df.pivot_table(values='PRICE', index='COUNTRY', columns='SOURCE', aggfunc='mean'))

# In the COUNTRY, SOURCE, SEX, AGE breakdown, What are average earnings?
print(df.pivot_table(values='PRICE', index=['COUNTRY', 'SOURCE', 'SEX', 'AGE'], aggfunc='mean'))

# Sorting
agg_df = df.pivot_table(values='PRICE', index=['COUNTRY', 'SOURCE', 'SEX', 'AGE'], aggfunc='mean')\
                        .sort_values('PRICE', ascending=False)
print(agg_df.head())

# Converting the names in the index to variable names.
agg_df.reset_index(inplace=True)

# Converting the age variable to categorical variable and adding it to agg_df.
agg_df['AGE_CAT'] = pd.cut(x=agg_df['AGE'], bins=[15, 19, 25, 34, 66], right=False,
                           labels=['15_19', '20_25', '26_34', '35_66'])
agg_df.head()

# Identifying new level-based customers (Personas).
agg_df['customers_level_based'] = [str(row[0]).upper() + "_" + str(row[1]).upper() + "_" + str(row[2]).upper() + "_" +
                                   str(row[5]).upper() for row in agg_df.values]

agg_df = pd.DataFrame(agg_df.groupby('customers_level_based')['PRICE'].mean())
agg_df.reset_index(inplace=True)

# Segment new customers (Personas).

agg_df['SEGMENT'] = pd.qcut(x=agg_df['PRICE'], q=4, labels=["D", "C", "B", "A"])

agg_df.groupby('SEGMENT')['PRICE'].agg(['mean', 'max', 'sum'])

# Descriptive statics of a spesific segment can be analysed.
c_seg = agg_df[agg_df['SEGMENT'] == "C"]
c_seg_summary = agg_df[agg_df['SEGMENT'] == "C"].describe().T

# Ex: In which segment and on average how much income would a 35-year-old French woman using IOS expect to earn?
new_user = "FRA_IOS_FEMALE_35_66"
print(agg_df[agg_df["customers_level_based"] == new_user])
# >>> C segment, expecting to earn 33.0 $ on average.
