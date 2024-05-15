from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sklearn.preprocessing import LabelEncoder
import pickle
import os

app = FastAPI()

# Load the trained model
with open('best_rf_clf.pkl', 'rb') as file:
    model = pickle.load(file)

# Assuming main.py is in the same directory as the templates and static directories
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
static_dir = os.path.join(os.path.dirname(__file__), "static")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict/")
async def predict(request: Request,
                  pclass: int = Form(...),
                  sex_female: int = Form(...),
                  sex_male: int = Form(...),
                  age: int = Form(...),
                  sibsp: int = Form(...),
                  parch: int = Form(...),
                  fare: int = Form(...),
                  embarked_c: int = Form(...),
                  embarked_q: int = Form(...),
                  embarked_s: int = Form(...)):

    features = [pclass, sex_female, sex_male, age, sibsp, parch, fare, embarked_c, embarked_q, embarked_s]

    # Make prediction
    prediction = model.predict([features])[0]
    result = "likely" if prediction == 1 else "unlikely"

    return templates.TemplateResponse("results.html", {"request": request, "prediction": result},
                                      headers={"Content-Type": "text/html; charset=utf-8"})

# Mounting the static files directory
@app.get("/static/{filename}")
async def get_static_file(filename: str):
    return FileResponse(os.path.join(static_dir, filename), media_type="text/css")  # Added media_type
