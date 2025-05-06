import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import GardenPage from './pages/GardenPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route 
          path="/" 
          element={<HomePage />}  
        />
        <Route 
          path="/garden/:id" 
          element={<GardenPage />} 
        />
      </Routes>
    </Router>
  );
}

export default App;