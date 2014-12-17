'''
rule 4:
сумма квадратов достоверностей, но прибавляем достоверность только если она больше порога min_conf
if conf_plus[i]>min_conf -> conf_plus+=conf_plus[i] 

'''
import pprint
import sys
import functools
import math
import numpy
import random


q=open("train.txt","r")
train = [ a.strip().split(",") for a in q]
plus = [a for a in train if a[0]=="1"]
minus = [a for a in train if a[0]=="0"]
#print (plus)
#print (minus)
#print t
q.close()
w=open("test.txt","r")
unknown = [a.strip().split(",") for a in w]
w.close()

min_conf=0.87

cv_res = {
 "1_1": 0,
 "1_0": 0,
 "0_1": 0,
 "0_0": 0,
 "contradictory": 0,
}

attrib_names = [
'OVERALL',
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
  #  print example
    eintent = make_intent(example)
  #  print eintent
    eintent.discard('OVERALL:1')
    eintent.discard('OVERALL:0')
    labels = {0:0,1:0}
    cand_intents=[]
    global cv_res
    conf_plus=0
    conf_minus=0
    for e in context_plus+context_minus:
        gi=make_intent(e)
        candidate_intent=gi&eintent
        if not candidate_intent in cand_intents:
            cand_intents.append(candidate_intent)
            closure_plus=[make_intent(i) for i in context_plus if make_intent(i).issuperset(candidate_intent)]
            closure_minus=[make_intent(i) for i in context_minus if make_intent(i).issuperset(candidate_intent)]
            conf_plus_new=len(closure_plus)/(len(closure_plus)+len(closure_minus))
            if (conf_plus_new>min_conf):
                conf_plus+=pow(conf_plus_new,2)
            if (1-conf_plus_new>min_conf):
                conf_minus+=pow(1-conf_plus_new,2)
            #print ('conf_plus=',conf_plus)
            #print ('conf_minus=',conf_minus)
            
    if (conf_minus>conf_plus):
        labels['class']=0
    else:
        if (conf_plus>=conf_minus):
            labels['class']=1
    
    #print (eintent)
    #print (labels)
    if labels['class']=='?':
       cv_res["contradictory"] += 1
       return
    if example[0] == "1" and labels['class']==1:
       cv_res["1_1"] += 1
    if example[0] == "0" and labels['class']==1:
       cv_res["0_1"] += 1
    if example[0] == "1" and labels['class']==0:
       cv_res["1_0"] += 1
    if example[0] == "0" and labels['class']==0:
       cv_res["0_0"] += 1

#sanity check:
#check_hypothesis(plus_examples, minus_examples, plus_examples[3])
full=train+unknown
#print(full)

lenFull=len(full)
lenUnc=math.trunc(0.1*lenFull)
print('lenFull=',len(full))
print('lenUnk=',lenUnc)

accuracy=[]
precision=[]
sensitivity=[]
specificity=[]
F1=[]
NPV=[]
for t in range(10):
    cv_res = {
     "1_1": 0,
     "1_0": 0,
     "0_1": 0,
     "0_0": 0,
     "contradictory": 0,
    }
    train=full.copy()
    randPos=[]
    unknown=[]
    
    while len(randPos)<lenUnc:
        y=random.randint(0,lenFull-1)
        if not y in randPos:
            unknown.append(full[y])
            randPos.append(y)
            train.remove(full[y])
    plus = [a for a in train if a[0]=="1"]
    minus = [a for a in train if a[0]=="0"]
    i = 0
    for elem in unknown:
        #print elem
        #print ("done")
        i += 1
        check_hypothesis(plus, minus, elem)
    #    if i == 3: break
    print (cv_res)
    TP=cv_res['1_1']
    TN=cv_res['0_0']
    FP=cv_res['0_1']
    FN=cv_res['1_0']
    accuracy.append((TP+TN)/(TP+TN+FP+FN))
    if TP+FP>0:
        precision.append(TP/(TP+FP))
    else:
        print('Pricision inf!')
    if TP+FN>0:
        sensitivity.append(TP/(TP+FN))
    else:
        print('Sens inf!')
    if FP+FN>0:
        specificity.append(TN/(FP+TN))
    else:
        print('Spec inf!')
    F1.append(2*TP/(2*TP+FP+FN))
    if TN+FN>0:
        NPV.append(TN/(TN+FN))
    else:
        print('NPV inf!')
print('min conf=',min_conf,'\n',
          'accuracy=(TP+TN)/(TP+TN+FP+FN)=',numpy.mean(accuracy),'\n',
          'Precision=TP/(TP+FP)=',numpy.mean(precision),'\n',
          'Sensitivity=TN/(TN+FN)=',numpy.mean(sensitivity),'\n',
          'Specificity=TN/(FP+TN)=',numpy.mean(specificity),'\n',
          'F1=2*TP/(2*TP+FP+FN)=',numpy.mean(F1),'\n',
          'NPV=TN/(TN+FN)=',numpy.mean(NPV))
