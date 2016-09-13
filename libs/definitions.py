from libs import constants

# Porcentagem da população que evoluirá para a próxima geração
naturalSelectionThreshold = 0.7
# Quantidade de gerações
numberOfGenerations = 100

# Seletores e classificadores utilizados
selectors = [constants.TStatistics]
classifiers = [constants.DecisionTree, constants.Lasso, constants.SVM, constants.GaussianNB, constants.MultinomialNB, constants.BernoulliNB]