import random

def create_new_instance(horizon, number_of_employe, number_of_projects, number_of_qualification):
    instance = dict()
    qualifications = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    instance['horizon'] = horizon
    instance['qualifications'] = [qualification for _, qualification in enumerate(qualifications[0:number_of_qualification])]
    instance['staff'] = list()
    staff_qualifications = []
    for employe in range (number_of_employe):
        instance['staff'].append(dict())
        instance['staff'][employe]['name'] = 'employe_' + str(employe)
        instance['staff'][employe]['qualifications'] = random.sample(instance['qualifications'], random.randint(1, number_of_qualification))
        number_of_vacation_days = random.randint(0, horizon//3)
        possible_vacation_days = [day for day in range(horizon)]
        instance['staff'][employe]['vacations'] = random.sample(possible_vacation_days, random.randint(0, number_of_vacation_days))
        for q in instance['staff'][employe]['qualifications']:
            if q not in staff_qualifications: staff_qualifications.append(q)
    instance['jobs'] = list()
    for job in range (number_of_projects):
        instance['jobs'].append(dict())
        instance['jobs'][job]['name'] = 'job_' + str(job)
        instance['jobs'][job]['gain'] = random.randint(10, 30)
        
        instance['jobs'][job]['daily_penalty'] = random.randint(1, 5)
        instance['jobs'][job]['working_days_per_qualification'] = dict()
        qualifications_for_the_job = random.sample(staff_qualifications, random.randint(1, len(staff_qualifications)))
        number_of_days_for_the_job = 0
        for qualification_for_the_job in qualifications_for_the_job:
            if horizon - number_of_days_for_the_job - len(qualifications_for_the_job) > 1:
                number_of_days_for_this_competence = random.randint(1, horizon - number_of_days_for_the_job - len(qualifications_for_the_job))
            else:
                number_of_days_for_this_competence = 1
            instance['jobs'][job]['working_days_per_qualification'][qualification_for_the_job] = number_of_days_for_this_competence
            number_of_days_for_the_job += number_of_days_for_this_competence
        instance['jobs'][job]['due_date'] = max(random.randint(horizon//3, horizon), max(instance['jobs'][job]['working_days_per_qualification'].values()))
    return instance
