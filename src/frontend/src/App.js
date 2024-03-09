import { BrowserRouter } from "react-router-dom";
import { AuthContext } from "./context/AuthContext";
import { Router } from "./components/Router";
import { useState } from "react";
import './style/App.css'
import acceptSettings from "./settings";

export default function App() {
  acceptSettings()
  const [isAuth, setIsAuth] = useState(false)
  return (
    <div className="App">
      <AuthContext.Provider
        value={{
          isAuth,
          setIsAuth
        }}
      >
        <BrowserRouter>
          <Router>
          </Router>
        </BrowserRouter>
      </AuthContext.Provider>
    </div>
  );
}
