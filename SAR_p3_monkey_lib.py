#!/usr/bin/env python
#! -*- encoding: utf8 -*-
# 3.- Mono Library

import pickle
import random
import re
import sys

## Nombres: 

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################

#Toni Blasco 


def sort_index(self, d):
    for k in d:
        l = sorted(((y, x) for x, y in d[k].items()), reverse=True)
        d[k] = (sum(x for x, _ in l), l)


class Monkey():

    def __init__(self):
        self.r1 = re.compile('[.;?!]')
        self.r2 = re.compile('\W+')
    
    def finalfrase(self, word):
        """ Recibe como entrada un caracter para comprobar si es final de frase."""
        if word == '.' or word == ';' or word == ',' or word == '?' or word == '!':
            return True
        return False


    def index_sentence(self, sentence, tri):
        """ realiza la indexacion de una frase, para ello crea una entrada de diccionario 
        sino existe, si existe le suma una aparicion más junto con la palabra que lo procede"""
        frase = sentence.split()
        anterior = ""
        word = ""
        i = 1
        while i < len(frase):
            word = frase[i]; anterior = frase[i-1]
            #print(anterior)              
            self.index["bi"][anterior] = self.index["bi"].get(anterior,[0 ,{}]) #sino hay creamos entrada diccionario
            #print(str(self.index["bi"][anterior]))
            self.index["bi"][anterior][0] += 1 
            self.index["bi"][anterior][1][word]= self.index["bi"][anterior][1].get(word, 0) + 1 #añadimos la palabra con la que aparece + 1
            i += 1 

    def compute_index(self, filename, tri):
        """ Recibe un fichero y un booleano de si hacer por tripletes o no y este metodo
        se encarga de dividir por frases llamando cada frase a ser indexada, luego escribe la indexacion final
        en un fichero"""
        self.index = {'name': filename, "bi": {}}
        if tri:
            self.index["tri"] = {}
        fichero  = open(filename, 'r').read()
        fichero = fichero.replace(";",".")
        fichero = fichero.replace("\n\n",".")
        fichero = fichero.replace(",",".")
        fichero = fichero.replace("?",".")
        fichero = fichero.replace("!",".")
        fichero = fichero.lower()

        for frase in fichero.split('.'):
            frase = self.r2.sub(" ", frase)
            frase = "$ " + frase + " $"
            Monkey.index_sentence(self, frase, tri)

        #sort_index(self, self.index['bi'])
        if tri:
            sort_index(self, self.index['tri'])

        extension = filename.find('.')
        aux = filename[:extension]    
        new_filename = aux + 'index'

        with open(new_filename, 'w') as fh:
            #print(self.index['bi'].items())
            for nombre, valor  in self.index['bi'].items():
                fh.write("%s %s\n" %(nombre, valor))
        
    def save_index(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self.index, fh)

    def load_index(self, filename):
        with open(filename, "rb") as fh:
            self.index = pickle.load(fh)


    def save_info(self, filename):
        with open(filename, "w") as fh:
            print("#" * 20, file=fh)
            print("#" + "INFO".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            print("filename: '%s'\n" % self.index['name'], file=fh)
            print("#" * 20, file=fh)
            print("#" + "BIGRAMS".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            for word in sorted(self.index['bi'].keys()):
                wl = self.index['bi'][word]
                print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)
            if 'tri' in self.index:
                print(file=fh)
                print("#" * 20, file=fh)
                print("#" + "TRIGRAMS".center(18) + "#", file=fh)
                print("#" * 20, file=fh)
                for word in sorted(self.index['tri'].keys()):
                    wl = self.index['tri'][word]
                    print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)


    def generate_sentences(self, n):
        count = 1; count2 = 1

        frase = ""; texto = ""
        word = "$"  
        while count2 < n:
            while (count < 25 or word == '$'):
                ran = random.randint(1, self.index['bi'][word][0]) #un numero random entre 1 y el numero de veces que ha aparecido esa palabra
                for llave, valor in self.index['bi'][word][1].items(): #cogemos las tuplas (llave,valor)
                    if ran <= valor: # si el numero aleatorio es menor que el valor de la tupla(estan ordenadas de mayor a menor)
                        word = llave #entonces la siguiente palabra sera la llave que la sigue
                        frase += llave + " " # la añadimos a la frase 
                        count += 1 # restamos uno al contador 
                        break
                    else:
                        ran -= valor # en caso de ser mayor restamos
            texto += frase +'\n'
        return texto

    


if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")


