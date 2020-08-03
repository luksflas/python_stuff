
lst = [100, 115, 784, 555, 400, 513, 200, 299, 315, 361, 787, 1029, 829, 899, 258, 321, 399, 523, 125, 199, 123, 699, 203, 259, 313, 1029, 999, 300, 399, 499, 279, 259, 200, 357, 396, 279, 299, 201, 279, 354,]
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
for x in  lst:
    x = int(x)
    if  x <= 200:
        count1 = count1 + 1
    elif  x <= 400:
        count2 = count2 + 1
    elif  x <= 600:
        count3 = count3 + 1
    elif  x <= 800:
        count4 = count4 + 1
    elif  x <= 1000:
        count5 = count5 + 1
    elif  x <= 1200:
        count6 = count6 + 1
total = 40.0
print('fi', count1, count2, count3, count4, count5, count6)
print('hi', count1/total, count2/total, count3/total, count4/total, count5/total, count6/total)
