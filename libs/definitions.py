#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs import constants

# Porcentagem da população que evoluirá para a próxima geração
naturalSelectionThreshold = 0.7
# Tamanho da população
populationSize = 100
# Quantidade máxima de características selecionadas
maxNumberOfSelectedFeatures = 10
# Quantidade de gerações
numberOfGenerations = 10
# Chance de mutação (0.0 - 1.0)
probMutation = 0.1

# Seletores e classificadores utilizados
selectors = [constants.TStatistics]
classifiers = [constants.DecisionTree, constants.Lasso, constants.SVM, constants.GaussianNB, constants.MultinomialNB, constants.BernoulliNB]