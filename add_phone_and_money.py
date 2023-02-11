import random
import pandas as pd

def phn():
    n = '000000000'
    while n[3:6]=='000' or n[6]==n[7]==n[8]:
        n = str(random.randint(10**8, 10**9-1))
    return '0' + n[:3] + n[3:6] + n[6:]

df = pd.read_csv('seller.csv')
df['Phone'] = [phn() for i in range(len(df))]
df['Money'] = [random.randint(0,1000000) for i in range(len(df))]
df = df[['NameUser','Address','Avatar','Phone','Money']]
df.to_csv('seller_phone_money.csv', index=False)
print(df)