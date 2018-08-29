import csv
import re
from time import sleep
import traceback
from socket import *
from components.anime import anime
from components.location import location
from components.motd import motd
STOP = 'ø'
class discover:
    def __init__(self):
        pass

    def listen(self):
        host = "0.0.0.0"
        port = 5556
        buf = 2048
        addr = ((host, port))
        TCPSock = socket(AF_INET, SOCK_STREAM)
        TCPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        TCPSock.bind(addr)
        TCPSock.listen(3)
        currentaddresses = []
        with open('database.csv') as csvfile:
             i = 0
             readCSV = csv.reader(csvfile, delimiter=',')
             header = next(readCSV)
             for row in readCSV:
                 value = row[0]
                 print(value)
                 if value not in currentaddresses and value != '127.0.0.1' and value != 'address':
                     currentaddresses.append(value)
             print(currentaddresses)
        try:
                print('waiting')

                (conn, ipaddr) = TCPSock.accept()
                print("got message!")
                data = conn.recv(buf)
                ipaddr = ipaddr[0]

                data = str(data)[10:-1]

                restdata = data
                search = "(.*?) (.*)"
                print(data)
                print(ipaddr)
                if ipaddr not in currentaddresses and ipaddr != '127.0.0.1':
                    print('adding..')
                    sleep(5)
                    try:        #see if you can get name.
                        traceback.print_exc()
                        name = re.search(search, restdata).group(1)
                        try:        #if so, see if you get type. if yes, run full function.
                            traceback.print_exc()
                            type = re.search(search, restdata).group(2)
                            print('connection from {} with name {} on device {}'.format(ipaddr, name, type))
                            id = discover().assign(ipaddr, conn, name, type)
                            conn.send(bytes("!id-{}".format(id), "utf-8"))
                        except:     #if not, run function with just name.
                            traceback.print_exc()
                            id = discover().assign(ipaddr, conn, name)
                            print('connection from {} with name {}'.format(ipaddr, name))
                            conn.send(bytes("!id-{}".format(id), "utf-8"))
                    except:     #if you can't get name, see if you get get type.
                        traceback.print_exc()

                        try:        #if so, run function with just name.
                            traceback.print_exc()
                            type = re.search(search, restdata).group(2)
                            print('connection from {} on device {}'.format(ipaddr, type))
                            id = discover().assign(ipaddr, conn, type)
                            conn.send(bytes("!id-{}".format(id), "utf-8"))
                        except:     #if not, run function with just ip.
                            traceback.print_exc()
                            id = discover().assign(ipaddr, conn)
                            print('connection from {}'.format(ipaddr))
                            conn.send(bytes("!id-{}{}".format(id, STOP), "utf-8"))
                       
                
        except KeyboardInterrupt:
             TCPSock.close()
    def assign(self, ipaddr, connection, name='unknown', type='generic', sub='none'):
        print(name, type)
        linelen = 0
        with open('database.csv', 'r') as f:
             reader = csv.reader(f, delimiter=',')
             linelen = sum(1 for row in reader)
        print(linelen)
        with open('database.csv', 'a', newline='') as f:  
            id = "00"+str(linelen)
            print(id)
            writer = csv.writer(f)
            writer.writerow((ipaddr, name.lower(), type.lower(), sub.lower(),id))
        return id
conndict = {}
class standardops:
    def __init__(self):
        print('in standard')
        self.targetid = []
        self.GREEN = '\033[92m'
        self.BLUE = '\033[94m'
        self.YELLOW = '\033[93m'
        self.RED = '\033[91m'
        self.ENDC = '\033[0m'
        self.connlist = []

    def update(self, targetchoice):
        self.targetid.clear()
        with open('database.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                for value in row:
                    if targetchoice in value:
                        print(row[-1])
                        self.targetid.append(row[-1]) #id

    def updateconn(self, id, conn, newip):
        print(self.YELLOW + "changing id.." + self.ENDC)
        oldlist = []
        newlist = []
        conndict[id]= conn
        with open('database.csv') as f:
            reader = csv.reader(f, delimiter=',')
            oldlist = list(reader)
            rowcount = 0
        idfound = 0
        with open('database.csv') as f:
            reader = csv.reader(f, delimiter=',')

            
            for row in reader:
                for value in row:
                    
                    if id in value:
                        
                        print(self.YELLOW + "found id {} on row number {}.".format(id, rowcount) + self.ENDC)
                        index = rowcount
                        idfound = 1
                        break
                rowcount += 1
        if idfound == 1: 
            oldlist[index][0]=newip
            with open('database.csv', 'w', newline='') as g:
                writer = csv.writer(g)
                for line in oldlist:
                    writer.writerow(line)
            print(self.YELLOW + 'done!' + self.ENDC)
            #send ok
            conn = conndict[id]
            self.send("!ack-1", conn)	#acknowledge + statuscode 1
        
        else:
            print(self.RED + "couldn't find id" + self.ENDC)
            self.send("!idfailure", conn)

        
    def getanime(self):
        print("running anime function")
        self.update("anime")

        message = anime().search()
        if message != "!failure":
            finalmessage = "!ani-{}".format(message)
            for id in self.targetid:
                conn = conndict[id]
                self.send(finalmessage, conn)
                
    def getgps(self, target):
        #get gps coordinates
        self.update(target) #just on mobile for now
        message = "!gps"
        id = self.targetid[0]
        conn = conndict[id]
        self.send(message, conn)
    
    def getdaily(self):
        self.getgps("greylynx")

    def getdaily2(self, gpscoords):
        lat = gpscoords[:17]
        lon = gpscoords[19:]
        print(self.YELLOW + "Trying to get city.." + self.ENDC)
        city = location().search(lat, lon)
        motd(city).createmotd()
    def standard(self):
        sleep(10)
        self.getdaily()
        while True:
            sleep(30)	#boot up time :)
            self.getanime()
            
            

    
    def listen(self):
        while True:
            host = "0.0.0.0"
            port = 5555
            buf = 2048
            addr = ((host, port))
            TCPSock = socket(AF_INET, SOCK_STREAM)
            TCPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            TCPSock.bind(addr)
            TCPSock.listen(54)
            (conn, ipaddr) = TCPSock.accept()
            data = str(conn.recv(buf))[10:-1]
            print(data)
            if data[:1] == "!":
                print(self.GREEN + "got a message!" + self.ENDC)
                print(data)
            if data[:5] == "!chk-":
                print('updating')
                self.updateconn(data[5:], conn, ipaddr[0])
            if data[:5] == "!gps-":
                print(self.YELLOW + "Got gps coords." + self.ENDC)
                self.updateconn(data[5:8], conn, ipaddr[0])
                self.getdaily2(data[8:])
        
    def send(self, message, conn):
       try:
           conn.sendall(bytes(message+STOP, "utf-8"))
           print(message + " sent.")
           return 0
       except ConnectionResetError:
           print("connection was reset by client")
           return 1
       except:
           print('eh..')
           return 2


class specops:
    def __init__(self):
        self.targetid = []
        self.GREEN = '\033[92m'
        self.BLUE = '\033[94m'
        self.YELLOW = '\033[93m'
        self.RED = '\033[91m'
        self.ENDC = '\033[0m'
       
        

    
    def update(self, targetchoice):
        self.targetid.clear()
        with open('database.csv') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
               for value in row:
                   if targetchoice in value:
                       print(conndict)
                       print(row[-1])
                       self.targetid.append(row[-1])

    def menu(self):
        print(self.BLUE + "1: Send a notification.\n"
              "Please enter your choice: "+self.ENDC)
        choice = input()
        
        
        if choice == "1":
            while True:
                targetchoice = input(self.BLUE + "Please enter your target. " + self.ENDC)
                self.update(targetchoice)
                if len(self.targetid) < 1:
                    print(self.RED + "couldn't find that id.." + self.ENDC)         
                else:    
                    for target in self.targetid:
                        self.notifications(target)
        else:
           print(self.RED + "That's not a valid option. please try again." + self.ENDC)
           self.menu()
    def notifications(self, target):
        try:
            conn = conndict[target]
        except KeyError:
            print("woops couldn't find that id")
        except:
            print('eh')
        title = input(self.BLUE + "what should the title be? " + self.ENDC)
        body = input(self.BLUE + "what should the body be? " + self.ENDC)
        titlemsg = "!not1-" + title + "\n"
        bodymsg = "!not2-" + body + "\n"
        print(self.YELLOW + 'printing title' + self.ENDC)
        print(self.update(target))
        
        self.send(titlemsg, conn)
        sleep(2)
        print(self.YELLOW + 'printing body' + self.ENDC)
        
        self.send(bodymsg, conn)
        self.menu()

    def send(self, message, conn):
       try:
           conn.send(bytes(message+STOP, "utf-8"))
           print(message + " sent.")
           return 0
       except ConnectionResetError:
           print("connection was reset by client")
           return 1
       except:
           print('eh..')
           return 2

