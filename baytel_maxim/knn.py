
#k nearest neighbors method....

cv_res = {
 "positive_positive": 0,
 "positive_negative": 0,
 "negative_positive": 0,
 "negative_negative": 0,
 "contradictory": 0,
 "not_classified": 0
}

#attrib_names = [ 'class','a1','a2','a3','a4','a5','a6' ]
attrib_names = [
'top-left-square',
'top-middle-square',
' top-right-square',
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

def classification(context_plus, context_minus, unknown,k):

    if k > len(context_plus) + len(context_minus):
        raise ValueError('K was chosen wrong')

    global cv_res
    cv_res["positive_positive"] = 0
    cv_res["positive_negative"] = 0
    cv_res["negative_positive"] = 0
    cv_res["negative_negative"] = 0
    cv_res["contradictory"] = 0
    cv_res["not_classified"] = 0
    for elem in unknown:
        check_hypothesis(context_plus, context_minus, elem,k)
    return cv_res

def check_hypothesis(context_plus, context_minus, example,k):
    eintent = make_intent(example)
    eintent.discard('class:positive')
    eintent.discard('class:negative')
    global cv_res

    hdistanceListMap=dict()

    for e in context_plus:
        ei = make_intent(e)
        ei.discard('class:positive')
        ei.discard('class:negative')

        temp = (ei|eintent) - (ei&eintent)
        hdistance = len(temp)/2 #из-за специфики нашей схемы кодирования если у одного объекта feature1= a
                                # другого feature1=b в temp будет {feature1:a,feature1:b} в тоже время по сути
                                # расстояние равно 1, правда для данного метода это не важно т.к. имеет значение лишь
                                # верность упорядочивания...

        allDistances.add(hdistance)

        if not hdistance in  hdistanceListMap:
            hdistanceListMap[hdistance]=[]

        tempList = hdistanceListMap[hdistance]
        tempList.append('+')

    for e in context_minus:
        ei = make_intent(e)
        ei.discard('class:positive')
        ei.discard('class:negative')
        temp = (ei|eintent) - (ei&eintent)
        hdistance = len(temp)/2

        if not hdistance in  hdistanceListMap:
            hdistanceListMap[hdistance]=[]

        tempList = hdistanceListMap[hdistance]
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
        cv_res["contradictory"] += 1
    else:
        if negCount < posCount:
            predicted_class = "positive"
            if predicted_class == example[-1]:
                cv_res["positive_positive"] += 1
            else:
                cv_res["negative_positive"] += 1
        else:
            predicted_class = "negative"
            if predicted_class == example[-1]:
                cv_res["negative_negative"] += 1
            else:
                cv_res["positive_negative"] += 1

def statistics(results,count):
    res={}
    res["positive_positive"] = 0
    res["positive_negative"] = 0
    res["negative_positive"] = 0
    res["negative_negative"] = 0
    res["contradictory"] = 0
    res["not_classified"] = 0
    for element in results:
        res["positive_positive"] += element["positive_positive"]
        res["positive_negative"] += element["positive_negative"]
        res["negative_positive"] += element["negative_positive"]
        res["negative_negative"] += element["negative_negative"]
        res["contradictory"] += element["contradictory"]
        res["not_classified"] += element["not_classified"]

    resPercentage={}

    for key in res:
        resPercentage[key] = str(round(res[key]*100/count,2))+'%'

    return resPercentage,res

results = []

#удивительно но с небольшими k (где-то до 15) нету ложных срабатываний и меньше процента противоричевых
#видимо что то не так

k=4

allUncnown = 0
for index in range(1,11):
    q=open("data/train"+str(index)+".csv","r")
    train = [ a.strip().split(",") for a in q]
    plus = [a for a in train if a[-1]=="positive"]
    minus = [a for a in train if a[-1]=="negative"]
    q.close()

    w=open("data/test"+str(index)+".csv","r")
    unknown = [a.strip().split(",") for a in w]

    allUncnown += len(unknown)
    w.close()
    unknown.pop(0)
    results.append(classification(plus, minus, unknown,k))

stats = statistics(results,allUncnown)
print(stats[0])

stats=stats[1]

print(stats)

print("min distances=",min(allDistances))

print('Sensitivity (TPR) of the procedure is ' + str(round(stats['positive_positive']/(stats['positive_positive'] + stats['positive_negative'])*100,2)) + '%')
print('Fall-out (FPR) of the procedure is ' + str(round(stats['negative_positive']/(stats['negative_negative'] + stats['negative_positive'])*100,2)) + '%')
print('Precision (PPV) of the procedure is ' + str(round(stats['positive_positive']/(stats['positive_positive'] + stats['negative_positive'])*100,2)) + '%')
print('False omission rate (FOR) of the procedure is ' + str(round(stats['positive_negative']/(stats['positive_negative'] + stats['negative_negative'])*100,2)) + '%')
print('Accuracy of the procedure is ' + str(round((stats['positive_positive'] + stats['negative_negative'])/(stats['positive_positive'] + stats['positive_negative'] + stats['negative_positive'] + stats['negative_negative'])*100,2)) + '%')