from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from db import DB
from datetime import datetime

app = FastAPI(title="RFID Sync Test - Cloud")
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
    uvicorn.run(app, host="0.0.0.0", port=8000)