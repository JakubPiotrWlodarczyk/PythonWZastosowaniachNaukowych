from time import time
import numpy as np
from tqdm import tqdm
import argparse

class Fib_Decorator:

    min_time = None 
    max_time = None
    average__time = None
    stdev_time = None
    times_of_exec = [] # pusta tablica na czasy wykonywania funkcji

    def __init__(self, func):
        self.function = func # atrybut instancji klasy 
 
    def __call__(self, *args, **kwargs):
        start_time = time()
        result = self.function(*args, **kwargs)
        end_time = time()

        single_exec_time = end_time-start_time    #wyliczenie czasu ktory uplynal

        self.times_of_exec.append(single_exec_time)
        self.min_time = min(self.times_of_exec)
        self.max_time = max(self.times_of_exec)
        self.average_time = np.average(self.times_of_exec) 
        self.stdev_time = np.std(self.times_of_exec)

        print("Czas wykonania: {0:.4f} sekund".format(single_exec_time))
        print("Minimalny czas wykonania: {0:.4f} sekund".format(self.min_time))
        print("Maksymalny czas wykonania: {0:.4f} sekund".format(self.max_time))
        print("Sredni czas wykonania:  {0:.4f} sekund".format(self.average_time))
        print("Odchylenie standardowe czasu wykonania: {0:.4f} sekund".format(self.stdev_time))
        return result


@Fib_Decorator
def fibbonacci(value):  # Fibbonacci
    n1, n2 = 0, 1
    count = 0

    if value <= 0:
        print("Please enter a positive integer")
    elif value == 1:
        print("Fibonacci sequence upto",value,":")
    else:
        with tqdm(total=value) as pbar: 
            while count < value:
                nth = n1 + n2
                n1 = n2
                n2 = nth
                count += 1
                pbar.update(1)  # update paska postepu
        pbar.close()

parser = argparse.ArgumentParser() 
parser.add_argument('-v', '--wartosc_dla_Fibbonacciego', default = 1000000)

args = parser.parse_args()    

value=int(args.wartosc_dla_Fibbonacciego)

for i in range(5):  #wywolanie funkcji 5 razy 

    print("Obliczenie wartosci ciagu Fibbonacciego dla wartosci " + str(value) + " po raz " + str(i+1) + ".")
    fibbonacci(value)
    print("\n")
