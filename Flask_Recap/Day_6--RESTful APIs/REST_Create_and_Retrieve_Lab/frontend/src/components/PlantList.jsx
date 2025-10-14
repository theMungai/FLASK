import React from 'react';

import PlantCard from "./PlantCard.jsx";

function PlantList({plants}) {
    return (
        <ul className="cards">
            {plants.map((plant) => {
                return <PlantCard key={plant} plant={plant} />
            })}
        </ul>
    );
}

export default PlantList;