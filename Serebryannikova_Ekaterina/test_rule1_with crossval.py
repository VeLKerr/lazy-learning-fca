'''
rule 1:

#'+':conf((g'&g(i)')->'+')>min_conf
#'-':conf((g'&g(i)')->'-')>min_conf
#'+'>#'-' then '+' else '-'
'''
import pprint
import sys
import functools
import random
import math
import numpy


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


min_conf=0.7



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
    for e in context_plus+context_minus:
        gi=make_intent(e)
        candidate_intent=gi&eintent
        if not candidate_intent in cand_intents:
            cand_intents.append(candidate_intent)
            closure_plus=[make_intent(i) for i in context_plus if make_intent(i).issuperset(candidate_intent)]
            closure_minus=[make_intent(i) for i in context_minus if make_intent(i).issuperset(candidate_intent)]
            conf_plus=len(closure_plus)/(len(closure_plus)+len(closure_minus))
            conf_minus=1-conf_plus
            #print ('conf_plus=',conf_plus)
            #print ('conf_minus=',conf_minus)
            if conf_plus>=min_conf:
                labels[1]+=1
            if conf_minus>=min_conf:
                labels[0]+=1
    if (labels[0]>labels[1]): #различие между rule 1.1 и rule 1.2
        labels['class']=0
    else:
        if (labels[1]>=labels[0]):
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
TP=[]
TN=[]
FP=[]
FN=[]

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
    TP.append(cv_res['1_1'])
    TN.append(cv_res['0_0'])
    FP.append(cv_res['0_1'])
    FN.append(cv_res['1_0'])
    '''accuracy=((TP[-1]+TN[-1])/(TP[-1]+TN[-1]+FP[-1]+FN[-1]))
    precision=(TP[-1]/(TP[-1]+FP[-1]))
    sensitivity=(TP[-1]/(TP[-1]+FN[-1]))
    specificity=(TN[-1]/(FP[-1]+TN[-1]))
    F1=(2*TP[-1]/(2*TP[-1]+FP[-1]+FN[-1]))
    NPV=(TN[-1]/(TN[-1]+FN[-1]))
    print('min conf=',min_conf,'\n',
          't=',t,'\n',
          'accuracy=(TP+TN)/(TP+TN+FP+FN)=',accuracy,'\n',
          'Precision=TP/(TP+FP)=',precision,'\n',
          'Sensitivity=TN/(TN+FN)=',sensitivity,'\n',
          'Specificity=TN/(FP+TN)=',specificity,'\n',
          'F1=2*TP/(2*TP+FP+FN)=',F1,'\n',
          'NPV=TN/(TN+FN)=',NPV)'''
tp=numpy.mean(TP)
tn=numpy.mean(TN)
fp=numpy.mean(FP)
fn=numpy.mean(FN)
accuracy=((tp+tn)/(tp+tn+fp+fn))
precision=(tp/(tp+fp))
sensitivity=(tp/(tp+fn))
specificity=(tn/(fp+tn))
F1=(2*tp/(2*tp+fp+fn))
NPV=(tn/(tn+fn))
print('min conf=',min_conf,'\n',
      'TP=',tp,'TN=',tn,'FP=',fp,'FN=',fn,'\n',
          'Средние значения','\n',
          'accuracy=(TP+TN)/(TP+TN+FP+FN)=',accuracy,'\n',
          'Precision=TP/(TP+FP)=',precision,'\n',
          'Sensitivity=TN/(TN+FN)=',sensitivity,'\n',
          'Specificity=TN/(FP+TN)=',specificity,'\n',
          'F1=2*TP/(2*TP+FP+FN)=',F1,'\n',
          'NPV=TN/(TN+FN)=',NPV)
