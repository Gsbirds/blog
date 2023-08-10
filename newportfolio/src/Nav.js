import { NavLink } from "react-router-dom";
import { ColorPicker, useColor } from "react-color-palette";
import "react-color-palette/lib/css/styles.css";
import React, { Component } from "react";
import { GithubPicker } from 'react-color';
import { CustomPicker } from 'react-color';
import { useState, useEffect } from "react";
function Nav(props) {
    const [color, setColor] = useColor("hex", "#121212");
    const [text, setText] = useState("");
    const [actColor, setActColor]=useState("")
  
  
    useEffect(() => {
      // document.body.style.backgroundColor = color.hex;
  
      // Get RGB values from the HEX color
      const red = parseInt(color.hex.substring(1, 3), 16);
      const green = parseInt(color.hex.substring(3, 5), 16);
      const blue = parseInt(color.hex.substring(5, 7), 16);
  
      // Calculate lighter shades of RGB values (e.g., increase each value by 50)
      const lighterRed = Math.min(red + 90, 255);
      const lighterGreen = Math.min(green + 90, 255);
      const lighterBlue = Math.min(blue + 90, 255);
  
      // Convert the lighter RGB values back to HEX
      const lighterHex =
        "#" +
        (lighterRed < 16 ? "0" : "") + lighterRed.toString(16) +
        (lighterGreen < 16 ? "0" : "") + lighterGreen.toString(16) +
        (lighterBlue < 16 ? "0" : "") + lighterBlue.toString(16);
        document.body.style.backgroundColor = lighterHex;
        setActColor(lighterHex)
      setText(color.hex);
    }, [color]); // This effect will only trigger when the 'color' state changes
  
    return (
        <nav className="navbar navbar-expand-lg">
            <NavLink style={{color: props.text}} className="navbar-brand mx-2" to="/">
             The Uninspired Philosoraptor
            </NavLink>
            <button
                className="navbar-toggler"
                type="button"
                data-toggle="collapse"
                data-target="#navbarNav"
                aria-controls="navbarNav"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span className="navbar-toggler-icon"></span>
            </button>
            <div className="navbar" id="navbarNav">
                <b>
                <ul className="navbar-nav">
                    

            <li> <NavLink style={{color: props.text}} className="nav-link" aria-current="page" to="/">
                            Blog
                        </NavLink></li>
                        {/* <li> <NavLink style={{color: props.text}} className="nav-link" aria-current="page" to="/">
                            About this bitch
                        </NavLink></li> */}

                </ul>
                </b>
            </div>
            {/* <GithubPicker className="custom-color-picker" onChangeComplete={ setColor } /> */}

        </nav>
    );
}
export default Nav;

