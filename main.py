from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import DB
from datetime import datetime

app = FastAPI(title="RFID Cloud - Usuarios")
db = DB()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        conn = db.connect()
        cur = conn.cursor()
        
        # Leer directamente de la tabla 'usuarios' de tu proyecto RFID
        cur.execute("""
            SELECT uid_limpio, nombre, fecha_registro, notas, ultimo_evento 
            FROM usuarios 
            ORDER BY fecha_registro DESC
        """)
        usuarios = cur.fetchall()
        conn.close()

        return templates.TemplateResponse("index.html", {
            "request": request,
            "usuarios": usuarios,
            "total": len(usuarios),
            "now": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
    except Exception as e:
        print(f"ERROR: {e}")
        return HTMLResponse(f"""
        <h1>❌ Error de conexión</h1>
        <p>{str(e)}</p>
        <p>Asegúrate de que la variable DATABASE_URL esté correcta y que la tabla 'usuarios' exista.</p>
        """, status_code=500)

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)