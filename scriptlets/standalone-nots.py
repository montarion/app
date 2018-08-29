from time import sleep
from socket import *
import sys
targetlist = ['192.168.178.74']


def send(message, targetlist):
    counter = 0

    while len(targetlist) > 0:
        for ipaddr in targetlist:
            print(targetlist)
            if counter == 3:
                targetlist.remove(ipaddr)
                print('failed to connect to{}'.format(ipaddr))
                counter = 0
                break
            print("running standardops send")
            host = ipaddr
            port = 5555
            buf = 1024
            addr = ((host, port))
            TCPSock = socket(AF_INET, SOCK_STREAM)
            if message[-1] != "\n":
                finalmsg = message + "\r\n"
            else:
                finalmsg = message
            print(finalmsg)

            try:
                TCPSock.connect(addr)
                print('connected to', addr)
                sleep(4)
                TCPSock.send(bytes(finalmsg, "utf-8"))
                print('succes!')
                targetlist.remove(ipaddr)
                counter = 0
            except:

                TCPSock.close()
                sleep(1)
                print("failure")
                counter += 1
        print('socket closed.')
        TCPSock.close()

#handles title
if sys.argv[1] == "notification":
    send("!not1-Alert!", [sys.argv[3]])
    sleep(3)
    send("!not2-" + sys.argv[2], [sys.argv[3]])

if sys.argv[1] == "morse":
    print("!mor-" + sys.argv[2], [sys.argv[3]])
    send("!mor-" + sys.argv[2], [sys.argv[3]])
    
else:
    send(sys.argv[1], [sys.argv[2]])

