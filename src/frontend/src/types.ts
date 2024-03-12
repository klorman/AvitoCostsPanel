export enum MatrixType {
    Base,
    Discount
}

export interface Matrix {
    id: number,
    type: MatrixType,
}

export interface Location {
    id: number,
    name: string
}