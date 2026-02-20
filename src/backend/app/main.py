from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, todos, users
from app.api.v1 import chat
from app.core.config import settings


def create_app():
    app = FastAPI(
        title="Todo Web Application API",
        description="Phase II Todo Web Application with user authentication and todo management",
        version="1.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify your frontend domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(todos.router, prefix="/api/todos", tags=["Todos"])
    app.include_router(users.router, prefix="/api/users", tags=["Users"])
    app.include_router(chat.router, prefix="/api/chat", tags=["AI Chat"])

    @app.get("/api/health")
    def health_check():
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)