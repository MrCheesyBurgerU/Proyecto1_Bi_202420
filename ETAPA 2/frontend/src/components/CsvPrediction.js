import React from "react";
import axios from "axios";
import { useState } from "react";
import { Button, Form, Container } from "react-bootstrap";

const CsvPrediction = () => {
    const [file, setFile] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [downloadUrl, setDownloadUrl] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files ? e.target.files[0] : null);
        setDownloadUrl(null);
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (file) {
            setIsUploading(true);
            const formData = new FormData();
            formData.append("file", file);

            try {
                const response = await axios.post(
                    "http://127.0.0.1:8000/predict_file",
                    formData,
                    {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        },
                        responseType: "blob",
                    }
                );
                
                const csvBlob = new Blob([response.data], { type: "text/csv" });
                const url = window.URL.createObjectURL(csvBlob);
                
                setDownloadUrl(url);
                setIsUploading(false);
            } catch (error) {
                console.error("Error uploading file: ", error);
                setIsUploading(false);
            }
        }
    };

    return (
        <Container style={{ maxWidth: "500px", margin: "0 auto", textAlign: "center" }}>
            <h1 style={{ fontWeight: "bold" }}>Predicción por Archivo</h1>
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

            {/* Mostrar la sección de descarga solo si downloadUrl no es null */}
            {downloadUrl && (
                <>
                    <h4 className="mt-4">Predicciones Completadas</h4>
                    <a
                        href={downloadUrl}
                        download={`predictions_${file?.name}`}
                        className="btn btn-success mt-3"
                    >
                        Descargar
                    </a>
                </>
            )}
        </Container>
    );
};

export default CsvPrediction;
