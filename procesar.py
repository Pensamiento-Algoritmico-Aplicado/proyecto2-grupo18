import sys
import os
import pickle
import array
import numpy as np

def ts_a_int(ts: str) -> int:
    return int(ts[0:4]+ts[5:7]+ts[8:10]+ts[11:13]+ts[14:16]+ts[17:19])

def ejecutar():
    if len(sys.argv) < 2: return
    archivo_in = sys.argv[1]
    
    with open(archivo_in, 'r', encoding='utf-8', buffering=16*1024*1024) as f:
        for linea in f:
            partes = linea.strip().split('|')
            if len(partes) != 5: continue
            
            ts_str, s_id, tipo, val_str, sec = partes
            if tipo not in ('VIB', 'TEMP'): continue
            
            try:
                v_num = float(val_str)
                if tipo == 'VIB' and not (0.0 <= v_num <= 50.0): continue
                if tipo == 'TEMP' and not (-10.0 <= v_num <= 60.0): continue
                
                t_int = ts_a_int(ts_str)
            except Exception:
                continue

if __name__ == '__main__':
    ejecutar()