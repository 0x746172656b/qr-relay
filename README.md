# QR Mirror

> **Archived.** Quick personal project, no longer maintained.

---

My gym uses a QR code for turnstile access. You open the app, generate a QR code, scan it, done.

The problem: the app ties your QR code to a single registered device. No multi-device support, no secondary device option, no way to authorize a second phone. If you want to use a different device, you can't. The subscription is paid per person, but access is enforced per device. That is a bad policy and the gym charged me money for it.

This project exists because that constraint is artificial and I had a free weekend.

---

**What this does:** captures the QR code displayed on one screen and serves it as a live image over a local web server. Any browser on the same network can load the mirrored QR code in real time, on any device, without the app.

The setup that motivated this: run the gym app on an Android VM on a desktop, capture the QR code it generates, push it to a web page accessible from any device on the network. If the app showed a confirmation dialog between scans, the auto-clicker dismissed it so the next scan could proceed without manual intervention.

---

## Security

If you expose this beyond your local network, put it behind an authentication layer (Authelia, Authentik, or HTTP basic auth at minimum) — the endpoint serves a live QR code with no access control.

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
