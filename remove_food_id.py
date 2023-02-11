import pandas as pd
df = pd.read_csv('dish.csv')
df = df[['UserId','CategoryId','NameFood','PriceFood','ImageFood','DescriptionFood']]
df.to_csv('food_no_id.csv', index=False)
print(df)