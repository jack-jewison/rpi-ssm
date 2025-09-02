import asyncio
import pigpio
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse

from config import HOST, PORT, CAPTURE_ENABLED_AT_BOOT, SAFEBOOT_CAMERA_DISABLE_ON_T1_LOW, PIN_T1
from counter import GpioState
from camera import FrameProducer

pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpio daemon not running. Start with: sudo systemctl start pigpiod")

gpio = GpioState(pi)

# Safe-boot: if T1 held low at boot, disable camera streaming
capture_enabled = CAPTURE_ENABLED_AT_BOOT and not (
    SAFEBOOT_CAMERA_DISABLE_ON_T1_LOW and (pi.read(PIN_T1) == 0)
)

fp = FrameProducer(gpio, capture_enabled=capture_enabled)
fp.start()

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/status")
def status():
    return {
        "spm": round(gpio.spm(), 2),
        "last_pulse_age_sec": gpio.last_pulse_age(),
        "twine_tripped": gpio.twine_tripped(),
        "moisture_wet": gpio.moisture_wet(),
        "capture_enabled": fp.capture_enabled,
    }

@app.post("/toggle_capture")
def toggle_capture():
    fp.capture_enabled = not fp.capture_enabled
    return {"capture_enabled": fp.capture_enabled}

@app.get("/snapshot.jpg")
def snapshot():
    jpg = fp.get_jpeg()
    if jpg is None:
        return Response(status_code=503)
    return Response(content=jpg, media_type="image/jpeg")

@app.get("/stream.mjpg")
async def stream_mjpg():
    async def gen():
        while True:
            jpg = fp.get_jpeg()
            if jpg is None:
                await asyncio.sleep(0.05)
                continue
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n"
                   + f"Content-Length: {len(jpg)}\r\n\r\n".encode('ascii')
                   + jpg + b"\r\n")
            await asyncio.sleep(0.02)
    return StreamingResponse(gen(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.on_event("shutdown")
async def _shutdown():
    fp.stop()
    gpio.close()
    pi.stop()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
