#!/usr/bin/env python
#! -*- encoding: utf8 -*-

# 1.- Pig Latin

import sys
import re

class Translator():

    def __init__(self, punt=None):
        """
        Constructor de la clase Translator

        :param punt(opcional): una cadena con los signos de puntuación
                                que se deben respetar
        :return: el objeto de tipo Translator
        """
        if punt is None:
            self.re = re.compile("(\w+)([.,;?!]*)")
        else:
            self.re = re.compile("(\w+)(["+punt+"]*)")

    def esVocal(self,vocal):        
        if vocal == 'a' or vocal == 'e' or vocal == 'i' or vocal == 'o' or vocal == 'u' or vocal == 'y' or vocal == 'A' or vocal == 'E' or vocal == 'I' or vocal == 'O' or vocal == 'U' or vocal == 'Y':
            aux = True
        else:
            aux = False
        return aux
    
    def esPuntuacion(self, word):
        if word == '.' or word == '?' or word == '!' or word == ';' or word == ',':
            return True
        return False

    def translate_word(self, word):
        """Casos:
        Que sea mayuscula y empiece por vocal
        que sea mayuscula y empiece por consonante
        que sea minuscula y empiece por vocal
        que sea minuscula y empiece por consonante
        --que tenga un signo de puntuacion al final
        si la palabra no es una palabra(4G ,) entonces dejar igual"""
        aux = word[0]
        tienePuntuacion = False
        todomayusculas = False

        if not aux.isalpha(): #Sino es una letra se devuelve todo lo que entra
            new_word = word
            return new_word

        if t.esPuntuacion(word[len(word)-1]):   #Cogemos los signos de puntuacion para añadirlos despues al final.
            j = len(word) - 1
            while j >= 0 and t.esPuntuacion(word[j]):
                j -= 1
            puntuacion = word[j+1:]
            word = word[:j+1]
            tienePuntuacion = True

        if word.isupper():   #Vemos si toda las palabras estan en mayusculas o no
            todomayusculas = True 

        if (aux.isupper() and t.esVocal(aux)) or (aux.islower() and t.esVocal(aux)):            
            if tienePuntuacion == True:
                new_word = word + "yay" + puntuacion
                return new_word
            else:
                new_word = word + "yay"
                return new_word
        elif (aux.isupper() and not t.esVocal(aux) or (aux.islower() and not t.esVocal(aux))):
            word = word.lower()
            i = 0
            while i < len(word) and not t.esVocal(word[i]): #Buscamos hasta la primera vocal
                i += 1              
            word = word[i:] + word[:i] + "ay"       #Formamos la palabra
            if todomayusculas:
                word = word.upper()                     #"Paso toda la palabra a mayusculas"
            else:
                word = word[0].upper() + word[1:]      #"Paso la primera vocal a mayuscula"
            if tienePuntuacion == True:
                new_word = word + puntuacion
            else :
                new_word = word        
        return new_word

    def translate_sentence(self, sentence):
        """
        Este método recibe una frase en inglés y la traduce a Pig Latin

        :param sentence: la frase que se debe pasar a Pig Latin
        :return: la frase traducida
        """
        frase = sentence.split()
        new_sentence = ""
        for i in range(len(frase)):
            y = frase[i]
            newword = t.translate_word(y)
            new_sentence += newword + " "
        return new_sentence

    def translate_file(self, filename):
        """
        Este método recibe un fichero y crea otro con su tradución a Pig Latin

        :param filename: el nombre del fichero que se debe traducir
        :return: True / False 
        """
        try:
            infile  = open(filename, 'r').read()
            new_file = open(filename[:-4] + "_piglatin.txt", "w")
            for lane in infile.split('\n'):
                new_file.write(t.translate_sentence(lane) + '\n')
            new_file.close()
            return True
        except ValueError:
            print("Error al abrir el fichero")   
            return False   

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print('Syntax: python %s [filename]' % sys.argv[0])
        exit
    else:
        t = Translator()
        if len(sys.argv) == 2:
            t.translate_file(sys.argv[1])
        else:
            while True:
                sentence = input("ENGLISH: ")
                if len(sentence) < 2:
                      break
                print("PIG LATIN:", t.translate_sentence(sentence))
