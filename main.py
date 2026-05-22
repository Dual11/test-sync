from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import DB
from datetime import datetime
import os

app = FastAPI(title="RFID Cloud View")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        db = DB()
        conn = db.connect()
        cur = conn.cursor()   # Cursor normal (devuelve tuplas)

        cur.execute("""
            SELECT uid_limpio, nombre, fecha_registro, notas, ultimo_evento 
            FROM usuarios 
            ORDER BY fecha_registro DESC
        """)
        
        rows = cur.fetchall()
        conn.close()

        # Convertir tuplas a diccionarios manualmente
        usuarios = []
        for row in rows:
            usuarios.append({
                "uid_limpio": row[0],
                "nombre": row[1],
                "fecha_registro": row[2],
                "notas": row[3],
                "ultimo_evento": row[4]
            })

        return templates.TemplateResponse("index.html", {
            "request": request,
            "usuarios": usuarios,
            "total": len(usuarios),
            "now": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        return HTMLResponse(f"""
        <h1>❌ Error de conexión / consulta</h1>
        <p><strong>Tipo:</strong> {type(e).__name__}</p>
        <p><strong>Mensaje:</strong> {str(e)}</p>
        <hr>
        <p>Revisa que la variable DATABASE_URL sea la correcta y que la tabla 'usuarios' tenga datos.</p>
        """, status_code=500)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)