import { useEffect, useRef, useState } from "react";
import {
    Alert,
    Box,
    Button,
    ButtonGroup,
    CircularProgress,
    Container,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { ApiConnector } from "../data/ApiConnector";
import { Project } from "../data/entities/Project";

type EditForm = {
    name: string;
    description: string;
    min_zoom: number;
    max_zoom: number;
};

export default function ProjectsPage() {
    const navigate = useNavigate();
    const [projects, setProjects] = useState<Project[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const fileInputRefs = useRef<Record<string, HTMLInputElement | null>>({});

    const [editProject, setEditProject] = useState<Project | null>(null);
    const [editForm, setEditForm] = useState<EditForm>({ name: "", description: "", min_zoom: 0, max_zoom: 18 });
    const [saving, setSaving] = useState(false);

    const handleUploadClick = (projectId: string) => {
        fileInputRefs.current[projectId]?.click();
    };

    const handleFileChange = (projectId: string, e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            ApiConnector.setProjectImage(projectId, file);
        }
        e.target.value = "";
    };

    const openEditDialog = (project: Project) => {
        setEditProject(project);
        setEditForm({
            name: project.name,
            description: project.description,
            min_zoom: project.min_zoom,
            max_zoom: project.max_zoom,
        });
    };

    const closeEditDialog = () => {
        setEditProject(null);
    };

    const handleSave = () => {
        if (!editProject) return;
        setSaving(true);
        ApiConnector.updateProject(editProject.id, editForm)
            .then(() => {
                setProjects((prev) =>
                    prev.map((p) =>
                        p.id === editProject.id ? { ...p, ...editForm } : p
                    )
                );
                closeEditDialog();
            })
            .finally(() => setSaving(false));
    };

    useEffect(() => {
        ApiConnector.getProjects()
            .then((data) => {
                setProjects(data);
            })
            .catch((err) => {
                setError(err.message ?? "Failed to load projects");
            })
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Container maxWidth="md" sx={{ mt: 4 }}>
                <Alert severity="error">{error}</Alert>
            </Container>
        );
    }

    return (
        <Container maxWidth="xl" sx={{ mt: 6 }}>
            <Typography variant="h4" component="h1" gutterBottom>
                Projects
            </Typography>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>ID</TableCell>
                            <TableCell>Name</TableCell>
                            <TableCell>Description</TableCell>
                            <TableCell>Status</TableCell>
                            <TableCell align="right">Min Zoom</TableCell>
                            <TableCell align="right">Max Zoom</TableCell>
                            <TableCell />
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {projects.map((project) => (
                            <TableRow key={project.id} hover>
                                <TableCell>{project.id}</TableCell>
                                <TableCell>{project.name}</TableCell>
                                <TableCell>{project.description}</TableCell>
                                <TableCell>{project.status}</TableCell>
                                <TableCell align="right">{project.min_zoom}</TableCell>
                                <TableCell align="right">{project.max_zoom}</TableCell>
                                <TableCell align="right">
                                    <input
                                        type="file"
                                        accept="image/*"
                                        style={{ display: "none" }}
                                        ref={(el) => { fileInputRefs.current[project.id] = el; }}
                                        onChange={(e) => handleFileChange(project.id, e)}
                                    />
                                    <ButtonGroup variant="outlined" size="small">
                                        <Button
                                            onClick={() => openEditDialog(project)}
                                        >
                                            Edit Details
                                        </Button>
                                        <Button
                                            onClick={() => handleUploadClick(project.id)}
                                        >
                                            Upload Image
                                        </Button>
                                        <Button
                                            onClick={() => navigate(`/projects/${project.id}`)}
                                        >
                                            Georeference
                                        </Button>
                                        <Button onClick={() =>ApiConnector.startRender(project.id)}>Start Processing</Button>
                                        <Button
                                            component="a"
                                            href={ApiConnector.getProjectTiles(project.id)}
                                            download
                                        >
                                            Download Tiles
                                        </Button>
                                    </ButtonGroup>

                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            <Dialog open={!!editProject} onClose={closeEditDialog} fullWidth maxWidth="sm">
                <DialogTitle>Edit Project</DialogTitle>
                <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}>
                    <TextField
                        label="Name"
                        value={editForm.name}
                        onChange={(e) => setEditForm((f) => ({ ...f, name: e.target.value }))}
                        fullWidth
                    />
                    <TextField
                        label="Description"
                        value={editForm.description}
                        onChange={(e) => setEditForm((f) => ({ ...f, description: e.target.value }))}
                        fullWidth
                        multiline
                        rows={3}
                    />
                    <TextField
                        label="Min Zoom"
                        type="number"
                        value={editForm.min_zoom}
                        onChange={(e) => setEditForm((f) => ({ ...f, min_zoom: Number(e.target.value) }))}
                        fullWidth
                    />
                    <TextField
                        label="Max Zoom"
                        type="number"
                        value={editForm.max_zoom}
                        onChange={(e) => setEditForm((f) => ({ ...f, max_zoom: Number(e.target.value) }))}
                        fullWidth
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={closeEditDialog} disabled={saving}>Cancel</Button>
                    <Button onClick={handleSave} variant="contained" disabled={saving}>
                        {saving ? "Saving…" : "Save"}
                    </Button>
                </DialogActions>
            </Dialog>
        </Container>
    );
}
