from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import DB
from datetime import datetime
import os   # ← Añade esto

app = FastAPI(title="RFID Cloud View")
db = DB()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    conn = db.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM test_usuarios ORDER BY creado_en DESC")
    usuarios = cur.fetchall()
    conn.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "usuarios": usuarios,
        "total": len(usuarios),
        "now": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))   # ← Cambia esto
    uvicorn.run(app, host="0.0.0.0", port=port)