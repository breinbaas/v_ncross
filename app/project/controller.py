from io import StringIO, BytesIO
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
from pathlib import Path

from viktor.core import ViktorController, File, ParamsFromFile
from viktor import UserException
from viktor.views import SVGResult, SVGView
from viktor.result import DownloadResult
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
        fig = plt.figure(figsize=(10,7))
        zmin = 1e9
        zmax = -1e9

        # generate crosssections
        crosssections = self._get_crosssections_weighted(params)

        # check if we have winners
        has_normatives = max([crs.weight for crs in crosssections]) > 0

        if has_normatives:
            num_results = params.num_results
        else:
            num_results = 0

        for crs in crosssections[num_results:]:          
            xs = [p.l for p in crs.points]
            zs = [p.z for p in crs.points]
            zmin = min(zmin, min(zs))
            zmax = max(zmax, max(zs))            
            plt.plot(xs, zs, 'k:')

        for crs in crosssections[:num_results]:
            xs = [p.l for p in crs.points]
            zs = [p.z for p in crs.points]
            zmin = min(zmin, min(zs))
            zmax = max(zmax, max(zs))            
            plt.plot(xs, zs, label=f"{crs.id}")
            

        xl = params.left_border
        xr = params.right_border
        
        plt.plot([xl, xl],[zmin, zmax], 'r--')
        plt.plot([xr, xr],[zmin, zmax], 'b--')
        fig.suptitle("normative crosssections")
        if has_normatives:
            fig.legend(loc='upper left')
        plt.tight_layout()
        

        # save figure
        svg_data = StringIO()
        fig.savefig(svg_data, format='svg')
        plt.close()

        return SVGResult(svg_data)

    # TODO > create download
    def on_download_surfacelines_csv(self, params, **kwargs):
        crosssections = self._get_crosssections_weighted(params)
        has_normatives = max([crs.weight for crs in crosssections]) > 0

        if has_normatives:
            data = "LOCATIONID;X1;Y1;Z1;.....;Xn;Yn;Zn;(Profiel)\n"
            for crs in crosssections[:params.num_results]:
                data += f"{crs.to_surfaceline()}\n"
            
            return DownloadResult(data, 'normative_surfacelines.csv')



    
    def _get_crosssections_weighted(self, params, **kwargs):
        crosssections = [Crosssection.parse_raw(crs_json) for crs_json in params.crosssections]

        # only proceed with valid input
        if params.left_border >= params.right_border:
            return crosssections

        # find zmin
        zmin = 1e9
        for crs in crosssections:
            zmin = min(zmin, min([p.z for p in crs.points]))
        
        # calculate the weight
        for crs in crosssections:
            crs.weight = self._handle_crosssection(crs, zmin, params.right_border - params.left_border, params.left_border)
       
        # we're done, sort the result (lowest weights first) and return
        return sorted(crosssections, key=lambda x:x.weight)    
    
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

    