import pprint
import sys

def metrik_potent(x,y):
    C = x.symmetric_difference(y)
    
def make_intent(example):
    global attrib_names
    
    return set([i+':'+str(k) for i,k in zip(attrib_names,example)])
   
def check_hypothesis(context_plus, context_minus, example,k):
    eintent = make_intent(example)
  
    eintent.discard('class:positive')
    eintent.discard('class:negative')
    distance = {};
    
    for e in context_plus:
        ei = make_intent(e)
        ei.discard('class:positive')
        ei.discard('class:negative')
        ## самый важный объект - центральная клетка
        metrik=((lambda x,y:  int(len(x.symmetric_difference(y))/2))(ei,eintent))
        if not metrik in distance:
            distance[metrik]=[]
        distance[metrik].append(1)

    for e in context_minus:
        ei = make_intent(e)
        ei.discard('class:positive')
        ei.discard('class:negative')
        ## самый важный объект - центральная клетка
##        metrik=((lambda x,y: (int(len(x.symmetric_difference(y))/2)))(ei,eintent))
        metrik=((lambda x,y:(int(len(x.symmetric_difference(y))/2)))(ei,eintent))
        if not metrik in distance:
            distance[metrik]=[]
        distance[metrik].append(-1)
    sdist = sorted(distance.keys())
    curLen = 0
    sumMetrik = 0
    for i in sdist:
##        sumMetrik += sum(distance[i])*(0.8**i)  ##экспоненциальный вес
##      sumMetrik +=sum                                          ##потенциальная функция
        sumMetrik += sum(distance[i])             ##классический knn
        curLen += len(distance[i])
        if curLen >= k:
            break
    
    global cv_res
    if sumMetrik==0:
       cv_res["contradictory"] += 1
       return
    if example[-1] == "positive" and sumMetrik>0:
       cv_res["positive_positive"] += 1
    if example[-1] == "negative" and sumMetrik>0:
       cv_res["negative_positive"] += 1
    if example[-1] == "positive" and sumMetrik<0:
       cv_res["positive_negative"] += 1
    if example[-1] == "negative" and sumMetrik<0:
       cv_res["negative_negative"] += 1

def statistics(results):
    count = len(results)
    res={}

    res['Sensitivity (TPR) of the procedure is ']           = 0
    res['Fall-out (FPR) of the procedure is ']              = 0
    res['Precision (PPV) of the procedure is ']             = 0
    res['False omission rate (FOR) of the procedure is ']   = 0
    res['Accuracy of the procedure is ']                    = 0
    
    for result in results:    
        res['Sensitivity (TPR) of the procedure is ']           += result['positive_positive']/(result['positive_positive'] + result['positive_negative'])
        res['Fall-out (FPR) of the procedure is ']              += result['negative_positive']/(result['negative_negative'] + result['negative_positive'])
        res['Precision (PPV) of the procedure is ']             += result['positive_positive']/(result['positive_positive'] + result['negative_positive'])
        res['False omission rate (FOR) of the procedure is ']   += result['positive_negative']/(result['positive_negative'] + result['negative_negative'])
        res['Accuracy of the procedure is ']                    += (result['positive_positive'] + result['negative_negative'])/(result['positive_positive'] + result['positive_negative'] + result['negative_positive'] + result['negative_negative'])

    resPercentage={}

    for key in res:
        resPercentage[key] = str(round(res[key]*100/count,2))+'%'

    return resPercentage

results = []
for index in range(1,11):
    index = str(index)
    ## считаем + и - контексты
    q=open("train"+index+".csv","r")
    train = [ a.strip().split(",") for a in q]
    plus = [a for a in train if a[-1]=="positive"]
    minus = [a for a in train if a[-1]=="negative"]

    q.close()
    w=open("test"+index+".csv","r")
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
        
    k = 11
    for elem in unknown:
        check_hypothesis(plus, minus, elem,k)
    results.append(cv_res)

stats = statistics(results)

pprint.pprint(results)
pprint.pprint(stats)
