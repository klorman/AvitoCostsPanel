import { loginRequiredRoutes, loginFreeRoutes } from "../router"
import { Route, Routes } from 'react-router-dom'
import { useContext } from "react" 
import { AuthContext } from "../context/AuthContext"

export const Router = () => {
    const { authData } = useContext(AuthContext)
    console.log(loginFreeRoutes)

    return (
        authData.isAuth?
        <Routes>
            { loginRequiredRoutes.map((route) =>  
                <Route 
                    key={route.path}
                    element={route.component}
                    path={route.path}
                /> 
            )
            }
        </Routes>
        :
        <Routes>
            { loginFreeRoutes.map((route) =>  
                <Route 
                    key={route.path}
                    element={route.component}
                    path={route.path}
                /> 
            )
            }
        </Routes>
    )
        
    
}
