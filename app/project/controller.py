from io import StringIO, BytesIO
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
from pathlib import Path

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

    @SVGView("SVG plot", duration_guess=3)
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

    def _handle_crosssection(
        self,
        crosssection: Crosssection,
        zmin: float,
        weight_length: float,
        offset_from_referenceline: float,
    ):

        result = 0.0
        zmax = crosssection.zmax + 0.1
        ls = np.linspace(
            offset_from_referenceline,
            offset_from_referenceline + int(weight_length),
            int(weight_length),
        )
        crspoints = [[p.l, p.z] for p in crosssection.points]
        crspoints += [[crspoints[-1][0], zmin - 1.0], [crspoints[0][0], zmin - 1.0]]
        crspolygon = Polygon(crspoints)
        for i in range(1, len(ls)):
            lmin = ls[i - 1]
            lmax = ls[i]
            rect = Polygon([(lmin, zmax), (lmax, zmax), (lmax, zmin), (lmin, zmin)])
            ipolygon = rect.intersection(crspolygon)
            result += pow(ipolygon.area, 3)  # * (lmid - lmin) / LENGTH_FOR_WEIGHTS

        return result

    def on_download_surfacelines_csv(self, params, **kwargs):
        # csv_path = Path(__file__).parent / 'surfacelines' / 'normative_surfacelines.csv'
        # surfacelines_csv = BytesIO()
        # with open(csv_path, "rb") as esa_file:
        #     surfacelines_csv.write(esa_file.read())
        
        # return scia_input_esa
        pass
        
    
    def on_btn_find_normative(self, params, **kwargs):
        selection_weighted = []
        #fig = Figure(figsize=(15, 6))
        #ax = fig.add_subplot()

        #f = open(Path(output_path) / "surfacelines_normative.csv", "w")
        #f.write("LOCATIONID;X1;Y1;Z1;.....;Xn;Yn;Zn;(Profiel)\n")

        crosssections = [Crosssection.parse_raw(crs_json) for crs_json in params.crosssections]
        
        zmin = 1e9
        for crs in crosssections:
            zmin = min(zmin, min([p.z for p in crs.points]))

        for crs_json in params.crosssections:
            crs = Crosssection.parse_raw(crs_json)
            weight = self._handle_crosssection(
                crs, zmin, params.right_border - params.left_border, params.left_border
            )
            xs = [p.l for p in crs.points]
            ys = [p.z for p in crs.points]
        #    ax.plot(xs, ys, "k:")
            selection_weighted.append((weight, crs))

        # sort on weight
        selection_weighted = sorted(selection_weighted, key=lambda x: x[0])

        #print(selection_weighted[:params.num_results])

        

        # for _, crs in selection_weighted[params.num_results]:
        #     xs = [p.l for p in crs.points]
        #     ys = [p.z for p in crs.points]
            #ax.plot(xs, ys, label=f"{crs.id}")
            #f.write(f"{crs.to_surfaceline()}\n")
        
        #f.close()
        #ax.set_title("normative crosssections")
        #fig.legend()
        #fig.savefig(Path(output_path) / f"normative_crosssections_result.png")

        

