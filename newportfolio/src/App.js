import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import { useState, useEffect } from "react";
import Wheel from "./Wheel";
import { ColorPicker, useColor } from "react-color-palette";
import "react-color-palette/lib/css/styles.css";
import React, { Component } from "react";
import { GithubPicker } from 'react-color';
import { CustomPicker } from 'react-color';
import Nav from "./Nav.js"
import Comment from "./Comment";

function App() {

  // ///////////////////////////////////////////////////////////////
  const [color, setColor] = useColor("hex", "#121212");
  const [text, setText] = useState("");
  const [actColor, setActColor]=useState("")
  const [hidden, setHidden]=useState("hidden")

  const setHiddenColor = () => {
    if (hidden=="custom-color-picker"){
    setHidden("hidden")
    }else if(hidden=="hidden"){
      setHidden("custom-color-picker")
    }
  };

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
    <>
      <div className="app" id="parallax">

        <BrowserRouter>
        <Nav text={text}/>
        <button className="change" onClick={setHiddenColor}>Change Theme</button>
        <GithubPicker className={hidden} onChangeComplete={ setColor } />
    {/* <img className="veloci" src="./veloci.png" style={{width:1500, position:"background"}}/> */}
          <Routes>
            <Route path="/" element={<Wheel text={text} color={actColor}/>} />
            <Route path="/Comment" element={<Comment text={text} color={actColor}/>} />

          </Routes>
        </BrowserRouter>
      </div>
    </>
  );
}

export default App;