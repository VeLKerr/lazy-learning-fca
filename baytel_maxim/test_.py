import pprint

#k nearest neighbors method....

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

allDistances=set()

def make_intent(example):
    global attrib_names
    return set([i+':'+str(k) for i,k in zip(attrib_names,example)])

def classification(context_plus, context_minus, unknown,res,alpha):
    for elem in unknown:
        check_hypothesis(context_plus, context_minus, elem,res,alpha)
    return res

def check_hypothesis(context_plus, context_minus, example,res,alpha):
    eintent = make_intent(example)
    eintent.discard('class:positive')
    eintent.discard('class:negative')

    totalPos=0
    totalNeg=0

    #как мера принадлежности к тому или другому классу будет выступать совокупное можность всех перечислений образца с
    # соотв классом, приведенная относительно мощности класса
    for e in context_plus:
        ei = make_intent(e)
        temp = ei&eintent
        if len(temp) < alpha*len(ei):
            continue
        totalPos += len(temp)

    for e in context_minus:
        ei = make_intent(e)
        temp = ei&eintent
        if len(temp) < alpha*len(ei):
            continue
        totalNeg += len(temp)

    global attrib_names

    totalPos /= ((len(attrib_names)-1)*len(context_plus))
    totalNeg /= ((len(attrib_names)-1)*len(context_minus))


    if totalPos == totalNeg:
        if totalPos>0.00001:
            res["contradictory"] += 1
        else:
            res["not_classified"] +=1
    else:
        if totalNeg < totalPos:
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

#удивительно но с небольшими k (где-то до 15) нету ложных срабатываний и меньше процента противоричевых
#видимо что то не так

alpha=0.7

for index in range(1,11):

    cv_res = \
        {
        "positive_positive": 0,
        "positive_negative": 0,
        "negative_positive": 0,
        "negative_negative": 0,
        "contradictory": 0,
        "not_classified": 0
        }


    q=open("data/train"+str(index)+".csv","r")
    train = [ a.strip().split(",") for a in q]
    plus = [a for a in train if a[-1]=="positive"]
    minus = [a for a in train if a[-1]=="negative"]
    q.close()

    w=open("data/test"+str(index)+".csv","r")
    unknown = [a.strip().split(",") for a in w]

    w.close()
    unknown.pop(0)
    results.append(classification(plus, minus, unknown,cv_res,alpha))


pprint.pprint(results)

stats = statistics(results)



pprint.pprint(stats)

