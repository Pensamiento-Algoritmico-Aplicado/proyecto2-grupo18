import sys

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
            except Exception:
                continue

if __name__ == '__main__':
    ejecutar()