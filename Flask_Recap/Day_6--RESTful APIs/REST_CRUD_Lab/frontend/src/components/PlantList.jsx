import React from 'react';

import PlantCard from "./PlantCard.jsx";

function PlantList({plants, handleUpdatePlant, handleDeletePlant}) {
    return (
        <ul className="cards">
            {plants.map((plant) => {
                return <PlantCard key={plant.id} plant={plant} handleUpdatePlant={handleUpdatePlant} handleDeletePlant={handleDeletePlant}  />
            })}
        </ul>
    );
}

export default PlantList;