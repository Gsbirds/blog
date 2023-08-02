import React from "react";
import './App.css';
import { useState, useEffect } from "react";
import axios from 'axios';
import Comment from "./Comment";

function Wheel(props) {
    const [blog, setBlog] = useState("");
    const [comment, setComment] = useState("");
    const [hiddenC, setHiddenC] = useState("hiddenC");
    const [hiddenF, setHiddenF]= useState("hiddenF");

    const showComments = () => {
        if (hiddenC=="hiddenC"){
        setHiddenC("visibleV");
        } else{
            setHiddenC("hiddenC")
        }
      };

    
      const addComments = () => {
        if (hiddenF=="hiddenF"){
        setHiddenF("visibleF");
        } else{
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
            <div style={{ backgroundColor: props.text }} className="container" >
                <b>
                    <p style={{ color: props.color }} >Here is a Blog that I am hard-coding into my react-app. Why, you probably dont ask?? Thanks for asking. Because I am terrified, uninspired, bored, and a bit listliss currently, and I wanted to do this cool
                        color thing that you see on the site. You probably think- oh. thats nifty. Or maybe- oh, how over-done. In any case, it took me a night. Changing topics now, I guess the reason for my blog is just to help people like me- the terrified and uninspired programmers, philosophers, and artists feel
                        a bit less terrified. Maybe even more inspired.
                        And if you dont feel that way, then I guess frack off? Or stay. You are welcome to. Today I wanted to complain about HackerRank. Hacker rank is big and mean and scary and notveryfriendly. As a lil 6oz 3 lb baby developer, ive had to practice and practice and practice. To no avail.
                        At something you don't ever really do when you are a big serious business person developer. You know, when you get to say stuff like "Let's circle back to that, Margaret", or "Marggie, have that to me by EOD". I like to make things- its part of why I like to paint i guess. I've never liked being tested.
                        It gives me an impending feeling of doom probably originating in highscool where we were all told that if we dont do well in school, that we would never cease to be... well. loosers. Am I a looser?
                        Are you a looser too? Then there's the pair of us...
                        In any case, back to serious developer business- HackerRank. I did not want to only address how seeminly innefficient this platform is for what it "perports" to do. I also
                        wanted to address the larger obsession with competition in programmin I have, to my dismay, noticed. Lets start with my observations of hackerrank as a lil beeb developer.

                        <ul>
                            <li> I have never read such a badly written prompt in my entire life.</li>
                            <li>Most of figuring out how to solve the problem when you first start hackerrank is figuring out how to handle just the inputs. This makes the
                                whole effort seem like a giant excercise in futility. Werent we just supposed to be learning how to use python, javascript, java, etc. to solve puzzles
                                that will convice employers -somehow- that we can actually put those tools to good use?
                            </li>
                        </ul>

                    </p>
                </b>
            </div>

            {blog.length ?
                <>
                    <>
                        {blog.map((blog) => {
                            const elements = [];
                            elements.push(
                                <div key={blog.id} style={{ backgroundColor: props.text }} className="container">
                                    <b>
                                        <p style={{ color: props.color }}>{blog.title}</p>
                                    </b>

                                    <p className="arrow" onClick={showComments} style={{ color:props.color, fontSize: 100 }}><b>˅</b></p>
                                    {comment
                                        .filter((c) => c.blogs_id === blog.id)
                                        .map((c) => (
                                            <div id={hiddenC} key={c.id} style={{ backgroundColor: props.color, width: 900 }} className="container">
                                                <b>
                                                    {/* Render the filtered comments' titles */}
                                                    <p style={{ color: props.text }}>{c.title}</p>
                                                </b>
                                            </div>
                                        ))}
                                </div>
                                
                            );

                            elements.push(<p className="arrow" onClick={addComments} style={{ color:props.text, fontSize: 50 }}><b>Comment</b></p>, <Comment hiddenF={hiddenF} blogid={blog.id} key={`comment_${blog.id}`}/> 
                            );


                            return elements;
                        })}

                    </>
                </>
                : ""
            }
        </>
    );

}

export default Wheel;