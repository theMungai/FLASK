import { useEffect, useState } from 'react'

import './App.css'

function App() {
    const [movies, setMovies] = useState([])

    useEffect(() => {
        fetch("/movies")
            .then((r) => r.json())
            .then((data) => setMovies(data))
    }, []);

    if (movies.length === 0){
        return <p>No movies found.</p>;
    }


  return (
    <div>
      <h1>Movie List</h1>
        <ol>
            {movies.map((movie, index) => (
                <li key={index}>{movie.title || movie}</li>
            ))}
        </ol>
    </div>
  )
}

export default App
