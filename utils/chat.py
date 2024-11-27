from fastapi import WebSocket


async def chat_func(ws: WebSocket):
    await ws.accept()
    while True:
        msg = await ws.receive_json()
        #res = {}
        await ws.send_json(msg)