import { apiLogin, apiIsLoggedIn } from '../../api.js';
import { Form, Button } from 'react-bootstrap';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LoginForm(props) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const doLogin = (event) => {  //do login, ask api to login, then ask data for user
        event.preventDefault();
        apiLogin(username, password).then((res) => {
            if (res) {
                apiIsLoggedIn().then((res) => {
                    props.setLoggedIn(true);
                    props.setUserID(res["ID"])
                    props.showSuccess("Succesfully logged in")
                    navigate("/");
                })
            } else {
                props.showError("Username or password invalid");
            }
        })
    }

    return (
        <Form onSubmit={doLogin} className="col-12 col-md-8 offset-md-2 col-lg-6 offset-lg-3 my-5">
            <Form.Group>
                <Form.Label>Username:</Form.Label>
                <Form.Control type="text" placeholder="Username" value={username} required={true} onChange={(event) => setUsername(event.target.value)} />
            </Form.Group>
            <Form.Group>
                <Form.Label>Password:</Form.Label>
                <Form.Control type="password" placeholder="Password" value={password} required={true} onChange={(event) => setPassword(event.target.value)} />
            </Form.Group>
            <Button className='mx-2 mt-2' variant="danger" onClick={() => navigate("/")}>
                Cancel
            </Button>
            <Button className='mx-2 mt-2' variant="success" type="submit">
                Submit
            </Button>
        </Form>
    );
}


export default LoginForm;