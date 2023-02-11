import pandas as pd
import re
import unicodedata
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

df = list(pd.read_csv('seller_phone_money.csv')['NameUser'])
df += ['thefour','tien','quang','thinh','minh','shipper1','shipper2','shipper3','shipper4']
account = []
for i in df:
    res = strip_accents(i).lower()
    res = re.sub('[-| ]','',res) + "@gmail.com"
    account.append(res)


ans = pd.DataFrame({'Email':account, 'Password': ["123456",]*len(df)})
print(ans)
ans.to_csv('account.csv', index=False)