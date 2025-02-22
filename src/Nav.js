import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import './Navbar.css';

function CollapsibleExample() {
  return (
    <Navbar collapseOnSelect expand="lg" className="custom-navbar" sticky="top">
      <Container>
        <Navbar.Brand href="#home" className="brand-logo">
          PenTest Pilot
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="#features" className="nav-link-custom">Home</Nav.Link>
            <Nav.Link href="#pricing" className="nav-link-custom">Features</Nav.Link>
            <NavDropdown title="More" id="collapsible-nav-dropdown" className="nav-link-custom">
              <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
            </NavDropdown>
          </Nav>
          <Nav>
            <Nav.Link href="#deets" className="nav-link-custom">About </Nav.Link>
            <Nav.Link eventKey={2} href="#memes" className="nav-link-custom">
              Dank memes
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default CollapsibleExample;
