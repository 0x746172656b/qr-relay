# QR Mirror

> **Archived.** Quick personal project, no longer maintained.

---

My gym uses a QR code to let you through the turnstile. You open the app, tap a button, a QR code appears, you scan it, you're in. Simple enough.

Except the app decides that one subscription equals one phone. Not one person. One phone. My QR code lives on my personal phone, and only my personal phone. Want to use your work phone today? Too bad. Left your phone at home? Hope you enjoy standing at the front desk explaining yourself to a 19-year-old who didn't write the software.

There's no family sharing, no secondary device, no "trust this phone too" option. Just a hard assumption baked into the product that a paying customer is a single biological entity permanently fused to a single Android or iOS device.

I found that insulting enough to spend a weekend on this.

---

**What this does:** captures the QR code visible on one screen and serves it as a live image over a local web server. Any browser on the same network can display the mirrored QR code in real time, on any device, no app required.

The original setup ran the app on an Android VM on my desktop. The VM generated the QR code, this tool captured it and pushed it to a web page, and I could open that page on whatever device I had on me that day. If the app showed a confirmation dialog between scans (its little way of making things annoying), the auto-clicker dismissed it automatically so the next scan could proceed without me babysitting it.

---

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
4. Click **Scan QR Code**. The server will capture your screen for up to 60 seconds, detect any QR code, and push updates to all connected browsers via WebSocket.

## Project structure

```
qr-relay/
├── main.py           # Entry point
├── scanner.py        # Screen capture and QR detection
├── auto_clicker.py   # Template-match auto-clicker
├── server.py         # aiohttp web server and routes
├── config.py         # All tunable constants
├── templates/
│   └── index.html    # Browser UI
└── requirements.txt
```
