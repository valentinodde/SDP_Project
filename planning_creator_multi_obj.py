from optimizer_multi_obj import *
from data_loader import *
import pandas as pd

instance = load_medium_data()


horizon = instance['horizon']
list_pers = [p['name'] for p in instance['staff']]
list_comp = instance['qualifications']
list_job = [p['name'] for p in instance['jobs']]

gain_per_job = create_gains_per_jobs(instance)
delay_per_job = create_delays_per_jobs(instance)
def gain_project(Y, L):
    res = 0
    for job in list_job:
        res = res + Y[job].x * gain_per_job[job] - L[job].x * (delay_per_job[job])
    return res

# m, X,Y,L = optimisation(instance,1, 1)
# print(gain_project(Y,L))

grid = []
X_grid = []
Y_grid = []


for constr_longest_proj in range (1,horizon):
    row = []
    row_X = []
    row_Y = []
    for constr_proj_per_employe in range (1, len(instance['jobs'])):
        row_X.append(constr_longest_proj)
        row_Y.append(constr_proj_per_employe)
        try:
            m, X,Y,L = optimisation(instance,constr_longest_proj, constr_proj_per_employe)
            row.append(gain_project(Y,L))
            
            print(constr_longest_proj)
            print(constr_proj_per_employe)
            print(gain_project(Y,L))
            print('____')
        except:
            row.append(0)
    X_grid.append(row_X)
    grid.append(row)
    Y_grid.append(row_Y)
    

print(grid)
print(X_grid)
print(Y_grid)


# edt = dict()
# for employe in list_pers:
#     edt[employe] = [None for day in list_horizon]
# for key in list(X):
#     if X[key].x>0.5:
        
#         edt[key[0]][key[1] - 1] = (key[2],key[3])

# df = pd.DataFrame.from_dict(edt, orient='index')

# df.to_csv('planning.csv')

# print(df)



# gain= gain_project(Y, L)
# print("gain:", gain)


# max_duration = 0
# for t in range(horizon):
#     max_duration = max_duration + START_PLAN[t, long_proj].x - LP[t, long_proj].x


# print("Gain : " + str(gain))

# #print(job_day)
# #print(START_PLAN)

# print("Longer project : " + long_proj)
# print("Max duration : " + str(max_duration))

# print("________")
# print("NB project per employe")

# for x in list(nb_proj_per_employe):
#     print(str(x) + ' : ' + str(nb_proj_per_employe[x].x))