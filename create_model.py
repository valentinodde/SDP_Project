def create_staff_qualifications(data):
    E = [] #Staff qualifications
    for staff_member in data['staff']:
        E.append(staff_member['qualifications'])
    return E
