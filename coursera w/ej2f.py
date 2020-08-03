def bisiesto(x):
  if x%4==0 and (not(x%100==0) or x%400==0 ):
    texto ='es bisiesto.'
  else:
    texto ='es un anno NO bisiesto.'
  return texto
x = int(input('Introduzca un anno entre 1600 y 2500:'))
print(x,bisiesto(x))
