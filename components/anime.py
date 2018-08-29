import json, requests, os


class anime:
    def __init__(self):
        self.targetip = []
        self.GREEN = '\033[92m'
        self.BLUE = '\033[94m'
        self.YELLOW = '\033[93m'
        self.RED = '\033[91m'
        self.ENDC = '\033[0m'


    def search(self):
        # ---url for releases, in JSON---#
        url = 'http://www.masterani.me/api/releases'

        # ---needed conversion---#
        test = requests.get(url)
        test1 = test.text
        test = str(test1)
        string = json.loads(str(test))
        filecheck = os.path.isfile('trackfiles/lastshow.txt')
        airingshow = string[0]['anime']["title"]
        anime = "!failure"
        if filecheck is False:
            print(self.YELLOW + "creating file.." + self.ENDC)
            lastshow = string[0]['anime']["title"]
            #---writes last aired show to file---#
            infile = open('trackfiles/lastshow.txt', 'w')
            infile.write(lastshow)
            infile.close()

        else:
            #---checks if new show has aired---#
            outfile = open('trackfiles/lastshow.txt')
            check = outfile.read()
            if check != airingshow:
                print(self.GREEN + "New show aired!" + self.ENDC)
                anime = string[0]['anime']['title']
                infile = open('trackfiles/lastshow.txt', 'w')
                extrafile = open('/var/www/tests/daemon-server-page/files/anime.txt', 'w')
                infile.write(anime)
                extrafile.write(anime)
                infile.close()
                extrafile.close()
            else:
                print(self.BLUE + "No new show" + self.ENDC)
                lastshow = string[0]['anime']["title"]
                infile = open('trackfiles/lastshow.txt', 'w')
                infile.write(lastshow)
                infile.close()
                anime = "!failure"

        return anime

