new = ['banana']
old = ['apple', 'pear']

for line in new:
   if line not in old:
       old.append(line)

print(old)
