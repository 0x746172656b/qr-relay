import os

# QR scanning
NO_QR_TIMEOUT = 5        # seconds before falling back to placeholder
SCAN_DURATION = 60       # active scan window length in seconds
DEBOUNCE_TIME = 0.1      # seconds to suppress duplicate QR reads

# Auto-clicker
TEMPLATE_PATH = os.environ.get('BUTTON_TEMPLATE', 'button.png')
MATCH_THRESHOLD = 0.8
FAST_CHECK_INTERVAL = 15     # seconds between checks while expecting the button
SLOW_CHECK_INTERVAL = 180    # seconds between checks otherwise
PAUSE_AFTER_CLICK = 60       # seconds to wait after clicking

# Countdown shown in the UI after the button is clicked
TIMER_DURATION = 3 * 60 * 60  # 3 hours

# Server
PORT = int(os.environ.get('PORT', '8080'))
