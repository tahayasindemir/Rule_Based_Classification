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

print(len(df['SOURCE'].unique()))
print(df['SOURCE'].value_counts())


print(len(df['PRICE'].unique()))


print(df['PRICE'].value_counts())


print(df['COUNTRY'].value_counts())


print(df.groupby('COUNTRY')['PRICE'].sum())


print(df['SOURCE'].value_counts())


print(df.groupby('COUNTRY')['PRICE'].mean())


print(df.groupby('SOURCE')['PRICE'].mean())

print(df.pivot_table(values='PRICE', index='COUNTRY', columns='SOURCE', aggfunc='mean'))


print(df.pivot_table(values='PRICE', index=['COUNTRY', 'SOURCE', 'SEX', 'AGE'], aggfunc='mean'))


agg_df = df.pivot_table(values='PRICE', index=['COUNTRY', 'SOURCE', 'SEX', 'AGE'], aggfunc='mean')\
                        .sort_values('PRICE', ascending=False)
print(agg_df.head())


agg_df.reset_index(inplace=True)


agg_df['AGE_CAT'] = pd.cut(x=agg_df['AGE'], bins=[15, 19, 25, 34, 66], right=False,
                           labels=['15_19', '20_25', '26_34', '35_66'])
agg_df.head()


agg_df['customers_level_based'] = [str(row[0]).upper() + "_" + str(row[1]).upper() + "_" + str(row[2]).upper() + "_" +
                                   str(row[5]).upper() for row in agg_df.values]

agg_df = pd.DataFrame(agg_df.groupby('customers_level_based')['PRICE'].mean())
agg_df.reset_index(inplace=True)


agg_df['SEGMENT'] = pd.qcut(x=agg_df['PRICE'], q=4, labels=["D", "C", "B", "A"])

agg_df.groupby('SEGMENT')['PRICE'].agg(['mean', 'max', 'sum'])


c_seg = agg_df[agg_df['SEGMENT'] == "C"]
c_seg_summary = agg_df[agg_df['SEGMENT'] == "C"].describe().T

new_user = "FRA_IOS_FEMALE_35_66"
print(agg_df[agg_df["customers_level_based"] == new_user])
