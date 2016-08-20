from libs.SelectionModule import SelectionModule
from libs.ClassificationModule import ClassificationModule

selection = SelectionModule(5)
selection.run()

classification = ClassificationModule()
classification.run()