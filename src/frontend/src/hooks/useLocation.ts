import { useEffect, useMemo, useState } from "react";
import { Matrix, Location, MatrixType } from "../types.ts";
import axios from "axios";
import { globalEnv } from "../env.js";


export default function useLocation(matrix: Matrix) {
    const [locations, setLocations] = useState<Location[]>([])

    useEffect(() => {
        const getLocations = async (matrix: Matrix): Promise<Location[]> => {
            if (!matrix) {
                return []
            }
            const params = new URLSearchParams()
            params.append('matrix_id', `${matrix.id}`)
            params.append('matrix_type', `${matrix.type}`)
            const resp = await axios.get(globalEnv.apiEndpoint + '/location?' + params.toString()).catch(() => {})
            let res: Location[] = []
            if (resp){
                resp.data.forEach(location => {
                    res.push({ id: matrix.id, name: location.name })
                });
            }
            return res
        } 

        getLocations(matrix).then((res) => {
            setLocations(res)
        })
    }, [matrix])

    const namedLocations = useMemo(() => {
        let result: string[] = []
        if (locations) {
            locations.forEach((location) => {
                result.push(location.name)
            })
        }
        return result
    }, [locations])
    return {
        namedLocations
    }
}