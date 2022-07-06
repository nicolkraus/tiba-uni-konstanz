import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Navbar, Nav } from "react-bootstrap";
import Generate from "../pages/Generate";
import Compare from "../pages/Compare";
import About from "../pages/About";

class BootstrapNavbar extends React.Component {
  render() {
    return (
      <div>
        <div className="row">
          <div className="col-md-12">
            <Router>
              <Navbar bg="dark" variant="dark" expand="lg" sticky="top">
                <Navbar.Brand href="#home">
                  <div className="padded-sm">
                    T.I.B.A. - The Interactive Behavior Analyzer
                  </div>
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                  <Nav className="mr-auto">
                    <div className="padded-sm">
                      <Nav.Link href="/">Generate</Nav.Link>
                    </div>
                    <div className="padded-sm">
                      <Nav.Link href="/compare">Compare</Nav.Link>
                    </div>
                    <div className="padded-sm">
                      <Nav.Link href="/about">About</Nav.Link>
                    </div>
                  </Nav>
                </Navbar.Collapse>
              </Navbar>
              <br />
              <Routes>
                <Route path="/" element={<Generate />} />
                <Route path="/compare" element={<Compare />} />
                <Route path="/about" element={<About />} />
              </Routes>
            </Router>
          </div>
        </div>
      </div>
    );
  }
}
export default BootstrapNavbar;
