import contextlib

import databases
import sqlalchemy
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Route


# Configuration from environment variables or '.env' file.
config = Config('.env')
DATABASE_URL = config('DATABASE_URL')

# Database table definitions.
metadata = sqlalchemy.MetaData()

blogs = sqlalchemy.Table(
    "blogs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("date", sqlalchemy.String),

)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
database = databases.Database(DATABASE_URL)

@contextlib.asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield
    await database.disconnect()

# Main application code.
async def list_blogs(request):
    query = blogs.select()
    results = await database.fetch_all(query)
    content = [
        {
            "text": result["text"],
            "title": result["title"]
        }
        for result in results
    ]
    return JSONResponse(content)

async def add_blog(request):
    data = await request.json()
    query = blogs.insert().values(
       text=data["text"],
       title=data["title"],
       date=data["date"]
    )
    await database.execute(query)
    return JSONResponse({
        "text": data["text"],
        "title": data["title"],
        "date": data["date"]
    })

routes = [
    Route("/blogs", endpoint=list_blogs, methods=["GET"]),
    Route("/blogs", endpoint=add_blog, methods=["POST"]),
]

app = Starlette(
    routes=routes,
    lifespan=lifespan,
)