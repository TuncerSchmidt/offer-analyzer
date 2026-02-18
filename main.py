from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from calculator import calculate_net_income
from calculator import compare_w2_vs_contractor
import stripe
from fastapi.responses import RedirectResponse
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PRICE_ID = os.getenv("STRIPE_PRICE_ID")
BASE_URL = "https://offer-analyzer.onrender.com"
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
@app.post("/create-checkout-session")
async def create_checkout_session():

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": PRICE_ID,
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"{BASE_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{BASE_URL}/",
    )

    return RedirectResponse(session.url)

from fastapi import Query

@app.get("/success", response_class=HTMLResponse)
async def success(session_id: str = Query(...)):

    # Stripe'dan session'ı çekiyoruz
    session = stripe.checkout.Session.retrieve(session_id)

    # Ödeme başarılı mı kontrol
    if session.payment_status != "paid":
        return "Payment not verified"

    return f"""
    <html>
        <body>
            <h1>Payment Successful 🎉</h1>
            <a href="/download-premium-report?session_id={session_id}">
                Download Your PDF
            </a>
        </body>
    </html>
    """

@app.get("/download-premium-report")
async def download_premium_report(session_id: str = Query(...)):

    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status != "paid":
        return "Unauthorized"

    filename = "premium_report.pdf"

    from pdf_generator import generate_pdf
    generate_pdf({
        "total_income": 100000,
        "federal_tax": 20000,
        "retirement_contribution": 5000,
        "net_income": 75000
    }, filename)

    return FileResponse(filename, media_type="application/pdf", filename=filename)

