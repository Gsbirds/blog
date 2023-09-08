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
from werkzeug.security import generate_password_hash, check_password_hash


# Retrieve the original DATABASE_URL
original_db_url = os.environ.get("DATABASE_URL1")

# Create SQLAlchemy engine and session
engine = create_engine(original_db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define your SQLAlchemy models using declarative_base
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
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

# def create_user(username, password):
#     session = SessionLocal()
#     new_user = User(username=username)
#     new_user.set_password(password)
#     session.add(new_user)
#     session.commit()
#     session.close()

# # # ... (other code)

# # # Create a new user (call this function with the desired username and password)
# create_user()

# Main application code.

async def list_users(request):
    session = SessionLocal()
    users = session.query(User).all()
    user_list = [
        {
            "id": user.id,
            "username": user.username,
        }
        for user in users
    ]
    session.close()
    return JSONResponse(user_list)

async def login(request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()

    if user and user.check_password(password):
        # Authentication successful
        return JSONResponse({"message": "Login successful"})
    else:
        # Authentication failed
        return JSONResponse({"message": "Login failed"}, status_code=401)


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
    username = request.query_params.get("username")
    password = request.query_params.get("password")

    if not (username and password):
        # Check headers if query parameters are not provided
        username = request.headers.get("X-Username")
        password = request.headers.get("X-Password")

    if not (username and password):
        return JSONResponse({"message": "Authentication required"}, status_code=401)

    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()

    if not (user and user.check_password(password)):
        return JSONResponse({"message": "Authentication failed"}, status_code=401)

    # Proceed with the route logic
    session = SessionLocal()
    data = await request.json()
    new_blog = Blog(**data)
    session = SessionLocal()
    session.add(new_blog)
    session.commit()
    session.close()
    return JSONResponse(data)

async def delete_blog(request):
    username = request.query_params.get("username")
    password = request.query_params.get("password")

    if not (username and password):
        # Check headers if query parameters are not provided
        username = request.headers.get("X-Username")
        password = request.headers.get("X-Password")

    if not (username and password):
        return JSONResponse({"message": "Authentication required"}, status_code=401)

    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()

    if not (user and user.check_password(password)):
        return JSONResponse({"message": "Authentication failed"}, status_code=401)

    # Proceed with the route logic
    session = SessionLocal()
    blog_id = request.path_params.get("id")
    session = SessionLocal()
    session.query(Blog).filter_by(id=blog_id).delete()
    session.commit()
    session.close()
    return JSONResponse({"message": "Blog successfully deleted"})

async def update_blog(request):
    username = request.query_params.get("username")
    password = request.query_params.get("password")

    if not (username and password):
        # Check headers if query parameters are not provided
        username = request.headers.get("X-Username")
        password = request.headers.get("X-Password")

    if not (username and password):
        return JSONResponse({"message": "Authentication required"}, status_code=401)

    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()

    if not (user and user.check_password(password)):
        return JSONResponse({"message": "Authentication failed"}, status_code=401)
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

async def protected_list_blogs(request):
    # Get the username and password from query parameters or headers
    username = request.query_params.get("username")
    password = request.query_params.get("password")

    if not (username and password):
        # Check headers if query parameters are not provided
        username = request.headers.get("X-Username")
        password = request.headers.get("X-Password")

    if not (username and password):
        return JSONResponse({"message": "Authentication required"}, status_code=401)

    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()

    if not (user and user.check_password(password)):
        return JSONResponse({"message": "Authentication failed"}, status_code=401)

    # Proceed with the route logic
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

app = Starlette()

# Define routes
app.add_route("/blogs", add_blog, methods=["POST"])
app.add_route("/blogs", list_blogs, methods=["GET"])
app.add_route("/blogs/{id}", delete_blog, methods=["DELETE"])
app.add_route("/blogs/{id}", update_blog, methods=["PUT"])
app.add_route("/comments", list_comments, methods=["GET"])
app.add_route("/comments", add_comment, methods=["POST"])
app.add_route("/comments/{id}", delete_comment, methods=["DELETE"])
app.add_route("/comments/{id}", update_comment, methods=["PUT"])

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[
        "http://localhost:3000",
        "https://blog.gabby.codes",
        "https://calm-reef-66202-3443b850ed8c.herokuapp.com/",
    ],
    allow_headers=[
        "http://localhost:3000",
        "https://blog.gabby.codes",
        "https://calm-reef-66202-3443b850ed8c.herokuapp.com/",
    ],
    allow_methods=["*"],
)

# Add authentication middleware
# Serve static files (e.g., index.html) from the 'static' folder
app.mount("/static", StaticFiles(directory="build/static"), name="static")

# Define a route to serve the index.html file
@app.route("/")
async def index(request):
    return HTMLResponse(open("./build/index.html", "r").read())
