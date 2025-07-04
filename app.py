from flask import Flask, request, jsonify
import json
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='2_Billion_Fireflies_Relay',
                            user='postgres',
                            password='{ENTER PASSWORD HERE}')
    return conn

@app.get("/ping")
def ping():
    return jsonify({})

@app.post("/api/send")
def add_message():
    if request.is_json:
        data = request.get_json()
        with get_db_connection() as conn:
            with conn.cursor() as curs:
                curs.execute("""
                insert into messages("from", "to", "payload", "when")
                values (%(from)s, %(to)s, %(payload)s, now())
                """, data)
        return {}, 200
    return {"error": "Request must be JSON"}, 415


@app.post("/api/receive")
def receive_messages():
    if request.is_json:
        data = request.get_json()
        result = []
        with get_db_connection() as conn:
            with conn.cursor() as curs:
                curs.execute("select \"from\", \"payload\" from messages where \"to\"=%(to)s", data)
                for message in curs.fetchall():
                    result.append({"from": message[0], "payload": message[1]})
        return result, 200
    return {"error": "Request must be JSON"}, 415
