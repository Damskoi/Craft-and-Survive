#!/usr/bin/python3

#from os import chdir
#chdir("C:\Linux I\kali\Doc Shared\data")

from random import *

#		FONCTIONS		#

def decoupe_tab(ligne):
    ligne= ligne.split('\t')
    last= len(ligne)-1
    ligne[last]= ligne[last].strip()
    return ligne

def import_distrib_ressources(fichier):
	tab = []
	f = open(fichier)
	ligne = f.readline()

	while ligne.strip() != '' :
		temp= decoupe_tab(ligne)
		i=0
		while i< (int)(temp[1]) :
			tab.append(temp[0])
			i+=1
		ligne = f.readline()

	f.close()
	return tab

def init_coffre(fichier):
	tab = {}
	f = open(fichier)
	ligne = f.readline()

	while ligne.strip() != '' :
		temp= decoupe_tab(ligne)
		tab[temp[0]] = 0;
		ligne = f.readline()

	f.close()
	return tab

def fixe_longueur(chaine, longueur):
	taille = len(chaine)
	if taille < longueur:
		i=0

		while i< longueur-taille :
			chaine = ' ' +chaine
			i+=1

		return chaine
	else:
		return chaine

def liste_items(coffre):
	items= list(coffre.keys())
	return items

def ouvre_coffre(coffre):
	items= liste_items(coffre)
	print('Votre coffre :')
	for i in items:
		print(fixe_longueur(i, 20)+ ' | '+ fixe_longueur(str(coffre[i]), 5))

def ajoute(coffre, item):
	coffre[item] += 1

def ajoute_plusieurs(coffre, tabItems):
	for i in tabItems:
		ajoute(coffre, i)

def est_present(coffre, item, qte=1):
	if coffre[item] >= qte:
		return True
	else:
		return False

def sont_presents(coffre, tabItems):
	for i in tabItems:
		if not est_present(coffre, i) :
			return False
	return True

def retire(coffre, item, qte=1):
	if est_present(coffre, item, qte):
		coffre[item] -= qte
		return True
	return False

def retire_plusieurs(coffre, tabItems):
	if sont_presents(coffre, tabItems):
		for i in tabItems:
			retire(coffre, i)
		return True
	return False

def glaner(tabRessourse, nb=5):
	tab =[]
	i=0
	while i<nb:
		rand= randint(0, len(tabRessourse))
		tab.append(tabRessourse[rand])
		i+=1
	return tab

def import_regles_craft_simple(fichier):
	regles= {}
	f = open(fichier)
	ligne = f.readline()

	while ligne.strip() != '' :
		temp= decoupe_tab(ligne)
		regles[temp[0]] = []
		i=1
		while i< len(temp) :
			regles[temp[0]].append(temp[i])
			i+=1
		ligne = f.readline()

	f.close()
	return regles

def import_regles_craft_plus(fichier):
	regles= {}
	f = open(fichier)
	ligne = f.readline()

	while ligne.strip() != 'fin' :
		if ligne[0] != '#' and ligne.strip() !='':
			temp= decoupe_tab(ligne)
		
			regles[temp[0]] = []
			regles[temp[0]].append(temp[1])
			regles[temp[0]].append({}) 
			i=2
			while i < len(temp) :
				regles[temp[0]][1][temp[i]]= temp[i+1]
				i+=2
		ligne = f.readline()

	f.close()
	return regles

def craft_possible_simple(coffre, regles, item):
	itemNecessaire = list(regles[item])
	if sont_presents(coffre, itemNecessaire):
		return True
	return False

def craft_possible_plus(coffre, regles, item):
	itemNecessaire = list(regles[item][1])
#	if sont_presents(coffre, itemNecessaire, regles[item][itemNecessaire]):
#		return True
#	return False
	for i in itemNecessaire:
		if not est_present(coffre, i, (int)(regles[item][1][i])):
			return False
	return True

def craft_simple(coffre, regles, item):
	if craft_possible_simple(coffre, regles, item):
		retire_plusieurs(coffre, list(regles[item]))
		ajoute(coffre, item)
		return True
	return False

def craft_plus(coffre, regles, item):
	if craft_possible_plus(coffre, regles, item):
	#	retire_plusieurs(coffre, list(regles[item]))
		itemNecessaire = list(regles[item][1])
		for i in itemNecessaire:
			retire(coffre, i, (int)(regles[item][1][i]))
		ajoute(coffre, item)
		return True
	return False

def manger(coffre, item, PdV):
	if (item == 'pain' or item == 'tomate' or item == 'ble'):
		if est_present(coffre, item):
			if item== 'pain':
				supra = 10
			elif item == 'tomate':
				supra = 5
			else:
				supra = 1
			retire(coffre, item)
			print('Vous veniez de gagner', supra, 'point de vie')
			return PdV + supra
		else:
			print('ERROR! :l\'item "', item, '" n\'est pas présent dans votre coffre!')
			return PdV;
	else:
		print('ERR! :l\'item "', item, '" n\'est pas comestible!')
		return PdV

def maj_PdV(coffre, PdV):
	decrement = 50
	if(est_present(coffre, 'vetement')):
		decrement -= 5
	if(est_present(coffre, 'lit')):
		decrement -= 7
	if(est_present(coffre, 'hutte')):
		decrement -= 15
	return PdV - decrement

def est_dans(mot, list):
	for i in list:
		if mot== i:
			return True
	return False

def saisie_controlee(message, admisible):
	saisie= input(message+'\n')
	while not est_dans(saisie, admisible) :
		print('Saisie non reconnue')
		saisie= input(message+'\n')
	return saisie

def choix_item(coffre):
	items=liste_items(coffre)
	saisie= saisie_controlee('Saisissez le nom d\'un item', items)
	return saisie

def craft_regles_simple():
	regles_craft = import_regles_craft_simple("data/regles_craft.txt")
	print(fixe_longueur('Pour crafter', 20)+ ' , '+ fixe_longueur('il vous faut :', 20))
	for x in regles_craft:
		regle= fixe_longueur(x, 20)+ ' = '
		y=0
		while y < len(regles_craft[x]):
			regle += str(regles_craft[x][y]) +', '
			y+=1 
		print(regle)

def craft_regles_plus():
	regles_craft= import_regles_craft_plus("data/regles_craft_plus.txt")
	for x in regles_craft:
		regle = 'Pour fabriquer '+ str(regles_craft[x][0])+ ' item(s) ' +str(x)+ ' il faut: '
		liste= list(regles_craft[x][1].keys())
		for y in liste :
			regle += str(regles_craft[x][1][y])+ ' item(s) ' +str(y)+' et '
		print(regle)
	 
def version_1():
	PdV = 1000
	coffre = init_coffre("data/ressources.txt")
	regles_craft = import_regles_craft_simple("data/regles_craft.txt")
	ressources = import_distrib_ressources('data/ressources.txt')

	print('Craft and Survive')
	print('---------------------')

	#	Ajout d'items au coffre
	ajoute_plusieurs(coffre, ['graine_coton', 'osier', 'osier', 'paille', 'tomate', 'ble'])

	while PdV > 0:
		ajoute_plusieurs(coffre, glaner(ressources, 5))
		ouvre_coffre( coffre )
		print('Vos PdV :', PdV)
		if saisie_controlee('Souhaitez vous crafter?', ['oui', 'non']) == 'oui':
#			print('la liste des items est :')
			items= list(regles_craft.keys())
#			print(items)
			craft_regles_simple()
			saisie= saisie_controlee('Que souhaitez vous crafter?', items)
			if craft_simple(coffre, regles_craft, saisie) :
				print('Vous venier de crafter "', saisie, '".')
			else :
				print('craft failed'.upper())
		
		if saisie_controlee('Souhaitez vous manger?', ['oui', 'non']) == 'oui':
			PdV= manger(coffre, saisie_controlee('Que souhaitez vous manger? (ble, pain, tomate)', ['ble', 'pain', 'tomate']), PdV)
		if saisie_controlee('Souhaitez vous continuer?', ['oui', 'non']) == 'non':
			print('partie Arreté')
			break
		
		PdV = maj_PdV(coffre, PdV)	
	if PdV <=0 :
		print('game over!'.upper())

def version_2():
	PdV = 1000
	coffre = init_coffre("data/ressources.txt")
	regles_craft_plus = import_regles_craft_plus("data/regles_craft_plus.txt")
	ressources = import_distrib_ressources('data/ressources.txt')

	print('Craft and Survive')
	print('---------------------')

	#	Ajout d'items au coffre
	ajoute_plusieurs(coffre, ['graine_coton', 'osier', 'osier', 'paille', 'tomate', 'ble'])

	# pour crafter marteau
	ajoute_plusieurs(coffre, ['bois', 'fer', 'fer','fer', 'fer', 'fer'])

	while PdV > 0:
		rand= randint(0,5)
		ajoute_plusieurs(coffre, glaner(ressources, rand))
		ouvre_coffre( coffre )
		print('Vos PdV :', PdV)
		if saisie_controlee('Souhaitez vous crafter?', ['oui', 'non']) == 'oui':
#			print('la liste des items est :')
			items= list(regles_craft_plus.keys())
#			print(items)
			craft_regles_plus()
			saisie= saisie_controlee('Que souhaitez vous crafter?', items)
			if craft_plus(coffre, regles_craft_plus, saisie) :
				print('Vous venier de crafter "', saisie, '".')
			else :
				print('craft failed'.upper())
		
		if saisie_controlee('Souhaitez vous manger?', ['oui', 'non']) == 'oui':
			PdV= manger(coffre, saisie_controlee('Que souhaitez vous manger? (ble, pain, tomate)', ['ble', 'pain', 'tomate']), PdV)

		PdV = maj_PdV(coffre, PdV)	
		if PdV <=0 :
			print('game over!'.upper())
			break
		else :
			if saisie_controlee('Souhaitez vous continuer?', ['oui', 'non']) == 'non':
				print('partie Arreté')
				break
		
#		PdV = maj_PdV(coffre, PdV)	
#	if PdV <=0 :
#		print('game over!'.upper())

def version_2_2():
	joueur1= input('Veillez Saisir le pseudio du joueur1 \n joueur1= ')
	joueur2= input('Veillez Saisir le pseudio du joueur2 \n joueur2= ')
	PdV_j1= 1000
	PdV_j2 = 1000
	coffre_j1 = init_coffre("data/ressources.txt")
	coffre_j2 = init_coffre("data/ressources.txt")
	regles_craft_plus = import_regles_craft_plus("data/regles_craft_plus.txt")
	ressources = import_distrib_ressources('data/ressources.txt')

	ajoute_plusieurs(coffre_j1, glaner(ressources))
	ajoute_plusieurs(coffre_j2, glaner(ressources))

	print('Craft and Survive')
	print('---------------------')

	while PdV_j1> 0 or PdV_j2>0:
			#	PARTI CONCERNANT LE JOUEUR 1
		rand= randint(0,5)
		ajoute_plusieurs(coffre_j1, glaner(ressources, rand))
		ouvre_coffre( coffre_j1 )
		print('Vos PdV :', PdV_j1)
		if saisie_controlee('Souhaitez vous crafter '+joueur1+'?', ['oui', 'non']) == 'oui':
#			print('la liste des items est :')
			items= list(regles_craft_plus.keys())
#			print(items)
			craft_regles_plus()
			saisie= saisie_controlee('Que souhaitez vous crafter?', items)
			if craft_plus(coffre_j1, regles_craft_plus, saisie) :
				print('Vous venier de crafter "', saisie, '".')
			else :
				print('craft failed'.upper())
		
		if saisie_controlee('Souhaitez vous manger '+joueur1+'?', ['oui', 'non']) == 'oui':
			PdV_j1 = manger(coffre_j1, saisie_controlee('Que souhaitez vous manger? (ble, pain, tomate)', ['ble', 'pain', 'tomate']), PdV_j1)

		PdV_j1 = maj_PdV(coffre_j1, PdV_j1)	
		if PdV_j1 <=0 :
			print('game over!'.upper())
			break
		else :
			if saisie_controlee('Souhaitez vous continuer '+joueur1+'?', ['oui', 'non']) == 'non':
				print(joueur1.upper(), 'à arreté la partie!')
				break


			#	PARTI CONCERNANT LE JOUEUR 2
		rand= randint(0,5)
		ajoute_plusieurs(coffre_j2, glaner(ressources, rand))
		ouvre_coffre( coffre_j2 )
		print('Vos PdV :', PdV_j2)
		if saisie_controlee('Souhaitez vous crafter '+joueur2+'?', ['oui', 'non']) == 'oui':
#			print('la liste des items est :')
			items= list(regles_craft_plus.keys())
#			print(items)
			craft_regles_plus()
			saisie= saisie_controlee('Que souhaitez vous crafter?', items)
			if craft_plus(coffre_j2, regles_craft_plus, saisie) :
				print('Vous venier de crafter "', saisie, '".')
			else :
				print('craft failed'.upper())
		
		if saisie_controlee('Souhaitez vous manger '+joueur2+'?', ['oui', 'non']) == 'oui':
			PdV_j2 = manger(coffre_j2, saisie_controlee('Que souhaitez vous manger? (ble, pain, tomate)', ['ble', 'pain', 'tomate']), PdV_j2)

		PdV_j2 = maj_PdV(coffre_j2, PdV_j2)	
		if PdV_j2 <=0 :
			print('game over!'.upper())
			break
		else :
			if saisie_controlee('Souhaitez vous continuer '+joueur2+'?', ['oui', 'non']) == 'non':
				print(joueur2.upper(), 'à arreté la partie!')
				break
	


def choix_partie():
	choix = saisie_controlee('Souhaitez vous Joueur seul ou à deux? (1 ou 2 ou 2.2)', ['1', '2', '2.2'])
	if choix == '2':
		version_2()
	elif choix == '2.2':
		version_2_2()
	else:
		partie()


#		END OF FONCTIONS		#




# ------------  TEST/EXEMPLE ---------- #

#	lancement du choix de version à jouer
choix_partie()
