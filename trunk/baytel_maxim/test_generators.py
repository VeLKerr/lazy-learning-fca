
import pprint

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
    return set([i+':'+str(k) for i,k in zip(attrib_names,example)])


def classification(context_plus, context_minus, unknown,alpha,res):
    for elem in unknown:
        check_hypothesis(context_plus, context_minus, elem,alpha,res)
    return res

    
def check_hypothesis(context_plus, context_minus,example,alpha,res):
  #  print example
    eintent = make_intent(example)
  #  print eintent
    eintent.discard('class:positive')
    eintent.discard('class:negative')

    posVotes=0
    negVotes=0

    for e in context_plus:
        ei = make_intent(e)
        candidate_intent = ei & eintent #перечечение ? с объектом положительного контекста

        #пересечение мало - не будем ничего с ним делать...
        if len(candidate_intent) < alpha * len(eintent):
            continue

        countPosObjs=0

        for key in context_plus:
            if len(make_intent(key) & candidate_intent) == len(candidate_intent):
                countPosObjs+=1

        countNegObjs=0
        for key in context_minus:
            if len(make_intent(key) & candidate_intent) == len(candidate_intent):
                countNegObjs+=1

        if countPosObjs > countNegObjs:
            posVotes += 1

    for e in context_minus:
        ei = make_intent(e)
        candidate_intent = ei & eintent #перечечение ? с объектом положительного контекста

        #пересечение мало - не будем ничего с ним делать...
        if len(candidate_intent) < alpha * len(eintent):
            continue

        countPosObjs=0

        for key in context_plus:
            if len(make_intent(key) & candidate_intent) == len(candidate_intent):
                countPosObjs+=1

        countNegObjs=0
        for key in context_minus:
            if len(make_intent(key) & candidate_intent) == len(candidate_intent):
                countNegObjs+=1

        if countNegObjs > countPosObjs:
            negVotes += 1

    if posVotes == negVotes:
        if posVotes > 0:
            res["contradictory"] += 1
        else:
            res["not_classified"] += 1
    else:
        if negVotes < posVotes:
            predicted_class = "positive"
            if predicted_class == example[-1]:
                res["positive_positive"] += 1
            else:
                res["negative_positive"] += 1
        else:
            predicted_class = "negative"
            if predicted_class == example[-1]:
                res["negative_negative"] += 1
            else:
                res["positive_negative"] += 1

def statistics(results):
    count = len(results)
    res={}

    res['Sensitivity (TPR) of the procedure is ']           = 0
    res['Fall-out (FPR) of the procedure is ']              = 0
    res['Precision (PPV) of the procedure is ']             = 0
    res['False omission rate (FOR) of the procedure is ']   = 0
    res['Accuracy of the procedure is ']                    = 0

    for element in results:

        res['Sensitivity (TPR) of the procedure is ']           += element['positive_positive']/(element['positive_positive'] + element['positive_negative'])
        res['Fall-out (FPR) of the procedure is ']              += element['negative_positive']/(element['negative_negative'] + element['negative_positive'])
        res['Precision (PPV) of the procedure is ']             += element['positive_positive']/(element['positive_positive'] + element['negative_positive'])
        res['False omission rate (FOR) of the procedure is ']   += element['positive_negative']/(element['positive_negative'] + element['negative_negative'])
        res['Accuracy of the procedure is ']                    += (element['positive_positive'] + element['negative_negative'])/(element['positive_positive'] + element['positive_negative'] + element['negative_positive'] + element['negative_negative'])

    resPercentage={}

    for key in res:
        resPercentage[key] = str(round(res[key]*100/count,2))+'%'

    return resPercentage

results = []

alpha=0.3

for index in range(1,11):

    cv_res = \
        {
            "positive_positive": 0,
            "positive_negative": 0,
            "negative_positive": 0,
            "negative_negative": 0,
            "contradictory": 0,
            "not_classified": 0,
    }

    q=open("data/train"+str(index)+".csv","r")
    train = [ a.strip().split(",") for a in q]
    plus = [a for a in train if a[-1]=="positive"]
    minus = [a for a in train if a[-1]=="negative"]
    q.close()

    w=open("data/test"+str(index)+".csv","r")
    unknown = [a.strip().split(",") for a in w]

    print('unknown len=',len(unknown))

    w.close()
    unknown.pop(0)
    results.append(classification(plus, minus, unknown,alpha,cv_res))


pprint.pprint(results)

stats = statistics(results)

pprint.pprint(stats)