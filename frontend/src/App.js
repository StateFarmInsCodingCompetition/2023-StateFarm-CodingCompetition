import './App.css'
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom'
import Cookies from "universal-cookie";
import Header from "./static/Header";

export const cookies = new Cookies();

export function getCurrentUser() {
    return cookies.get("user");
}

export function setCurrentUser(user) {
    cookies.set("user", user); // Will jsonify the user object
}

export function removeCurrentUser() {
    cookies.remove("user");
}

export function validateUser(currentUser, navigate) {
    if (currentUser === undefined) {
        console.log("User is not logged in");
        navigate("/")
        return false;
    }
    return true;
}

function App() {
    return (
        <Router>
            <Routes>
                <Route exact path="/" element={<Header/>}/>
            </Routes>
        </Router>
    );
}

export default App;