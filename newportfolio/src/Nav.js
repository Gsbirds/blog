import { NavLink } from "react-router-dom";

function Nav(props) {

    return (
        <nav className="navbar navbar-expand-lg">
            <NavLink style={{color: props.text}} className="navbar-brand mx-2" to="/">
             The Uninspired Philosoraptor
            </NavLink>
            <button
                className="navbar-toggler"
                type="button"
                data-toggle="collapse"
                data-target="#navbarNav"
                aria-controls="navbarNav"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
                <ul className="navbar-nav">
                    <li className="nav-item">
                        <NavLink style={{color: props.text}} className="nav-link" aria-current="page" to="/">
                            Home
                        </NavLink>
                    </li>
            <li> <NavLink style={{color: props.text}} className="nav-link" aria-current="page" to="/Wheel">
                            Blog
                        </NavLink></li>
                        <li> <NavLink style={{color: props.text}} className="nav-link" aria-current="page" to="/Wheel">
                            About this bitch
                        </NavLink></li>
                    
                </ul>
            </div>
        </nav>
    );
}
export default Nav;

