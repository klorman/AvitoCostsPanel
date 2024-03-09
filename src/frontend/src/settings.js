import axios from 'axios'

export default function acceptSettings() {
    axios.defaults.withCredentials = true // Allow to working with cookies.
}