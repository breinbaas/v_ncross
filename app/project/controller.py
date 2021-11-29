from io import StringIO
import matplotlib.pyplot as plt
import numpy as np

from viktor.core import ViktorController, File, ParamsFromFile
from viktor import UserException
from viktor.views import SVGResult, SVGView
from .parametrization import ProjectParametrization
from .models.crosssection import Crosssection

class ProjectController(ViktorController):
    label = 'Project controller'
    parametrization = ProjectParametrization
    
    @ParamsFromFile()
    def process_file(self, file: File, **kwargs):  # viktor.core.File
        crosssections = []
        for line in file.getvalue(encoding='utf-8').splitlines()[1:]:
            crosssection = Crosssection.from_dam_data(line)
            if crosssection is not None:
                crosssections.append(crosssection.json())

        return {
            'crosssections':crosssections
        }

    @SVGView("SVG plot", duration_guess=1)
    def create_svg_result(self, params, **kwargs):
        fig = plt.figure()
        zmin = 1e9
        zmax = -1e9

        for crs_json in params.crosssections:
            crs = Crosssection.parse_raw(crs_json)
            xs = [p.l for p in crs.points]
            zs = [p.z for p in crs.points]
            zmin = min(zmin, min(zs))
            zmax = max(zmax, max(zs))
            plt.plot(xs, zs, 'k:')

        xl = params.left_border
        xr = params.right_border
        
        plt.plot([xl, xl],[zmin, zmax], 'r--')
        plt.plot([xr, xr],[zmin, zmax], 'b--')
        plt.tight_layout()
        

        # save figure
        svg_data = StringIO()
        fig.savefig(svg_data, format='svg')
        plt.close()

        return SVGResult(svg_data)

        

