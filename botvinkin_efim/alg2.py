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
    return set([i+':'+str(k) for i,k in zip(attrib_names,example)])

def check_hypothesis(context_plus, context_minus, example):
    eintent = make_intent(example)
    eintent.discard('class:positive')
    eintent.discard('class:negative')
    positive=0
    negative=0
    global cv_res
    for e in context_plus:
        ei = make_intent(e)
        inter=ei&eintent
        x=0
        for int in inter:
            if int[-1]=='x':
                x=x+1
        if x>=3:
            positive=positive+1
    for e in context_minus:
        ei = make_intent(e)
        inter=ei&eintent
        o=0
        for int in inter:
            if int[-1]=='o':
                o=o+1
        if o>=3:
            negative=negative+1
    if positive==negative:
       cv_res["contradictory"] += 1
       return
    if example[-1] == "positive" and positive>negative:
       cv_res["positive_positive"] += 1
    if example[-1] == "negative" and positive>negative:
       cv_res["negative_positive"] += 1
    if example[-1] == "positive" and positive<negative:
       cv_res["positive_negative"] += 1
    if example[-1] == "negative" and positive<negative:
       cv_res["negative_negative"] += 1

sensitivity=0
specificity=0
precision=0
NPV=0
FPR=0
FDR=0
FNR=0
accuracy=0

for file in range(1,11):
    q=open("train"+str(file)+".csv","r")
    train = [a.strip().split(",") for a in q]
    plus = [a for a in train if a[-1]=="positive"]
    minus = [a for a in train if a[-1]=="negative"]

    q.close()
    w=open("test"+str(file)+".csv","r")
    unknown = [a.strip().split(",") for a in w]
    w.close()

    for elem in unknown:
        check_hypothesis(plus, minus, elem)
    TP=cv_res["positive_positive"]
    TN=cv_res["negative_negative"]
    FP=cv_res["negative_positive"]
    FN=cv_res["positive_negative"]
    sensitivity+=(TP/(TP+FN))/10
    specificity+=(TN/(FP+TN))/10
    precision+=(TP/(TP+FP))/10
    NPV+=(TN/(TN+FN))/10
    FPR+=(FP/(FP+TN))/10
    FDR+=(FP/(FP+TP))/10
    FNR+=(FN/(FN+TP))/10
    accuracy+=((TP+TN)/(TP+FN+FP+TN))/10
    cv_res["positive_positive"]=0
    cv_res["negative_negative"]=0
    cv_res["negative_positive"]=0
    cv_res["positive_negative"]=0
print("sensitivity="+str(sensitivity))
print("specificity="+str(specificity))
print("precision="+str(precision))
print("NPV="+str(NPV))
print("FPR="+str(FPR))
print("FDR="+str(FDR))
print("FNR="+str(FNR))
print("accuracy="+str(accuracy))

