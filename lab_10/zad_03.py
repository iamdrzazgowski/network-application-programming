import asyncio
import websockets

async def websocket_client():
    uri = "wss://echo.websocket.org"
    async with websockets.connect(uri) as websocket:
        message = "To jest wiadomość o dowolnej długości, którą wysyłam do serwera echo."

        print(f"Wysyłam wiadomość: {message}")
        await websocket.send(message)

        response = await websocket.recv()
        print(f"Otrzymałem echo: {response}")

asyncio.run(websocket_client())
