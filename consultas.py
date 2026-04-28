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

if __name__ == '__main__':
    ejecutar()