from libs.SelectionProcess import SelectionProcess
from libs.ClassificationProcess import ClassificationProcess
import weka.core.jvm as jvm
import numpy as np
import os

classificatorsFile = os.getcwd() + '/resource/classifiersToUse.txt'
selectionResultFile = os.getcwd() + '/results/selection/selection.txt'
resultsDirPath = os.getcwd() + '/results'

selection = SelectionProcess(10)
classification = ClassificationProcess(folds=5)

selection.run()
classification.run()