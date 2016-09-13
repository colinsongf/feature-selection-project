from libs import constants

# Porcentagem da população que evoluirá para a próxima geração
naturalSelectionThreshold = 0.7
# Quantidade de gerações
numberOfGenerations = 100
# Chance de mutação (0 - 100%)
probMutation = 10 # 10%

# Seletores e classificadores utilizados
selectors = [constants.TStatistics]
classifiers = [constants.DecisionTree, constants.Lasso, constants.SVM, constants.GaussianNB, constants.MultinomialNB, constants.BernoulliNB]