import { BrowserRouter } from "react-router-dom";
import { AuthContext } from "./context/AuthContext";
import { Router } from "./components/Router";
import { useState } from "react";

export default function App() {
  const [authData, setAuthData] = useState({ isAuth: false, token: '' })

  return (
    <div className="App">
      <AuthContext.Provider
        value={{
          authData,
          setAuthData
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
