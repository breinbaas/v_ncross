from viktor.parametrization import Parametrization, Section, NumberField, HiddenField, ActionButton, DownloadButton


class ProjectParametrization(Parametrization):
    general = Section('Limits')
    general.left_border = NumberField('Border Left', name="left_border", suffix='m', default=0)
    general.right_border = NumberField('Border Right', name='right_border', suffix='m', default=0)    
    general.crosssections = HiddenField('CrosssectionsData', name="crosssections")
    
    settings = Section('Settings')  
    settings.num_results =  NumberField('Number of results', name="num_results", suffix='m', default=3)

    output = Section('Output')
    output.surfacelines_csv = DownloadButton("Output .csv", method="on_download_surfacelines_csv")





    
    

    



    
    