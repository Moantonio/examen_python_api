from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from datetime import datetime
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")
 
def get_db(): 
    db = sqlite3.connect("alumnos.db",check_same_thread=False)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/alumnos", response_class=HTMLResponse)
async def alumnos_list(request: Request, db=Depends(get_db)):
    cursor = db.execute("SELECT * FROM alumnos")
    alumnos = cursor.fetchall()
    return templates.TemplateResponse("alumnos_list.html", {"request": request, "alumnos": alumnos})

@app.get("/alumnos/create", response_class=HTMLResponse)
async def alumno_create_form(request: Request):
    return templates.TemplateResponse("alumno_create.html", {"request": request})

@app.post("/alumnos/create", response_class=HTMLResponse)
async def alumno_create(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    aprobado: bool = Form(...),
    nota: float = Form(...),
    db=Depends(get_db),
):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.execute(
        "INSERT INTO alumnos (nombre, apellido, aprobado, nota, fecha) VALUES (?, ?, ?, ?, ?)",
        (nombre, apellido, aprobado, nota, fecha),
    )
    db.commit()
    return RedirectResponse(url="/alumnos", status_code=303)

@app.get("/alumnos/{alumno_id}", response_class=HTMLResponse)
async def alumno_detail(request: Request, alumno_id: int, db=Depends(get_db)):
    cursor = db.execute("SELECT * FROM alumnos WHERE id = ?", (alumno_id,))
    alumno = cursor.fetchone()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return templates.TemplateResponse("alumno_detail.html", {"request": request, "alumno": alumno})


@app.get("/alumnos/{alumno_id}/edit", response_class=HTMLResponse)
async def alumno_edit_form(request: Request, alumno_id: int, db=Depends(get_db)):
    cursor = db.execute("SELECT * FROM alumnos WHERE id = ?", (alumno_id,))
    alumno = cursor.fetchone()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return templates.TemplateResponse("alumno_edit.html", {"request": request, "alumno": alumno})

@app.post("/alumnos/{alumno_id}/edit", response_class=HTMLResponse)
async def alumno_edit(
    request: Request,
    alumno_id: int,
    nombre: str = Form(...),
    apellido: str = Form(...),
    aprobado: bool = Form(...),
    nota: float = Form(...),
    db=Depends(get_db),
):
    db.execute(
        "UPDATE alumnos SET nombre = ?, apellido = ?, aprobado = ?, nota = ? WHERE id = ?",
        (nombre, apellido, aprobado, nota, alumno_id),
    )
    db.commit()
    return RedirectResponse(url=f"/alumnos/{alumno_id}", status_code=303)

@app.get("/alumnos/{alumno_id}/delete", response_class=HTMLResponse)
async def alumno_delete_form(request: Request, alumno_id: int, db=Depends(get_db)):
    cursor = db.execute("SELECT * FROM alumnos WHERE id = ?", (alumno_id,))
    alumno = cursor.fetchone()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return templates.TemplateResponse("alumno_delete.html", {"request": request, "alumno": alumno})

@app.post("/alumnos/{alumno_id}/delete", response_class=HTMLResponse)
async def alumno_delete(alumno_id: int, db=Depends(get_db)):
    db.execute("DELETE FROM alumnos WHERE id = ?", (alumno_id,))
    db.commit()
    return RedirectResponse(url="/alumnos", status_code=303)

# Iniciar el servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.1.1.1", port=8000)
