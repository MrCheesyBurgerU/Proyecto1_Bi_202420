import { Navbar, Nav } from "react-bootstrap";
import { useLocation } from "react-router-dom";
import "./NavBar.css";

const NavBar = () => {
    // Hook para obtener la ruta actual
    const location = useLocation();

    return (
        <>
            <Navbar bg="light" expand="lg">
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="mx-auto nav">
                        <Nav.Link
                            href="/text"
                            className={location.pathname === "/text" ? "active" : ""}
                        >
                            Predicción por Texto
                        </Nav.Link>
                        <span className="separator">|</span>
                        <Nav.Link
                            href="/csv"
                            className={location.pathname === "/csv" ? "active" : ""}
                        >
                            Predicción por Archivo
                        </Nav.Link>
                        <span className="separator">|</span>
                        <Nav.Link
                            href="/words"
                            className={location.pathname === "/words" ? "active" : ""}
                        >
                            Palabras Relevantes por ODS
                        </Nav.Link>
                        <span className="separator">|</span>
                        <Nav.Link
                            href="/model"
                            className={location.pathname === "/model" ? "active" : ""}
                        >
                            Re-entrenar Modelo
                        </Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
            <br />
        </>
    );
};

export default NavBar;
