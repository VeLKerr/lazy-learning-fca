__author__ = 'olegkhomyuk'


def importdata(index):
    with open("train" + index + ".csv", "r") as q:
        ql = q.readlines()
        train = [a.strip().split(",") for a in ql[1:len(ql)]]
        plus = [a for a in train if a[-1] == "positive"]
        minus = [a for a in train if a[-1] == "negative"]

    with open("test" + index + ".csv", "r") as w:
        wl = w.readlines()
        unknown = [a.strip().split(",") for a in wl[1:len(wl)]]

    return plus, minus, unknown


attrib_names = [
'top-left-square',
'top-middle-square',
'top-right-square',
'middle-left-square',
'middle-middle-square',
'middle-right-square',
'bottom-left-square',
'bottom-middle-square',
'bottom-right-square',
'class'
]


# Algorithm 1.
# For each sample, find its intersection with positive/negative contexts;
# vote +1 for the positive/negative class, if the hypothesis is not falsifiable.


def make_intent(example):
    return set((i + ':' + k) for i, k in zip(attrib_names, example))


def check_hypothesis(context_plus, context_minus, example):
    example_intent = make_intent(example)
    example_intent.discard('class:positive')
    example_intent.discard('class:negative')

    labels = {"positive": 0, "negative": 0}
    for positive_example in context_plus:
        positive_example_intent = make_intent(positive_example)
        intersection_intent = positive_example_intent & example_intent
        contradictions = [make_intent(i) for i in context_minus if make_intent(i).issuperset(intersection_intent)]
        if intersection_intent and not contradictions:
            labels["positive"] += 1

    for negative_example in context_minus:
        negative_example_intent = make_intent(negative_example)
        intersection_intent = negative_example_intent & example_intent
        contradictions = [make_intent(i) for i in context_plus if make_intent(i).issuperset(intersection_intent)]
        if intersection_intent and not contradictions:
            labels["negative"] += 1

    if labels["positive"] > labels["negative"]:
        if example[-1] == "positive":
            return "PP"
        else:
            return "NP"
    elif labels["positive"] < labels["negative"]:
        if example[-1] == "negative":
            return "NN"
        else:
            return "PN"
    else:
        return "?"


def classify(tr_plus, tr_minus, examples):
    cv_res = {
     "PP": 0,
     "PN": 0,
     "NP": 0,
     "NN": 0,
     "?": 0,
    }
    l = len(examples)
    i = 0
    for elem in examples:
        i += 1
        print("%i/%i" % (i, l))
        result = check_hypothesis(tr_plus, tr_minus, elem)
        cv_res[result] += 1
    print(cv_res)
    return cv_res


for exp in range(1, 11):
    (dplus, dminus, dunknown) = importdata(str(exp))
    classify(dplus, dminus, dunknown)