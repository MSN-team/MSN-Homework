import asyncio
import websockets

async def test_websocket():
    uri = "ws://127.0.0.1:8000/record-audio"
    async with websockets.connect(uri) as websocket:
        print("WebSocket connected!")
        await websocket.send(b"Test audio data")
        response = await websocket.recv()
        print(f"Response: {response}")

asyncio.run(test_websocket())