import React, { useMemo, useState } from 'react'
import classes from './Select.module.css'
import AvitoInput from './AvitoInput'

export default function Select(props) {
    const [filter, setFilter] = useState('')
    const [listVisible, setListVisible] = useState(false)
    const filteredList = useMemo(() => {
        if (props.list) {
            return props.list.filter(line => line.toLowerCase().startsWith(filter.toLowerCase()))
        }
    }, [props.list, filter])

    return (
        <div className={ classes.content }>
            { <props.label onClick={ () => setListVisible(!listVisible) } disabled={ props.disabled } /> }
            {listVisible?
            <div className={ classes.list }>
                <AvitoInput 
                placeholder={ filteredList? filteredList[0]: '' } 
                className={ classes.avitoInput } 
                value={ filter } 
                onChange={ (e) => setFilter(e.target.value) } 
                />
                <ul>
                    { filteredList.slice(0, Math.min(5, filteredList.length)).map((line, index) => (
                        <li onClick={ () => { props.onSelect(index); setListVisible(!listVisible) } } key={index}>{ line }</li>
                    )) 
                    }
                </ul>
            </div>
             :
            <div></div>
            }
        </div>
    )
}
 