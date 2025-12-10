from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.routers.v1.auth import router as auth
# from app.routers.v1.users import router as users 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# ✨ Create FastAPI App with Metadata
app = FastAPI(
    title="🎉 LIVORA API",
    description="Authentication & User Management System",
    version="1.0.0",
)

# 🌍 Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth, prefix="/auth", tags=["Authentication"])
# app.include_router(users, prefix="/users", tags=["Users"])

@app.get("/", response_class=HTMLResponse, tags=["Root"])
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎉 LIVORA API Service</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 40px;
                background: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                margin-bottom: 20px;
            }
            .info {
                color: #666;
                line-height: 1.6;
            }
            .endpoints {
                margin-top: 20px;
            }
            .endpoint {
                background: #f8f9fa;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                font-weight: bold;
            }
            a {
                color: #3498db;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 Welcome to LIVORA API</h1>
            <div class="info">
                <p>This API handles Authentication, Authorization, and User Management.</p>
                <p>Use the links below to explore endpoints and check server status.</p>
            </div>
            <div class="endpoints">
                <div class="endpoint">📚 API Documentation: <a href="/docs">Swagger UI</a></div>
                <div class="endpoint">🏥 Health Check: <a href="/health">Status</a></div>
                <div class="endpoint">📑 API Reference: <a href="/redoc">ReDoc</a></div>
            </div>
        </div>
    </body>
    </html>
    """

# 🩺 Health Endpoint
@app.get("/health", tags=["Root"])
def health():
    return {"status": "OK", "service": "LIVORA API"}

