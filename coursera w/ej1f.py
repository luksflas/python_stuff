def esNumeropar(n):
    if n%2 == 0:
        print(n, 'es par')
    else:
        print(n, 'no es par')
def esNumeroimpar(n):
    if n%2 != 0:
        print(n, 'es impar')
    else:
        print(n, 'no es impar')
num = input('Di un numero')
esNumeropar(num)
esNumeroimpar(num)
