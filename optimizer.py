#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 09:44:03 2023

@author: valentin
"""
from gurobipy import *
from data_loader import *
from instance_generator import * 

#instance = load_medium_data()
instance = create_new_instance(10, 4, 5, 4)
print(instance)

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

def create_competences_per_employe():
    """competences per employe"""
    competences = dict()
    for employe in instance['staff']:
        competences[employe['name']] = employe['qualifications']
    return competences

def create_competences_per_job():
    """competences per job"""
    competences = dict()
    for job in instance['jobs']:
        competences[job['name']] = list(job['working_days_per_qualification'])
    return competences

def create_number_of_competences_per_job():
    """competences per job"""
    competences = dict()
    for job in instance['jobs']:
        competences[job['name']] = job['working_days_per_qualification']
    return competences

def create_due_date_of_jobs():
    """competences per job"""
    due_dates = dict()
    for job in instance['jobs']:
        due_dates[job['name']] = job['due_date']
    return due_dates

def create_gains_per_jobs():
    """gains per job"""
    gains = dict()
    for job in instance['jobs']:
        gains[job['name']] = job['gain']
    return gains

def create_delays_per_jobs():
    """gains per job"""
    daily_penalties = dict()
    for job in instance['jobs']:
        daily_penalties[job['name']] = job['daily_penalty']
    return daily_penalties

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
list_horizon = [i for i in range (1, horizon + 1)]

nb_comp = len(list_comp)

L = []
for pers in list_pers:
    for t in list_horizon:
        for p in list_job:
            for c in list_comp:
                L.append((pers, t, p, c))

# person x time x job x competence
possibility = tuplelist(L)


L2 = []

for t in list_horizon:
    for p in list_job:
        for c in list_comp:
            L2.append((t, p, c))

# time x job x competence
possibility_reduced = tuplelist(L2)

L3 = []

for t in list_horizon:
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

Y = m.addVars(list_job, vtype=GRB.BINARY, lb = 0, name='s')

L = m.addVars(list_job, vtype=GRB.INTEGER, lb = 0, name='s')

E = m.addVars(list_job, vtype=GRB.INTEGER, lb = 0, ub = horizon , name='s')

START_MAT = m.addVars(possibility_reduced2, vtype=GRB.INTEGER,lb = -100, name='start_matrix')
START_PLAN = m.addVars(possibility_reduced2, vtype=GRB.BINARY, name='start_planning')
S = m.addVars(list_job, vtype=GRB.INTEGER, lb = 0, ub = horizon , name='s')

#objectif 2 nombre de projets par employé

# project per employe
proj_employe = m.addVars(possibility_reduced4,vtype=GRB.INTEGER,lb = 0)
proj_employe_count = m.addVars(possibility_reduced4,vtype=GRB.BINARY)

# constraints

# une personne par projet par jour
m.addConstrs(X.sum(pers,t,'*','*') <= 1 for pers in list_pers for t in list_horizon)

# vacances
vacations = create_vacations()
m.addConstrs(X.sum(pers,t,'*','*') == 0 for pers in list_pers for t in vacations[pers])

# une personne ne travaille pas sur un job inutile ou pour lequel elle n'est pas qualifiée
competence_per_employe = create_competences_per_employe() 
competence_per_job = create_competences_per_job() 

for pers in list_pers:
    for day in list_horizon:  
        for job in list_job:
            for comp in list_comp:
                if not (comp in competence_per_employe[pers]) or not (comp in competence_per_job[job]):
                    m.addConstr(X[pers, day, job, comp] == 0)

number_of_competence_per_project = create_number_of_competences_per_job()

for job in list_job:
    for comp in competence_per_job[job]:
        m.addConstr(Y[job] * number_of_competence_per_project[job][comp] <= X.sum('*','*', job,comp))
        m.addConstr(X.sum('*','*', job,comp) <= number_of_competence_per_project[job][comp])


m.addConstrs(X[pers, day, job, comp] * (day) <= E[job] for pers in list_pers for day in list_horizon for job in list_job for comp in list_comp)

due_dates = create_due_date_of_jobs()
m.addConstrs(E[job] - due_dates[job] <= L[job] for job in list_job)

#constraint nombre de projets par employés
nb_proj_per_employe = m.addVars(list_pers,vtype=GRB.INTEGER,lb = 0)
m.addConstrs(proj_employe[pers, proj] == X.sum(pers,'*',proj,'*') for pers in list_pers for proj in list_job)
m.addConstrs(proj_employe_count[pers, proj] == min_(proj_employe[pers, proj],1) for pers in list_pers for proj in list_job)
m.addConstrs(nb_proj_per_employe[pers] == proj_employe_count.sum(pers, '*') for pers in list_pers)

# constraint number of day of the longest project
# Start matrix planning
m.addConstrs(START_MAT[T, job] == quicksum(X[pers, t, job, comp] for t in range (1,T) for pers in list_pers for comp in list_comp) for index_job, job in enumerate(list_job) for T in list_horizon)

m.addConstrs(START_PLAN[T, job] == min_(START_MAT[T, job],1) for index_job, job in enumerate(list_job) for T in list_horizon)

m.addConstrs(S[job] == horizon - START_PLAN.sum('*', job) for job in list_job)

# add start date project
def duration_max_project(job, E, S):
    duration = E[job] - S[job]
    return duration

# gain
gain_per_job = create_gains_per_jobs()
delay_per_job = create_delays_per_jobs()

def gain_project(Y, L):
    res = 0
    for job in list_job:
        res = res + Y[job] * gain_per_job[job] - L[job] * delay_per_job[job]
    return res

m.update()

# Fonction Objectifs
m.setObjective(gain_project(Y, L), GRB.MAXIMIZE)  

# m.setObjective(gain_project(Y, L), 0, 3, -1)  
# m.setObjectiveN(nb_proj_per_employe.sum('*'), 1, 2, 1)
# m.setObjectiveN(duration_max_project(get_longest_project(), E, S), 2, 1, 1)

# Résolution du PL
m.optimize()



