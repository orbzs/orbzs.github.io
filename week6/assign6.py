from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

import json
import urllib.request
from typing import Annotated

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(SessionMiddleware, secret_key="w6login")

import mysql.connector
con = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
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

@app.post("/login")
async def signin(request: Request, email: Annotated[str, Form(...)], password: Annotated[str, Form(...)]):
    cursor=con.cursor()
    cursor.execute("SELECT * FROM member WHERE email=%s and password=%s", [email, password])
    result=cursor.fetchone()
    if result==None:
        request.session["member"]=None
        return RedirectResponse(url="/ohoh?msg=電子郵件或密碼錯誤", status_code=303)
    else:
        request.session["member"]={
            "id": result[0],"name":result[1],"email":result[2]
        }
        return RedirectResponse(url="/member", status_code=303)

    
@app.get("/login")
async def statuscheck(request: Request):
    if "member" in request.session and request.session["member"]:
        member=request.session["member"]
        return {"ok": True, "id": member["id"], "name": member["name"], "email": member["email"]}
    else:
        return {"ok":False}

@app.get("/member", response_class=HTMLResponse) 
async def member_page(request: Request): 
    member = request.session.get("member") 
    if not member: 
        return RedirectResponse(url="/", status_code=303) 
    return templates.TemplateResponse("member.html", {"request": request, "member": member}) 


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"ok":True}

@app.post("/createMessage")
async def creatMessage(request: Request, content: Annotated[str, Form(...)]):
    cursor=con.cursor()
    member = request.session.get("member")
    member_id = member.get("id")
    cursor.execute(
        "INSERT INTO message (member_id, content) VALUES (%s, %s)",
        (member_id, content),
    )
    con.commit()
    cursor.close()
    return RedirectResponse(url="/member", status_code=303)

@app.get("/createMessage")
async def getMessage():
    cursor=con.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            message.id, 
            message.content, 
            message.member_id,
            member.name
        FROM message
        JOIN member ON message.member_id = member.id
    """)
    
    data=cursor.fetchall()
    cursor.close()
    return data

@app.post("/deleteMessage/{message_id}")
async def delete_message(request: Request, message_id: int):
    member = request.session.get("member")
    if not member:
        return {"ok": False, "error": "not logged in"}

    cursor = con.cursor()
    cursor.execute("SELECT member_id FROM message WHERE id=%s", (message_id,))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        return {"ok": False, "error": "no such message"}

    owner_id = row[0]
    if owner_id != member.get("id"):
        cursor.close()
        return {"ok": False, "error": "not owner"}

    cursor.execute("DELETE FROM message WHERE id=%s", (message_id,))
    con.commit()
    cursor.close()
    return {"ok": True}


@app.get("/ohoh", response_class=HTMLResponse)
async def ohoh(request: Request, msg: str = "錯誤訊息"):
    return templates.TemplateResponse("ohoh.html", {"request": request, "msg": msg})