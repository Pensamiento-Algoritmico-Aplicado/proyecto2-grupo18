import sys
import pickle
from bisect import bisect_left, bisect_right
 
def truncar(valor: float) -> str:
    """Trunca a 1 decimal (no redondea)."""
    return f"{int(valor * 10) / 10.0:.1f}"
 
def procesar_consultas(archivo_consultas: str, archivo_salida: str) -> None:
    with open('datos.pkl', 'rb') as f:
        datos = pickle.load(f)
 
    sectores = datos['sectores']             # (sector, tipo) -> {horas, valores}
    sensores = datos['sensores']             # (sensor, tipo) -> {horas, valores}
    sensores_sector = datos['sensores_sector']  # sector -> set de sensores
 
    resultados = []
 
    with open(archivo_consultas, 'r') as f:
        for linea in f:
            partes = linea.strip().split()
            if not partes:
                continue
            tipo = partes[0]
 
            # MAX_VIB_RANGO <sector> <tiempo_inicial> <tiempo_final> 
            if tipo == 'MAX_VIB_RANGO':
                clave = (partes[1], 'VIB')
                if clave not in sectores:
                    resultados.append('NODATA')
                    continue
                horas = sectores[clave]['horas']
                valores = sectores[clave]['valores']
                i = bisect_left(horas, partes[2])
                j = bisect_right(horas, partes[3])
                if i < j:
                    resultados.append(truncar(max(valores[i:j])))
                else:
                    resultados.append('NODATA')
 
            # ── PROM_TEMP <sector> <fecha_específica> ─────────────────────────────────
            elif tipo == 'PROM_TEMP':
                clave = (partes[1], 'TEMP')
                fecha = partes[2]
                if clave not in sectores:
                    resultados.append('NODATA')
                    continue
                horas = sectores[clave]['horas']
                valores = sectores[clave]['valores']
                i = bisect_left(horas, f"{fecha}T00:00:00")
                j = bisect_right(horas, f"{fecha}T23:59:59")
                if i < j:
                    sub = valores[i:j]
                    resultados.append(truncar(sum(sub) / len(sub)))
                else:
                    resultados.append('NODATA')
 
            # ── PICOS_VIB <sensor> <limite_umbral> ───────────────────────────────
            elif tipo == 'PICOS_VIB':
                clave = (partes[1], 'VIB')
                umbral = float(partes[2])
                if clave not in sensores:
                    resultados.append('NODATA')
                    continue
                horas = sensores[clave]['horas']
                valores = sensores[clave]['valores']
                picos = [horas[i] for i, v in enumerate(valores) if v > umbral]
                resultados.append(','.join(picos) if picos else 'NONE')
 # ── RANGO_TEMP_TS <sector> <ts_ini> <ts_fin> ──────────────────
            elif tipo == 'RANGO_TEMP_TS':
                clave = (partes[1], 'TEMP')
                if clave not in sectores:
                    resultados.append('NODATA')
                    continue
                horas = sectores[clave]['horas']
                valores = sectores[clave]['valores']
                i = bisect_left(horas, partes[2])
                j = bisect_right(horas, partes[3])
                if i < j:
                    sub = valores[i:j]
                    resultados.append(
                        f"{truncar(min(sub))},{truncar(max(sub))},{truncar(sum(sub)/len(sub))}"
                    )
                else:
                    resultados.append('NODATA')
 
            # ── SENSORES_SECTOR <sector> ───────────────────────────────────
            elif tipo == 'SENSORES_SECTOR':
                sector = partes[1]
                if sector not in sensores_sector:
                    resultados.append('NODATA')
                    continue
                lista = sorted(sensores_sector[sector], key=lambda s: int(s[1:]))
                resultados.append(','.join(lista))
 
            # ── SIGUIENTE_MEDICION <sensor> <tipo_med> <timestamp> ─────────
            elif tipo == 'SIGUIENTE_MEDICION':
                clave = (partes[1], partes[2])
                ts = partes[3]
                if clave not in sensores:
                    resultados.append('NODATA')
                    continue
                horas = sensores[clave]['horas']
                valores = sensores[clave]['valores']
                i = bisect_right(horas, ts)   # estrictamente posterior
                if i < len(horas):
                    resultados.append(f"{horas[i]},{truncar(valores[i])}")
                else:
                    resultados.append('NONE')
 
    with open(archivo_salida, 'w') as f:
        f.write('\n'.join(resultados) + '\n')
 
if __name__ == '__main__':
    procesar_consultas(sys.argv[1], sys.argv[2])
          