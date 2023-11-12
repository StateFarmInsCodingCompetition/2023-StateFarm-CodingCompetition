import './App.css'
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom'
import Header from "./static/Header";
import CRM from "./pages/CRM";
import GIS from "./pages/GIS";

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
            <Header/>
            <Routes>
                <Route exact path="/" element={<CRM/>}/>
                <Route exact path="/gis" element={<GIS/>}/>
            </Routes>
        </Router>
    );
}

export default App;