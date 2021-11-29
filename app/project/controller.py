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
    crosssections = []

    @ParamsFromFile()
    def process_file(self, file: File, **kwargs):  # viktor.core.File
        for line in file.getvalue(encoding='utf-8').splitlines()[1:]:
            crosssection = Crosssection.from_dam_data(line)
            if crosssection is not None:
                self.crosssections.append(crosssection)

    @SVGView("SVG plot", duration_guess=1)
    def create_svg_result(self, params, **kwargs):
        fig = plt.figure()

        for crs in self.crosssections:
            xs = [p.l for p in crs.points]
            zs = [p.z for p in crs.points]
            plt.plot(xs, zs, 'k:')

        # save figure
        svg_data = StringIO()
        fig.savefig(svg_data, format='svg')
        plt.close()

        return SVGResult(svg_data)

        

