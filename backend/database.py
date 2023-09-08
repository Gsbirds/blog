import contextlib
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from datetime import datetime
import os

# Retrieve the original DATABASE_URL
original_db_url = os.environ.get("DATABASE_URL1")

# Create SQLAlchemy engine and session
engine = create_engine(original_db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define your SQLAlchemy models using declarative_base
Base = declarative_base()

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    title = Column(String)
    date = Column(String)
    comments = relationship("Comment", back_populates="blog", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    title = Column(String)
    date = Column(String)
    name = Column(String)
    blogs_id = Column(Integer, ForeignKey("blogs.id"))

    blog = relationship("Blog", back_populates="comments")


# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Main application code.
async def list_blogs(request):
    session = SessionLocal()
    blogs = session.query(Blog).all()
    content = [
        {
            "text": blog.text,
            "title": blog.title,
            "id": blog.id
        }
        for blog in blogs
    ]
    session.close()
    return JSONResponse(content)

async def add_blog(request):
    data = await request.json()
    new_blog = Blog(**data)
    session = SessionLocal()
    session.add(new_blog)
    session.commit()
    session.close()
    return JSONResponse(data)

async def delete_blog(request):
    blog_id = request.path_params.get("id")
    session = SessionLocal()
    session.query(Blog).filter_by(id=blog_id).delete()
    session.commit()
    session.close()
    return JSONResponse({"message": "Blog successfully deleted"})

async def update_blog(request):
    blog_id = request.path_params.get("id")
    data = await request.json()
    session = SessionLocal()
    session.query(Blog).filter_by(id=blog_id).update(data)
    session.commit()
    session.close()
    return JSONResponse({"message": "Blog successfully updated"})

async def list_comments(request):
    session = SessionLocal()
    comments = session.query(Comment).all()
    content = [
        {
            "text": comment.text,
            "title": comment.title,
            "date": comment.date,
            "name": comment.name,
            "blogs_id": comment.blogs_id
        }
        for comment in comments
    ]
    session.close()
    return JSONResponse(content)

async def delete_comment(request):
    comment_id = request.path_params.get("id")
    session = SessionLocal()
    session.query(Comment).filter_by(id=comment_id).delete()
    session.commit()
    session.close()
    return JSONResponse({"message": "Comment successfully deleted"})

async def update_comment(request):
    comment_id = request.path_params.get("id")
    data = await request.json()
    session = SessionLocal()
    session.query(Comment).filter_by(id=comment_id).update(data)
    session.commit()
    session.close()
    return JSONResponse({"message": "Comment successfully updated"})

async def add_comment(request):
    data = await request.json()
    new_comment = Comment(**data)
    session = SessionLocal()
    session.add(new_comment)
    session.commit()
    session.close()
    return JSONResponse(data)

routes = [
    Route("/blogs", endpoint=list_blogs, methods=["GET"]),
    Route("/blogs/{id}", endpoint=delete_blog, methods=["DELETE"]),
    Route("/blogs/{id}", endpoint=update_blog, methods=["PUT"]),
    Route("/blogs", endpoint=add_blog, methods=["POST"]),
    Route("/comments", endpoint=list_comments, methods=["GET"]),
    Route("/comments", endpoint=add_comment, methods=["POST"]),
    Route("/comments/{id}", endpoint=delete_comment, methods=["DELETE"]),
    Route("/comments/{id}", endpoint=update_comment, methods=["PUT"]),
]

app = Starlette(
    routes=routes
)

app.mount("/static", StaticFiles(directory="./build/static"), name="static")

@app.route("/")
async def index(request):
    with open("./build/index.html") as f:
        return HTMLResponse(f.read())

app.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_origins=["http://localhost:3000", "https://blog.gabby.codes", "https://calm-reef-66202-3443b850ed8c.herokuapp.com/"], allow_headers=["http://localhost:3000", "https://blog.gabby.codes", "https://blog.gabby.codes", "https://calm-reef-66202-3443b850ed8c.herokuapp.com/"], allow_methods=["*"]
)
