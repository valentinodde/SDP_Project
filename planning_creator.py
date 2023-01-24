from optimizer import *
from data_loader import *
import pandas as pd

instance = load_small_data()



horizon = instance['horizon']
list_pers = [p['name'] for p in instance['staff']]
list_comp = instance['qualifications']
list_job = [p['name'] for p in instance['jobs']]

edt = dict()
for employe in list_pers:
    edt[employe] = [None for day in range (horizon)]
for key in list(X):
    if X[key].x>0.5:
        edt[key[0]][key[1]] = (key[2],key[3])

df = pd.DataFrame.from_dict(edt, orient='index')

print(df)