import React from 'react';

const SelectSemaine = ({ PDGsemaine, semaineSelected, setPDGsemaine, setsemaineSelected }) => {
    return (
        <div className='col-12 d-flex justify-content-end align-items-center'>
            <div className='col-8 d-flex justify-content-end align-items-center flex-row gap-3'>
                {PDGsemaine.length > 0 ? (
                    PDGsemaine.map((PDG) => (
                        <div
                            key={PDG.semaine}
                            className={'select-semaine px-3 py-1 ' + (semaineSelected === PDG.semaine ? 'active' : '')}
                            aria-label={`Select week ${PDG.semaine}`}
                            onClick={() => setsemaineSelected(PDG.semaine)}>
                            semaine : {PDG.semaine}
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
