export interface ContextMenuInterface {


    open(x: number, y: number): void;

    close(): void;

    getContainer(): HTMLDivElement;
}