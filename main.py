from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fastapi.staticfiles import StaticFiles

app = FastAPI()

model_path = "./model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

class SummarizationRequest(BaseModel):
    text: str

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.post("/summarize")
async def summarize(request: SummarizationRequest):
    input_text = request.text
    print("Summarization started")
    inputs = tokenizer("summarize: " + input_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=30, length_penalty=2.0, num_beams=4)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return JSONResponse(content={"summary": summary})
