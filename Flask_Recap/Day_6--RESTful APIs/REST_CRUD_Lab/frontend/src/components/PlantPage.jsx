import React, {useState, useEffect} from 'react';

import NewPlantForm from "./NewPlantForm.jsx";
import PlantList from "./PlantList.jsx";
import Search from "./Search.jsx";

function PlantPage() {
    const [plants, setPlants] = useState([])
    const [searchTerm, setSearchTerm] = useState("")

    useEffect(() => {
        fetch("/plants")
            .then((r) => r.json())
            .then(plantsArray => {
                setPlants(plantsArray)
            })
    }, []);

    function handleAddPlant(newPlant){
        const updatedPlantsArray = [...plants, newPlant];
        setPlants(updatedPlantsArray)
    }

    function handleUpdatePlant(updatedPlant){
        const updatedPlantsArray = plants.map(plant => {
            if (plant.id === updatedPlant.id) return updatedPlant
            else return plant
        })
        setPlants(updatedPlantsArray)
    }

    function handleDeletePlant(id){
        const  updatedPlantsArray = plants.filter((plant) => plant.id !== id)
        setPlants(updatedPlantsArray)
    }

    const displayedPlants = plants.filter((plant) => {
        return plant.name.toLowerCase().includes(searchTerm)
    })

    return (
        <main>
            <NewPlantForm onAddPlant={handleAddPlant} />
            <Search searchTerm={searchTerm} onSearchChange={setSearchTerm} />
            <PlantList plants={displayedPlants} handleUpdatePlant={handleUpdatePlant} handleDeletePlant={handleDeletePlant}/>
        </main>
    );
}

export default PlantPage;