#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 09:44:03 2023

@author: valentin
"""
from gurobipy import *
from data_loader import *

instance = load_small_data()

def create_qualifications(data):
    qualifs = []
    for staff_member in data['staff']:
        qualifs.append([1 if q in staff_member['qualifications'] else 0 for q in list(data['qualifications'])])
    return qualifs


def working_days_per_qualification(data):
    CP = list() 
    for job in data['jobs']:
        CPi = list()
        for qualification in data['qualifications']:
            if qualification in job['working_days_per_qualification']:
                CPi.append(job['working_days_per_qualification'][qualification])
            else:
                CPi.append(0)
        CP.append(CPi)
    return CP



def create_vacations():
    """A staff member cannot work during his holidays"""
    vacations = dict()
    for employe in instance['staff']:
        vacations[employe['name']] = employe['vacations']
    return vacations

def get_longest_project():
    max_score = 0
    longest_project = None
    for job in instance['jobs']:
        qualifs = job['working_days_per_qualification']
        score = 0
        for qualif in qualifs:
            score +=qualifs[qualif]
        if score > max_score:
            max_score = score
            longest_project = job['name']
    return (longest_project)

def get_job_day():
    job_day = dict()
    for job in instance['jobs']:
        s=0
        for key in list(job['working_days_per_qualification']):
            s = s + job['working_days_per_qualification'][key]
        job_day[job['name']] = s
    return job_day

job_day = get_job_day()

long_proj = max(job_day, key=job_day.get)


CP = working_days_per_qualification(instance)
vacations = create_vacations()





horizon = instance['horizon']
list_pers = [p['name'] for p in instance['staff']]
list_comp = instance['qualifications']
list_job = [p['name'] for p in instance['jobs']]

nb_comp = len(list_comp)

L = []
for pers in list_pers:
    for t in range(horizon):
        for p in list_job:
            for c in list_comp:
                L.append((pers, t, p, c))

# person x time x job x competence
possibility = tuplelist(L)


L2 = []

for t in range(horizon):
    for p in list_job:
        for c in list_comp:
            L2.append((t, p, c))

# time x job x competence
possibility_reduced = tuplelist(L2)

L3 = []

for t in range(horizon):
    for p in list_job:
        L3.append((t, p))

# time x job
possibility_reduced2 = tuplelist(L3)

L4 = []

for pers in list_pers:
    for p in list_job:
        L4.append((pers, p))

# pers x job
possibility_reduced4 = tuplelist(L4)



m = Model()

# planning
X = m.addVars(possibility, name='x', vtype=GRB.BINARY)

S = m.addVars(possibility_reduced, vtype=GRB.INTEGER, lb = 0, name='s')

LP_MIN = m.addVars(possibility_reduced2, vtype=GRB.INTEGER,lb = -100, name='lpm')


START_MAT = m.addVars(possibility_reduced2, vtype=GRB.INTEGER,lb = -100, name='start_matrix')
START_PLAN = m.addVars(possibility_reduced2, vtype=GRB.BINARY, name='start_planning')



#vacation days
m.addConstrs(X.sum(pers,t,'*','*') == 0 for pers in list_pers for t in range(horizon) if t+1 in vacations[pers])


# Matrice de projet au cours du temps : vaut 1 à partir du moment où le projet est fini
LP = m.addVars(possibility_reduced2, vtype=GRB.BINARY,name='lp')


# Donne pour chaque projet sa date de fin moins 1 et vaut horizon si il n'est pas fini
timeline_project = m.addVars(list_job,vtype=GRB.INTEGER,lb = 0)



delay_project_temp = m.addVars(list_job,vtype=GRB.INTEGER,lb = -100)

# donne les jours de retard pour chaque projets
delay_project = m.addVars(list_job,vtype=GRB.INTEGER,lb = -horizon)


# project per employe
proj_employe = m.addVars(possibility_reduced4,vtype=GRB.INTEGER,lb = 0)
proj_employe_count = m.addVars(possibility_reduced4,vtype=GRB.BINARY)

nb_proj_per_employe = m.addVars(list_pers,vtype=GRB.INTEGER,lb = 0)



# variable pour modéliser le if
b = m.addVars(list_job, vtype=GRB.BINARY)

# donne le gain pour chaque projet
gain_project = m.addVars(list_job,lb = -100)




m.update()


# une personne par projet et par jour
m.addConstrs(X.sum(pers,t,'*','*') <= 1 for pers in list_pers for t in range(horizon))


# une personne travail sur des projet où elle a les compétences
qualifs = create_qualifications(instance)
m.addConstrs(qualifs[i][j] >= X[pers,t,job,comp] for i,pers in enumerate(list_pers) for t in range(horizon) for j,comp in enumerate(list_comp) for job in list_job)


#avancement du projet
m.addConstrs((LP_MIN[T, job] == (quicksum(X[pers, t, job, comp] for t in range(T+1) for pers in list_pers for comp in list_comp) - quicksum(CP[index_job][index_comp] for index_comp in range(nb_comp)) + 1))  for index_job, job in enumerate(list_job) for T in range(horizon))

#contrainte sur les compétences : pas plus que nécessaire sur chaque projet
m.addConstrs(CP[index_job][index_comp] >= quicksum(X[pers,t,job,comp] for pers in list_pers for t in range(horizon)) for index_comp,comp in enumerate(list_comp) for index_job,job in enumerate(list_job))

#construction of LP
m.addConstrs(LP[T, job] == max_(LP_MIN[T, job],0) for T in range(horizon) for job in list_job)

# construct timeline project
#m.addConstrs(timeline_project[proj] == horizon - LP.sum('*',proj) for proj in list_job)
m.addConstrs(timeline_project[proj] == horizon - quicksum(LP[day,proj] for day in range(horizon)) for proj in list_job)


# calculate project delay
# verifier la ligne suivante +1 ou - 1...???
m.addConstrs(delay_project_temp[proj] == (instance['jobs'][i]['due_date']-timeline_project[proj] - 1) for i, proj in enumerate(list_job))
m.addConstrs(delay_project[proj] == min_(delay_project_temp[proj],0) for i, proj in enumerate(list_job))


# big M method to model if
M = horizon

m.addConstrs(timeline_project[proj] >= horizon - M * (1 - b[proj]) for i, proj in enumerate(list_job))
m.addConstrs(timeline_project[proj] <= horizon-1 + M * b[proj] for i, proj in enumerate(list_job))

m.addConstrs((b[proj] == 1) >> (gain_project[proj] == 0) for i, proj in enumerate(list_job))
m.addConstrs((b[proj] == 0) >> (gain_project[proj] == instance['jobs'][i]['gain'] + delay_project[proj]*instance['jobs'][i]['daily_penalty']) for i, proj in enumerate(list_job))

# Start matrix planning
m.addConstrs(START_MAT[T, job] == quicksum(X[pers, t, job, comp] for t in range(T+1) for pers in list_pers for comp in list_comp) for index_job, job in enumerate(list_job) for T in range(horizon))

m.addConstrs(START_PLAN[T, job] == min_(START_MAT[T, job],1) for index_job, job in enumerate(list_job) for T in range(horizon))

# add start date project
def duration_max_project(project_name, M_END, M_START):
    duration = M_START.sum('*', project_name) - M_END.sum('*', project_name)
    return duration


# project per employe

m.addConstrs(proj_employe[pers, proj] == X.sum(pers,'*',proj,'*') for pers in list_pers for proj in list_job)
m.addConstrs(proj_employe_count[pers, proj] == min_(proj_employe[pers, proj],1) for pers in list_pers for proj in list_job)
m.addConstrs(nb_proj_per_employe[pers] == proj_employe_count.sum(pers, '*') for pers in list_pers)

m.update()

# Fonction Objectifs

m.setObjectiveN(gain_project.sum('*'),0, 3, -1)  
m.setObjectiveN(nb_proj_per_employe.sum('*'), 1, 2, 1)
m.setObjectiveN(duration_max_project(get_longest_project(), LP, START_PLAN), 2, 1, 1)

# Résolution du PL
m.optimize()




















