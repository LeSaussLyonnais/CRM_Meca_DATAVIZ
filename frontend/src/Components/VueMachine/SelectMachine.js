import React, { useState, useEffect, useContext } from 'react';
import '../../Styles/vuemachine.css'; // Assurez-vous que le chemin du fichier CSS est correct
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import { SiteContext } from '../ContexteSelectionSite';

// export default function SelectMachine({ SelectedMachine, setSelectedMachine, AllMachine, setAllMachine }) {
    // const genereMachine = () => {
    //     let machine = [];
    //     for (let i = 1; i <= 6; i++) {
    //         machine.push({ machine: `Machine ${i}`, value: `Machine ${i}` });
    //     }
    //     return machine;
    // }

    // const initData = () => {
    //     setAllMachine(genereMachine());
    //     setSelectedMachine(genereMachine()[0]);
    // }

    // useEffect(() => {
    //     initData();
    // }, []);

    // const handleChange = (event) => {
    //     const findMachine = AllMachine.find(machine => machine.machine === event.target.value);
    //     setSelectedMachine(findMachine);
    // }

    //////////////////////////////////////////////////////
    //////////////////////////////////////////////////////
export default function SelectMachine({ SelectedPoste, setSelectedPoste, PostesDisponibles, setPostesDisponibles}) {
    const { selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop } = useContext(SiteContext);
    // const [PostesDisponibles, setPostesDisponibles] = useState([]);

    const initPoste = () => {
        if (PostesDisponibles && PostesDisponibles.length > 0) {
            setSelectedPoste(PostesDisponibles[0]);
        }
    }

    useEffect(() => {
        if (selectedSite && selectedWorkshop) {
            fetchPostes();
            // initPoste();
        }
    }, [selectedSite, selectedWorkshop]);

    useEffect(() => {
        initPoste();
    }, [PostesDisponibles]);

    const handlePosteClick = (event) => {
        const findPoste = PostesDisponibles.find(poste => poste.COFRAIS === event.target.value);
        setSelectedPoste(findPoste);
    }

    const fetchPostes = async () => {
        try {
          const response = await fetch('http://127.0.0.1:8000/BlogApp/Ordo_getPoste', {
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

        }
        catch (error) {
          console.error('Error fetching postes:', error);
        }
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
                                borderColor: '#4972B7', // Change la couleur de la bordure lorsqu'il est en focus
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
    //////////////////////////////////////////////////////
    //////////////////////////////////////////////////////

//     return (
//         <div className='col-5 d-flex flex-row justify-content-end align-items-center'>
//             <div className="form-group custom-select"> {/* Ajout de la classe custom-select */}
//                 <FormControl sx={{ m: 1, minWidth: 140 }}>
//                     <InputLabel
//                         id="demo-simple-select-autowidth-label"
//                         sx={{
//                             fontSize: '1rem',
//                             fontFamily: 'Poppins',
//                             fontWeight: 500,
//                             fontStyle: 'normal',
//                             '&.Mui-focused': {
//                                 color: '#4972B7', // Change la couleur du label lorsqu'il devient petit et se déplace vers le haut
//                             },
//                         }}
//                     >
//                         Machine
//                     </InputLabel>
//                     <Select
//                         labelId="demo-simple-select-autowidth-label"
//                         id="demo-simple-select-autowidth"
//                         value={SelectedMachine.machine}
//                         onChange={handleChange}
//                         autoWidth
//                         label="Machine"
//                         sx={{
//                             fontSize: '1rem',
//                             fontFamily: 'Poppins',
//                             fontWeight: 500,
//                             fontStyle: 'normal',
//                             '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
//                                 borderColor: '#4972B7', // Change la couleur de la bordure lorsqu'il est en focus
//                             },
//                         }}
//                     >
//                         {AllMachine.map((machine, index) => (
//                             <MenuItem
//                                 key={index}
//                                 value={machine.value}
//                                 sx={{
//                                     fontSize: '1rem',
//                                     fontFamily: 'Poppins',
//                                     fontWeight: 300,
//                                     fontStyle: 'normal',
//                                 }}
//                             >
//                                 {machine.machine}
//                             </MenuItem>
//                         ))}
//                     </Select>
//                 </FormControl>
//             </div>
//         </div>
//     );
// }
