from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from calculator import calculate_net_income
from calculator import compare_w2_vs_contractor

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    salary: float = Form(...),
    bonus: float = Form(0),
    healthcare_cost: float = Form(0),
    retirement_percent: float = Form(5)
):
    result = calculate_net_income(
        salary,
        bonus,
        healthcare_cost,
        retirement_percent
    )

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result}
    )


from calculator import advanced_compare

@app.post("/compare", response_class=HTMLResponse)
async def compare(
    request: Request,
    w2_salary: float = Form(...),
    contractor_rate: float = Form(...),
    hours_per_year: float = Form(...),
    state: str = Form(...),
    healthcare_cost: float = Form(...),
    retirement_percent: float = Form(...),
    employer_match_percent: float = Form(...),
    pto_days: float = Form(...)
):
    result = advanced_compare(
        w2_salary,
        contractor_rate,
        hours_per_year,
        state,
        healthcare_cost,
        retirement_percent,
        employer_match_percent,
        pto_days
    )

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "comparison": result}
    )
