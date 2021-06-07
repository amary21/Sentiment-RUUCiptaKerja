import numpy as np

class NaiveBayes(object):
    def __init__(self, alpha=0.5):
        self.alpha = alpha

    def _predict(self, x_test):
        # Calculate posterior for each class
        posteriors = []
        for idx, _ in enumerate(self._classes):
            prior_c = np.log(self._priors[idx])
<<<<<<< Updated upstream
            conditionals_c = self._calc_conditional(self._conditionals[idx, :], x_test)
=======
            conditionals_c = self._calc_conditionals(self._conditionals[idx, :], x_test)
>>>>>>> Stashed changes
            posteriors_c = np.sum(conditionals_c) + prior_c
            posteriors.append(posteriors_c)

        return self._classes[np.argmax(posteriors)]

<<<<<<< Updated upstream
    def _calc_conditional(self, cls_cond, x_test):
=======
    def _calc_conditionals(self, cls_cond, x_test):
>>>>>>> Stashed changes
        return np.log(cls_cond) * x_test

    def fit(self, X_train, y_train):
        X_train = np.array(X_train)
        m, n = X_train.shape
        self._classes = np.unique(y_train)
        n_classes = len(self._classes)

        # init: Prior & Conditional
        self._priors = np.zeros(n_classes)
        self._conditionals = np.zeros((n_classes, n))

        # Get Prior and Conditional
        for idx, c in enumerate(self._classes):
            X_train_c = X_train[c == y_train]
            self._priors[idx] = X_train_c.shape[0] / m
            self._conditionals[idx, :] = ((X_train_c.sum(
                axis=0)) + self.alpha) / (np.sum(X_train_c.sum(axis=0) + self.alpha))

    def predict(self, X_test):
        return [self._predict(x_test) for x_test in X_test]
