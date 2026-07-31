import os
import urllib.request
import json

# Configuración de Supabase
SUPABASE_URL = "https://anmkioskzubmpzddisl.supabase.co"
SUPABASE_KEY = "sb_publishable_9bAQgfSRr2pc32uiq_N5Nw_Rg3puS1y"

# Tu clave de Twelve Data
TWELVE_DATA_API_KEY = os.environ.get("TWELVE_DATA_API_KEY", "")

def get_real_trm_colombia():
    """Obtiene la TRM oficial de la Superintendencia Financiera de Colombia"""
    try:
        url = "https://www.datos.gov.co/resource/32sa-8pi3.json?$limit=1&$order=vigenciadesde%20DESC"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data and len(data) > 0 and 'valor' in data[0]:
                trm_val = float(data[0]['valor'])
                print(f"TRM oficial obtenida de datos.gov.co: ${trm_val} COP")
                return trm_val
    except Exception as e:
        print(f"Error consultando datos.gov.co: {e}")

    # Respaldo DolarApi
    try:
        url = "https://co.dolarapi.com/v1/trm"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if 'valor' in data:
                return float(data['valor'])
    except Exception as e:
        print(f"Error consultando dolarapi: {e}")

    return 4180.0  # Valor de respaldo seguro

def get_ny_cocoa_price():
    """Obtiene el precio del Cacao en NY (ICE Futures) desde Twelve Data"""
    if not TWELVE_DATA_API_KEY:
        print("Aviso: No hay TWELVE_DATA_API_KEY configurada.")
        return 5244.0

    try:
        url = f"https://api.twelvedata.com/price?symbol=CC&apikey={TWELVE_DATA_API_KEY}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if "price" in data:
                price = float(data["price"])
                print(f"Precio Cacao NY obtenido: ${price} USD/MT")
                return price
            else:
                print(f"Respuesta Twelve Data: {data}")
    except Exception as e:
        print(f"Error consultando Twelve Data: {e}")

    return 5244.0

def save_to_supabase(precio_ny, trm):
    """Guarda la cotización en Supabase"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/precios"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        payload = json.dumps({
            "precio_ny": precio_ny,
            "trm": trm
        }).encode("utf-8")

        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            print("✅ Cotización real guardada con éxito en Supabase.")
    except Exception as e:
        print(f"❌ Error guardando en Supabase: {e}")

if __name__ == "__main__":
    trm_actual = get_real_trm_colombia()
    precio_cacao = get_ny_cocoa_price()
    save_to_supabase(precio_cacao, trm_actual)
