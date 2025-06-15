import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        print(f"Otrzymano: {message}")
        await websocket.send(f"Echo: {message}")

async def main():
    server = await websockets.serve(echo, "127.0.0.1", 8765)
    print("Serwer WebSocket działa na ws://127.0.0.1:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
