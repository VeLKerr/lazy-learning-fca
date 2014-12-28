import sys

import algorithm0, algorithm1, algorithm2, algorithm3, algorithm4
import utils


def kfold(classification_algorithm, k):
    res = {"accuracy": 0, "precision": 0, "recall": 0, "f1": 0}
    for i in range(1, k + 1):
        validation = utils.load_train(i)
        validation = validation["plus"] + validation["minus"]
        train = {"plus": [], "minus": []}
        for j in range(1, k + 1):
            if j != i:
                extension = utils.load_train(j)
                train["plus"].extend(extension["plus"])
                train["minus"].extend(extension["minus"])
        classification = classification_algorithm(train, validation)
        res["accuracy"] += utils.accuracy(classification)
        res["precision"] += utils.precision(classification)
        res["recall"] += utils.recall(classification)
        res["f1"] += utils.F1_score(classification)
    for k in res:
        res[k] /= k
    print res
    return res


# Syntax: python kfold.py <Classification algorithm ID> <K>

if __name__ == "__main__":

    algorithm = int(sys.argv[1])
    k = int(sys.argv[2])

    if algorithm == 0:
        classification_algorithm = algorithm0.classify
    elif algorithm == 1:
        classification_algorithm = algorithm1.classify
    elif algorithm == 2:
        classification_algorithm = algorithm2.classify
    elif algorithm == 3:
        classification_algorithm = algorithm3.classify
    elif algorithm == 4:
        classification_algorithm = algorithm4.classify

    kfold(classification_algorithm, k)
