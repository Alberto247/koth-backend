import { NavItem, Navbar, NavLink, Nav, Container} from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import {apiLogout} from '../../api.js'



function Topbar(props) {
    const navigate = useNavigate();

    const buttonText = props.loggedIn ? "Logout" : "Login";

    const logout = async ()=>{  //logout on click
        await apiLogout();
        props.setLoggedIn(false);
        props.setUserID(-1);
        navigate("/");
    }

    return (
        <Navbar className='px-5' bg="success" expand="lg" variant="dark">
            <Container fluid>
                <div className='d-flex col-4' onClick={() => navigate('/')}>
                    <Navbar.Brand href="/"><h1>Koth frontend</h1></Navbar.Brand>
                </div>
                {/* <div className="text-white d-flex col-4"><Navbar.Brand>{props.loggedIn?"Welcome "+props.loggedIn.username:""}</Navbar.Brand></div> */}
                <Nav>
                <NavItem>
                    <NavLink  eventKey="/" onClick={() => {props.loggedIn ? logout() : navigate("/login")}}><h3>{buttonText}</h3></NavLink>
                </NavItem>
                </Nav>
            </Container>
        </Navbar>
    );
}

export default Topbar;