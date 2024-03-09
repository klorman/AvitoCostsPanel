import { loginRequiredRoutes, loginFreeRoutes } from "../router"
import { Route, Routes, Navigate } from 'react-router-dom'
import { useContext } from "react" 
import { AuthContext } from "../context/AuthContext"

export const Router = () => {
    const { isAuth, setIsAuth } = useContext(AuthContext)
    
    return (
        isAuth?
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
            <Route 
                    key='navigate'
                    element={<Navigate to='/auth'/>}
                    path='*'
            /> 
        </Routes>
    )
        
    
}
