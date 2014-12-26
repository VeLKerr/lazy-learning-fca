import pprint

#k nearest neighbors method....


allDistances=set()

'''
def make_intent(example):
    global attrib_names
    return set([i+':'+str(k) for i,k in zip(attrib_names,example)])
'''

def classification(context_plus, context_minus, unknown,k,res):

    if k > len(context_plus) + len(context_minus):
        raise ValueError('K was chosen wrong')

    for elem in unknown:
        check_hypothesis(context_plus, context_minus, elem,k,res)
    return res

def check_hypothesis(context_plus, context_minus, example,k,res):

    examp=example.copy()

    example.pop()

    hdistanceListMap=dict()

    for e in context_plus:
        ee=e.copy()

        ee.pop()
        #считаем нашу метрику так, если соотв атрибуты совпадают - 0, если x b или o b - 1, если x o - 2
        #идея  втом, что б b менее категорично чем конкретное значение и следовательно надо считать разницу поменьше...
        distance=0
        for i,j in zip(example,ee):
            if i == j:
                continue
            if i=='b' or j=='b':
                distance += 1
            else:
                distance += 2

        allDistances.add(distance)

        if not distance in  hdistanceListMap:
            hdistanceListMap[distance]=[]

        tempList = hdistanceListMap[distance]
        tempList.append('+')

    for e in context_minus:
        ee=e.copy()

        ee.pop()
        #считаем нашу метрику так, если соотв атрибуты совпадают - 0, если x b или o b - 1, если x o - 2
        #идея  втом, что б b менее категорично чем конкретное значение и следовательно надо считать разницу поменьше...
        distance=0
        for i,j in zip(example,ee):
            if i == j:
                continue
            if i=='b' or j=='b':
                distance += 1
            else:
                distance += 2

        allDistances.add(distance)

        if not distance in  hdistanceListMap:
            hdistanceListMap[distance]=[]

        tempList = hdistanceListMap[distance]
        tempList.append('-')

    distances = sorted(hdistanceListMap.keys())

    totalCount = 0
    posCount=0
    negCount=0

    for dist in distances:
        tempList = hdistanceListMap[dist]

        for sign in tempList:
            if sign=='+':
                posCount+=1
            else:
                negCount+=1

        totalCount += len(tempList)

            #может возникнуть такая ситуация что у нас не один объект живет на определенном расстоянии,в том числе объекты разных знаков
            #в этом случае считаю все объекты и фактически получаю больше чем k ближайших соседей, но как ещё разгрести этот случай?
        if (totalCount >= k):
            break

    if posCount == negCount:
        res["contradictory"] += 1
    else:
        if negCount < posCount:
            predicted_class = "positive"
            if predicted_class == examp[-1]:
                res["positive_positive"] += 1
            else:
                res["negative_positive"] += 1
        else:
            predicted_class = "negative"
            if predicted_class == examp[-1]:
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

k=5

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
    results.append(classification(plus, minus, unknown,k,cv_res))


pprint.pprint(results)
stats = statistics(results)



pprint.pprint(stats)
pprint.pprint(allDistances)

