from uuid import uuid4
from os import path, remove, makedirs, environ
from urllib.parse import unquote

from fastapi import FastAPI
from paddleocr import PaddleOCR
import uvicorn
import httpx

# download and load model into memory
print("loading model before starting server...")
ocr = PaddleOCR(lang="en", use_gpu=False)
print("model loaded. server starting...")
makedirs('tmp', exist_ok=True)

#initialize fast api app
app = FastAPI()

@app.get("/health")
def health():
  return "OK"

@app.get("/infer")
async def infer(url: str):
  req_id = str(uuid4())
  [_, ext] = path.splitext(url)
  f_path = path.join(".", "tmp", req_id+ext)

  async with httpx.AsyncClient() as client:
    r = await client.get(url)
    if r.status_code == 200:
      with open(f_path, "wb") as f:
        f.write(r.content)

  img_path = path.join(f_path)
  result = ocr.ocr(img_path)

  remove(f_path)

  result_text = []
  for line in result[0]:
    result_text.append(line[1][0])

  return { "text": ' '.join(result_text) }

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=int(environ.get("PORT", 5000)), log_level="info")
