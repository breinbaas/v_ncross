from pydantic import BaseModel
import math
from typing import List, Dict, Union
from .point3d import Point3D

class Crosssection(BaseModel):
    id: str = ""
    points: List[Point3D] = []

    @classmethod
    def from_dam_data(cls, surfaceline: str) -> Union[None, "Crosssection"]:
        result = Crosssection()
        args = surfaceline.split(";")
        result.id = args[0]      
        
        xs = [float(args[i]) for i in range(1, len(args), 3)]
        ys = [float(args[i]) for i in range(2, len(args), 3)]
        zs = [float(args[i]) for i in range(3, len(args), 3)]
        ls = []
        for i in range(len(xs)):
            if i==0:
                ls.append(0)
            else:
                ls.append(math.hypot(xs[0]-xs[i], ys[0]-ys[i]))

        result.points = [
            Point3D(x=xs[i], y=ys[i], z=zs[i], l=round(ls[i], 3))
            for i in range(len(xs))
        ]
        return result

    @property
    def zmin(self) -> float:
        if len(self.points) <= 0:
            raise ValueError("Trying to find zmin on a crosssection without points")
        return min([p.z for p in self.points])

    @property
    def zmax(self) -> float:
        if len(self.points) <= 0:
            raise ValueError("Trying to find zmax on a crosssection without points")
        return max([p.z for p in self.points])

    def to_surfaceline(self) -> str:
        line = f"{self.id};"
        for p in self.points:
            line += f"{p.x:.03f};{p.y:.03f};{p.z:.03f};"
        return line[:-1]  # remove last semi colon