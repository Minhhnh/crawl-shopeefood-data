from cgitb import enable
import numpy as np
import pandas as pd

group_id = [4]*123 + [5] + [2]*4 + [3]*4
account_id = np.arange(1,len(group_id)+1)
enable_group_detail = ["true",]* len(account_id)

ans = pd.DataFrame({'AccountId':account_id, 'GroupId': group_id})
print(ans)
ans.to_csv('group_detail.csv', index=False)