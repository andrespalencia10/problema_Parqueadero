import numpy as np
import matplotlib.pyplot as plt

# parámetros
tipos_usuarios = {
    'Rápido': {'tiempo_servicio': 1, 'tiempo_llegada': 3, 'proporcion': 0.25},
    'Normal': {'tiempo_servicio': 3, 'tiempo_llegada': 3, 'proporcion': 0.20},
    'Lento': {'tiempo_servicio': 4, 'tiempo_llegada': 5, 'proporcion': 0.35},
    'Muy Lento': {'tiempo_servicio': 6, 'tiempo_llegada': 7, 'proporcion': 0.20},
}

num_cajeros = 3
# tiempo total de simulación
tiempo_simulacion = 10000  
# número de réplicas 
num_replicas = 100  


def simular_cola(tipos_usuarios, num_cajeros, tiempo_simulacion):
    colas = [[] for _ in range(num_cajeros)]
    tiempo_total_espera = {tipo_usuario: 0 for tipo_usuario in tipos_usuarios}
    conteo_usuarios = {tipo_usuario: 0 for tipo_usuario in tipos_usuarios}

    for _ in range(tiempo_simulacion):
        for cajero in range(num_cajeros):
            if colas[cajero] and colas[cajero][0] <= 0:
                colas[cajero].pop(0)
            if not colas[cajero]:
                tipo_usuario = np.random.choice(list(tipos_usuarios.keys()), p=[tipos_usuarios[tu]['proporcion'] for tu in tipos_usuarios])
                tiempo_servicio = np.random.exponential(tipos_usuarios[tipo_usuario]['tiempo_servicio'])
                tiempo_llegada = np.random.exponential(tipos_usuarios[tipo_usuario]['tiempo_llegada'])
                colas[cajero].append(tiempo_servicio)
                tiempo_total_espera[tipo_usuario] += tiempo_servicio
                conteo_usuarios[tipo_usuario] += 1
            else:
                colas[cajero][0] -= 1
    
    tiempo_promedio_espera = {tipo_usuario: tiempo_total_espera[tipo_usuario] / conteo_usuarios[tipo_usuario] if conteo_usuarios[tipo_usuario] > 0 else 0 for tipo_usuario in tipos_usuarios}
    return tiempo_promedio_espera, conteo_usuarios

# Realizar múltiples réplicas
todos_tiempos_espera = []
todos_conteos_usuarios = []
for _ in range(num_replicas):
    tiempo_promedio_espera, conteo_usuarios = simular_cola(tipos_usuarios, num_cajeros, tiempo_simulacion)
    todos_tiempos_espera.append(tiempo_promedio_espera)
    todos_conteos_usuarios.append(conteo_usuarios)

# Promedios 
promedio_tiempos_espera = {tipo_usuario: np.mean([rep[tipo_usuario] for rep in todos_tiempos_espera]) for tipo_usuario in tipos_usuarios}
promedio_conteos_usuarios = {tipo_usuario: np.mean([rep[tipo_usuario] for rep in todos_conteos_usuarios]) for tipo_usuario in tipos_usuarios}

# Gráficos
plt.figure(figsize=(10, 6))
plt.bar(promedio_tiempos_espera.keys(), promedio_tiempos_espera.values())
plt.xlabel('Tipo de Usuario')
plt.ylabel('Tiempo Promedio de Espera (minutos)')
plt.title('Tiempo Promedio de Espera por Tipo de Usuario')
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(promedio_conteos_usuarios.keys(), promedio_conteos_usuarios.values())
plt.xlabel('Tipo de Usuario')
plt.ylabel('Promedio de Usuarios Atendidos')
plt.title('Promedio de Usuarios Atendidos por Tipo')
plt.show()
