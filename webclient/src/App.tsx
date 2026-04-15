import {Route, Routes} from "react-router-dom";
import './style.scss'
import ProjectsPage from "./pages/ProjectsPage.tsx";
import 'maplibre-gl/dist/maplibre-gl.css';
import EditProjectPage from "./pages/EditProjectPage.tsx";


function App() {
    
    return (
        <Routes>
            <Route index path="/projects" element={<ProjectsPage />} />
            <Route path="/projects/:id" element={<EditProjectPage />} />
        </Routes>
    )
}

export default App
