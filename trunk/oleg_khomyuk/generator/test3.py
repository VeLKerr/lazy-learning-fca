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


cv_res = {
    "TP": 0,
    "FN": 0,
    "FP": 0,
    "TN": 0,
    "?": 0,
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


def classify(context_plus, context_minus, example):
    eintent = make_intent(example)
    eintent.discard('class:positive')
    eintent.discard('class:negative')

    plus_rate = 0

    for e in context_plus:
        # Пересечение описания объекта с элементом плюс-контекста. Формирование гипотезы.
        candidate_intent = make_intent(e) & eintent

        # Мощность пересечения описания объекта с элементом плюс-контекста
        intent_power = len(candidate_intent) * 1.0 / len(eintent)

        # Поддержка плюс-гипотезы. Замыкание в плюс-контексте.
        closure_plus = [make_intent(obj) for obj in context_plus if make_intent(obj).issuperset(candidate_intent)]
        closure_plus_size = len(closure_plus)
        support = len(closure_plus) * 1.0 / len(context_plus)

        # Фальсифицируемость плюс-гипотезы - объекты минус-контекста, подходящие под описание текущей гипотезы.
        closure_minus = [make_intent(obj) for obj in context_minus if make_intent(obj).issuperset(candidate_intent)]
        closure_minus_size = len(closure_minus)
        falsif = closure_minus_size * 1.0 / len(context_minus)

        plus_rate += (intent_power > 0.6) * (support > falsif) * (support - falsif) * 100.0 / (len(context_plus))

    minus_rate = 0

    for e in context_minus:
        # Пересечение описания объекта с элементом минус-контекста. Формирование гипотезы.
        candidate_intent = make_intent(e) & eintent

        # Мощность пересечения описания объекта и элемента минус-контекста.
        intent_power = len(candidate_intent) * 1.0 / len(eintent)

        # Поддержка минус-гипотезы. Замыкание в минус-контексте.
        closure_minus = [make_intent(obj) for obj in context_minus if make_intent(obj).issuperset(candidate_intent)]
        closure_minus_size = len(closure_minus)
        support = len(closure_minus) * 1.0 / len(context_minus)

        # Фальсифицируемость минус-гипотезы - объекты плюс-контекста, подходящие под описание текущей гипотезы.
        closure_plus = [make_intent(obj) for obj in context_plus if make_intent(obj).issuperset(candidate_intent)]
        closure_plus_size = len(closure_plus)
        falsif = closure_plus_size * 1.0 / len(context_plus)

        minus_rate += (intent_power > 0.6) * (support > falsif) * (support - falsif) * 100.0 / len(context_minus)

    if plus_rate + minus_rate:
        p = (plus_rate - minus_rate)/(plus_rate + minus_rate)
        if abs(p) > 0.05:
            if p > 0:
                ans = 'positive'
            else:
                ans = 'negative'
        else:
            ans = '?'
    else:
        ans = '?'

    global cv_res

    if ans == '?':
        cv_res['?'] += 1
    if ans == 'positive':
        if example[-1] == 'positive':
            cv_res['TP'] += 1
        elif example[-1] == 'negative':
            cv_res['FP'] += 1
    elif ans == 'negative':
        if example[-1] == 'negative':
            cv_res['TN'] += 1
        elif example[-1] == 'positive':
            cv_res['FN'] += 1

    return ans, plus_rate, minus_rate


for exp in range(1, 11):
    (dplus, dminus, dunknown) = importdata(str(exp))
    i = 0
    for elem in dunknown:
        i += 1
        ans = classify(dplus, dminus, elem)
        print(exp, i, elem[-1], ans)

    print(cv_res)
