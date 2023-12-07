from fastapi.responses import StreamingResponse

class MyStreamingResponse(StreamingResponse):
    async def stream_response(self, send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )

        async for chunk in self.body_iterator:
            if not isinstance(chunk, bytes):
                chunk = chunk.encode(self.charset)
            
            # 打印发送的消息内容
            print(chunk)
            
            await send({"type": "http.response.body", "body": chunk, "more_body": True})

        await send({"type": "http.response.body", "body": b"", "more_body": False})
