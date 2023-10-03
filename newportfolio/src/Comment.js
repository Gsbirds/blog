import React from "react";
import "./App.css";
import { useState, useEffect } from "react";
import DOMPurify from "dompurify";

function Comment(props) {
  const [comment, setComment] = useState("");
  const [title, setTitle] = useState("");
  const [name, setName] = useState("");
  const [date, setDate] = useState("");
  const [text, setText] = useState("");
  const [blog, setBlog] = useState([]);

  const handleTitleChange = (event) => {
    const value = event.target.value;
    setTitle(value);
  };
  const handleNameChange = (event) => {
    const value = event.target.value;
    setName(value);
  };
  const handleDateChange = (event) => {
    const value = event.target.value;
    setDate(value);
  };
  const handleTextChange = (event) => {
    const value = event.target.value;
    setText(value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    // create an empty JSON object
    const data = {};

    data.title = DOMPurify.sanitize(title);
    data.name = DOMPurify.sanitize(name);
    data.text = DOMPurify.sanitize(text);
    data.date = DOMPurify.sanitize(date);
    data.blogs_id = props.blogid;

    const Url = "https://calm-reef-66202-3443b850ed8c.herokuapp.com/comments";
    const fetchConfig = {
      method: "post",
      body: JSON.stringify(data),
    };

    const response = await fetch(Url, fetchConfig);
    if (response.ok) {
      const res = await response.json();
      setTitle("");
      setName("");
      setDate("");
      setText("");
    }
  };

  // const colorPicker = document.getElementById("color-picker");
  return (
    <>
      <div id={props.hiddenF} className="row">
        <div className="offset-3 col-6">
          <div
            style={{ backgroundColor: props.text }}
            id="comment-box"
            className="shadow p-4 mt-4"
          >
            <h1>Add a comment</h1>
            <form onSubmit={handleSubmit} id="create-presentation-form">
              <div className="form-floating mb-3">
                <input
                  onChange={handleTitleChange}
                  value={title}
                  placeholder="title"
                  required
                  type="text"
                  id="title"
                  className="form-control"
                />
                <label htmlFor="presenter_name">Title</label>
              </div>
              <div className="form-floating mb-3">
                <input
                  type="text"
                  onChange={handleNameChange}
                  value={name}
                  placeholder="name"
                  id="name"
                  className="form-control"
                />
                <label htmlFor="presenter_name">Name</label>
              </div>
              <div className="form-group">
                <textarea
                  type="text"
                  onChange={handleTextChange}
                  value={text}
                  placeholder="Your comment"
                  className="form-control"
                  rows="4"
                  id="exampleFormControlTextarea1"
                />
                <label htmlFor="presenter_name"></label>
              </div>
              <div className="form-floating mb-3">
                <input
                  className="form-control"
                  onChange={handleDateChange}
                  name="date"
                  id="date"
                  // className="form-select "
                  type="text"
                  value={date}
                />
                <label htmlFor="presenter_name">Date</label>
              </div>
              <button className="btn btn-dark">Comment</button>
            </form>
          </div>
        </div>
      </div>
    </>
  );
}

export default Comment;
