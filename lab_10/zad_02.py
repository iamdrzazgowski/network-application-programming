import asyncio
import websockets


def truncate_utf8(s, max_bytes):
    encoded = s.encode('utf-8')
    if len(encoded) <= max_bytes:
        return s
    truncated = encoded[:max_bytes]
    while True:
        try:
            return truncated.decode('utf-8')
        except UnicodeDecodeError:
            truncated = truncated[:-1]
            if not truncated:
                return ''


async def websocket_client():
    uri = "wss://echo.websocket.org"
    async with websockets.connect(uri) as websocket:
        full_message = ("To jest bardzo długa wiadomość, która zostanie obcięta, jeśli przekroczy limit 125 bajtów. "
                        "Dodaj tutaj tyle tekstu, ile chcesz, żeby sprawdzić działanie programu.")

        max_len = 125
        message = truncate_utf8(full_message, max_len)

        print(f"Wysyłam ({len(message.encode('utf-8'))} bajtów): {message}")
        await websocket.send(message)

        response = await websocket.recv()
        print(f"Otrzymałem echo: {response}")


asyncio.run(websocket_client())
