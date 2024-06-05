import React, { useEffect, useState } from 'react';

const SelectSemaine = ({ PDCsemaine, semaineSelected, setPDCsemaine, setsemaineSelected }) => {

    const getWeekNumber = (date) => {
        const firstJan = new Date(date.getFullYear(), 0, 1);
        const pastDaysOfYear = (date - firstJan) / 86400000;
        return Math.ceil((pastDaysOfYear + firstJan.getDay() + 1) / 7);
    };

    // Obtenir la date actuelle
    const currentDate = new Date();

    // Obtenir le numéro de la semaine en cours
    // const currentWeekNumber = 12;
    const currentWeekNumber = getWeekNumber(currentDate);
    useEffect(() => {
        setsemaineSelected(currentWeekNumber);
    },[])
    
    // Générer un tableau de semaines
    const weeks = Array.from({ length: 6 }, (_, i) => currentWeekNumber + i);

    return (
        <div className='col-12 d-flex justify-content-end align-items-center'>
            <div className='col-8 d-flex justify-content-end align-items-center flex-row gap-3'>
                {weeks.map((weekNumber, i) => (
                    <div
                        key={weekNumber}
                        className={'select-semaine px-3 py-1 ' + (semaineSelected === weekNumber ? 'active' : '')}
                        aria-label={`Select week ${weekNumber}`}
                        onClick={() => setsemaineSelected(weekNumber)}
                    >
                        Semaine : {weekNumber}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SelectSemaine;
