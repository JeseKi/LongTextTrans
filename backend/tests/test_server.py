from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

@app.get("/stream")
async def stream_numbers():
    async def number_generator():
        for i in range(10):
            yield f"{i}\n"
            await asyncio.sleep(0.5)  # 模拟延迟
    return StreamingResponse(number_generator(), media_type="text/plain")

@app.get("/stream_test")
async def stream_messages():
    async def gen() :
        for i in range(10):
            yield f"{i}\n"
            await asyncio.sleep(1)
            i += 1
    
    return StreamingResponse(gen())