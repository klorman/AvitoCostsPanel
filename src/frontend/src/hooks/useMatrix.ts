import { useEffect, useMemo, useState } from "react";
import axios from 'axios'
import { globalEnv } from '../env'
import { MatrixType, Matrix } from "../types.ts";


export default function useMatrix() {
    const [matrices, setMatrices] = useState<Matrix[]>([]);
    const [state, setState] = useState<boolean>(false);
    const toggleUpdateMatrix = () => setState(!state)

    useEffect(() => {
        const getMatrices = async (): Promise<Matrix[]> => {
            const resp = await axios.get(globalEnv.apiEndpoint + '/matrix').catch(() => {})
            let res: Matrix[] = []
            if (resp){
                resp.data.forEach(matrix => {
                    res.push({ id: matrix.id, type: matrix.type === 'Base'? MatrixType.Base: MatrixType.Discount })
                });
            }
            return res
        } 

        getMatrices().then((matrices) => {
            if (matrices) {
                setMatrices(matrices)
            }
        })
    }, [state])

    const namedMatrices = useMemo(() => {
        let result: string[] = []
        if (matrices) {
            matrices.forEach((matrix) => {
                if (matrix.type === MatrixType.Base) {
                    result.push(`baseline_${matrix.id}`)
                }
                else {
                    result.push(`discount_${matrix.id}`)
                }
            })
        }
        return result.sort().reverse()
    }, [matrices])
    return {
        namedMatrices,
        matrices,
        toggleUpdateMatrix
    }
}