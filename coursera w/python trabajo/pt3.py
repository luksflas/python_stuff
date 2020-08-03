import re
fname = 'Documento.txt'
lst = []
fh = open(fname)
suma = re.findall('[0-9]+', fh.read())
for i in suma:
    i = int(i)
    lst.append(i)
print(sum(lst))





