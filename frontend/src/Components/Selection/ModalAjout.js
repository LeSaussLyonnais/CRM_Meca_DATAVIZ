//Creer moi un composant vide
import React, { useState } from "react";
import { FaCheck } from "react-icons/fa";


const ModalAjout = ({ show , setshow, site, AllDispoPoste }) => {


    const [selectedItems, setselectedItems] = useState([]);
    const [NomAtelier, setNomAtelier] = useState("");
    const [items, setItems] = useState([
        'CX-2',
        'CX-3',
        'CX-4',
        'CX-5',
        'CX-6',
        'CX-7',
        'CX-8',
        'CX-9',
        'CX-10',
        'CRM-1',
        'CRM-2',
        'CRM-3',
        'CRM-4',
        'CRM-5',
        'CRM-6',
        'AFF-55',
        'AFF-56',
        'AFF-57',
        'AFF-58',
        'AFF-59',

    ]);

    const toggleSelectItem = (item) => {
        if (selectedItems.includes(item)) {
            setselectedItems(selectedItems.filter(i => i !== item));
        } else {
            setselectedItems([...selectedItems, item]);
        }
    }

    const SaveAtelier = () => {
        // Code pour enregistrer l'atelier
        const confirm_Ajout = window.confirm("Voulez-vous enregistrer l'atelier ?");
        if (confirm_Ajout) {
            const New_Atelier={
                site,
                NomAtelier:NomAtelier,
                Machines:selectedItems
            }
    
            console.log('Atelier enregistré:', New_Atelier);
            handleClose();
        }
    }
    const handleClose = () => {
        setselectedItems([]);
        setNomAtelier("");
        setshow(false);
    }

    return (
        <>
            <div className={`bg-modal-perso modal ${show ? 'show' : ''}`} style={{ display: show ? 'block' : 'none' }} onClick={() => handleClose(false)}>
                <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title">Ajout atelier</h5>
                            <button type="button" className="btn-close" onClick={() => handleClose(false)} />
                        </div>
                        <div className="modal-body">
                            <form>
                                <div className="form-group mb-2">
                                    <label htmlFor="Nom-Atelier">Nom</label>
                                    <input type="text" className="form-control" id="Nom-Atelier" placeholder="Usinage" onChange={(e)=> setNomAtelier(e.target.value)} value={NomAtelier}/>
                                </div>
                                <div className="form-group">
                                    <label htmlFor="SelectionMachine">Machine à affecter</label>
                                    <div className="selectable-list" id="SelectionMachine">
                                        {items.map(item => (
                                            <div
                                                key={item}
                                                className={`list-item ${selectedItems.includes(item) ? 'selected' : ''}`}
                                                onClick={() => toggleSelectItem(item)}
                                            >
                                               {selectedItems.includes(item) ? (<FaCheck className="check-icon-poste-ajout me-1"/>) : ""} {item}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-success" onClick={() => SaveAtelier()}>Ajouter</button>
                            <button type="button" className="btn btn-secondary" onClick={() => handleClose(false)}>Close</button>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );

}
export default ModalAjout;