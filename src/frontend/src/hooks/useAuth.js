import globalEnv from '../env'
import axios from 'axios'

export const useAuth = (authContext) => {

    const login = async (username, password) => {
        const response = await axios.post(globalEnv.authEndpoint, {
                username,
                password,
            }).catch(() => {
            authContext.isAuth = false
            // stub for undefined case
        })

        if (response.status == 200) {
            authContext.isAuth = true
            // and other...
        }
    };

    const checkAuthState = async () => {
        const response = await axios.get(globalEnv.authEndpoint
            ).catch(() => {
            authContext.isAuth = false
            // stub for undefined case
        })
    }

    return {
        login, checkAuthState
    }
}