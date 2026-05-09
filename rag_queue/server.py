from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queue.worker import process_query

app = FastAPI()

@app.get("/")
def root():
    return {"status": "server is up and running"}

@app.post("/chat")
def chat(
    query:str = Query(..., description="The user query to process")
):
    job = queue.enqueue(process_query, query)
    print(f"Job {job.id} enqueued with query: {query}")
    
    return {"status": "Job enqueued", "job_id": job.id}


@app.get("/result/{job_id}")
def get_result(job_id: str):
    job = queue.fetch_job(job_id)
    if job is None:
        return {"status": "Job not found"}
    
    if job.is_finished:
        return {"status": "Job finished", "result": job.result}
    elif job.is_failed:
        return {"status": "Job failed", "error": str(job.exc_info)}
    else:
        return {"status": "Job is still processing"}