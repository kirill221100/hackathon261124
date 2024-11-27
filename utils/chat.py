from fastapi import WebSocket, WebSocketDisconnect


async def chat_func(ws: WebSocket):
    await ws.accept()
    while True:
        try:
            msg = await ws.receive_json()
            #res = {}
            await ws.send_json(msg)
        except (WebSocketDisconnect, RuntimeError) as e:
            pass