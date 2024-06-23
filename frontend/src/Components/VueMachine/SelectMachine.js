import React, { useState, useEffect, useContext, useRef } from 'react';
import '../../Styles/vuemachine.css'; // Assurez-vous que le chemin du fichier CSS est correct
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import { SiteContext } from '../ContexteSelectionSite';

export default function SelectMachine({ SelectedPoste, setSelectedPoste, PostesDisponibles, setPostesDisponibles }) {
    const { selectedSite, selectedWorkshop } = useContext(SiteContext);
    const isFetching = useRef(false);

    useEffect(() => {
        const fetchPostes = async () => {
            if (isFetching.current) return; // Évite les appels redondants
            isFetching.current = true;

            try {
                console.log(selectedWorkshop);
                const response = await fetch('http://192.168.0.117:8000/BlogApp/Ordo_getPoste', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        atelier: selectedWorkshop.Libelle_Atelier,
                    }),
                });
                const data = await response.json();

                setPostesDisponibles(data.Postes);
                setSelectedPoste(data.Postes[0]);
            } catch (error) {
                console.error('Error fetching postes:', error);
            } finally {
                isFetching.current = false;
            }
        };

        if (selectedSite && selectedWorkshop) {
            fetchPostes();
        }
    }, [selectedWorkshop, selectedSite, setPostesDisponibles, setSelectedPoste]);

    const handlePosteClick = (event) => {
        const findPoste = PostesDisponibles.find(poste => poste.COFRAIS === event.target.value);
        setSelectedPoste(findPoste);
    };

    return (
        <div className='col-5 d-flex flex-row justify-content-end align-items-center'>
            <div className="form-group custom-select">
                <FormControl sx={{ m: 1, minWidth: 140 }}>
                    <InputLabel
                        id="demo-simple-select-autowidth-label"
                        sx={{
                            fontSize: '1rem',
                            fontFamily: 'Poppins',
                            fontWeight: 500,
                            fontStyle: 'normal',
                            '&.Mui-focused': {
                                color: '#4972B7',
                            },
                        }}
                    >
                        Machine
                    </InputLabel>
                    <Select
                        labelId="demo-simple-select-autowidth-label"
                        id="demo-simple-select-autowidth"
                        value={SelectedPoste?.COFRAIS || ''}
                        onChange={handlePosteClick}
                        autoWidth
                        label="Machine"
                        sx={{
                            fontSize: '1rem',
                            fontFamily: 'Poppins',
                            fontWeight: 500,
                            fontStyle: 'normal',
                            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                                borderColor: '#4972B7',
                            },
                        }}
                    >
                        {PostesDisponibles && PostesDisponibles.map((poste, index) => (
                            <MenuItem
                                key={index}
                                value={poste.COFRAIS}
                                sx={{
                                    fontSize: '1rem',
                                    fontFamily: 'Poppins',
                                    fontWeight: 300,
                                    fontStyle: 'normal',
                                }}
                            >
                                {poste.COFRAIS}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </div>
        </div>
    );
}
