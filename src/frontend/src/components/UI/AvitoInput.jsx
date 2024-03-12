import React from 'react'
import classes from './AvitoInput.module.css'

export default function AvitoInput(props) {
  return (
    <div className={ classes.hero }>
        <input { ...props } autoFocus></input>
    </div>
  )
}
