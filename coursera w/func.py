def func1(b):
    print('esto es b', b)
    a = []
    for i in range(0, len(b), 2):
        a.append(b[i])
    return(a)
def main():
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    for i in [51, 4, 6]:
        a = func1(a)
    print(a)
main()
