import React, { useEffect } from 'react';

const PDCMachine = ({ SelectedMachine, AllPDCData, setAllPDCData }) => {

  const generePDC = () => {
    //Génération de la liste de PDC
    let data = [];

    const MinValuePDC = 50;
    const MaxValuePDC = 150;
    for (let i = 0; i < 6; i++) {
      data.push({
        semaine: i + 1,
        pdc: Math.floor(Math.random() * (MaxValuePDC - MinValuePDC) + MinValuePDC),
      });
    }
    return data;
  };

  const setData = () => {
    setAllPDCData(generePDC());
  }

  useEffect(() => {
    setData();
  }, [])

  useEffect(() => {
    setData();
  }, [SelectedMachine])


  return (
    <div className='col-12 container-perso-content d-flex flex-column justify-content-center align-items-start'>
      <div className='col-12 d-flex flex-column justify-content-center align-items-start px-5'>
        <p className='Title_machine'>
          Plan de charge : {SelectedMachine.machine}
        </p>
        <p className='Subtitle_machine'>
          Liste prévisionnelle pour les 6 prochaines semaines
        </p>
        <hr className='col-12' />
      </div>

      <div className='col-12 d-flex flex-row justify-content-center align-items-start px-5 gap-3'>
        {AllPDCData.map((data, index) => {
          return (
            <div className='col d-flex flex-column justify-content-center align-items-center gap-1'>
              <div className='Text_Semaine_PDC'>
                S {data.semaine}
              </div>
              <div className='rond_PDC' style={data.pdc <= 100 ? { backgroundColor: '#379740' } : { backgroundColor: '#CE2626' }} />
              <p className='Value_Semaine_PDC' style={data.pdc <= 100 ? { color: '#379740' } : { color: '#CE2626' }}>
                {data.pdc}%
              </p>

            </div>
          )
        })}
      </div>

    </div>
  );
};

export default PDCMachine;
