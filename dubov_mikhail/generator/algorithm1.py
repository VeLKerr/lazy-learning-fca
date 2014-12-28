import sys

import utils


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
# vote = +1 for the positive/negative class, if the intersection is not falsifiable.
# Aggr = Sum of votes for each sample (for pos/neg classes)


def make_intent(example):
    return set((i + ':' + k) for i, k in zip(attrib_names,example))
    
def check_hypothesis(context_plus, context_minus, example):
    example_intent = make_intent(example)
    example_intent.discard('class:positive')
    example_intent.discard('class:negative')
    labels = {"positive": 0, "negative": 0}
    for positive_example in context_plus:
        positive_example_intent = make_intent(positive_example)
        intersection_intent = positive_example_intent & example_intent
        falsifications = [make_intent(i) for i in context_minus if make_intent(i).issuperset(intersection_intent)]
        if intersection_intent and not falsifications:
            labels["positive"] += 1
    for negative_example in context_minus:
        negative_example_intent = make_intent(negative_example)
        intersection_intent = negative_example_intent & example_intent
        falsifications = [make_intent(i) for i in context_plus if make_intent(i).issuperset(intersection_intent)]
        if intersection_intent and not falsifications:
            labels["negative"] += 1
    labels["positive"] = float(labels["positive"]) / len(context_plus)
    labels["negative"] = float(labels["negative"]) / len(context_minus)
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
       return "contradictory"


def classify(train, examples):
    cv_res = {
     "PP": 0,
     "PN": 0,
     "NP": 0,
     "NN": 0,
     "contradictory": 0,
    }
    plus = train["plus"]
    minus = train["minus"]
    l = len(examples)
    i = 0
    for elem in examples:
        i += 1
        print "%i/%i" % (i, l)
        result = check_hypothesis(plus, minus, elem)
        cv_res[result] += 1
    return cv_res


if __name__ == "__main__":

    index = int(sys.argv[1])

    train = utils.load_train(index)
    test = utils.load_test(index)

    res = classify(train, test)
    print res
    print utils.summary(res)
