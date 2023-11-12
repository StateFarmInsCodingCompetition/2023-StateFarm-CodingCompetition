import {Button} from "@mui/material";
import {useNavigate} from "react-router-dom";

function Header() {
    let navigate = useNavigate()

    return (
        <div className="header">
            <div className="pill">
                <h1>SF Data Tool</h1>
            </div>

            <div className="pill">
                <Button onClick={() => navigate("/")}>Data View</Button>
                <Button onClick={() => navigate("/gis")}>Plot View</Button>
            </div>
        </div>

    )
}

export default Header;