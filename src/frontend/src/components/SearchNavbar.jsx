import React from 'react'
import classes from './SearchNavbar.module.css'
import TreeNavbar from './TreeNavbar'
import Select from './UI/Select'

export default function SearchNavbar() {



    return (
        <div className={classes.hero}>
            <div className={classes.content}>
                <div className={classes.avitoLabel}>
                    <a 
                    href="/" 
                    title="Авито — сайт объявлений"
                    data-marker="search-form/logo"
                    marker="search-form/logo"
                    >
                        <svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="10.595" cy="5.225" r="3.325" fill="#965EEB"></circle>
                            <circle cx="22.245" cy="7.235" r="7.235" fill="#0AF"></circle>
                            <circle cx="8.9" cy="18.6" r="8.9" fill="#04E061"></circle>
                            <circle cx="24.325" cy="21.005" r="5.375" fill="#FF4053"></circle>
                        </svg>
                        <svg width="79" height="30" viewBox="0 0 79 30" xmlns="http://www.w3.org/2000/svg">
                            <path d="M11.36.62 2 25.06h5.03l1.92-5.1h9.94l1.93 5.1h4.99L16.5.62h-5.15Zm-.68 14.85 3.27-8.6 3.25 8.6h-6.52Zm21.14 3.29L27.76 7.89h-4.8l6.54 17.17h4.75L40.69 7.9h-4.8l-4.06 10.87Zm14.9-10.87h-4.57v17.17h4.56V7.9Zm-2.3-1.24a3.33 3.33 0 1 0 0-6.65 3.33 3.33 0 0 0 0 6.65Zm11.34-3.34H51.2v4.55h-2.67V12h2.67v7.3c0 4.13 2.28 5.92 5.49 5.92a7.86 7.86 0 0 0 3.15-.62v-4.26c-.54.2-1.11.3-1.7.31-1.39 0-2.4-.54-2.4-2.4V12h4.1V7.9h-4.1V3.31Zm13.7 4.27a8.9 8.9 0 0 0-8.23 5.49 8.9 8.9 0 0 0 0 6.8 8.9 8.9 0 0 0 4.8 4.83 8.9 8.9 0 0 0 3.41.68 8.9 8.9 0 0 0 6.24-15.16 8.9 8.9 0 0 0-6.23-2.64Zm0 13.24a4.33 4.33 0 0 1-4.26-5.17 4.33 4.33 0 0 1 7.85-1.57 4.33 4.33 0 0 1 .73 2.41 4.32 4.32 0 0 1-4.33 4.32v.01Z"></path>
                        </svg>
                    </a>
                </div>
                <TreeNavbar />
                <Select list={ ['Новосибирск', 'Омск', 'Казань', 'Куйбышев' ] } />
            </div>
        </div>
    )
}
