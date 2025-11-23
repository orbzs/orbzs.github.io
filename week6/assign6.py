from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

import json
import urllib.request
from typing import Annotated

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_middleware(SessionMiddleware, secret_key="w6login")

import mysql.connector
con = mysql.connector.connect(
  host="localhost",
  user="myusername",
  password="mypassword",
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

# /member get messages
@app.get("/member", response_class=HTMLResponse) 
async def member_page(request: Request): 
    member = request.session.get("member")
    if not member: 
        return RedirectResponse(url="/", status_code=303) 
    cursor=con.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            message.id AS message_id, 
            message.content, 
            message.member_id,
            member.name
        FROM message
        JOIN member ON message.member_id = member.id
        ORDER BY message.id DESC
    """)
    messages=cursor.fetchall()
    cursor.close()
    return templates.TemplateResponse(
      "member.html",
     {
          "request": request,
          "member": member,
          "messages": messages,
       }
    )

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

@app.post("/createMessage")
async def creatMessage(request: Request, content: Annotated[str, Form(...)]):
    member = request.session.get("member")
    member_id = member.get("id")
    cursor=con.cursor()
    cursor.execute(
        "INSERT INTO message (member_id, content) VALUES (%s, %s)",
        (member_id, content)
    )
    con.commit()
    cursor.close()
    return RedirectResponse(url="/member", status_code=303)
  
@app.post("/deleteMessage")
async def deleteMessage(request: Request, message_id: Annotated[int, Form(...)]):
    member = request.session.get("member")
    if not member:
        return RedirectResponse(url="/", status_code=303)
    cursor = con.cursor()
    cursor.execute(
        "DELETE FROM message WHERE id=%s AND member_id=%s",
        (message_id, member["id"])
    )
    con.commit()
    cursor.close()
    return RedirectResponse(url="/member", status_code=303)


@app.get("/ohoh", response_class=HTMLResponse)
async def ohoh(request: Request, msg: str = "錯誤訊息"):
    return templates.TemplateResponse("ohoh.html", {"request": request, "msg": msg})


