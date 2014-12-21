__author__ = 'Marat Bakiev'

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

def make_intent(example):
    global attrib_names
    return set([i+':'+str(k) for i,k in zip(attrib_names,example)])

def classification(context_plus, context_minus, unknown):
    global cv_res
    cv_res["positive_positive"] = 0
    cv_res["positive_negative"] = 0
    cv_res["negative_positive"] = 0
    cv_res["negative_negative"] = 0
    cv_res["contradictory"] = 0
    cv_res["not_classified"] = 0
    for elem in unknown:
        check_hypothesis(context_plus, context_minus, elem)
    return cv_res

def check_hypothesis(context_plus, context_minus, example):
    eintent = make_intent(example)
    eintent.discard('class:positive')
    eintent.discard('class:negative')
    global cv_res

    hdistance_plus = 0
    for e in context_plus:
        ei = make_intent(e)
        hdistance_plus += len(eintent) - len(eintent & ei)
    av_hdistance_plus = hdistance_plus/len(context_plus)

    hdistance_minus = 0
    for e in context_minus:
        ei = make_intent(e)
        hdistance_minus += len(eintent) - len(eintent & ei)
    av_hdistance_minus = hdistance_minus/len(context_minus)

    if av_hdistance_minus == av_hdistance_plus:
        cv_res["contradictory"] += 1
    else:
        if av_hdistance_plus < av_hdistance_minus:
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

def statistics(results):
    length = len(results)
    res = {}
    res["positive_positive"] = 0
    res["positive_negative"] = 0
    res["negative_positive"] = 0
    res["negative_negative"] = 0
    res["contradictory"] = 0
    res["not_classified"] = 0
    for element in results:
        res["positive_positive"] += element["positive_positive"]/length
        res["positive_negative"] += element["positive_negative"]/length
        res["negative_positive"] += element["negative_positive"]/length
        res["negative_negative"] += element["negative_negative"]/length
        res["contradictory"] += element["contradictory"]/length
        res["not_classified"] += element["not_classified"]/length

    return res

results = []

for index in range(1,11):
    q=open("train"+str(index)+".csv","r")
    train = [ a.strip().split(",") for a in q]
    plus = [a for a in train if a[-1]=="positive"]
    minus = [a for a in train if a[-1]=="negative"]
    q.close()

    w=open("test"+str(index)+".csv","r")
    unknown = [a.strip().split(",") for a in w]
    w.close()
    unknown.pop(0)
    results.append(classification(plus, minus, unknown))

stats = statistics(results)
print(stats)

print('Sensitivity (TPR) of the procedure is ' + str(round(stats['positive_positive']/(stats['positive_positive'] + stats['positive_negative'])*100,2)) + '%')
print('Fall-out (FPR) of the procedure is ' + str(round(stats['negative_positive']/(stats['negative_negative'] + stats['negative_positive'])*100,2)) + '%')
print('Precision (PPV) of the procedure is ' + str(round(stats['positive_positive']/(stats['positive_positive'] + stats['negative_positive'])*100,2)) + '%')
print('False omission rate (FOR) of the procedure is ' + str(round(stats['positive_negative']/(stats['positive_negative'] + stats['negative_negative'])*100,2)) + '%')
print('Accuracy of the procedure is ' + str(round((stats['positive_positive'] + stats['negative_negative'])/(stats['positive_positive'] + stats['positive_negative'] + stats['negative_positive'] + stats['negative_negative'])*100,2)) + '%')