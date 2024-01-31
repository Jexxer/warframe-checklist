from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth.router import router as authRouter
from src.database import Base, SessionLocal, engine
from src.gamedata.router import router as gamedataRouter
from src.users.router import router as usersRouter

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(authRouter)
app.include_router(usersRouter)
app.include_router(gamedataRouter)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
