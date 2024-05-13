import React, { useEffect, useState } from 'react';
import CroixSecuriteComponent from './CroixSecuriteComponent';
import MonthSelector from './MonthSelector';

const CroixSecurite = () => {
    const [AccidentDay, setAccidentDay] = useState([]);
    const [SelectMois, setSelectMois] = useState(new Date());

    return (
        <div
            className="col-12 container-perso-content d-flex flex-column justify-content-center align-items-center px-4 py-3"
        >
            <div className='col-12 d-flex flex-column justify-content-between align-items-center'>
                <div className='col-12 d-flex flex-row justify-content-between align-items-center'>
                    <h3 className='Title_global'>Croix de sécurité du site</h3>
                </div>
                <hr className='col-12' />
            </div>
            <div className='col-12 d-flex flex-column justify-content-around align-items-center'>
                <MonthSelector SelectMois={SelectMois} setSelectMois={setSelectMois}/>
                <CroixSecuriteComponent AccidentDay={AccidentDay} setAccidentDay={setAccidentDay} SelectMois={SelectMois}/>
            </div>
        </div>
    );
};

export default CroixSecurite;
