import React, { useMemo, useState } from 'react'
import classes from './Select.module.css'
import AvitoInput from './AvitoInput'

export default function Select(props) {
    const [filter, setFilter] = useState('')
    const [listVisible, setListVisible] = useState(false)
    const filteredList = useMemo(() => {
        if (props.list) {
            return props.list.filter(wrapper => wrapper.body.toLowerCase().startsWith(filter.toLowerCase()))
        }
    }, [props.list, filter])
    const handleKeyUp = (e) => {
        if (e.key === 'Escape') {
            setListVisible(false)
            document.removeEventListener('keyup', handleKeyUp)
        }
    }

    return (
        <div className={ classes.content }>
            { <props.label 
                onClick={() => {
                    if(!listVisible) {
                        document.addEventListener('keyup', handleKeyUp)
                    }
                    else {
                        document.removeEventListener('keyup', handleKeyUp)
                    }
                    setListVisible(!listVisible)
                }} 
                disabled={ props.disabled } /> }
            {listVisible?
            <div className={ classes.list }>
                <AvitoInput 
                placeholder={ filteredList.length? filteredList[0].body: '' } 
                className={ classes.avitoInput } 
                value={ filter } 
                onChange={ (e) => setFilter(e.target.value) } 
                />
                <ul>
                    { filteredList.slice(0, Math.min(5, filteredList.length)).map((wrapper, index) => (
                        <li onClick={ () => { props.onSelect(wrapper); setListVisible(!listVisible) } } key={index}><strong>{wrapper.body.slice(0, filter.length)}</strong>{ wrapper.body.slice(filter.length) }</li>
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
 