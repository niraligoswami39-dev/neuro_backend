# =========================
# IMPORTS
# =========================
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import numpy as np

# =========================
# APP INIT
# =========================
app = FastAPI()

# =========================
# CORS (IMPORTANT)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROOT TEST
# =========================
@app.get("/")
def home():
    return {"message": "NeuroPulse Backend Running"}

# =========================
# SIGNATURE GENERATION (REAL)
# =========================
def generate_signature(content):

    # Convert bytes → numeric array
    arr = np.frombuffer(content, dtype=np.uint8)

    if len(arr) == 0:
        return [0]*16

    # Split into 16 equal parts
    chunks = np.array_split(arr, 16)

    # Mean of each chunk → stable fingerprint
    signature = [float(chunk.mean()) for chunk in chunks]

    return signature


# =========================
# ANALYZE API
# =========================
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    # Read file
    content = await file.read()

    # =========================
    # HASH (REAL)
    # =========================
    file_hash = hashlib.sha256(content).hexdigest()

    # =========================
    # SIGNATURE (REAL)
    # =========================
    signature = generate_signature(content)

    # =========================
    # RESPONSE
    # =========================
    return {
        "filename": file.filename,
        "size_bytes": len(content),
        "file_type": file.content_type,
        "hash": file_hash,
        "signature": signature
    }