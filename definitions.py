from libs import constants

selectors = [constants.TStatistics]
classifiers = [constants.DecisionTree, constants.Lasso, constants.SVM, constants.GaussianNB, constants.MultinomialNB, constants.BernoulliNB]

# Porcentagem da população que evoluirá para a próxima geração
naturalSelectionThreshold = 0.7