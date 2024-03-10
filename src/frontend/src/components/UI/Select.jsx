import React, { useMemo, useState } from 'react'
import classes from './Select.module.css'
import AvitoInput from './AvitoInput'

export default function Select(props) {
    const [filter, setFilter] = useState('')
    const [listVisible, setListVisible] = useState(false)

    const filteredList = useMemo(() => {
        return props.list.filter(line => line.toLowerCase().startsWith(filter.toLowerCase()))
    }, [props.list, filter])

    return (
        <div className={ classes.content }>
            <div className={ classes.label } onClick={ () => setListVisible(!listVisible) }>
                <div>
                    <svg  className={ classes.icon } width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="7.999" cy="6.8" stroke="#000" strokeWidth="1.2" r="1.8"></circle>
                        <path d="m8.002 14.998-.452.395a.6.6 0 0 0 .903 0l-.451-.395Zm-4.196-4.8-.466.378.014.017.452-.395Zm8.396 0 .451.396a.587.587 0 0 0 .014-.018l-.465-.378Zm-9-3.4a4.8 4.8 0 0 1 4.8-4.8v-1.2a6 6 0 0 0-6 6h1.2Zm4.8-4.8a4.8 4.8 0 0 1 4.8 4.8h1.2a6 6 0 0 0-6-6v1.2Zm.451 12.606-4.195-4.8-.904.79 4.196 4.8.903-.79Zm3.297-4.8-4.2 4.8.903.79 4.2-4.8-.903-.79Zm1.052-3.006a4.774 4.774 0 0 1-1.066 3.022l.931.756a5.974 5.974 0 0 0 1.335-3.778h-1.2ZM4.272 9.82a4.778 4.778 0 0 1-1.07-3.022h-1.2c0 1.432.501 2.747 1.338 3.778l.932-.756Z" fill="#000"></path>
                    </svg>
                </div>
                <span>
                    <span>
                        <span>
                            <span>
                                <span>Выберите локацию</span>
                            </span>
                        </span>
                    </span>
                </span>
            </div>
            {listVisible?
            <div className={ classes.list }>
                <AvitoInput 
                placeholder={ filteredList? filteredList[0]: '' } 
                className={ classes.avitoInput } 
                value={ filter } 
                onChange={ (e) => setFilter(e.target.value) } 
                />
                <ul>
                    { filteredList.slice(0, 3).map((line, index) => (
                        <li key={index}>{ line }</li>
                    ), ) }
                </ul>
            </div>
             :
            <div></div>
            }
        </div>
    )
}
 