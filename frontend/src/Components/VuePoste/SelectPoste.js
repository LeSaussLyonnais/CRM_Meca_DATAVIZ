import React, { useEffect } from 'react';
import '../../Styles/vueposte.css'; // Assurez-vous que le chemin du fichier CSS est correct
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';

export default function SelectPoste({ SelectedPoste, setSelectedPoste, AllPoste, setAllPoste }) {
    const generePoste = () => {
        let poste = [];
        for (let i = 1; i <= 6; i++) {
            poste.push({ poste: `Poste ${i}`, value: `Poste ${i}` });
        }
        return poste;
    }

    const initData = () => {
        setAllPoste(generePoste());
        setSelectedPoste(generePoste()[0]);
    }

    useEffect(() => {
        initData();
    }, []);

    const handleChange = (event) => {
        const findPoste = AllPoste.find(poste => poste.poste === event.target.value);
        setSelectedPoste(findPoste);
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
                        Poste
                    </InputLabel>
                    <Select
                        labelId="demo-simple-select-autowidth-label"
                        id="demo-simple-select-autowidth"
                        value={SelectedPoste.poste}
                        onChange={handleChange}
                        autoWidth
                        label="Poste"
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
                        {AllPoste.map((poste, index) => (
                            <MenuItem
                                key={index}
                                value={poste.value}
                                sx={{
                                    fontSize: '1rem',
                                    fontFamily: 'Poppins',
                                    fontWeight: 300,
                                    fontStyle: 'normal',
                                }}
                            >
                                {poste.poste}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </div>
        </div>
    );
}
