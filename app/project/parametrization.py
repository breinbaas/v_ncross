from viktor.parametrization import Parametrization, Section, NumberField, HiddenField, ActionButton, DownloadButton, Text


class ProjectParametrization(Parametrization):
    general = Section('Limits')
    general.howto = Text("*The algorithm calculates the 'weight' of the crosssection based on the area between the left and right border. For levees it is recommended to set the left border somewhere on the crest of the levee and the right border about 20 meters offset from the left border.*")
    
    general.left_border = NumberField('Border Left', name="left_border", suffix='m', default=0)
    general.right_border = NumberField('Border Right', name='right_border', suffix='m', default=0)    
    general.crosssections = HiddenField('CrosssectionsData', name="crosssections")
    
    settings = Section('Settings')  
    settings.howto = Text("*Define the number of normative crosssections you want in the resulting download.*")
    settings.num_results =  NumberField('Number of results', name="num_results", default=3)

    output = Section('Output')
    output.surfacelines_csv = DownloadButton("Output .csv", method="on_download_surfacelines_csv")





    
    

    



    
    