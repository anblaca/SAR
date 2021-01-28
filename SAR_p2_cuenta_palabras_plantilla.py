#! -*- encoding: utf8 -*-

#Ampliacion de Biwords

## Nombres: 

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################

import argparse
import re
import sys
from operator import itemgetter


def sort_dic_by_values(d, asc=True):
    return sorted(d.items(), key=lambda a: (-a[1], a[0]))

class WordCounter:

    def __init__(self):
        """
           Constructor de la clase WordCounter
        """
        self.clean_re = re.compile('\W+')
    
    def sort_dic(self, diccionario):
            for key, value in sorted(sorted(diccionario.items()), key=itemgetter(1), reverse=True):
                yield key, value

    def write_stats(self, filename, stats, use_stopwords, full):
        """
        Este método escribe en fichero las estadísticas de un texto
            

        :param 
            filename: el nombre del fichero destino.
            stats: las estadísticas del texto.
            use_stopwords: booleano, si se han utilizado stopwords
            full: boolean, si se deben mostrar las stats completas

        :return: None
        """

        with open(filename, 'w') as fh:
            
            pass
    

    def file_stats(self, filename, lower, stopwordsfile, bigrams, full):
        """
        Este método calcula las estadísticas de un fichero de texto
            

        :param 
            filename: el nombre del fichero.
            ####lower: booleano, se debe pasar todo a minúsculas?
            ####stopwordsfile: nombre del fichero con las stopwords o None si no se aplican
            bigram: booleano, se deben calcular bigramas?
            full: booleano, se deben montrar la estadísticas completas?

        :return: None
        """

        stopwords = [] if stopwordsfile is None else open(stopwordsfile).read().split()

        # variables for results
        clean_re = re.compile('\W+')        
        sts = {
                'nwords': 0,
                'nlines': 0,
                'word': {},
                'symbol': {}
                }
        diccionarioWords = {}
        diccionarioSymbol = {}
        diccionarioBiword = {}
        diccionarioBisymbol = {}

        if bigrams:
            sts['biword'] = {}
            sts['bisymbol'] = {}

        suma = 0
        infile  = open(filename, 'r').read()
        for lane in infile.split('\n'): #Recogo la linea
            lane = clean_re.sub(' ',lane)

            if lower: #pasar a minuscula si es necesario
                lane = lane.lower()

            sts['nlines'] += 1  

            if full and sts['nlines'] == 20:  # si esta la opcion de mostrar solo 20 iteraciones, break
                break
            #si tenemos q hacer brigramas, entonces cogemos la linea la partimos, comprobamos q no haya stopwords, sino los hay se añaden.
            if bigrams:
                aux = '$ ' + lane + ' $'
                aux = aux.split()
                for i in range(0, len(aux)-1):
                    if stopwordsfile != None and aux[i] in stopwords:            #compruebo si es un stop word, si lo es, fuera.      
                        break                
                    diccionarioBiword[aux[i] + ' ' + aux[i+1]] = diccionarioBiword.get(aux[i] + ' ' + aux[i+1], 0) + 1
                    sts['biword'] = diccionarioBiword[aux[i] + ' ' + aux[i+1]]

            for word in lane.split(): #Recorro la linea palabra a palabra
                if stopwordsfile != None and word in stopwords:            #compruebo si es un stop word si lo es fuera.      
                    break               
                #se añade al diccionario 
                sts['nwords'] += 1
                diccionarioWords[word] = diccionarioWords.get(word,0) + 1
                sts['word'] = diccionarioWords[word]     

                aux2 = ''                               
                for simbolo in word: #Recorro la palabra
                    diccionarioSymbol[simbolo] = diccionarioSymbol.get(simbolo,0) + 1
                    sts['symbol'] = diccionarioSymbol[simbolo]
                    suma += 1
                    if (aux2 != ''):
                        diccionarioBisymbol[aux2+simbolo] = diccionarioBisymbol.get(aux2+simbolo, 0) + 1
                    aux2 = simbolo

        extension = filename.find('.')
        aux = filename[:extension]
        if lower == True:  
            aux += 'l'
        
        if stopwordsfile != None: 
            aux += 's'
        
        if bigrams == True: 
            aux += 'b'
        
        if full == True: 
            aux += 'f'
        
        new_filename = aux + '_stats' + filename[extension:]

        with open(new_filename, 'w') as fh:
            a = sts['nlines']
            b = sts['nwords']
            fh.write("Lines: " + str(a) + '\n' + 'Number words: ' + str(b) + '\n') #Numero de linias y numero de palabras
            fh.write("Vocabulary size: " + str(len(diccionarioWords.keys())) + '\n' + 'Number of symbols: ' + str(suma) + '\n') #Numero de palabras y numero de simbolos 
            fh.write("Number of different symbols: " + str(diccionarioSymbol.keys()) + '\n' + 'Words (alphabetical order):' + '\n')
                                
            for k, v in sorted(diccionarioWords.items()):
                fh.write(str(k) + ': ' + str(v) + ', ')
                
            fh.write('Words (by frequency):'+ '\n') 
            for word, count in WordCounter.sort_dic(self,diccionarioWords):
                fh.write(str(word) + " " + str(count) + ', ')
        
            fh.write('\n''Symbols (alphabetical order):' + '\n')

            for k,v in sorted(diccionarioSymbol.items()):
                fh.write(str(k) + ': ' + str(v) + ', ')
        
            fh.write('\n''Symbols (by frequency):'+ '\n') 
            for letter, count in WordCounter.sort_dic(self,diccionarioSymbol):
                fh.write(str(letter) + " " + str(count) + ', ')

            fh.write('\n'"Bigrams (alphabetical order):" + '\n')
            for bigram, count in sorted(diccionarioBiword.items()):
                fh.write(str(bigram) + " " + str(count) + ', ')

            fh.write("Bigrams (by frequency):" + '\n')
            for bigram, count in WordCounter.sort_dic(self,diccionarioBiword):
                fh.write(str(bigram)  + " " + str(count) + ', ')
            
            fh.write("Bisymbols (alphabetical order):" + '\n')
            for bisymbol, count in sorted(diccionarioBisymbol.items()):
                fh.write(str(bisymbol) + " " + str(count) + ', ')
            fh.write("Bisymbols (by frequency):" + '\n')
            for bisymbol, count in WordCounter.sort_dic(self,diccionarioBisymbol):
                fh.write(str(bisymbol)  + " " + str(count) + ', ')                
            pass
        

        #self.write_stats(new_filename, sts, stopwordsfile is not None, full)

    def compute_files(self, filenames, **args):
        """
        Este método calcula las estadísticas de una lista de ficheros de texto
            

        :param 
            filenames: lista con los nombre de los ficheros.
            args: argumentos que se pasan a "file_stats".

        :return: None
        """

        for filename in filenames:
            self.file_stats(filename, **args)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compute some statistics from text files.')
    parser.add_argument('file', metavar='file', type=str, nargs='+',
                        help='text file.')

    parser.add_argument('-l', '--lower', dest='lower', action='store_true', default=False, 
                    help='lowercase all words before computing stats.')

    parser.add_argument('-s', '--stop', dest='stopwords', action='store',
                    help='filename with the stopwords.')

    parser.add_argument('-b', '--bigram', dest='bigram', action='store_true', default=False, 
                    help='compute bigram stats.')

    parser.add_argument('-f', '--full', dest='full', action='store_true', default=False, 
                    help='show full stats.')

    args = parser.parse_args()
    wc = WordCounter()
    wc.compute_files(args.file, lower=args.lower, stopwordsfile=args.stopwords, bigrams=args.bigram, full=args.full)