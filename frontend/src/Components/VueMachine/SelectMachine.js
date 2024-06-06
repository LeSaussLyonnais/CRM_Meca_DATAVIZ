import React, { useEffect } from 'react';
import '../../Styles/vuemachine.css'; // Assurez-vous que le chemin du fichier CSS est correct
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';

export default function SelectMachine({ SelectedMachine, setSelectedMachine, AllMachine, setAllMachine }) {
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
    }, []);

    const handleChange = (event) => {
        const findMachine = AllMachine.find(machine => machine.machine === event.target.value);
        setSelectedMachine(findMachine);
    }

    return (
        <div className='col-5 d-flex flex-row justify-content-end align-items-center'>
            <div className="form-group custom-select"> {/* Ajout de la classe custom-select */}
                <FormControl sx={{ m: 1, minWidth: 140 }}>
                    <InputLabel
                        id="demo-simple-select-autowidth-label"
                        sx={{
                            fontSize: '1rem',
                            fontFamily: 'Poppins',
                            fontWeight: 500,
                            fontStyle: 'normal',
                            '&.Mui-focused': {
                                color: '#4972B7', // Change la couleur du label lorsqu'il devient petit et se déplace vers le haut
                            },
                        }}
                    >
                        Machine
                    </InputLabel>
                    <Select
                        labelId="demo-simple-select-autowidth-label"
                        id="demo-simple-select-autowidth"
                        value={SelectedMachine.machine}
                        onChange={handleChange}
                        autoWidth
                        label="Machine"
                        sx={{
                            fontSize: '1rem',
                            fontFamily: 'Poppins',
                            fontWeight: 500,
                            fontStyle: 'normal',
                            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                                borderColor: '#4972B7', // Change la couleur de la bordure lorsqu'il est en focus
                            },
                        }}
                    >
                        {AllMachine.map((machine, index) => (
                            <MenuItem
                                key={index}
                                value={machine.value}
                                sx={{
                                    fontSize: '1rem',
                                    fontFamily: 'Poppins',
                                    fontWeight: 300,
                                    fontStyle: 'normal',
                                }}
                            >
                                {machine.machine}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </div>
        </div>
    );
}
