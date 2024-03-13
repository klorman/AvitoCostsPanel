import React, { useMemo, useState } from 'react'
import classes from './TreeSelect.module.css'

const categories = {
	'Транспорт': ["Автомобили", "Мотоциклы и мототехника", "Грузовики и спецтехника", "Аренда спецтехники", "Водный транспорт", "Запчасти и аксессуары"],
	'Недвижимость': ["Купить жилье", "Снять посуточно", "Снять долгосрочно", "Коммерческая недвижимость", "Другие категории"],
	'Работа': ["Ищу работу", "Ищу сотрудника"],
	// добавить остальные
};

export default function TreeSelect(props) {
	const [listVisible, setListVisible] = useState(false)
	const handleKeyUp = (e) => {
		if (e.key === 'Escape') {
			setListVisible(false)
			document.removeEventListener('keyup', handleKeyUp)
		}
	}

	return (
		<div className={classes.content}>
			<button>
				<svg width="20" height="20" fill="none" xmlns="http://www.w3.org/2000/svg">
					<g clip-path="url(#a)" stroke="#fff" stroke-width="1.5">
						<path d="m15.625 13.125 2.5 2.5M0 4.375h5m-5 5h3.75m-3.75 5h5"></path>
						<circle cx="11.875" cy="9.375" r="4.875"></circle>
					</g>
				</svg>
				<div>
					<span>Все&nbsp;категории</span>
				</div>
			</button>
			{listVisible ?
				<div className={classes.list}>
					<ul>
						{categories.slice(0, Math.min(5, categories.length)).map((key, index) => (
							<li onClick={() => { setListVisible(!listVisible) }} key={index}></li>
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
