from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3
import random
import string
import os

server = FastAPI()
baza = "storage.sqlite"
def generate_code(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
@server.get("/", response_class=HTMLResponse)
def serve_form():
    return """
    <!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>Скорочення силок</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: linear-gradient(to bottom right, #f7f7f7, #ffffff);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .container {
            background-color: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            width: 450px;
            text-align: center;
            position: relative;
        }

        h1 {
            font-size: 26px;
            margin-bottom: 30px;
            color: #333;
        }

        .input-wrapper {
            position: relative;
            display: flex;
            align-items: center;
            border: 2px solid #000;
            border-radius: 30px;
            padding: 10px 15px;
            background-color: #fafafa;
            transition: box-shadow 0.3s;
        }

        .input-wrapper:focus-within {
            box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.2);
        }

        .dot-left {
            display: flex;
            gap: 5px;
            position: absolute;
            top: 50%;
            left: 15px;
            transform: translateY(-50%);
        }

        .dot {
            width: 6px;
            height: 6px;
            background-color: black;
            border-radius: 50%;
            opacity: 0;
            animation: blink 1.5s infinite;
        }

        .dot:nth-child(2) {
            animation-delay: 0.2s;
        }

        .dot:nth-child(3) {
            animation-delay: 0.4s;
        }

        @keyframes blink {
            0%, 100% { opacity: 0; }
            50% { opacity: 1; }
        }

        input[type="text"] {
            flex: 1;
            border: none;
            outline: none;
            font-size: 16px;
            background: transparent;
            padding: 5px 10px;
        }
    </style>
</head>
<body>
<form action="/submit" method="post">
    <div class="container">
        <h1>Скорочення силок</h1>
        <div class="input-wrapper">
            <div class="dot-left">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
            <input type="text" id="urlInput" name="url">
            <button type="submit">Скоротити</button>
        </div>
</form>
    </div>

    <script>
        const leftDots = document.querySelector('.dot-left');
        const input = document.getElementById('urlInput');

        function updateDotsVisibility() {
            const isEmpty = input.value.trim().length === 0;
            leftDots.style.display = isEmpty ? 'flex' : 'none';
        }

        input.addEventListener('focus', updateDotsVisibility);
        input.addEventListener('blur', updateDotsVisibility);
        input.addEventListener('input', updateDotsVisibility);
        window.addEventListener('DOMContentLoaded', updateDotsVisibility);
    </script>
</body>
</html>
    """
def init_db():
    with sqlite3.connect(baza) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS links (
                code TEXT PRIMARY KEY,
                url TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()
@server.post("/submit")
def handle_submit(url: str = Form(...)):
    code = generate_code()
    with sqlite3.connect(baza) as conn:
        conn.execute("INSERT INTO links (code, url) VALUES (?, ?)", (code, url))
        conn.commit()
    return {"short_url": f"http://127.0.0.1:8888/{code}"}

@server.get("/{code}")
def redirect(code: str):
    with sqlite3.connect(baza) as conn:
        cursor = conn.execute("SELECT url FROM links WHERE code = ?", (code,))
        result = cursor.fetchone()
        if result:
            return RedirectResponse(result[0])
