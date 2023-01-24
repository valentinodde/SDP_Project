
from data_loader import load_small_data
from gurobipy import *

m = Model("Simple PL modelling")
instance = load_small_data()
nb_pers = len(instance['staff'])
nb_proj = len(instance['jobs'])
nb_comp = len(instance['qualifications'])
horizon = instance['horizon']

# creation of ref functions
def create_qualifications(data):
    qualifs = []
    for staff_member in data['staff']:
        qualifs.append([1 if q in staff_member['qualifications'] else 0 for q in list(data['qualifications'])])
    return qualifs

def give_projects_per_qualification(data):
    projects_per_qualification = list() 
    for job in data['jobs']:
        project_i_per_qualification = list()
        for qualification in data['qualifications']:
            if qualification in job['working_days_per_qualification']:
                project_i_per_qualification.append(job['working_days_per_qualification'][qualification])
            else:
                project_i_per_qualification.append(0)
        projects_per_qualification.append(project_i_per_qualification)
    return projects_per_qualification

# creation of vars
def create_var_plannning():
    planning=[]
    for pers in instance['staff']:
        row = []
        for t in range(horizon):
            proj=[]
            for p in range(nb_proj):
                comp = []
                for c in range(nb_comp):
                    comp.append(m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name=pers['name']+'_time:'+str(t)+'_comp:'+str(c)+'_proj:'+str(p)))
                proj.append(comp)      
            row.append(proj)
        planning.append(row)
    return planning
        
def create_var_project_through_time():
    projects_through_time = []
    for i in range(nb_proj):
        project_i_through_time = []
        for t in range(horizon):                     
            project_i_through_time.append(m.addVar(lb=0,ub=1,vtype=GRB.INTEGER, name='Project:'+str(i)+'_time:'+str(t)))
        projects_through_time.append(project_i_through_time)
    return projects_through_time

# creation of constraints 
def working_time(t,s):
    time = 0
    for p in range(nb_proj):
        for c in range(nb_comp):
            time += planning[s][t][p][c]
    return time

def create_unicity_constraint():
    """Each person can only work on one project with one skill at a time"""
    for t in range(horizon):
        for s in range(nb_pers):
            m.addConstr(working_time(t,s) <= 1)
    return

def create_qualification_constraint():
    """A staff member can only be appointed to a project he is qualified for"""
    for t in range(horizon):
        for s in range(nb_pers):
            for c in range(nb_comp):
                for p in range(nb_proj):
                    m.addConstr(qualifs[s][c] >= planning[s][t][p][c])
    return

def create_vacations_constraint():
    """A staff member cannot work during his holidays"""
    for index_employe,employe in enumerate(instance['staff']):
        vacations = employe['vacations']
        for day in vacations:
            for project in range (nb_proj):
                for competence in range(nb_comp):
                    m.addConstr(planning[index_employe][day-1][project][competence] == 0, name="vacations_constr" + str(employe))
    return

def create_evolution_of_projects_constraints():
    """Project evolution through time"""
    for time in range (horizon):
        for project in range (nb_proj):
            evolution = 0
            for employe in range (nb_pers):
                for competence in range (nb_comp):
                    for day in range (time):
                        evolution += planning[employe][day][project][competence]
                        print(evolution)
            #print(evolution)
            m.addConstr(projects_through_time == evolution)
    return

# creation of objective function
def progress_of_projects(plan,T,p,c):
    progress = 0
    for t in range(T):
        for i in range(nb_pers):
            progress += plan[i][t][p][c]
    return progress

def compute_time_to_finish_project(projects_through_time):
    res = []
    for i in range(nb_proj):
        res.append(horizon - sum(projects_through_time[i]) + 1)
    return res

def compute_gain(projects_done, data):
    gain = 0
    for i in range(len(projects_done)):
        g = projects_done[i]
        job = data['jobs'][i]
        #if g <= horizon :
        # gain += job['gain'] + min(0, (job['due_date'] - g) * job['daily_penalty'])     
        #print(gain_min[i])
        #gain += min_(horizon + 1 - g, 1)*(job['gain'] + gain_min[i] * job['daily_penalty'])  
        gain += (horizon + 1 - g)*(job['gain'] + (job['due_date'] - g) * job['daily_penalty'])  
    return gain

def gain(projects_through_time):
    return compute_gain(compute_time_to_finish_project(projects_through_time),instance)

projects_per_qualification = give_projects_per_qualification(instance)
planning = create_var_plannning()
projects_through_time = create_var_project_through_time()
# maj du modèle
m.update()
# ajout des contraintes
create_unicity_constraint()
qualifs = create_qualifications(instance)
create_qualification_constraint()
create_vacations_constraint()
create_evolution_of_projects_constraints()
# ajout des fonctions objectifs
gain(projects_through_time)
m.update()
m.setObjective(gain(projects_through_time), GRB.MAXIMIZE)  
# Résolution du PL
m.optimize()
