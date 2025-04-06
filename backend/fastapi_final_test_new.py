from fastapi import FastAPI
from pydantic import BaseModel
import logging
import socket
import asyncio
import time
import uvicorn
from uvicorn.protocols.http.h11_impl import H11Protocol

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

class TestRequest(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "FastAPI server is running"}

@app.post("/test")
async def test_endpoint(request: TestRequest):
    logger.debug(f"Received test request: {request.text}")
    return {
        "status": "SUCCESS",
        "message": "Final test endpoint working",
        "input": request.text
    }

def find_available_port(start_port=8000, max_attempts=20):
    """Find first available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except socket.error:
                continue
    raise RuntimeError(f"No available ports in range {start_port}-{start_port+max_attempts-1}")

async def serve():
    loop = asyncio.get_event_loop()
    server = await loop.create_server(
        lambda: H11Protocol(app, loop),
        host='127.0.0.1',
        port=PORT
    )
    logger.info(f"Serving on http://127.0.0.1:{PORT}")
    try:
        await server.serve_forever()
    except asyncio.CancelledError:
        logger.info("Shutting down server...")
    finally:
        server.close()
        await server.wait_closed()

if __name__ == "__main__":
    try:
        PORT = find_available_port()
        logger.info(f"Starting server on port {PORT}")
        
        # Run server with persistent loop
        # Verify port availability
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(('0.0.0.0', PORT))
                logger.info(f"Port {PORT} is available and bound successfully")
            except socket.error as e:
                logger.error(f"Port {PORT} binding failed: {str(e)}")
                raise

        config = uvicorn.Config(
            app,
            host='0.0.0.0',
            port=PORT,
            log_level="trace",
            access_log=True,
            loop="asyncio",
            reload=True,
            timeout_keep_alive=60,
            proxy_headers=True
        )
        server = uvicorn.Server(config)
        
        # Keep server running
        import asyncio
        async def run_server():
            await server.serve()
            
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(run_server())
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        finally:
            loop.close()
            
    except Exception as e:
        logger.critical(f"Server failed: {str(e)}")
        raise
