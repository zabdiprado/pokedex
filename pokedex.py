import sqlite3
import requests
from PIL import Image
from io import BytesIO

# Crear la base de datos y la tabla
def inicializar_bd():
    conexion = sqlite3.connect("pokedex.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            nivel INTEGER NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

# Función para agregar un Pokémon
def agregar_pokemon(nombre, tipo, nivel):
    conexion = sqlite3.connect("pokedex.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO pokemon (nombre, tipo, nivel) VALUES (?, ?, ?)", (nombre, tipo, nivel))
    conexion.commit()
    conexion.close()
    print(f"Pokémon {nombre} agregado exitosamente.")

# Función para buscar un Pokémon en la Pokédex local y obtener información de la API
def buscar_pokemon(nombre):
    # Primero, buscamos el Pokémon en nuestra base de datos local
    conexion = sqlite3.connect("pokedex.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pokemon WHERE nombre = ?", (nombre,))
    pokemon_bd = cursor.fetchone()
    conexion.close()
    
    if pokemon_bd:
        print(f"Información de la base de datos: ID: {pokemon_bd[0]}, Nombre: {pokemon_bd[1]}, Tipo: {pokemon_bd[2]}, Nivel: {pokemon_bd[3]}")
    else:
        print("Pokémon no encontrado en la base de datos. Buscando en la API...")

    # Consultamos la API de Pokémon para obtener más información
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        nombre_api = data['name'].capitalize()
        tipos = [tipo['type']['name'] for tipo in data['types']]
        imagen = data['sprites']['front_default']

        print(f"\nInformación desde la API:")
        print(f"Nombre: {nombre_api}")
        print(f"Tipos: {', '.join(tipos)}")
        print(f"Imagen: {imagen}")

        # Mostrar la imagen
        mostrar_imagen(imagen)
    else:
        print("No se pudo encontrar el Pokémon en la API.")

# Función para mostrar la imagen
def mostrar_imagen(imagen_url):
    response = requests.get(imagen_url)
    img = Image.open(BytesIO(response.content))
    img.show()

# Función para actualizar un Pokémon
def actualizar_pokemon(id, nombre, tipo, nivel):
    conexion = sqlite3.connect("pokedex.db")
    cursor = conexion.cursor()
    cursor.execute("UPDATE pokemon SET nombre = ?, tipo = ?, nivel = ? WHERE id = ?", (nombre, tipo, nivel, id))
    conexion.commit()
    conexion.close()
    print(f"Pokémon con ID {id} actualizado correctamente.")

# Función para eliminar un Pokémon
def eliminar_pokemon(id):
    conexion = sqlite3.connect("pokedex.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM pokemon WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()
    print(f"Pokémon con ID {id} eliminado correctamente.")

# Función para listar todos los Pokémon
def listar_pokemon():
    conexion = sqlite3.connect("pokedex.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pokemon")
    pokemones = cursor.fetchall()
    conexion.close()
    return pokemones

# Menú interactivo
def menu():
    while True:
        print("\n--- Pokédex ---")
        print("1. Agregar Pokémon")
        print("2. Buscar Pokémon")
        print("3. Actualizar Pokémon")
        print("4. Eliminar Pokémon")
        print("5. Listar todos los Pokémon")
        print("6. Salir")
        
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nombre = input("Nombre del Pokémon: ")
            tipo = input("Tipo del Pokémon: ")
            nivel = int(input("Nivel del Pokémon: "))
            agregar_pokemon(nombre, tipo, nivel)

        elif opcion == "2":
            nombre = input("Nombre del Pokémon a buscar: ")
            buscar_pokemon(nombre)

        elif opcion == "3":
            id = int(input("ID del Pokémon a actualizar: "))
            nombre = input("Nuevo nombre del Pokémon: ")
            tipo = input("Nuevo tipo del Pokémon: ")
            nivel = int(input("Nuevo nivel del Pokémon: "))
            actualizar_pokemon(id, nombre, tipo, nivel)

        elif opcion == "4":
            id = int(input("ID del Pokémon a eliminar: "))
            eliminar_pokemon(id)

        elif opcion == "5":
            pokemones = listar_pokemon()
            for p in pokemones:
                print(f"ID: {p[0]}, Nombre: {p[1]}, Tipo: {p[2]}, Nivel: {p[3]}")

        elif opcion == "6":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intenta nuevamente.")

inicializar_bd()
menu()

