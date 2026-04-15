import type { Project } from "../entities/Project";




export interface ApiProjects {
    count: number;
    next: string | null;
    previous: string | null;
    results: Project[];
}