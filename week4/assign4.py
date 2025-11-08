from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

import json
import urllib.request

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(SessionMiddleware, secret_key="keyforlogin")


# Task1
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Task2 + Task3
@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    if not email or not password:
        return RedirectResponse(url="/ohoh?msg=請輸入信箱和密碼", status_code=303)

    if email == "abc@abc.com" and password == "abc":
        request.session["LOGGED-IN"] = True
        return RedirectResponse(url="/member", status_code=303)
    else:
        request.session["LOGGED-IN"] = False
        return RedirectResponse(url="/ohoh?msg=帳號、或密碼輸入錯誤", status_code=303)


# Task3
@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    logged_in = request.session.get("LOGGED-IN", False)
    if not logged_in:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("member.html", {"request": request})

@app.get("/logout")
async def logout(request: Request):
    request.session["LOGGED-IN"] = False
    return RedirectResponse(url="/", status_code=303)

@app.get("/ohoh", response_class=HTMLResponse)
async def ohoh(request: Request, msg: str = "錯誤訊息"):
    return templates.TemplateResponse("ohoh.html", {"request": request, "msg": msg})


# Task4
url_ch = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
url_en = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

with urllib.request.urlopen(url_ch) as res:
    hotels_ch = json.loads(res.read().decode())

with urllib.request.urlopen(url_en) as res:
    hotels_en = json.loads(res.read().decode())

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/hotel/{hotel_id}", response_class=HTMLResponse)
async def show_hotel(request: Request, hotel_id: int):
    hotel_ch = next((h for h in hotels_ch["list"] if h["_id"] == hotel_id), None)
    hotel_en = next((h for h in hotels_en["list"] if h["_id"] == hotel_id), None)
    if hotel_ch and hotel_en:
        info = {
            "id": hotel_id,
            "ch_name": hotel_ch["旅宿名稱"],
            "en_name": hotel_en["hotel name"],
            "tel": hotel_ch["電話或手機號碼"] if "電話或手機號碼" in hotel_ch else hotel_en.get("tel", "N/A"),
        }
    else:
        info = None
    return templates.TemplateResponse("hotel.html", {"request": request, "hotel": info})
