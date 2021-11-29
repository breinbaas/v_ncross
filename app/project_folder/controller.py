from viktor.core import ViktorController

class ProjectFolderController(ViktorController):
    label = 'Project folder'
    children = ['Project']
    show_children_as = 'Cards'  # or 'Table'
