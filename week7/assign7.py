from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

import json
import urllib.request
from typing import Annotated

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(SessionMiddleware, secret_key="w6login")

import mysql.connector
con = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql",
  database="website"
)
print("database ready")

# index.html
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# signup
@app.post("/signup")
async def signup(request: Request, name: Annotated[str, Form(...)], email: Annotated[str, Form(...)], password: Annotated[str, Form(...)]):
    cursor=con.cursor()
    cursor.execute("SELECT * FROM member WHERE email=%s", [email])
    result=cursor.fetchone()
    if result==None:
        cursor.execute("INSERT INTO member(name,email,password) VALUES(%s,%s,%s)", [name, email, password])
        con.commit()
        return RedirectResponse(url="/", status_code=303)
    else:
        return RedirectResponse(url="/ohoh?msg=重複的電子郵件", status_code=303)

# login
@app.post("/login")
async def signin(request: Request, email: Annotated[str, Form(...)], password: Annotated[str, Form(...)]):
    if not email or not password:
        return RedirectResponse(url="/ohoh?msg=電子郵件或密碼錯誤", status_code=303)
    cursor = con.cursor(dictionary=True) 
    cursor.execute("SELECT * FROM member WHERE email=%s and password=%s", [email, password])
    result=cursor.fetchone()
   
    if result==None:
        request.session["member"]=None
        return RedirectResponse(url="/ohoh?msg=電子郵件或密碼錯誤", status_code=303)
    request.session["member"] = {
        "id": result["id"],
        "name": result["name"],
        "email": result["email"]
    }
    return RedirectResponse(url="/member", status_code=303)

# member page
@app.get("/member", response_class=HTMLResponse) 
async def member_page(request: Request): 
    member = request.session.get("member")
    if not member: 
        return RedirectResponse(url="/", status_code=303) 
    return templates.TemplateResponse(
      "member.html",
     {
          "request": request,
          "member": member,
       }
    )

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"ok":True}


@app.get("/ohoh", response_class=HTMLResponse)
async def ohoh(request: Request, msg: str = "錯誤訊息"):
    return templates.TemplateResponse("ohoh.html", {"request": request, "msg": msg})

# Task 1: Build a Member Query API in the back-end
@app.get("/api/member/{id}")
async def search(request: Request, id: int): 
    member = request.session.get("member")
    if not member: 
        return {
            "data":None
        } 
    cursor = con.cursor(dictionary=True) 
    cursor.execute("SELECT * FROM member WHERE id=%s", [id])
    result=cursor.fetchone()
    if result==None:
        cursor.close()
        return {
            "data":None
        }
    if result and member["id"] != id:
        cursor.execute(
            "INSERT INTO history (member_id, searched_id) VALUES (%s, %s)",
            (member["id"], id)
        )
        con.commit()
        cursor.close()
    return {
        "data":{
        "id": result["id"],
        "name": result["name"],
        "email": result["email"]
        }
    }

# Task 3: Add feature for updating name
@app.patch("/api/member")
async def search(request: Request, body: dict = Body(...)): 
    member = request.session.get("member")
    if not member: 
        return {"error":True}    
    newName = body.get("name")
    if not newName:
        return {"error": True}
    cursor = con.cursor(dictionary=True) 
    cursor.execute("UPDATE member SET name=%s where id=%s", [newName,member["id"]])
    con.commit()
    cursor.close()
    member["name"] = newName
    request.session["member"] = member
    return{"ok":True}    

# Task 4: Add feature for tracking member queries
@app.get("/api/history")
async def history(request: Request):
    member = request.session.get("member")
    if not member: 
        return {"error":True}
    cursor = con.cursor(dictionary=True) 
    cursor.execute("""
        SELECT 
            history.member_id,                   
            history.time,
            member.name
        FROM history
        JOIN member ON history.member_id = member.id
        WHERE history.searched_id = %s
        ORDER BY history.time DESC  
        LIMIT 10
    """,[member["id"]])
    histories=cursor.fetchall()
    cursor.close()
    return{"histories":histories}

    


