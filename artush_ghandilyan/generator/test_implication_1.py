import pprint
import sys

q = open("train.csv","r")
train = [ a.strip().split(",") for a in q]
plus = [a for a in train if a[0] == "1"]
minus = [a for a in train if a[0] == "0"]
q.close()

w = open("test.csv","r")
unknown = [a.strip().split(",") for a in w]
w.close()

cv_res = {
    "positive_positive": 0,
    "positive_negative": 0,
    "negative_positive": 0,
    "negative_negative": 0,
    "contradictory": 0,
}

attrib_names = [
    'OVERALL_DIAGNOSIS',
    'F1',
    'F2',
    'F3',
    'F4',
    'F5',
    'F6',
    'F7',
    'F8',
    'F9',
    'F10',
    'F11',
    'F12',
    'F13',
    'F14',
    'F15',
    'F16',
    'F17',
    'F18',
    'F19',
    'F20',
    'F21',
    'F22'
]

def make_intent(example):
    global attrib_names
    return set([i+':'+str(k) for i,k in zip(attrib_names,example)])


cv_res = {
 "positive_positive": 0,
 "positive_negative": 0,
 "negative_positive": 0,
 "negative_negative": 0,
 "contradictory": 0,
}
    
def check_hypothesis(context_plus, context_minus, example):
    global cv_res
    eintent = make_intent(example)
    big_context = context_plus + context_minus
    labels = {}
    conf_minus = 0
    conf_plus = 0
    for e in big_context:
        ei = make_intent(e)
        candidate_intent = ei&eintent
        if not candidate_intent:
            continue

        closure_plus = [make_intent(i) for i in context_plus if make_intent(i).issuperset(candidate_intent)]
        closure_minus = [make_intent(i) for i in context_minus if make_intent(i).issuperset(candidate_intent)]

        res_plus = reduce(lambda x,y: x&y if x&y else x|y, closure_plus, set())
        res_minus = reduce(lambda x,y: x&y if x&y else x|y, closure_minus, set())

        conf_plus += len(res_plus) * len(closure_plus) / (len(closure_plus) + len(closure_minus))
        conf_minus += len(res_minus) * len(closure_minus) / (len(closure_plus) + len(closure_minus))

    if conf_minus > conf_plus:
        labels['0'] = True
    else:
        if conf_plus > conf_minus:
            labels['1'] = True

    if labels.get("1",False) and labels.get("0",False):
       cv_res["contradictory"] += 1
       return
    if example[0] == "1" and labels.get("1",False):
       cv_res["positive_positive"] += 1
    if example[0] == "0" and labels.get("1",False):
       cv_res["negative_positive"] += 1
    if example[0] == "1" and labels.get("0",False):
       cv_res["positive_negative"] += 1
    if example[0] == "0" and labels.get("0",False):
       cv_res["negative_negative"] += 1


i = 0
for elem in unknown:
    i += 1
    print('done: ', i)
    check_hypothesis(plus, minus, elem)

print cv_res

TP = cv_res['positive_positive']
TN = cv_res['negative_negative']
FP = cv_res['negative_positive']
FN = cv_res['positive_negative']

accuracy = (TP + TN) / float(TP + TN + FP + FN)
precision = TP / float(TP + FP)
sensitivity = TP / float(TP + FN)
specificity = TN / float(FP + TN)
F1 = 2 * TP / float(2 * TP + FP + FN)
NPV = TN / float(TN + FN)
print('Accuracy = ' + str(accuracy) +
      ' Precision = ' + str(precision) +
      ' Sensitivity = ' + str(sensitivity) +
      ' Specificity = ' + str(specificity) +
      ' F1 score = ' + str(F1) +
      ' NPV = ' + str(NPV))

