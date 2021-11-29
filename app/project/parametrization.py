from viktor.parametrization import Parametrization, Section, NumberField, HiddenField


class ProjectParametrization(Parametrization):
    general = Section('General')
    general.left_border = NumberField('Border Left', name="left_border", suffix='m', default=0)
    general.right_border = NumberField('Border Right', name='right_border', suffix='m', default=0)    
    general.crosssections = HiddenField('CrosssectionsData', name="crosssections")



    
    

    



    
    