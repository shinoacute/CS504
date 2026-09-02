import json
import os

import azure.functions as func
import pyodbc

app = func.FunctionApp()

ALLOWED_ORIGINS = {
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5000",
    "http://localhost:5000",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
}

CONNECTION_STRING = (
    "DRIVER={SQL Server};"
    "SERVER=cityuweek8thao.database.windows.net;"
    "DATABASE=week8-thao;"
    "UID=thao-admin;"
    "PWD=Buihoangco123.;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)


def add_cors_headers(req: func.HttpRequest, response: func.HttpResponse) -> func.HttpResponse:
    origin = req.headers.get("Origin")
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
    return response


def check_credentials(username, password):
    with pyodbc.connect(CONNECTION_STRING) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT 1
            FROM dbo.[user]
            WHERE username = ? AND password = ?
            """,
            username,
            password,
        )
        return cursor.fetchone() is not None


@app.route(route="", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def index(req: func.HttpRequest) -> func.HttpResponse:
    body = {
        "message": "Login successful, welcome!",
        "username": req.params.get("username"),
    }
    response = func.HttpResponse(json.dumps(body), mimetype="application/json")
    return add_cors_headers(req, response)


@app.route(route="login", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def login(req: func.HttpRequest) -> func.HttpResponse:
    username = req.params.get("username")
    password = req.params.get("password")

    if not username or not password:
        response = func.HttpResponse(
            json.dumps({"error": "username and password are required"}),
            status_code=400,
            mimetype="application/json",
        )
        return add_cors_headers(req, response)

    if check_credentials(username, password):
        response = func.HttpResponse(
            json.dumps({"authenticated": True}), status_code=200, mimetype="application/json"
        )
    else:
        response = func.HttpResponse(
            json.dumps({"authenticated": False}), status_code=401, mimetype="application/json"
        )

    return add_cors_headers(req, response)
