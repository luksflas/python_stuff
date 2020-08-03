import re
fname = input('enter file name:')
fh = open(fname)
for line in fh:
    suma = re.findall('[0-9]+')
sumt = sum(suma)
print(sumt)
