#Jakub Wlodarczyk 305064
import argparse
from pickletools import optimize
import numpy as np
import tqdm
from PIL import Image, ImageDraw

class Ising:
    def __init__(self, n, j, beta, b, steps, dens):     #konstruktor
        self.n = n  #rozmiar siatki
        self.j = j  #calka wymiany
        self.beta = beta    #parametr beta
        self.b = b  #wektor indukcji magentycznej
        self.steps = steps  #ilosc makro krokow
        self.system = np.random.choice([1, -1], [self.n, self.n], p=[dens, 1-dens]) #generacja siatki

    def calculate_energy(self, S0, Sn): #wyliczenie energii
        return 2 * S0 * (self.b + self.j * Sn)

    def magnetization(self):    #wyliczenie magnetyzacji
        return np.abs(np.sum(self.system)/self.n**2)

    def run_png_gif_mag(self, png, gif, txt):   #run symulacji (obrazki, gif i plik z magnetyzacja)
        img = Image.new('RGB', (2*self.n, 2*self.n), (255, 255, 255))   
        images_for_gif = [] #tabela na obrazki 
        draw = ImageDraw.Draw(img)

        f = open(str(txt)+'.txt', 'w')      #otworzenie pliku z magnetyzacja
        f.write('krok \t magnetyzacja \n')  #zapis naglowka do pliku
        
        for row in range(self.n):           #narysowanie poczatkowej konfiguracji siatki
            for column in range(self.n):
                if(self.system[row, column] == 1):  #spiny w gore czarne
                    draw.rectangle((2*row, 2*column, 2*(row+1), 2*(column+1)), (0,0,0)) 
                else:                               #spiny w dol biale
                    draw.rectangle((2*row, 2*column, 2*(row+1), 2*(column+1)), (255,255,255))


        for s in tqdm.tqdm(range(self.steps)):      #licznik postepu, petla po ilosci krokow
            img = Image.new('RGB', (2*self.n, 2*self.n), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            for spins in range(self.n*self.n):      #petla po ilosci spinow

                i = np.random.randint(self.n)       #biore losowy spin    
                j = np.random.randint(self.n)

                #warunki brzegowe
                Sn = self.system[(i - 1) % self.n, j] + self.system[(i + 1) % self.n, j] + self.system[i, (j - 1) % self.n] + self.system[i, (j + 1) % self.n]

                dE = self.calculate_energy(self.system[i, j], Sn)   #wyliczenie energii

                if dE < 0 or np.random.random() < np.exp(-dE*self.beta):    #zmiana wartosci spinu przy okreslonych warunkach
                    self.system[i, j] = -self.system[i, j]

                if(self.system[i,j]==1):                                    #uaktualnienie stanu ukladu na obrazku
                    draw.rectangle((2*i, 2*j, 2*(i+1), 2*(j+1)), (0,0,0))
                else:
                    draw.rectangle((2*i, 2*j, 2*(i+1), 2*(j+1)), (255,255,255))


            mag = self.magnetization()      #wyliczenie magnetyzacji
            f.write(str(s) + '\t' + str(mag) + '\n')    #zapis do pliku
            img.save(str(png)+str(s)+'.png')            #zapis obrazka
            images_for_gif.append(img) #dodawanie obrazkow na gifa
            
        images_for_gif[0].save(str(gif)+'.gif', save_all = True, append_images=images_for_gif[1:], optimize=False, duration=40, loop=0) #stworzenie gifa
        f.close()

    def run_png_gif(self, png, gif):    #run symulacji (obrazki, gif )
        img = Image.new('RGB', (2*self.n, 2*self.n), (255, 255, 255))
        images_for_gif = [] #tabela na obrazki 
        draw = ImageDraw.Draw(img)
        
        for row in range(self.n):
            for column in range(self.n):
                if(self.system[row, column] == 1):
                    draw.rectangle((2*row, 2*column, 2*(row+1), 2*(column+1)), (0,0,0))
                else:
                    draw.rectangle((2*row, 2*column, 2*(row+1), 2*(column+1)), (255,255,255))


        for s in tqdm.tqdm(range(self.steps)):
            img = Image.new('RGB', (2*self.n, 2*self.n), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            for spins in range(self.n*self.n):

                i = np.random.randint(self.n)
                j = np.random.randint(self.n)

                # Periodic Boundary Condition
                Sn = self.system[(i - 1) % self.n, j] + self.system[(i + 1) % self.n, j] + self.system[i, (j - 1) % self.n] + self.system[i, (j + 1) % self.n]

                dE = self.calculate_energy(self.system[i, j], Sn)

                if dE < 0 or np.random.random() < np.exp(-dE*self.beta):
                    self.system[i, j] = -self.system[i, j]

                if(self.system[i,j]==1):
                    draw.rectangle((2*i, 2*j, 2*(i+1), 2*(j+1)), (0,0,0))
                else:
                    draw.rectangle((2*i, 2*j, 2*(i+1), 2*(j+1)), (255,255,255))

            img.save(str(png)+str(s)+'.png')
            images_for_gif.append(img) #dodawanie obrazkow na gifa
            
        images_for_gif[0].save(str(gif)+'.gif', save_all = True, append_images=images_for_gif[1:], optimize=False, duration=40, loop=0) #stworzenie gifa

    def run_mag(self, txt):     #run symulacji (plik z magnetyzacja)

        f = open(str(txt)+'.txt', 'w')
        f.write('krok \t magnetyzacja \n')

        for s in tqdm.tqdm(range(self.steps)):
            for spins in range(self.n*self.n):

                i = np.random.randint(self.n)
                j = np.random.randint(self.n)

                # Periodic Boundary Condition
                Sn = self.system[(i - 1) % self.n, j] + self.system[(i + 1) % self.n, j] + self.system[i, (j - 1) % self.n] + self.system[i, (j + 1) % self.n]

                dE = self.calculate_energy(self.system[i, j], Sn)

                if dE < 0 or np.random.random() < np.exp(-dE*self.beta):
                    self.system[i, j] = -self.system[i, j]

            mag = self.magnetization()
            f.write(str(s) + '\t' + str(mag) + '\n')
            
        f.close()

    def run_png_mag(self, png, txt):        #run symulacji (obrazki i plik z magnetyzacja)
        img = Image.new('RGB', (2*self.n, 2*self.n), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        f = open(str(txt)+'.txt', 'w')
        f.write('krok \t magnetyzacja \n')
        
        for row in range(self.n):
            for column in range(self.n):
                if(self.system[row, column] == 1):
                    draw.rectangle((2*row, 2*column, 2*(row+1), 2*(column+1)), (0,0,0))
                else:
                    draw.rectangle((2*row, 2*column, 2*(row+1), 2*(column+1)), (255,255,255))


        for s in tqdm.tqdm(range(self.steps)):
            for spins in range(self.n*self.n):

                i = np.random.randint(self.n)
                j = np.random.randint(self.n)

                # Periodic Boundary Condition
                Sn = self.system[(i - 1) % self.n, j] + self.system[(i + 1) % self.n, j] + self.system[i, (j - 1) % self.n] + self.system[i, (j + 1) % self.n]

                dE = self.calculate_energy(self.system[i, j], Sn)

                if dE < 0 or np.random.random() < np.exp(-dE*self.beta):
                    self.system[i, j] = -self.system[i, j]

                if(self.system[i,j]==1):
                    draw.rectangle((2*i, 2*j, 2*(i+1), 2*(j+1)), (0,0,0))
                else:
                    draw.rectangle((2*i, 2*j, 2*(i+1), 2*(j+1)), (255,255,255))


            mag = self.magnetization()
            f.write(str(s) + '\t' + str(mag) + '\n')
            img.save(str(png)+str(s)+'.png')            

        f.close()

    def run_png(self, png):         #run symulacji (obrazki)
        img = Image.new('RGB', (2*self.n, 2*self.n), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        for row in range(self.n):
            for column in range(self.n):
                if(self.system[row, column] == 1):
                    draw.rectangle((2*row, 2*column, 2*(row+1), 2*(column+1)), (0,0,0))
                else:
                    draw.rectangle((2*row, 2*column, 2*(row+1), 2*(column+1)), (255,255,255))


        for s in tqdm.tqdm(range(self.steps)):
            for spins in range(self.n*self.n):

                i = np.random.randint(self.n)
                j = np.random.randint(self.n)

                # Periodic Boundary Condition
                Sn = self.system[(i - 1) % self.n, j] + self.system[(i + 1) % self.n, j] + self.system[i, (j - 1) % self.n] + self.system[i, (j + 1) % self.n]

                dE = self.calculate_energy(self.system[i, j], Sn)

                if dE < 0 or np.random.random() < np.exp(-dE*self.beta):
                    self.system[i, j] = -self.system[i, j]

                if(self.system[i,j]==1):
                    draw.rectangle((2*i, 2*j, 2*(i+1), 2*(j+1)), (0,0,0))
                else:
                    draw.rectangle((2*i, 2*j, 2*(i+1), 2*(j+1)), (255,255,255))

            img.save(str(png)+str(s)+'.png')            


parser = argparse.ArgumentParser()  #argumenty

parser.add_argument('-n', '--rozmiar_siatki', default = 1000)
parser.add_argument('-j', '--calka_wymiany', default = 1)
parser.add_argument('-beta', '--parametr', default = 4e5)
parser.add_argument('-b', '--indukcja_magnetyczna', default = 1.9)
parser.add_argument('-k', '--liczba_krokow', default = 100)
parser.add_argument('-g', '--gestosc_spinow', default = 0.2)
parser.add_argument('-png', '--plik_obrazki')
parser.add_argument('-gif', '--plik_animacja')
parser.add_argument('-txt', '--plik_magnetyzacja')

args = parser.parse_args()

N=int(args.rozmiar_siatki)
J=args.calka_wymiany
Beta=args.parametr
B=args.indukcja_magnetyczna
K=args.liczba_krokow
G=args.gestosc_spinow

ising = Ising(N, J, Beta, B, K, G)  #stworzenie obiektu

#uruchomienie odpowiedniej funkcji zaleznie od podanych argumentow wejsciowych
if args.plik_obrazki is not None:   #png ok
    png=args.plik_obrazki
    if args.plik_animacja is not None:  #gif ok
        gif=args.plik_animacja
        if args.plik_magnetyzacja is not None:  #txt ok
            txt=args.plik_magnetyzacja
            ising.run_png_gif_mag(png, gif, txt)
        else:   #txt not
            ising.run_png_gif(png, gif)
    else:   #gif not
        if args.plik_magnetyzacja is not None:  #txt ok
            txt=args.plik_magnetyzacja
            ising.run_png_mag(png, txt)
        else:   #txt not
            ising.run_png(png)
else:   #png not
    if args.plik_magnetyzacja is not None:
        txt=args.plik_magnetyzacja
        ising.run_mag(txt)
    else:   #txt not
        print('Nie podano nazwy dla plikow .txt, .png, .gif! Nie zostanie utworzony zadny plik wyjsciowy!')
    
    





