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
    
def check_hypothesis(context_plus, context_minus, example):
    eintent = make_intent(example)
    eintent.discard('OVERALL_DIAGNOSIS:1')
    eintent.discard('OVERALL_DIAGNOSIS:0')
    labels = {}
    conf_minus = 0
    conf_plus = 0
    global cv_res
    for e in context_plus:
        ei = make_intent(e)
        candidate_intent = ei & eintent
        closure = [make_intent(i) for i in context_minus if make_intent(i).issuperset(candidate_intent)]
        closure_size = len([i for i in closure if len(i)])

        res = reduce(lambda x,y: x&y if x&y else x|y, closure ,set())
        if closure_size != 0:
            conf_minus += len(res) / closure_size
        # minus_weight = closure_size * 1.0 / len(context_minus) / len(context_plus)
        # if minus_weight > 0.8:
        #     conf_minus += minus_weight

        # res = reduce(lambda x,y: x&y if x&y else x|y, closure ,set())
        # for cs in ['1', '0']:
        #     if 'OVERALL_DIAGNOSIS:'+cs in res:
        #         labels[cs] = True
        #         labels[cs+'_res'] = candidate_intent
        #         labels[cs+'_total_weight'] = \
        #             labels.get(cs+'_total_weight', 0) + closure_size * 1.0 / len(context_minus) / len(context_plus)
    for e in context_minus:
        ei = make_intent(e)
        candidate_intent = ei & eintent
        closure = [make_intent(i) for i in context_plus if make_intent(i).issuperset(candidate_intent)]
        closure_size = len([i for i in closure if len(i)])

        res = reduce(lambda x, y: x & y if x & y else x | y, closure, set())
        if closure_size != 0:
            conf_plus += len(res) / closure_size

        # plus_weight = closure_size * 1.0 / len(context_minus) / len(context_plus)
        # if plus_weight > 0.8:
        #     conf_plus += plus_weight

        # res = reduce(lambda x, y: x & y if x & y else x | y, closure, set())
        # for cs in ['1', '0']:
        #     if 'OVERALL_DIAGNOSIS:'+cs in res:
        #         labels[cs] = True
        #         labels[cs+'_res'] = candidate_intent
        #         labels[cs+'_total_weight'] = \
        #             labels.get(cs+'_total_weight', 0) + closure_size * 1.0 / len(context_plus) / len(context_minus)
    # print eintent
    # print labels

    if reduce(lambda x, y: int(x)+int(y), example) < 3:
        labels['0'] = True
    else:
        if conf_minus > conf_plus:
            labels['0'] = True
        else:
            if conf_plus > conf_minus:
                labels['1'] = True

    if labels.get("1", False) and labels.get("0", False):
       cv_res["contradictory"] += 1
       return
    if example[0] == "1" and labels.get("1", False):
       cv_res["positive_positive"] += 1
    if example[0] == "0" and labels.get("1", False):
       cv_res["negative_positive"] += 1
    if example[0] == "1" and labels.get("0", False):
       cv_res["positive_negative"] += 1
    if example[0] == "0" and labels.get("0", False):
       cv_res["negative_negative"] += 1



i = 0
for elem in unknown:
    print "done: " + str(i)
    i += 1
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


