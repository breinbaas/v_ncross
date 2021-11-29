from viktor.parametrization import Parametrization, Section, NumberField




class ProjectParametrization(Parametrization):
    general = Section('General')
    general.beam_length = NumberField('Length', suffix='mm', default=2000)
    
    

    



    
    