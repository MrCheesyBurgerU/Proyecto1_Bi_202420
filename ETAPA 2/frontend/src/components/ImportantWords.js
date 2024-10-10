import ReactWordcloud from "react-wordcloud";
import "tippy.js/animations/scale.css";
import "tippy.js/dist/tippy.css";
import { useState, useEffect } from "react";
import React from "react";
import axios from "axios";

const ImportantWords = () => {
    const [words, setWords] = useState([{ text: " ", value: 10 }]);
    const [selectedOds, setSelectedOds] = useState(3); // Por defecto ODS 3

    const a = [10, 60];
    const options = {
        fontSizes: a,
        colors: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
        enableTooltip: true,
        deterministic: false,
        fontFamily: "Helvetica",
        fontStyle: "normal",
        fontWeight: "bold",
        padding: 1,
        rotations: 0,
        transitionDuration: 1000
    };

    const fetchWords = async (classId) => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/words_relevance/${classId}`);
            setWords(response.data);
        } catch (error) {
            console.error("Error fetching prediction:", error);
            alert("Failed to fetch words. Check the console for more details.");
        }
    };

    const handleClick = (classId) => {
        setSelectedOds(classId);
        fetchWords(classId);
    };

    // Obtener las palabras del ODS 3 al cargar el componente
    useEffect(() => {
        fetchWords(3);
    }, []);

    return (
        <div>
            <div>
                <h1 style={{ fontWeight: "bold", justifyContent: "center", display: "flex" }}>
                    Palabras más relevantes por ODS
                </h1>
                <div style={{ display: "flex", justifyContent: "center" }}>
                    <h3
                        id="label3"
                        onClick={() => handleClick(3)}
                        style={{ fontWeight: selectedOds === 3 ? "bold" : "normal", cursor: "pointer" }}
                    >
                        ODS 3&nbsp;&nbsp;
                    </h3>
                    <h3
                        id="label4"
                        onClick={() => handleClick(4)}
                        style={{ fontWeight: selectedOds === 4 ? "bold" : "normal", cursor: "pointer" }}
                    >
                        ODS 4&nbsp;&nbsp;
                    </h3>
                    <h3
                        id="label5"
                        onClick={() => handleClick(5)}
                        style={{ fontWeight: selectedOds === 5 ? "bold" : "normal", cursor: "pointer" }}
                    >
                        ODS 5
                    </h3>
                </div>
                <div id="cloud">
                    <ReactWordcloud options={options} words={words} />
                </div>
            </div>
        </div>
    );
};

export default ImportantWords;
