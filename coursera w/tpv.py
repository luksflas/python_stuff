monedas_y_billetes = [50, 20, 10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.01]

cambio = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
vueltas = None
precio = float(input('Introduzca el precio:'))
descuento = float(input('Introduzca descuento:'))
cantidad_entregada = float(input('Introduzca importe:'))
if descuento != 0:
    des = precio/100*descuento
    precio = precio - des
    vueltas = cantidad_entregada-precio
    print('A devolver:', vueltas)
else:
    vueltas = cantidad_entregada-precio
    print('A devolver:', vueltas)

print('Para sumar', vueltas, 'Se necesitan:', )

for i in range(len(monedas_y_billetes)):

    while vueltas >= monedas_y_billetes[i]:
        vueltas -= monedas_y_billetes[i]
        cambio[i] += 1

print(sum(cambio), 'monedas o billetes:')

for i in range(len(monedas_y_billetes)):
    print(cambio[i], 'monedas o billete de ', monedas_y_billetes[i], 'euros' )
