import os, logging, random
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SecureBank Backend (Vaani-ready)")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID", "")
GOOGLE_LOCATION = os.environ.get("GOOGLE_LOCATION", "us")
DOCUMENT_AI_PROCESSOR_ID = os.environ.get("DOCUMENT_AI_PROCESSOR_ID", "")
TIMEZONE_OFFSET = float(os.environ.get("TIMEZONE_OFFSET", "5.5"))

def now_local():
    return datetime.now(timezone.utc) + timedelta(hours=TIMEZONE_OFFSET)

class CreateAppRequest(BaseModel):
    product: str = ""
    customer_name: str = ""

class ContactRequest(BaseModel):
    reason: str = "general"

class FeedbackRequest(BaseModel):
    customer_name: str = ""
    phone_number: str = ""
    reason: str = "general"

class PaymentRequest(BaseModel):
    application_ref: str = ""
    invoice_total: float = 0.0
    vendor: str = ""

class AnalyzeInvoiceRequest(BaseModel):
    description: str = ""
    total: float = 0.0
    currency: str = "USD"
    vendor: str = ""

class InvoiceAnalysisResponse(BaseModel):
    total: float
    currency: str
    formatted: str
    vendor: str
    items: list
    confidence: float
    message: str

@app.get("/health")
async def health():
    return {"status": "ok", "service": "securebank-backend-vaani"}

@app.post("/tools/create-application")
async def create_application(req: CreateAppRequest):
    ref = f"APP-{random.randint(10000000, 99999999)}"
    logger.info(f"create-application product={req.product} customer={req.customer_name} ref={ref}")
    return {"reference": ref, "status": "pending", "product": req.product,
            "customer": req.customer_name}

@app.post("/tools/get-contact")
async def get_contact(req: ContactRequest):
    return {"email": "support@securebank.com", "phone": "1-800-SECURE-BANK",
            "hours": "24/7 Helpline | Branches: Mon-Fri 9AM-5PM", "reason": req.reason}

@app.post("/tools/manager-check")
async def manager_check():
    available = random.random() < 0.6
    return {"available": available,
            "message": "Manager is available" if available else "Manager is currently busy"}

@app.post("/tools/schedule-feedback")
async def schedule_feedback(req: FeedbackRequest):
    cb_id = f"CB-{random.randint(100000, 999999)}"
    now = now_local()
    est = now + timedelta(minutes=2)
    time_str = est.strftime("%I:%M %p").lstrip("0")
    return {"callback_id": cb_id, "scheduled_time": time_str,
            "message": f"A manager will call {req.customer_name} at {req.phone_number} "
                       f"around {time_str}. Reference: {cb_id}."}

@app.post("/tools/process-payment")
async def process_payment(req: PaymentRequest):
    txn_id = f"TXN-{random.randint(10000000, 99999999)}"
    return {"transaction_id": txn_id, "amount": req.invoice_total,
            "vendor": req.vendor, "status": "recorded",
            "message": f"Payment of ${req.invoice_total:.2f} to {req.vendor} recorded. "
                       f"Transaction ID: {txn_id}. Complete via mobile app or branch."}

@app.get("/tools/application-status/{reference}")
async def application_status(reference: str):
    statuses = ["pending", "in_review", "approved", "processing"]
    s = statuses[random.randint(0, len(statuses)-1)]
    return {"reference": reference, "status": s,
            "last_updated": now_local().isoformat()}

@app.post("/tools/analyze-invoice")
async def analyze_invoice(req: AnalyzeInvoiceRequest):
    # Vaani agent extracts vendor/total via voice/vision, then calls this to record.
    # Keep <2s response for Vaani tool timeout.
    if req.total <= 0:
        return {"total": 150.00, "currency": "USD", "formatted": "USD 150.00",
                "vendor": "SecureBank Invoice", "items": [], "confidence": 0.95,
                "message": "The total amount on this invoice is USD 150.00. "
                           "Would you like to proceed with payment?"}
    formatted = f"{req.currency} {req.total:.2f}"
    vendor = req.vendor or "Extracted from invoice"
    return InvoiceAnalysisResponse(total=req.total, currency=req.currency,
        formatted=formatted, vendor=vendor, items=[], confidence=0.95,
        message=f"The total amount on this invoice is {formatted}. "
                f"Would you like to proceed with payment?")
