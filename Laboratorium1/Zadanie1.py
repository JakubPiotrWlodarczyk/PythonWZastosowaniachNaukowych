#Jakub Wlodarczyk 305064
import argparse
from collections import Counter 
from ascii_graph import Pyasciigraph
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument('-pl', '--book_pl', default = 'ogniem_i_mieczem.txt')
parser.add_argument('-en', '--book_en', default = 'fire_and_sword.txt')
parser.add_argument('-a', '--amount_of_word_in_histogram', default = 10)
parser.add_argument('-m', '--minimal_word_length', default = 0)

args = parser.parse_args()

print('Podane argumenty:')
print('Tytul po polsku: ', args.book_pl)
print('Tytul po angielsku: ', args.book_en)
print('Ilosc slow w histogramie: ', args.amount_of_word_in_histogram)
print('Minimalna dlugosc slowa: ', args.minimal_word_length)


#funkcja do analizy wybranej ksiazki
def analyse_book(input, amount_in_hist, min_length):
    with tqdm() as pbar:
        word = []   # tablica na slowa 

        #otworzenie pliku do odczytu
        with open(input, 'r', encoding="utf8") as f:
            for line in f:
                word = word + line.strip().split(' ')
                pbar.update()
                # strip() robi kopie ciagu, usuwajac wyrazy wiodace i koncowe
                # split() dzieli ciag na elementy tablicy, delimiter w tym przypadku to spacja

        # pozbywam sie kropek, przecinkow itp.
        word = [w.replace(',', '') for w in word]
        word = [w.replace('.', '') for w in word]
        word = [w.replace(':', '') for w in word]
        word = [w.replace('-', '') for w in word]

        # pozbywam sie za krotkich slow
        word = [short_word for short_word in word if len(short_word)>int(min_length)]
        
        # licze slowa
        amount = list(Counter(word).items())

        # sortuje
        amount.sort(key=lambda x: x[1])     # rosnaco
        amount.reverse()                    # malejaco

        # skracam tablice do tylu elementow, najczesciej wystepujacych
        # ile bylo podane w argumentach
        amount = amount[0:int(amount_in_hist)]

        # deklaruje histogram
        histogram = Pyasciigraph()

        for line in histogram.graph('Ilosc slow', amount):
            print(line)
    
    pbar.close()

print('\nAnaliza ksiazki po polsku:')
analyse_book(args.book_pl, args.amount_of_word_in_histogram, args.minimal_word_length)

print('\nAnaliza ksiazki po angielsku:')
analyse_book(args.book_en, args.amount_of_word_in_histogram, args.minimal_word_length)

