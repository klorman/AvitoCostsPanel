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