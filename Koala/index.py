from fastapi import FastAPI, File, Request
import csv
import uvicorn
from threading import Thread
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="Koala/templates")

# @app.get("/")
# async def upload():
#     with open('Koala/Datas/CSV/Interview.csv', 'r', encoding='utf-8') as csvfile:
#         csvReader = csv.DictReader(csvfile)
#         data = {}
#         for idx, rows in enumerate(csvReader):
#             # Assuming a column named 'Id' to be the primary key
#             data[idx+1] = rows
#     return data

@app.get('/', response_class=HTMLResponse)
async def show_interview(request: Request):
    with open('Koala/Datas/CSV/Interview.csv', 'r', encoding='utf-8') as csvfile:
        csvReader = csv.DictReader(csvfile)
        data = list(csvReader)
    return templates.TemplateResponse("index.html", {"request": request, "data": data})

def index():
    t = Thread(target=run)
    t.start()

def run():
    uvicorn.run(app, host='0.0.0.0', port=8081)