# QR Mirror

> **Archived.** This was a quick personal project, no longer maintained.

> Built out of spite for a subscription system that assumed one person could only ever own one phone.

Captures a QR code visible on screen and serves it as a live image over a local web server. A browser on any device on the same network can display the mirrored QR code in real time.

Originally run on an Android VM — the QR code generated on the "real" device was mirrored to the VM and served over the web, so anyone with access to the server could display it on their own device. If a confirmation dialog appeared between scans, the auto-clicker dismissed it automatically so the next scan could proceed without manual intervention.


## Requirements

- Python 3.9+
- A PNG screenshot of the button you want to auto-click (see Configuration)

```
pip install -r requirements.txt
```

## Configuration

All settings live in `config.py`. The following can also be overridden via environment variables:

| Variable          | Default       | Description                                  |
|-------------------|---------------|----------------------------------------------|
| `PORT`            | `8080`        | Port the web server listens on               |
| `BUTTON_TEMPLATE` | `button.png`  | Path to the button template image            |

## Usage

1. Place a grayscale-compatible PNG of the button you want auto-clicked at the path set by `BUTTON_TEMPLATE`.
2. Run the server:

```bash
python main.py
```

3. Open `http://<host-ip>:8080` in a browser on any device on the same network.
4. Click **Scan QR Code** — the server will capture your screen for up to 60 seconds, detect any QR code, and push updates to all connected browsers via WebSocket.

## Project structure

```
qr_mirror/
├── main.py           # Entry point
├── scanner.py        # Screen capture and QR detection
├── auto_clicker.py   # Template-match auto-clicker
├── server.py         # aiohttp web server and routes
├── config.py         # All tunable constants
├── templates/
│   └── index.html    # Browser UI
└── requirements.txt
```
