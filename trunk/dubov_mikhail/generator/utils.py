
def load_train(i):
    with open("train" + str(i) + ".csv", "r") as q:
        train = [a.strip().split(",") for a in q][1:]
        plus = [a for a in train if a[-1]=="positive"]
        minus = [a for a in train if a[-1]=="negative"]
    return {"plus": plus, "minus": minus}


def load_test(i):
    with open("test" + str(i) + ".csv","r") as q:
        test = [a.strip().split(",") for a in q]
    return test[1:]


def accuracy(res):
    return float(res["PP"] + res["NN"]) / max(1, res["PP"] + res["NN"] + res["PN"] + res["NP"] + res["contradictory"])


def precision(res):
    return float(res["PP"]) / max(1, res["PP"] + res["NP"])


def recall(res):
    return float(res["PP"]) / max(1, res["PP"] + res["PN"])


def F1_score(res):
    prec = precision(res)
    rec = recall(res)
    return 2 * prec * rec / max(1, prec + rec)


def summary(res):
    stats = {}
    stats["accuracy"] = accuracy(res)
    stats["precision"] = precision(res)
    stats["recall"] = recall(res)
    stats["f1"] = F1_score(res)
    return stats

