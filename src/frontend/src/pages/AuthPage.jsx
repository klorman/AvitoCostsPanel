import { useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'
import '../style/AuthPage.css'

export default function AuthPage() {
    return (
        <form>
            <label>
                Имя пользователя:
                <input
                type="text"
                />
            </label>
            <br />
            <label>
                Пароль:
                <input
                type="password"
                />
            </label>
            <br />
            <button type="submit">Войти</button>
        </form>
    )
}