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
gain = 0
for key in list(gain_project):
    gain = gain + gain_project[key].x


max_duration = 0
for t in range(horizon):
    max_duration = max_duration + START_PLAN[t, long_proj].x - LP[t, long_proj].x


print("Gain : " + str(gain))

#print(job_day)
#print(START_PLAN)

print("Longer project : " + long_proj)
print("Max duration : " + str(max_duration))

print("________")
print("NB project per employe")

for x in list(nb_proj_per_employe):
    print(str(x) + ' : ' + str(nb_proj_per_employe[x].x))