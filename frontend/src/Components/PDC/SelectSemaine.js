import React from 'react';

const SelectSemaine = ({ PDCsemaine, semaineSelected, setPDCsemaine, setsemaineSelected }) => {
    return (
        <div className='col-12 d-flex justify-content-end align-items-center'>
            <div className='col-8 d-flex justify-content-end align-items-center flex-row gap-3'>
                {PDCsemaine.length > 0 ? (
                    PDCsemaine.map((PDC) => (
                        <div
                            key={PDC.semaine}
                            className={'select-semaine px-3 py-1 ' + (semaineSelected === PDC.semaine ? 'active' : '')}
                            aria-label={`Select week ${PDC.semaine}`}
                            onClick={() => setsemaineSelected(PDC.semaine)}>
                            semaine : {PDC.semaine}
                        </div>
                    ))
                ) : (
                    <p>No weeks available.</p>
                )}
            </div>
        </div>
    );
};

export default SelectSemaine;
