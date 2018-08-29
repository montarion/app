import csv
newvidlist = []
oldvidlist = []
with open('vidlist3.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    header = next(reader)
    header = next(reader)
    for row in reader:
        vidlink = row[1]
        newvidlist.append(vidlink)
print(newvidlist)
with open('realvidlinks.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        oldvidlink = row[0]
        oldvidlist.append(oldvidlink)

with open('realvidlinks.csv', 'a') as f:
    writer = csv.writer(f)
    i = 0
    for line in newvidlist:
        if line not in oldvidlist: 
            writer.writerow([line])
            i += 1
    print(i)
