# Verificacion-VLAN.py
numero_vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= numero_vlan <= 1005:
    print("La VLAN corresponde al rango normal.")
elif 1006 <= numero_vlan <= 4094:
    print("La VLAN corresponde al rango extendido.")
else:
    print("Número de VLAN no válido.")

