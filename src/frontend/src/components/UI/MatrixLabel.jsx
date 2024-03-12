import React from 'react'
import classes from './Select.module.css'

export default function MatrixLabel(props) {
    return (
        <div className={ classes.label } onClick={ props.onClick }>
            <span>Матрица</span>
        </div>
    )
}
 