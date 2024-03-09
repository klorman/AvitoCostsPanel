import AuthPage from '../pages/AuthPage'
import MainPage from '../pages/MainPage'

export const loginRequiredRoutes = [
    {
        path: '/',
        component: (<MainPage />)
    }
]

export const loginFreeRoutes = [
    {
        path: '/auth',
        component: (<AuthPage />),
    }
]