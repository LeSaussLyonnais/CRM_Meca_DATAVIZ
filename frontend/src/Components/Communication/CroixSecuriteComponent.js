import React, { useEffect, useState } from 'react';
import { v4 as uuidv4 } from 'uuid'; // Importez uuidv4 pour générer des identifiants uniques

const CroixSecuriteComponent = ({ AccidentDay, setAccidentDay, SelectMois }) => {

    const currentDate = new Date();

    const [nbJour, setnbJour] = useState(null);
    const [ListHorizontalDay, setListHorizontalDay] = useState([]);
    const [ListVerticalHighDay, setListVerticalHighDay] = useState([]);
    const [ListVerticalLowDay, setListVerticalLowDay] = useState([]);
    const [ListDayAccident, setListDayAccident] = useState([]);

    const TailleCroix = 12;

    const getDaysInMonth = (date) => {
        const year = date.getFullYear();
        const month = date.getMonth() + 1; // Les mois sont indexés à partir de 0, donc on ajoute 1
        return new Date(year, month, 0).getDate();
    };

    const SortDay = () => {
        let listhori = [];
        let listvertiHigh = [];
        let listvertiLow = [];
        for (let i = 1; i <= 33; i++) {
            if (i <= 6) {
                listvertiHigh.push(i);
            } else if (i > 6 && i <= 27) {
                listhori.push(i);
            } else if (i > 27 && i <= getDaysInMonth(SelectMois)) {
                listvertiLow.push(i);
            } else {
                listvertiLow.push('');
            }
        }
        return [listhori, listvertiHigh, listvertiLow];
    };

    const genereAccident = () => {
        const currentDate = new Date(SelectMois);
        const currentYear = currentDate.getFullYear();
        const currentMonth = currentDate.getMonth();
        const LastMonthDay = new Date(currentYear, currentMonth + 1, 0);
        let currentDay = null;
        if (currentMonth === new Date().getMonth() && currentYear === new Date().getFullYear()){
            currentDay = currentDate.getDate();
        }
        else {
            currentDay = LastMonthDay.getDate();
        }
        const minAccident = 1;
        const List_accident = ['Tomber de + de 1.5m', "chute d'un objet de 200kg", "doigt cassé"]
        const randomAccident = Math.floor(Math.random() * (currentDay - minAccident + 1)) + minAccident;

        const ListReturn = Array.from({ length: randomAccident }, (_, index) => ({
            id: uuidv4(),
            accident: true,
            date: new Date(currentYear, currentMonth, Math.floor(Math.random() * (currentDay - 1)) + 1),
            description: List_accident[Math.floor(Math.random() * List_accident.length)]
        }));
        return ListReturn;
    };

    const initData = () => {
        const accidents = genereAccident();
        setAccidentDay(accidents);

    };

    const setData = () => {
        const dayAccidents = AccidentDay.map((accident) => (new Date(accident.date).getDate()));
        setListDayAccident(dayAccidents);
        const daysInMonth = getDaysInMonth(SelectMois);
        setnbJour(daysInMonth);
        const [horizontalDays, verticalHighDays, verticalLowDays] = SortDay();
        setListHorizontalDay(horizontalDays);
        setListVerticalHighDay(verticalHighDays);
        setListVerticalLowDay(verticalLowDays);
    }

    useEffect(() => {
        initData();
        setData();
    }, []);
    useEffect(() => {
        initData();
    }, [SelectMois]);

    useEffect(() => {
        setData();
    }, [AccidentDay]);


    return (
        <div className='d-flex justify-content-center align-items-center flex-column p-lg-4 p-1'>
            <div className="croix" style={{ width: TailleCroix + 'vw', height: TailleCroix + 'vw' }}>
                <div className="ligne-vertical d-flex flex-column justify-content-between" style={{ width: (TailleCroix / 7) * 3 + 'vw' }}>
                    <div className='d-flex flex-wrap'>
                        {nbJour &&
                            ListVerticalHighDay.map((day, index) => (
                                <div
                                    className={`calendar_cell ${((SelectMois.getMonth()<currentDate.getMonth() || SelectMois.getFullYear()<currentDate.getFullYear()) || (SelectMois.getMonth()===currentDate.getMonth() && SelectMois.getFullYear()===currentDate.getFullYear() && day <= currentDate.getDate()) ) && ListDayAccident.includes(day) ? 'Accident_day' : (((SelectMois.getMonth()<currentDate.getMonth() || SelectMois.getFullYear()<currentDate.getFullYear()) || (SelectMois.getMonth()===currentDate.getMonth() && SelectMois.getFullYear()===currentDate.getFullYear() && day <= currentDate.getDate()) ) && day !== '') ? 'noAccident_day' : 'futur_day'}`}
                                    key={index}
                                    style={{ width: (TailleCroix / 7) + 'vw', height: (TailleCroix / 7) + 'vw', fontSize: (TailleCroix / 14) + 'rem' }}
                                >
                                    {day}
                                </div>
                            ))
                        }
                    </div>
                    <div className='d-flex flex-wrap'>
                        {nbJour &&
                            ListVerticalLowDay.map((day, index) => (
                                <div
                                    className={`calendar_cell ${((SelectMois.getMonth()<currentDate.getMonth() || SelectMois.getFullYear()<currentDate.getFullYear()) || (SelectMois.getMonth()===currentDate.getMonth() && SelectMois.getFullYear()===currentDate.getFullYear() && day <= currentDate.getDate()) ) && ListDayAccident.includes(day) ? 'Accident_day' : (((SelectMois.getMonth()<currentDate.getMonth() || SelectMois.getFullYear()<currentDate.getFullYear()) || (SelectMois.getMonth()===currentDate.getMonth() && SelectMois.getFullYear()===currentDate.getFullYear() && day <= currentDate.getDate()) ) && day !== '') ? 'noAccident_day' : 'futur_day'}`}
                                    key={index}
                                    style={{ width: (TailleCroix / 7) + 'vw', height: (TailleCroix / 7) + 'vw', fontSize: (TailleCroix / 14) + 'rem'}}
                                >
                                    {day}
                                </div>
                            ))
                        }
                    </div>
                    {/* <Calendar onChange={onChange} value={date} /> */}
                </div>
                <div className="ligne-horizontal d-flex flex-wrap" style={{ height: (TailleCroix / 7) * 3 + 'vw' }}>
                    {nbJour &&
                        ListHorizontalDay.map((day, index) => (
                            <div
                                className={`calendar_cell 
                                ${((SelectMois.getMonth()<currentDate.getMonth() || SelectMois.getFullYear()<currentDate.getFullYear()) || (SelectMois.getMonth()===currentDate.getMonth() && SelectMois.getFullYear()===currentDate.getFullYear() && day <= currentDate.getDate()) ) && ListDayAccident.includes(day) ? 'Accident_day' :((SelectMois.getMonth()<currentDate.getMonth() || SelectMois.getFullYear()<currentDate.getFullYear()) || (SelectMois.getMonth()===currentDate.getMonth() && SelectMois.getFullYear()===currentDate.getFullYear() && day <= currentDate.getDate())) ? 'noAccident_day' : 'futur_day'}`}
                                key={index}
                                style={{ width: (TailleCroix / 7) + 'vw', height: (TailleCroix / 7) + 'vw', fontSize: (TailleCroix / 14) + 'rem'}}
                            >
                                {day}
                            </div>
                        ))
                    }
                    {/* <Calendar onChange={onChange} value={date} /> */}
                </div>
            </div>
            <div className='col-12 d-flex justify-content-between align-items-center flex-lg-row flex-column gap-4 mt-3'>
                <div className='col-lg-6 col-12 d-flex justify-content-center align-items-center flex-row gap-2'>
                    <div className='legend noAccident_day' />
                    <p className='legend-text'>Jour sans incident</p>
                </div>
                <div className='col-lg-6 col-12 d-flex justify-content-end align-items-center flex-row gap-2'>
                    <div className='legend Accident_day' />
                    <p className='legend-text'>Jour avec incident</p>
                </div>
            </div>
        </div>
    );
};

export default CroixSecuriteComponent;
