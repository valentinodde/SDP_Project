
def planifier_horaires_v1(equipes,horaires,periode_rotation,nb_semaines): 
  
    jours_semaine=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'] 
  
    horaires_jour = horaires[:len(equipes)] # horaires des équipes le 1er jour : ['Matin', 'Après-midi', 'Nuit', 'Repos'] 
    horaires_jours=[] # liste enregistrant les horaires des équipes jour par jour : [{'Semaine': '01', 'Jour': 'Lundi', 'Horaires Equipes': ['Matin', 'Après-midi', 'Nuit', 'Repos']},etc..] 
  
    nb_jours=nb_semaines*7 # nombre de jours correspondant au nombre de semaines 
  
    for indice_jour in range(nb_jours): # parcours des indices des jours : (0 : 1er jour, 1: 2ème jour, 2: 3ème jour, 4: 4ème jour, etc..) 
  
        num_semaine=indice_jour//7 + 1 # on évalue le numéro de la semaine en fonction de l'indice du jour 
        indice_jour_semaine=indice_jour % 7 # on évalue l'indice du jour de la semaine en fonction de l'indice du jour 
        jour_semaine=jours_semaine[indice_jour_semaine] # on détermine le jour de la semaine en fonction de son indice 
  
        horaires_jours.append({'Semaine':"%02d" % num_semaine, 'Jour':jour_semaine, 'Horaires Equipes': horaires_jour}) # ajout des horaires du jour  
  
        if ((indice_jour+1) % periode_rotation)==0: # on teste si on doit effectuer une rotation 
            horaires=horaires[1:] + horaires[:1] # rotation des horaires de la liste d'une position vers la gauche 
            horaires_jour=horaires[:len(equipes)] # affectation des horaires aux équipes 
  
    return horaires_jours # on retourne la liste des horaires journaliers des équipes


liste_horaires_jours=planifier_horaires_v1(['Equipe 1','Equipe 2','Equipe 3','Equipe 4'],['Matin', 'Après-midi', 'Nuit', 'Repos'],2,3) 
print(liste_horaires_jours)

def planifier_horaires_v2(equipes,horaires,periode_rotation,num_semaine,nb_semaines): 
  
    jours_semaine=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche'] 
  
    horaires_jour = horaires[:len(equipes)] # horaires des équipes le 1er jour : ['Matin', 'Après-midi', 'Nuit', 'Repos']         
    horaires_jours=[] # liste enregistrant les horaires des équipes jour par jour : [{'Semaine': '01', 'Jour': 'Lundi', 'Horaires Equipes': ['Matin', 'Après-midi', 'Nuit', 'Repos']},etc..] 
  
    nb_equipes=len(equipes) # nombre total d'équipes 
    nb_horaires=len(horaires) # nombre total de tranches horaires ou de périodes de repos 
    indice_jour1=(num_semaine-1)*7 # indice du 1er jour 
    indice_jourN= indice_jour1 + nb_semaines*7 # indice du dernier jour 
  
    for indice_jour in range(indice_jour1,indice_jourN): # parcours des indices des jours  
  
        if (indice_jour % periode_rotation)==0: # on teste par rapport à la période de rotation, si on doit effectuer une rotation 
            indice_rotation = indice_jour // periode_rotation # indice de rotation, exemple incrémentation tous les 2 jours 
  
            for indice_equipe in range(nb_equipes): # parcours des indices des équipes : (0 : Equipe 1, 1: Equipe 2, 2: Equipe 3, 3: Equipe 4)             
                indice_horaire=(indice_rotation+indice_equipe) % nb_horaires # l'indice de l'horaire est égal à l'indice de rotation ajouté à l'indice de l'équipe, modulo le nombre de tranches_horaires 
                horaires_jour[indice_equipe]=horaires[indice_horaire] # copie de l'horaire d'indice indice_horaire_jour 
  
        num_semaine=indice_jour//7 + 1 # on évalue le numéro de la semaine en fonction de l'indice du jour 
        indice_jour_semaine=indice_jour % 7 # on évalue l'indice du jour de la semaine en fonction de l'indice du jour 
        jour_semaine=jours_semaine[indice_jour_semaine] # on détermine le jour de la semaine en fonction de son indice 
  
        horaires_jours.append({'Semaine':"%02d" % num_semaine, 'Jour':jour_semaine, 'Horaires Equipes': list(horaires_jour)}) # ajout des horaires du jour  
  
    return horaires_jours #  on retourne la liste des horaires journaliers des équipes