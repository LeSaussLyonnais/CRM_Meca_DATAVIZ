import React, { useEffect, useState } from 'react';
import { MdArrowRight, MdOutlineArrowLeft } from "react-icons/md";

const MonthSelector = ({ SelectMois, setSelectMois }) => {

    let monthName = SelectMois.toLocaleString('fr-FR', { month: 'long' });
    monthName = monthName.charAt(0).toUpperCase() + monthName.slice(1);

    const handleMonthChange = (change) => {
        const newDate = new Date(SelectMois);
        if (change === "+") {
            newDate.setMonth(newDate.getMonth() + 1);
        } else if (change === "-") {
            newDate.setMonth(newDate.getMonth() - 1);
        }
        setSelectMois(newDate);
    };

    return (
        <div className="col-12 d-flex flex-row justify-content-center align-items-center px-4" >
            <MdOutlineArrowLeft className='Month_Icon' onClick={() => handleMonthChange("-")} />
            <p className='p-0 m-0'>
                {monthName}
            </p>
            <MdArrowRight className='Month_Icon' onClick={() => handleMonthChange("+")} />
        </div>
    );
};

export default MonthSelector;
