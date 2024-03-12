import SearchNavbar from "../components/SearchNavbar"
import classes from "./MainPage.module.css"

export default function MainPage() {
    return (
       
        <div className={ classes.content }> 
            <SearchNavbar />
        </div>
    )
}