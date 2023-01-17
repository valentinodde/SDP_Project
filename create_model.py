import string


def create_staff_qualifications(data):
    E = [] #Staff qualifications
    for staff_member in data['staff']:
        E.append([1 if q in staff_member['qualifications'] else 0 for q in list(data['qualifications'])])
    return E
