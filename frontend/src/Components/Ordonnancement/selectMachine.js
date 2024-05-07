import React, { useEffect } from 'react';

const SelectMachine = ({ SelectedMachine, setSelectedMachine, AllMachine, setAllMachine }) => {

    const genereMachine = () => {
        let machine = [];
        for (let i = 1; i <= 6; i++) {
            machine.push({ machine: `Machine ${i}`, value: `Machine ${i}` });
        }
        return machine;
    }
    const initData = () => {
        setAllMachine(genereMachine());
        setSelectedMachine(genereMachine()[0]);
    }

    useEffect(() => {
        initData();
    }, [])

    const handleChange = (event) => {
        const findMachine = AllMachine.find(machine => machine.machine === event.target.value);
        setSelectedMachine(findMachine);
    }
    return (
        <div className='col-12 d-flex flex-row justify-content-end align-items-center'>

            <div className="form-group">
                <select className="form-select" id="machine" name="machine" onChange={handleChange} >
                    {AllMachine.length > 0 && AllMachine.map((machine, index) => {
                        return (
                            <option key={index} value={machine.machine}>{machine.machine}</option>
                        )
                    })}
                </select>
            </div>

        </div>
    );
};

export default SelectMachine;
