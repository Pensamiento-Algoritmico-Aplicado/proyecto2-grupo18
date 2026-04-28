import sys
import pickle
import numpy as np

def ts_a_int(ts: str) -> int:
    return int(ts[0:4]+ts[5:7]+ts[8:10]+ts[11:13]+ts[14:16]+ts[17:19])

def int_a_ts(n: int) -> str:
    s = f"{n:014d}"
    return f"{s[:4]}-{s[4:6]}-{s[6:8]}T{s[8:10]}:{s[10:12]}:{s[12:14]}"

def tr(n: float) -> str:
    return f"{int(n * 10) / 10.0:.1f}"

def ejecutar():
    if len(sys.argv) < 3: return
    
    with open('db_datos/meta.pkl', 'rb') as f:
        d = pickle.load(f)
    
    meta_sec, meta_sen, mapeo = d['sec'], d['sen'], d['map']
    respuestas = []
    cache_mmap = {}

    def get_arrays(tipo, k):
        nombre = f"{tipo}_{k[0]}_{k[1]}"
        if nombre not in cache_mmap:
            t = np.load(f"db_datos/{nombre}_t.npy", mmap_mode='r')
            v = np.load(f"db_datos/{nombre}_v.npy", mmap_mode='r')
            cache_mmap[nombre] = (t, v)
        return cache_mmap[nombre]

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea: continue
            
            p = linea.split()
            cmd = p[0]
            res = "NODATA"

            if cmd == 'MAX_VIB_RANGO':
                k = (p[1], 'VIB')
                if k in meta_sec:
                    t, v = get_arrays('sec', k)
                    i = np.searchsorted(t, ts_a_int(p[2]), side='left')
                    j = np.searchsorted(t, ts_a_int(p[3]), side='right')
                    if i < j: res = tr(np.max(v[i:j]))

            elif cmd == 'PROM_TEMP':
                k = (p[1], 'TEMP')
                if k in meta_sec:
                    t, v = get_arrays('sec', k)
                    ini = int(p[2].replace('-','')) * 1000000
                    fin = int(p[2].replace('-','')) * 1000000 + 235959
                    i = np.searchsorted(t, ini, side='left')
                    j = np.searchsorted(t, fin, side='right')
                    if i < j: res = tr(np.mean(v[i:j]))

            elif cmd == 'RANGO_TEMP_TS':
                k = (p[1], 'TEMP')
                if k in meta_sec:
                    t, v = get_arrays('sec', k)
                    i = np.searchsorted(t, ts_a_int(p[2]), side='left')
                    j = np.searchsorted(t, ts_a_int(p[3]), side='right')
                    if i < j:
                        sub = v[i:j]
                        res = f"{tr(np.min(sub))},{tr(np.max(sub))},{tr(np.mean(sub))}"
            
            respuestas.append(res)

if __name__ == '__main__':
    ejecutar()