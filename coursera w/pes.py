vehiculos = {}
while True:
    respuesta = input('Si quiere agregra un matricula pulse A\n si quiere buscar una pulse B\n si quiere salir pulse S\n recuerde usar mayusculas, y apostrofos cuando escriba algo en la consola, gracias \n > ')
    if respuesta == 'A':
        matricula = input('introduzca la matricula: ')
        nombre = input('intruduzca el nombre: ')
        if nombre in vehiculos.keys() and matricula in vehiculos.values():
            print('ERROR')
            continue
        vehiculos[nombre] = matricula
    elif respuesta == 'B':
        busqueda = input('Inicia una busqueda')
        busqueda2 = vehiculos.get(busqueda)
        if not busqueda2 :
            print('No hemos encontrado', busqueda2)
        else:
            print(busqueda2)
    elif respuesta == 'S':
        break
