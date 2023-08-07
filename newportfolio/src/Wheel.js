import React from "react";
import './App.css';
import { useState, useEffect } from "react";
import axios from 'axios';
import Comment from "./Comment";

function Wheel(props) {
    const [blog, setBlog] = useState("");
    const [comment, setComment] = useState("");
    const [hiddenF, setHiddenF] = useState("hiddenF");
    const [arrow, setArrow] = useState("arrow");
    const [activeArrow, setActiveArrow] = useState({});

    const showComments = (key) => {
      setActiveArrow((prevActiveArrows) => ({
        ...prevActiveArrows,
        [key]: !prevActiveArrows[key],
      }));
    };


    const addComments = () => {
        if (hiddenF == "hiddenF") {
            setHiddenF("visibleF");
        } else {
            setHiddenF("hiddenF")
        }
    };

    const fetchBlogs1 = {
        method: 'GET',
        url: 'http://localhost:8000/blogs',
    }

    useEffect(() => {
        const fetchBlogs = async () => {
            axios.get(fetchBlogs1.url).then((response) => {
                setBlog(response.data)
                console.log(blog)

            }).catch((error) => {
                console.error(error)
            })
        }
        fetchBlogs()
    }, []);

    const fetchComments1 = {
        method: 'GET',
        url: 'http://localhost:8000/comments',
    }
    useEffect(() => {
        const fetchComments = async () => {
            axios.get(fetchComments1.url).then((response) => {
                setComment(response.data)
                console.group(comment)

            }).catch((error) => {
                console.error(error)
            })
        }
        fetchComments()
    }, []);
    // const colorPicker = document.getElementById("color-picker");
    return (
        <>
            <h1 className="blog-title" style={{ color: props.text }}>An uninspired blog.</h1>
            <b>
                <p className="poem"><ul style={{ color: props.text }}>
                    <li>I'm Nobody! Who are you?</li>
                    <li>Are you - Nobody - too?</li>
                    <li>Then there's the pair of us!</li>
                    <li>Don't tell! They'd advertise- you know!</li>
                    <li>How dreary -to be- somebody</li>
                    <li>How public -like a Frog- </li>
                    <li>To tell one's name- the livelong June-</li>
                    <li>To an admiring Bog!</li>

                    - I'm Nobody! Who are you?
                    Emily Dickinson
                </ul></p>
            </b>

            {blog.length ? (
        <>
          {blog.map((blog) => {
            const elements = [];
            elements.push(
              <div key={blog.id} style={{ backgroundColor: props.text }} className="container">
                <b>
                  <p style={{ color: props.color }}>{blog.title}</p>
                  <p style={{ color: props.color }}>{blog.text}</p>
                </b>

                <p
                  className={arrow}
                  key={blog.id}
                  onClick={() => showComments(blog.id)}
                  style={{ color: props.color, fontSize: 100 }}
                >
                  <b>˅</b>
                </p>
                {comment
                  .filter((c) => c.blogs_id === blog.id && activeArrow[blog.id])
                  .map((c) => (
                    <div
                      key={c.blogs_id}
                      style={{ backgroundColor: props.color, width: 900 }}
                      className="container"
                    >
                      <b>
                        {/* Render the filtered comments' titles */}
                        <p style={{ color: props.text }}>{c.title}</p>
                      </b>
                    </div>
                  ))}
              </div>
            );

            elements.push(
              <p className="arrow" onClick={addComments} style={{ color: props.text, fontSize: 50 }} key={`comment_${blog.id}`}>
                <b>Comment</b>
              </p>,
              <Comment hiddenF={hiddenF} blogid={blog.id} key={`comment_${blog.id}`} />
            );

            return elements;
          })}
        </>
      ) : (
        ""
      )}
    </>
  );
}

export default Wheel;




