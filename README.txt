Bus365 Demo - Flask app
Location: /mnt/data/bus365_demo

To run locally (you need Python 3.8+ and pip):
1. cd /mnt/data/bus365_demo
2. python3 -m venv venv
3. source venv/bin/activate   (Windows: venv\Scripts\activate)
4. pip install flask
5. python app.py
6. Open http://127.0.0.1:8787 in your browser

Notes:
- This is a demo with in-memory data. No database included.
- For production, add persistent storage, authentication, real payment integration, and security hardening.
