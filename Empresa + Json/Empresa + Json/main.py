import os
import DAO.CRUDCliente
from DTO.Tipo import Tipo_Usuario
from DTO.Cliente import Cliente
from DTO.Usuario import Usuario
from getpass import getpass
import re
from DAO.Conexion import Conexion
import requests
import mysql.connector

def obtener_datos_desde_api():
    url = "https://raw.githubusercontent.com/SeeHunm/CodigoEv4/refs/heads/main/watonaculina"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error al hacer la solicitud:", e)
        return None

#Módulo Json --------------------------------------------------
# print("Datos de json")
# data = obtener_datos_desde_api()
# print(data)

# conn = mysql.connector.connect(
#     host = 'localhost',
#     user = 'userempresa',
#     password = 'V3ntana.13',
#     db = 'empresa'
# )

# cursor= conn.cursor()
# for item in data: 
#     try:
#         cursor.execute('''
#             INSERT INTO cliente (run,nombre,apellido,direccion,fono,correo,montoCredito,deuda,Tipo_id)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         ''', (item['run'], item['nombre'], item['apellido'], item['direccion'], item['fono'], item['correo'], item['montoCredito'], item['deuda'], item['tipo']))
#     except mysql.connector.Error as err:
#         print(f"Error al insertar los datos: {err}")

# conn.commit()
# input("\n\n Datos Json traspasados con éxito...")
# conn.close()
#-----------------------------------------------------------------------

def validar_no_vacio(mensaje):
    while True:
        valor = input(mensaje)
        if valor.strip():
            return valor
        print("El campo no puede estar vacío. Intente nuevamente.")

def validar_nombre(mensaje):
    patron = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$'
    while True:
        valor = input(mensaje).strip()
        if re.match(patron, valor):
            return valor
        print(f"Su nombre solo debe contener letras. Intente nuevamente.")

def validar_num(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit():
            return valor
        print("El campo debe contener solo números. Intente nuevamente.")

def validar_correo(mensaje):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    while True:
        valor = input(mensaje)
        if re.match(patron, valor):
            return valor
        print("Correo inválido. Intente nuevamente.")

def validar_tipo_usuario():
    while True:
        try:
            tipo = int(input("Ingrese el tipo de usuario (1 para Administrador, 2 para Vendedor): "))
            if tipo in [1, 2]:
                return "Administrador" if tipo == 1 else "Vendedor"
            else:
                print("Opción no válida. Debe ser 1 o 2.")
        except ValueError:
            print("Debe ingresar un número válido.")

def validar_op():
    while True:
        try:
            tipo = int(input("Ingrese el tipo de usuario (1 para Administrador, 2 para Vendedor): "))
            if tipo in [1, 2, 3]:
                return "Administrador" if tipo == 1 else "Vendedor"
            else:
                print("Opción no válida. Debe ser 1 o 2.")
        except ValueError:
            print("Debe ingresar un número válido.")            

def menuUsuarios():
    while True:
        try:
            print("=================================")
            print("          MENÚ USUARIOS          ")
            print("=================================")
            print("     1. Iniciar sesión           ")
            print("     2. Registrar usuario        ")
            print("     3. Salir                    ")
            print("=================================")            
            opcion = int(input("INGRESE OPCIÓN: "))
            
            if opcion in [1, 2, 3]:
                return opcion
            else:
                print("Error: El valor ingresado está fuera de rango. Intente nuevamente.")
        except ValueError:
            print("Error: Debe ingresar un número válido. Intente nuevamente.")

def ingresoUsuarios():
    os.system('cls')
    print("=================================")
    print("       INGRESO DE USUARIO       ")
    print("=================================")
    username = validar_no_vacio("INGRESE NOMBRE DE USUARIO: ")
    
    while True:
        clave1 = getpass("INGRESE PASSWORD   : ")
        clave2 = getpass("REPITA PASSWORD    : ")
        if clave1 == clave2:
            break
        print("Las contraseñas no coinciden. Intente nuevamente")
    
    nombre = validar_nombre("INGRESE NOMBRE      : ")
    apellidos = validar_nombre("INGRESE APELLIDOS   : ")
    correo = validar_correo("INGRESE CORREO      : ")
    
    print("--------- TIPOS DE USUARIOS ---------")
    print("    1 para Administrador")
    print("    2 para Vendedor")
    tipo = validar_tipo_usuario()
    print("-------------------------------------")
    
    if tipo == 1:
        tipo = "Administrador"
    else:
        tipo = "Vendedor"
    
    Usuario.registrar_usuario(username, clave1, nombre, apellidos, correo, tipo)
    print("=================================")

def menuprincipal():
        while True:
            os.system('cls')
            try:
                
                print("""
                        ================================
                            M E N Ú  P R I N C I P A L
                        ================================
                                1.- (C) INGRESAR
                                2.- (R) MOSTRAR
                                3.- (U) MODIFICAR
                                4.- (D) ELIMINAR
                                5.- (E) TRASPASO DE JSON A BD
                                6.- (P) SALIR AL MENÚ USUARIOS
                        ================================""")
                opcion = int(input("Seleccione una opción [1-6]: "))
                if opcion in [1, 2, 3, 4, 5, 6]:
                    return opcion
                else:
                    print("Error: El valor ingresado está fuera de rango. Intente nuevamente.")
            except ValueError:
                print("Error: Debe ingresar un número válido. Intente nuevamente.")

def menumostrar():
    os.system('cls')
    print("""
            ================================
                M E N Ú  M O S T R A R
            ================================
                    1.- MOSTRAR TODO
                    2.- MOSTRAR UNO
                    3.- MOSTRAR PARCIAL
                    4.- VOLVER
            ================================""")

def ingresardatos():
    os.system('cls')
    print("""
            ================================
                INGRESAR DATOS CLIENTE
            ================================""")
    run = validar_num("INGRESE RUN: ")
    nombre = validar_nombre("INGRESE NOMBRE: ")
    apellido = validar_nombre("INGRESE APELLIDO: ")
    direccion = validar_no_vacio("INGRESE DIRECCION: ")
    fono = validar_num("INGRESE TELEFONO: ")
    correo = validar_correo("INGRESE CORREO: ")

    datos = DAO.CRUDCliente.mostrartipos()
    print("-----------------------------------")
    for dato in datos:
        print("CÓDIGO: {} - {}.".format(dato[0], dato[1]))
    print("-----------------------------------")

    tipo = int(validar_num("Ingrese el código del Tipo de Cliente: "))
    monto = int(validar_num("INGRESE MONTO CRÉDITO: "))

    c = Cliente(run, nombre, apellido, direccion, fono, correo, tipo, monto, deuda=0)
    DAO.CRUDCliente.agregar(c)

def mostrar():
    while(True):
        menumostrar()
        op2 = int(input("   INGRESE OPCIÓN: "))
        if op2 == 1:
            mostrartodo()
            input("\n\n PRESIONE ENTER PARA CONTINUAR")
        elif op2 == 2:
            mostraruno()
        elif op2 == 3:
            mostrarparcial()
        elif op2 == 4:
            break
        else:
            print("Opción Fuera de Rango")

def mostrartodo():
    os.system('cls')
    print("""
            ================================
            MUESTRA DE TODOS LOS CLIENTES
            ================================""")
    datos = DAO.CRUDCliente.mostrartodos()
    for dato in datos:
        print("ID: {} - RUN: {} - NOMBRE: {} - APELLIDO: {} - DIRECCIÓN: {} - FONO: {} - CORREO: {} - MONTO CRÉDITO: {} - DEUDA: {} - TIPO: {}".format(
        dato[0],dato[1],dato[2],dato[3],dato[4],dato[5],dato[6],dato[7],dato[8],dato[9]))
        print("-------------------------------------------------------------------------------------------------------------------------------------")

def mostraruno():
    os.system('cls')
    print("""
            ================================
                MUESTRA DE DATOS PARTICULAR
            ================================""")
    op = int(input("\n Ingrese valor de ID del Cliente que desea Mostrar los Datos: "))
    datos = DAO.CRUDCliente.consultaparticular(op)
    print("""
            ================================
                MUESTRA DE DATOS DEL CLIENTE
            ================================
            ID              : {}
            RUN             : {}
            NOMBRE          : {}
            APELLIDO        : {}
            DIRECCIÓN       : {}
            FONO            : {}
            CORREO          : {}
            TIPO            : {}
            MONTO CRÉDITO   : {}
            DEUDA           : {}
            --------------------------------
            """.format(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6],datos[7],datos[8],datos[9]))
    input("\n\n PRESIONE ENTER PARA CONTINUAR")

def mostrarparcial():
    os.system('cls')
    print("""
            ===================================
                MUESTRA PARCIALMENTE LOS CLIENTES
            ===================================""")
    cant = int(input("\nIngrese la Cantidad de Clientes a Mostrar: "))
    datos = DAO.CRUDCliente.consultaparcial(cant)
    for dato in datos:
        print("ID: {} - RUN: {} - NOMBRE: {} - APELLIDO: {} - DIRECCIÓN: {} - FONO: {} - CORREO: {} - MONTO CRÉDITO: {} - DEUDA: {} - TIPO: {}".format(
        dato[0],dato[1],dato[2],dato[3],dato[4],dato[5],dato[6],dato[7],dato[8],dato[9]))
        print("-------------------------------------------------------------------------------------------------------------------------------------")
    input("\n\n PRESIONE ENTER PARA CONTINUAR")

def modificardatos():
    os.system('cls')
    listanuevos=[]
    print("""
            ===================================
                MÓDULO MODIFICAR CLIENTE
            ===================================""")
    mostrartodo()
    mod = int(input("Ingrese valor de ID del Cliente que desea Modificar: "))
    datos = DAO.CRUDCliente.consultaparticular(mod)

    if not datos:
        print("\n\n No se encontró un cliente con el ID proporcionado.")
        input("Presione ENTER para continuar.")
        return

    print("ID              : {}".format(datos[0]))
    listanuevos.append(datos[0])
    print("RUN             : {}".format(datos[1]))
    listanuevos.append(datos[1])
    opm = input("DESEA MODIFICAR EL NOMBRE: {} - [SI/NO] ".format(datos[2]))
    if opm.lower() == "si":
        nombrenuevo = input("INGRESE NOMBRE: ")
        listanuevos.append(nombrenuevo)
    elif opm.lower() == "no":
        listanuevos.append(datos[2])
    opm = input("DESEA MODIFICAR EL APELLIDO: {} - [SI/NO] ".format(datos[3]))
    if opm.lower() == "si":
        apellidonuevo = input("INGRESE APELLIDO: ")
        listanuevos.append(apellidonuevo)
    elif opm.lower() == "no":
        listanuevos.append(datos[3])
    opm = input("DESEA MODIFICAR LA DIRECCIÓN: {} - [SI/NO] ".format(datos[4]))
    if opm.lower() == "si":
        direcnueva = input("INGRESE DIRECCIÓN: ")
        listanuevos.append(direcnueva)
    elif opm.lower() == "no":
        listanuevos.append(datos[4])
    opm = input("DESEA MODIFICAR EL TELÉFONO: {} - [SI/NO] ".format(datos[5]))
    if opm.lower() == "si":
        fononuevo = input("INGRESE TELÉFONO: ")
        listanuevos.append(fononuevo)
    elif opm.lower() == "no":
        listanuevos.append(datos[5])
    opm = input("DESEA MODIFICAR EL CORREO: {} - [SI/NO] ".format(datos[6]))
    if opm.lower() == "si":
        correonuevo = input("INGRESE EL CORREO: ")
        listanuevos.append(correonuevo)
    elif opm.lower() == "no":
        listanuevos.append(datos[6])
    opm = input("DESEA MODIFICAR LA DEUDA: {} - [SI/NO] ".format(datos[8]))
    if opm.lower() == "si":
        deudanuevo = input("INGRESE DEUDA: ")
        listanuevos.append(deudanuevo)
    elif opm.lower() == "no":
        listanuevos.append(datos[8])
    opm = input("DESEA MODIFICAR EL MONTO DE CRÉDITO: {} - [SI/NO] ".format(datos[7]))
    if opm.lower() == "si":
        montonuevo = input("INGRESE MONTO DE CRÉDITO: ")
        listanuevos.append(montonuevo)
    elif opm.lower() == "no":
        listanuevos.append(datos[7])
    opm = input("DESEA MODIFICAR EL TIPO: {} - [SI/NO] ".format(datos[9]))
    if opm.lower() == "si":
        #recorremos los tipos
        datos = DAO.CRUDCliente.mostrartipos()
        print("-----------------------------------")
        for dato in datos:
            print("CÓDIGO: {} - {}.".format(dato[0], dato[1]))
        print("-----------------------------------")
        tiponuevo = int(validar_num("INGRESE EL TIPO: "))
        listanuevos.append(tiponuevo)
    elif opm.lower() == "no":
        listanuevos.append(datos[9])
    DAO.CRUDCliente.editar(listanuevos)

def eliminardatos():
    os.system('cls')
    print("""
            ===================================
                MÓDULO ELIMINAR CLIENTE
            ===================================""")
    mostrartodo()
    elim = int(input("Ingrese valor de ID del Cliente que desea Eliminar: "))
    DAO.CRUDCliente.eliminar(elim)


while(True):
    opUsu= menuUsuarios()
    if opUsu == 1:
        usuario1 = input("Ingrese nombre de usuario: ")
        clave = getpass("Ingrese password: ")
        usuario = Usuario.login(usuario1, clave)
        if not usuario:
            input("...Usuario No Registrado. Presione ENTER para continuar.")
        else:
            print(f"Bienvenido {usuario.nombre.upper()} {usuario.apellidos.upper()}.")
            input("...Presiona ENTRAR para ingresar al Menú Principal.")
            while True:
                opcionPrincipal = menuprincipal()
                if opcionPrincipal == 1:
                    ingresardatos()
                    input("\nPresione ENTER para volver al Menú Principal.")
                elif opcionPrincipal == 2:
                    mostrar()
                    input("\nPresione ENTER para volver al Menú Principal.")
                elif opcionPrincipal == 3:
                    modificardatos()
                    input("\nPresione ENTER para volver al Menú Principal.")
                elif opcionPrincipal == 4:
                    eliminardatos()
                elif opcionPrincipal == 5:
                    print("Datos de json")
                    data = obtener_datos_desde_api()
                    print(data)

                    conn = mysql.connector.connect(
                    host = 'localhost',
                    user = 'userempresa',
                    password = 'V3ntana.13',
                    db = 'empresa'
                    )
                    cursor= conn.cursor()
                    for item in data: 
                        try:
                            cursor.execute('''
                                INSERT INTO cliente (run,nombre,apellido,direccion,fono,correo,montoCredito,deuda,Tipo_id)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ''', (item['run'], item['nombre'], item['apellido'], item['direccion'], item['fono'], item['correo'], item['montoCredito'], item['deuda'], item['tipo']))
                        except mysql.connector.Error as err:
                            print(f"Error al insertar los datos: {err}")

                    conn.commit()
                    input("\n\n Datos Json traspasados con éxito...")
                    conn.close()
                elif opcionPrincipal == 6:
                    op2 = input("DESEA SALIR [SI/NO]: ")
                    if op2.lower() == "si":
                        exit()
                else:
                    print("Opción Fuera de Rango")
    elif opUsu == 2:
        ingresoUsuarios()
        input("....Presione ENTRAR para continuar")
    else:
        opSalir = input("DESEA SALIR [SI/NO] : ")
        if opSalir.lower() == "si":
            exit()
