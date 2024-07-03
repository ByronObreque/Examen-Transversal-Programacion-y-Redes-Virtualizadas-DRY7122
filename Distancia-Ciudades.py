import requests
import urllib.parse

# Define la clave de API y las URLs de geocodificación y ruta
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "e955bb45-d45b-4b79-90ab-0333606009bb"  # Reemplaza con tu clave de API de Graphhopper

# Función para obtener coordenadas de una ciudad
def get_coordinates(city, key):
    url = geocode_url + urllib.parse.urlencode({"q": city, "limit": "1", "key": key})
    response = requests.get(url)
    data = response.json()
    
    if 'hits' not in data or len(data['hits']) == 0:
        print(f"No se encontraron coordenadas para {city}")
        return None
    
    location = data['hits'][0]['point']
    return location['lat'], location['lng']

# Función para obtener información de la ruta
def get_route_info(api_key, origin_coords, destination_coords, vehicle):
    params = {
        'point': [f"{origin_coords[0]},{origin_coords[1]}", f"{destination_coords[0]},{destination_coords[1]}"],
        'vehicle': vehicle,
        'locale': 'es',
        'instructions': 'true',
        'calc_points': 'true',
        'key': api_key
    }
    
    response = requests.get(route_url, params=params)
    data = response.json()
    
    if 'paths' not in data:
        print("Error al obtener la ruta. Por favor, verifica las ciudades ingresadas.")
        return None
    
    path = data['paths'][0]
    distance_km = path['distance'] / 1000.0
    time_ms = path['time']
    
    return distance_km, time_ms, path['instructions']

# Función principal
def main():
    api_key = key  # Usamos la clave de API definida anteriormente
    
    while True:
        origin = input("Ingrese Ciudad de Origen: ")
        if origin.lower() in ['s', 'salir']:
            print("Saliendo del programa.")
            break
        
        destination = input("Ingrese Ciudad de Destino: ")
        if destination.lower() in ['s', 'salir']:
            print("Saliendo del programa.")
            break
        
        origin_coords = get_coordinates(origin, api_key)
        destination_coords = get_coordinates(destination, api_key)
        
        if not origin_coords or not destination_coords:
            continue

        print("Medios de transporte disponibles: car, bike, or foot.")
        vehicle = input("Ingrese el medio de transporte: ").lower()
        while vehicle not in ['car', 'bike', 'foot', 's']:
            print("Medio de transporte no válido. Intente de nuevo.")
            vehicle = input("Ingrese el medio de transporte: ").lower()
        if vehicle == 's':
            print("Saliendo del programa.")
            break
        
        # Obtén información de la ruta entre las ciudades proporcionadas por el usuario
        route_info = get_route_info(api_key, origin_coords, destination_coords, vehicle)
        if route_info is None:
            continue

        distance_km, time_ms, instructions = route_info
        print(f"\nDistancia entre {origin} y {destination}: {distance_km:.2f} km")
        
        # Mostrar la duración del viaje en horas, minutos y segundos
        hours = int(time_ms // (1000 * 60 * 60))
        minutes = int((time_ms % (1000 * 60 * 60)) // (1000 * 60))
        seconds = int((time_ms % (1000 * 60)) // 1000)
        
        print(f"Duración del viaje: {hours} horas, {minutes} minutos, {seconds} segundos")

        # Imprimir la narrativa del viaje
        print("\nNarrativa del viaje:")
        for instruction in instructions:
            print(f"{instruction['distance']:.2f} m: {instruction['text']}")
        
        salir = input("\nIngrese 's' para salir o cualquier otra tecla para continuar: ").lower()
        if salir == 's':
            print("Saliendo del programa.")
            break

if __name__ == "__main__":
    main()

