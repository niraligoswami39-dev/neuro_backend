from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import time
import traceback

app = FastAPI()

# ✅ Allow frontend requests (important)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🚀 Starting NeuroPulse Backend...")

# ================================
# 🔹 ROOT CHECK
# ================================
@app.get("/")
def home():
    return {"status": "NeuroPulse Backend Running 🚀"}

@app.get("/test")
def test():
    return {"message": "API working perfectly ✅"}


# ================================
# 🔹 FILE HASH FUNCTION
# ================================
def generate_hash(data):
    return hashlib.sha256(data).hexdigest()


# ================================
# 🔹 COMPARE FILES API
# ================================
@app.post("/compare")
async def compare_files(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        start_time = time.time()

        data1 = await file1.read()
        data2 = await file2.read()

        # 🔹 Basic metadata
        size1 = len(data1)
        size2 = len(data2)

        # 🔹 Hash check
        hash1 = generate_hash(data1)
        hash2 = generate_hash(data2)

        hash_match = hash1 == hash2

        # 🔹 Simple similarity logic
        similarity = 100 if hash_match else round((min(size1, size2) / max(size1, size2)) * 100, 2)

        # 🔹 Behavior detection
        behavior = []
        if hash_match:
            behavior.append("⚠️ Exact duplicate files detected")

        if abs(size1 - size2) < 100:
            behavior.append("⚠️ Very similar file sizes")

        if similarity > 80:
            behavior.append("⚠️ High similarity pattern")

        if not behavior:
            behavior.append("✅ No suspicious behavior")

        # 🔹 Case ID
        case_id = f"NP-{int(time.time())}"

        end_time = time.time()

        return {
            "case_id": case_id,
            "file1": {
                "filename": file1.filename,
                "size_bytes": size1
            },
            "file2": {
                "filename": file2.filename,
                "size_bytes": size2
            },
            "hash_match": hash_match,
            "similarity": similarity,
            "behavior": behavior,
            "processing_time": round(end_time - start_time, 2)
        }

    except Exception as e:
        print("❌ ERROR in /compare:")
        print(traceback.format_exc())
        return {
            "error": "Something went wrong",
            "details": str(e)
        }


# ================================
# 🔹 STARTUP CHECK
# ================================
try:
    print("✅ App loaded successfully")
except Exception:
    print("❌ Startup error:")
    print(traceback.format_exc())