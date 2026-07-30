import urllib.request
import json

# Credenciales configuradas
TWELVE_DATA_KEY = "845b63a569314ab292f32bf91c0aeebd"
SUPABASE_URL = "https://anmkioskzubmpzddisl.supabase.co"
SUPABASE_KEY = "sb_publishable_9bAQgfSRr2pc32uiq_N5Nw_Rg3puS1y"

def obtener_precio_cacao():
    url = f"https://api.twelvedata.com/price?symbol=CC&apikey={TWELVE_DATA_KEY}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if "price" in data:
                return float(data["price"])
            else:
                print("Aviso API Twelve Data:", data)
                return 5244.0
    except Exception as e:
        print("Error al obtener Cacao NY:", e)
        return 5244.0

def obtener_trm_colombia():
    url = "https://www.datos.gov.co/resource/32sa-213a.json?$limit=1&$order=vigenciadesde%20DESC"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if len(data) > 0 and "valor" in data[0]:
                return float(data[0]["valor"])
            else:
                return 3920.50
    except Exception as e:
        print("Error al obtener TRM Colombia:", e)
        return 3920.50

def guardar_en_supabase(precio_ny, trm):
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

    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            print(f"✅ Sincronización exitosa -> Cacao NY: ${precio_ny} USD/MT | TRM: ${trm} COP")
    except Exception as e:
        print("Error al guardar en Supabase:", e)

if __name__ == "__main__":
    ny = obtener_precio_cacao()
    trm = obtener_trm_colombia()
    guardar_en_supabase(ny, trm)
