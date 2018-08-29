# first off, what do you want?
# always on server, reads messages and decides what to do with them
#
#
#
#
#
import csv, threading
from time import sleep

from components.server import discover, standardops, specops
t1 = threading.Thread(target=discover().listen)
t2 = threading.Thread(target=standardops().listen)
t3 = threading.Thread(target=standardops().standard)
t1.start()
t2.start()
t3.start()
print('nope still here muahahah')
targetchoice = 'anime'
targetip = []


def update(targetchoice):
    targetip.clear()
    with open('database.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            for value in row:
                if targetchoice in value:
                    print("found {}".format(row[0]))
                    targetip.append(row[0])


ipaddr = "192.168.178.74"
t4 = threading.Thread(target=specops().menu)
t4.start()
