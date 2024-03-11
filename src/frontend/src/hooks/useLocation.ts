import { useEffect, useMemo, useState } from "react";
import { Matrix, Location } from "../types.ts";


export default function useLocation(matrix: Matrix) {
    const [locations, setLocations] = useState<Location[]>([])

    useEffect(() => {
        const getLocations = async (matrix: Matrix): Promise<Location[]> => {
            return [{ id: 1, name: "Russia" }]
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