import sys
import pickle
 
def procesar_log(archivo: str) -> None:
    sectores = {}         # (sector, tipo) -> {'horas': [...], 'valores': [...]}
    sensores = {}         # (sensor, tipo) -> {'horas': [...], 'valores': [...]}
    sensores_sector = {}  # sector -> set de sensores
 
    with open(archivo, 'r') as f:
        for linea in f:
            partes = linea.strip().split('|')
            if len(partes) != 5:
                continue
 
            ts, sensor, tipo, valor_str, sector = partes
 
            # Filtrar tipos no válidos
            if tipo not in ('VIB', 'TEMP'):
                continue
 
            # Filtrar valores fuera de rango
            try:
                valor = float(valor_str)
            except ValueError:
                continue
 
            if tipo == 'VIB' and not (0.0 <= valor <= 50.0):
                continue
            if tipo == 'TEMP' and not (-10.0 <= valor <= 60.0):
                continue
 
            # Guardar en sectores
            clave_sector = (sector, tipo)
            if clave_sector not in sectores:
                sectores[clave_sector] = {'horas': [], 'valores': []}
            sectores[clave_sector]['horas'].append(ts)
            sectores[clave_sector]['valores'].append(valor)
 
            # Guardar en sensores
            clave_sensor = (sensor, tipo)
            if clave_sensor not in sensores:
                sensores[clave_sensor] = {'horas': [], 'valores': []}
            sensores[clave_sensor]['horas'].append(ts)
            sensores[clave_sensor]['valores'].append(valor)
 
            # Registrar sensor en su sector
            if sector not in sensores_sector:
                sensores_sector[sector] = set()
            sensores_sector[sector].add(sensor)
 
    # Ordenar todo por timestamp antes de guardar
    for reg in sectores.values():
        pares = sorted(zip(reg['horas'], reg['valores']))
        reg['horas'] = [h for h, _ in pares]
        reg['valores'] = [v for _, v in pares]
 
    for reg in sensores.values():
        pares = sorted(zip(reg['horas'], reg['valores']))
        reg['horas'] = [h for h, _ in pares]
        reg['valores'] = [v for _, v in pares]
 
    # Serializar
    datos = {
        'sectores': sectores,
        'sensores': sensores,
        'sensores_sector': sensores_sector
    }
    with open('datos.pkl', 'wb') as f:
        pickle.dump(datos, f)
 
    print("Listo. Archivo datos.pkl generado.")
 
if __name__ == '__main__':
    procesar_log(sys.argv[1])