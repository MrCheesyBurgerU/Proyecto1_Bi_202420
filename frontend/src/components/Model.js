import { Button, Form, Container } from "react-bootstrap";
import React, { useState } from "react";
import axios from "axios";

const Model = () => {
    const [f1, setF1] = useState(0);
    const [recall, setRecall] = useState(0);
    const [precision, setPrecision] = useState(0);
    const [file, setFile] = useState(null);
    const [isUploading, setIsUploading] = useState(false);

    // Función para obtener las métricas del modelo
    const fetchMetrics = async () => {
        try {
            const metrics = await axios.get(`http://127.0.0.1:8000/report`);
            const obj = metrics.data;
            setF1(obj.f1);
            setRecall(obj.recall);
            setPrecision(obj.precision);
        } catch (error) {
            console.error("Error fetching metrics:", error);
            alert("Failed to fetch metrics. Check the console for more details.");
        }
    };

    // Llamada inicial a la API para obtener métricas
    const handleInitialMetrics = () => {
        fetchMetrics();
    };

    // Manejo del cambio de archivo
    const handleFileChange = (e) => {
        setFile(e.target.files ? e.target.files[0] : null);
    };

    // Manejo del envío del archivo para reentrenar el modelo
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (file) {
            setIsUploading(true);
            const formData = new FormData();
            formData.append("file", file);

            try {
                await axios.post(
                    "http://127.0.0.1:8000/retrain",
                    formData,
                    {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        },
                    }
                );
                setIsUploading(false);

                // Llamada a la API para actualizar las métricas
                fetchMetrics();
            } catch (error) {
                console.error("Error uploading file:", error);
                setIsUploading(false);
                alert("Error en el reentrenamiento. Por favor, revisa la consola para más detalles.");
            }
        }
    };

    // Llamada para cargar las métricas iniciales cuando se carga el componente
    handleInitialMetrics();

    return (
        <Container style={{ maxWidth: "500px", margin: "0 auto", textAlign: "center" }}>
            <div>
                <h1 style={{ fontWeight: "bold" }}>Métricas del modelo</h1>
                <div style={{ display: "flex", justifyContent: "center", alignItems: "center", textAlign: 'center', verticalAlign: 'middle' }}>
                    <div>
                        <h5>Precisión: &nbsp;</h5>
                        <meter style={{ minWidth: '100px', minHeight: '30px' }} value={precision}></meter>
                        <h5>&nbsp;{precision.toFixed(4)}</h5>
                    </div>
                    &nbsp;&nbsp;&nbsp;
                    <div>
                        <h5>Recall: &nbsp;</h5>
                        <meter style={{ minWidth: '100px', minHeight: '30px' }} value={recall}></meter>
                        <h5>&nbsp;{recall.toFixed(4)}</h5>
                    </div>
                    &nbsp;&nbsp;&nbsp;
                    <div>
                        <h5>Puntaje F1: &nbsp;</h5>
                        <meter style={{ minWidth: '100px', minHeight: '30px' }} value={f1}></meter>
                        <h5>&nbsp;{f1.toFixed(4)}</h5>
                    </div>
                </div>
            </div>
            <div>
                <h1>&nbsp;&nbsp;</h1>
            </div>
            <h1 style={{ fontWeight: "bold" }}>Reentrenar modelo</h1>
            <h4>Cargar archivo CSV o XLSX</h4>
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formFile" className="mb-3">
                    <Form.Control type="file" onChange={handleFileChange} />
                </Form.Group>
                <Button
                    variant={isUploading ? "danger" : "success"}
                    type="submit"
                    disabled={!file || isUploading}
                >
                    {isUploading ? "Cargando..." : "Enviar"}
                </Button>
            </Form>
        </Container>
    );
};

export default Model;
