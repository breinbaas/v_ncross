from pydantic import BaseModel

class Point3D(BaseModel):
    l: float
    x: float
    y: float
    z: float