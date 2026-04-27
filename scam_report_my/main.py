from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import shutil
import uvicorn
import hashlib

# ───────────── LOAD ENV ─────────────
load_dotenv()

client = MongoClient(os.getenv("mongo_URL"))
db = client[os.getenv("DB_NAME")]
reports_collection = db["reports"]
users_collection = db["users"]

app = FastAPI(title="ScamWatch API", version="4.0")

# ───────────── STATIC FILES ─────────────
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# ───────────── MODELS ─────────────
class ReportCreate(BaseModel):
    title: str
    scam_type: str
    description: str
    scammer_contact: Optional[str] = None
    amount_lost: Optional[float] = 0
    reported_by: Optional[str] = "Anonymous"
    location: Optional[str] = None


class ReportUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    scammer_contact: Optional[str] = None
    amount_lost: Optional[float] = None
    status: Optional[str] = None


class UserRegister(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"   # "user" or "admin"
    admin_secret: Optional[str] = None  # required when role == "admin"


class UserLogin(BaseModel):
    username: str
    password: str


# ───────────── AUTH HELPERS ─────────────
ADMIN_SECRET = os.getenv("ADMIN_SECRET")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ───────────── HELPERS ─────────────
def serialize_report(report):
    if not report:
        return None
    report.pop("_id", None)
    return report


def get_next_report_id():
    existing_ids = set(
        r["id"] for r in reports_collection.find({}, {"id": 1})
    )
    if not existing_ids:
        return 1
    max_id = max(existing_ids)
    for candidate in range(1, max_id + 2):
        if candidate not in existing_ids:
            return candidate


# ───────────── ROOT ─────────────
@app.get("/")
async def root():
    return {"message": "ScamWatch API v4.0 running"}


# ───────────── AUTH: REGISTER ─────────────
@app.post("/auth/register")
async def register(data: UserRegister):
    # Validate role
    if data.role not in ("user", "admin"):
        raise HTTPException(status_code=400, detail="Role must be 'user' or 'admin'")

    # Admin registration requires the secret key
    if data.role == "admin":
        if data.admin_secret != ADMIN_SECRET:
            raise HTTPException(status_code=403, detail="Invalid admin secret key")

    if users_collection.find_one({"username": data.username}):
        raise HTTPException(status_code=409, detail="Username already exists")

    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user_doc = {
        "username": data.username,
        "password_hash": hash_password(data.password),
        "role": data.role,
        "created_at": datetime.utcnow().isoformat()
    }
    users_collection.insert_one(user_doc)

    return {"message": "Registered successfully", "username": data.username, "role": data.role}


# ───────────── AUTH: LOGIN ─────────────
@app.post("/auth/login")
async def login(data: UserLogin):
    user = users_collection.find_one({"username": data.username})

    if not user or user["password_hash"] != hash_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "message": "Login successful",
        "username": user["username"],
        "role": user["role"]
    }


# ───────────── CREATE REPORT ─────────────
@app.post("/reports")
async def create_report(report: ReportCreate):
    new_report = {
        "id": get_next_report_id(),
        "title": report.title,
        "scam_type": report.scam_type,
        "description": report.description,
        "scammer_contact": report.scammer_contact,
        "amount_lost": report.amount_lost,
        "reported_by": report.reported_by,
        "location": report.location,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }
    reports_collection.insert_one(new_report)
    new_report.pop("_id", None)
    return new_report


# ───────────── GET ALL REPORTS ─────────────
@app.get("/reports")
async def get_reports(
    scam_type: Optional[str] = None,
    status_filter: Optional[str] = None,
    reported_by: Optional[str] = None
):
    query = {}
    if scam_type:
        query["scam_type"] = scam_type
    if status_filter:
        query["status"] = status_filter
    if reported_by:
        query["reported_by"] = reported_by

    reports = []
    for r in reports_collection.find(query).sort("id", -1):
        reports.append(serialize_report(r))
    return reports


# ───────────── GET REPORT BY ID ─────────────
@app.get("/reports/{report_id}")
async def get_report(report_id: int):
    report = reports_collection.find_one({"id": report_id})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return serialize_report(report)


# ───────────── UPDATE REPORT ─────────────
@app.put("/reports/{report_id}")
async def update_report(report_id: int, data: ReportUpdate):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = reports_collection.update_one(
        {"id": report_id},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"message": "Updated successfully"}



# ───────────── DELETE REPORT ─────────────
@app.delete("/reports/{report_id}")
async def delete_report(report_id: int):
    result = reports_collection.delete_one({"id": report_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Report not found")

    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        for f in os.listdir(uploads_dir):
            if f.startswith(f"{report_id}_"):
                try:
                    os.remove(os.path.join(uploads_dir, f))
                except Exception:
                    pass

    return {"message": "Deleted successfully"}


# ───────────── UPLOAD EVIDENCE ─────────────
@app.post("/reports/{report_id}/evidence")
async def upload_evidence(report_id: int, file: UploadFile = File(...)):
    report = reports_collection.find_one({"id": report_id})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)

    filename = f"{report_id}_{file.filename}"
    file_path = os.path.join(uploads_dir, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": filename, "file_path": file_path}


# ───────────── GET EVIDENCE ─────────────
@app.get("/reports/{report_id}/evidence")
async def get_evidence(report_id: int):
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        return []

    files = []
    for f in os.listdir(uploads_dir):
        if f.startswith(f"{report_id}_"):
            files.append({"filename": f, "file_path": os.path.join(uploads_dir, f)})
    return files


# ───────────── STATS ─────────────
@app.get("/stats")
async def get_stats():
    total = reports_collection.count_documents({})
    pending = reports_collection.count_documents({"status": "pending"})
    verified = reports_collection.count_documents({"status": "verified"})
    rejected = reports_collection.count_documents({"status": "rejected"})

    total_amount = sum(
        r.get("amount_lost", 0) or 0
        for r in reports_collection.find({}, {"amount_lost": 1})
    )

    scam_types = {}
    for r in reports_collection.find({}, {"scam_type": 1}):
        st = r.get("scam_type", "Other")
        scam_types[st] = scam_types.get(st, 0) + 1

    return {
        "total_reports": total,
        "pending": pending,
        "verified": verified,
        "rejected": rejected,
        "total_amount_lost": total_amount,
        "by_scam_type": scam_types
    }

# ───────────── GET USERS ─────────────
@app.get("/users")
async def get_users():
    users = []
    for u in users_collection.find({}, {"_id": 0, "password_hash": 0}):
        users.append(u)
    return users


# ───────────── RUN ─────────────
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
