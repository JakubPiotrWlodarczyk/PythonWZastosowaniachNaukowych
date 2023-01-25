import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image, ImageFilter
import argparse

parser = argparse.ArgumentParser() 
parser.add_argument('-type', '--typ_liczenia', default = 'ex')  # ex lin

args = parser.parse_args()    

type=str(args.typ_liczenia)


def image_change(val):

    source = 'http://www.if.pw.edu.pl/~mrow/dyd/wdprir/'        #strona

    req = requests.get(source)  #pobieram strone
    status = req.status_code    #sprawdzam status

    print("Status code = ", status)

    soup = BeautifulSoup(req.text,'html.parser')

    for a in soup.find_all('a', href=True):     #szukam a href
        url =  a['href']

        imag = 'img'+str(val)   #szukam konkretne obrazki

        if imag in url:
            img = requests.get(url=source+url, stream=True).content     #tworze url


            with open('img/obrazek'+str(val)+'.png', 'wb') as handler:    #zapisuje obrazek
                handler.write(img) 
                im = Image.open('img/obrazek'+str(val)+'.png')
                im1 = im.convert("L")
                im2 = im1.filter(ImageFilter.GaussianBlur(radius = 9))  #aplikuje blur i czarno-bialy wyglad
                im2.save('img/obrazek_blur'+str(val)+'.png')  #zapis nowego obrazka
                print('stworzono obrazek ' + str(val))



if type=='lin':
    start = time.time()
    for val0 in range(0, 10):
        image_change(val0)
    stop = time.time() 

    print(f'Liniowo: {stop - start = } s')   #czas


if type=='ex':
    if __name__ == '__main__':
        start_ex = time.time()
        with ProcessPoolExecutor(10) as ex:
            for val0 in range(0, 10):
                ex.submit(image_change, val0)
        stop_ex = time.time() 

        print(f'Przyspieszone: {stop_ex - start_ex = } s')   #czas

