import contextlib
from sqlalchemy import ForeignKey
import databases
import sqlalchemy
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse 
from sqlalchemy.orm import relationship, mapper
from sqlalchemy import Text

# Configuration from environment variables or '.env' file.
config = Config('.env')
DATABASE_URL = config('DATABASE_URL')

# Database table definitions.
metadata = sqlalchemy.MetaData()

blogs = sqlalchemy.Table(
    "blogs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", Text), 
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("date", sqlalchemy.String),

)

comments = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("date", sqlalchemy.String),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("blogs_id", sqlalchemy.Integer, ForeignKey("blogs.id")),

)

class Blog:
    pass

class Comment:
    pass

mapper(Blog, blogs, properties={
    "comments": relationship(Comment, backref="blog", cascade="all, delete-orphan")
})

mapper(Comment, comments, properties={
    "blog": relationship(Blog, back_populates="comments", cascade="all, delete-orphan")
})


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
            "title": result["title"],
            "id": result["id"]
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

async def delete_blog(request):
    blog_id = request.path_params.get("id")
    
    query = blogs.delete().where(blogs.c.id == blog_id)
    
    await database.execute(query)

    return JSONResponse({"message": "Blog successfully deleted"})


async def update_blog(request):
    blog_id = request.path_params.get("id")

    data = await request.json()

    query = blogs.update().where(blogs.c.id == blog_id).values(
        text=data.get("text"),
        title=data.get("title"),
        date=data.get("date")
    )

    await database.execute(query)

    return JSONResponse({"message": "Blog successfully updated"})


async def list_comments(request):
    query = comments.select()
    results = await database.fetch_all(query)
    content = [
        {
            "text": result["text"],
            "title": result["title"],
            "date": result["date"],
            "name": result["name"],
            "blogs_id":result["blogs_id"]
        }
        for result in results
    ]
    return JSONResponse(content)


async def delete_comment(request):
    comment_id = request.path_params.get("id")
    
    query = comments.delete().where(comments.c.id == comment_id)
    
    await database.execute(query)

    return JSONResponse({"message": "Comment successfully deleted"})

async def update_comment(request):
    comment_id = request.path_params.get("id")

    data = await request.json()

    query = blogs.update().where(comments.c.id == comment_id).values(
        text=data.get("text"),
        title=data.get("title"),
        name=data.get("title"),
        date=data.get("date")
    )

    await database.execute(query)

    return JSONResponse({"message": "Comment successfully updated"})

async def add_comment(request):
    data = await request.json()
    query = comments.insert().values(
       text=data["text"],
       title=data["title"],
       date=data["date"],
       name=data["name"],
       blogs_id=data["blogs_id"]

    )
    await database.execute(query)
    return JSONResponse({
        "text": data["text"],
        "title": data["title"],
        "date": data["date"],
        "name":data["name"],
        "blogs_id":data["blogs_id"]
    })

routes = [
    Route("/blogs", endpoint=list_blogs, methods=["GET"]),
    Route("/blogs/{id}", endpoint=delete_blog, methods=["DELETE"]),
    Route("/blogs/{id}", endpoint=update_blog, methods=["PUT"]),
    Route("/blogs", endpoint=add_blog, methods=["POST"]),
    Route("/comments", endpoint=list_comments, methods=["GET"]),
    Route("/comments", endpoint=add_comment, methods=["POST"]),
    Route("/comment/{id}", endpoint=delete_comment, methods=["DELETE"]),
    Route("/comment/{id}", endpoint=update_comment, methods=["PUT"]),
]

app = Starlette(
    routes=routes,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="./build/static"), name="static")

@app.route("/")
async def index(request):
    with open("./build/index.html") as f:
        return HTMLResponse(f.read())

app.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_origins=["http://localhost:3000"], allow_headers=["http://localhost:3000"], allow_methods=["*"]
)
