# import pprint
import sys
from functools import reduce

#index = sys.argv[1]

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


cv_res = {
    "positive_positive": 0,
    "positive_negative": 0,
    "negative_positive": 0,
    "negative_negative": 0,
    "contradictory": 0,
}

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


def make_intent(example):
    global attrib_names
    return set([i + ':' + str(k) for i, k in zip(attrib_names, example)])


def check_hypothesis(context_plus, context_minus, example):
    eintent = make_intent(example)
    eintent.discard('class:positive')
    eintent.discard('class:negative')

    labels = {}
    global cv_res

    plus_rate = 0

    for e in context_plus:
        # Пересечение описания объекта с элементом плюс-контекста. Формирование гипотезы.
        candidate_intent = make_intent(e) & eintent

        # Мощность пересечения описания объекта с элементом плюс-контекста
        intent_power = len(candidate_intent) / len(eintent)

        # Поддержка плюс-гипотезы. Замыкание в плюс-контексте.
        closure_plus = [make_intent(obj) for obj in context_plus if make_intent(obj).issuperset(candidate_intent)]
        closure_plus_size = len(closure_plus)
        support = len(closure_plus) / len(context_plus)

        # Фальсифицируемость плюс-гипотезы - объекты минус-контекста, подходящие под описание текущей гипотезы.
        closure_minus = [make_intent(obj) for obj in context_minus if make_intent(obj).issuperset(candidate_intent)]
        closure_minus_size = len(closure_minus)
        falsif = closure_minus_size / len(context_minus)

        plus_rate += 1000 * (support > falsif) * (support - falsif) / (len(context_plus)+len(context_minus))

        #closure_size = len([i for i in closure if len(i)])
        #print(e, closure_size, len(closure))
        #print(closure)
        #print closure_size * 1.0 / len(context_minus)

        res = reduce(lambda x, y: x & y if x & y else x | y, closure_plus, set())
        for cs in ['positive', 'negative']:
            if 'class:' + cs in res:
                labels[cs] = True
                labels[cs + '_res'] = candidate_intent
                labels[cs + '_total_weight'] = labels.get(cs + '_total_weight', 0) + closure_plus_size * 1.0 / len(
                    context_minus) / len(context_plus)

    #print(plus_rate)

    minus_rate = 0

    for e in context_minus:
        # Пересечение описания объекта с элементом минус-контекста. Формирование гипотезы.
        candidate_intent = make_intent(e) & eintent

        # Мощность пересечения описания объекта и элемента минус-контекста.
        intent_power = len(candidate_intent) / len(eintent)

        # Поддержка минус-гипотезы. Замыкание в минус-контексте.
        closure_minus = [make_intent(obj) for obj in context_minus if make_intent(obj).issuperset(candidate_intent)]
        closure_minus_size = len(closure_minus)
        support = len(closure_minus) / len(context_minus)

        # Фальсифицируемость минус-гипотезы - объекты плюс-контекста, подходящие под описание текущей гипотезы.
        closure_plus = [make_intent(obj) for obj in context_plus if make_intent(obj).issuperset(candidate_intent)]
        closure_plus_size = len(closure_plus)
        falsif = closure_plus_size / len(context_plus)

        minus_rate += 1000 * (support > falsif) * (support - falsif) / (len(context_minus))


        #closure = [make_intent(i) for i in context_minus if make_intent(i).issuperset(candidate_intent)]
        #closure_size = len([i for i in closure if len(i)])
        #print closure_size * 1.0 / len(context_plus)
        res = reduce(lambda x, y: x & y if x & y else x | y, closure_minus, set())
        for cs in ['positive', 'negative']:
            if 'class:' + cs in res:
                labels[cs] = True
                labels[cs + '_res'] = candidate_intent
                labels[cs + '_total_weight'] = labels.get(cs + '_total_weight', 0) + closure_minus_size * 1.0 / len(
                    context_plus) / len(context_minus)
    #print(eintent)
    #print(labels)

    #print(minus_rate)

    #if labels.get("positive",False) and labels.get("negative",False):
    #   cv_res["contradictory"] += 1
    #   return
    #if example[-1] == "positive" and labels.get("positive",False):
    #   cv_res["positive_positive"] += 1
    #if example[-1] == "negative" and labels.get("positive",False):
    #   cv_res["negative_positive"] += 1
    #if example[-1] == "positive" and labels.get("negative",False):
    #   cv_res["positive_negative"] += 1
    #if example[-1] == "negative" and labels.get("negative",False):
    #   cv_res["negative_negative"] += 1

    return plus_rate, minus_rate

#sanity check:
#check_hypothesis(plus_examples, minus_examples, plus_examples[3])

(plus, minus, unknown) = importdata('6')
i = 0
for elem in unknown:
    #print elem

    i += 1
    ans = check_hypothesis(plus, minus, elem)
    print(i, elem[-1], ans)
    #print(ans[0])
#    if i == 3: break
print(cv_res)
