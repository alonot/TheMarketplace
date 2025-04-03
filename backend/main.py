from contextlib import asynccontextmanager
import os
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

load_dotenv()

DEBUG = os.environ.get("DEBUG") != "False"

if not DEBUG:
    TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
    TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")
    dbUrl = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"
else:
    sqlite_file_name = "database.db"
    dbUrl = f"sqlite:///{sqlite_file_name}"

engine = create_engine(dbUrl, connect_args={'check_same_thread': False}, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    runs before starting the server
    '''
    ## initializes the database tables if debug is on
    if DEBUG:
        create_db_and_tables()
    yield
    ## code to be ran after shutting the server


def get_session():
    '''
    yields a session for each request. Hence each request will occur in separate session
    '''
    with Session(engine) as session:
        # yield Session
        #seems like an error
        yield session

## A dependency which will run on each request
SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)

from .app.views import apirouter 
from .auth.views import authrouter 
from .admin.views import adminrouter 
from .dependencies import admin_middleware, app_middleware, auth_middleware

## Welcome message
@app.get('/', response_class=HTMLResponse)
def home():
    return """
    <h1>Welcome</h1> <strong>to the TheIITPKDMarketplace api.</strong>
    """

app.add_middleware(app_middleware)

api_app = FastAPI()
api_app.include_router(apirouter)

auth_app = FastAPI()
auth_app.add_middleware(auth_middleware)
auth_app.include_router(authrouter)

admin_app = FastAPI()
admin_app.add_middleware(admin_middleware)
admin_app.include_router(adminrouter)

app.mount("/api", api_app)
app.mount("/auth", auth_app)
app.mount("/admin", admin_app)