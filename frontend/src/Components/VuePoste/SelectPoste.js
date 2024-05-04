import React, { useEffect } from 'react';

const SelectPoste = ({ SelectedPoste, setSelectedPoste, AllPoste, setAllPoste }) => {

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
    }, [])

    const handleChange = (event) => {
        const findPoste = AllPoste.find(poste => poste.poste === event.target.value);
        setSelectedPoste(findPoste);
    }
    return (
        <div className='col-5 d-flex flex-row justify-content-end align-items-center'>

            <div className="form-group">
                <select className="form-perso-select" id="poste" name="poste" onChange={handleChange} >
                    {AllPoste.length > 0 && AllPoste.map((poste, index) => {
                        return (
                            <option key={index} value={poste.poste}>{poste.poste}</option>
                        )
                    })}
                </select>
            </div>

        </div>
    );
};

export default SelectPoste;
