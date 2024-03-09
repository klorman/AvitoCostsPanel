import { useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'

export default function AuthPage() {
    const navigate = useNavigate()
    const { authData, setAuthData } = useContext(AuthContext)

    return (
        <div>Hello world from auth!</div>
    )
}