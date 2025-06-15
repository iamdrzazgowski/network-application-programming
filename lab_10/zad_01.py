import asyncio
import websockets

async def hello():
    uri = "wss://echo.websocket.org"
    async with websockets.connect(uri) as websocket:
        print("Połączono z serwerem WebSocket!")

        message = "Hello WebSocket!"
        await websocket.send(message)
        print(f"Wysłano: {message}")

        response = await websocket.recv()
        print(f"Odebrano: {response}")

asyncio.run(hello())
