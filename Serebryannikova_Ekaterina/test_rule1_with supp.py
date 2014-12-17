'''
rule 1:

#'+':conf((g'&g(i)')->'+')>min_conf
#'-':conf((g'&g(i)')->'-')>min_conf
#'+'>#'-' then '+' else '-'
'''
import pprint
import sys
import functools


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

min_conf=0.88
min_sup=0.1

cv_res = {
 "1_1": 0,
 "1_0": 0,
 "0_1": 0,
 "0_0": 0,
 "contradictory": 0,
}

#attrib_names = [ 'OVERALL','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','F13','F14','F15','F16','F17','F18','F19','F20','F21','F22' ]
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
            sup_plus=len(closure_plus)/len(context_plus)
            
            sup_minus=len(closure_minus)/len(context_minus)
            
            #print ('conf_plus=',conf_plus)
            #print ('conf_minus=',conf_minus)
            if conf_plus>=min_conf and sup_plus>=min_sup:
                labels[1]+=1
                #print('sup_plus=',sup_plus)
            if conf_minus>=min_conf and sup_minus>=min_sup:
                #print('sup_minus=',sup_minus)
                labels[0]+=1
    if (labels[0]>=labels[1]): #различие между rule 1.1 и rule 1.2
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
i = 0
for elem in unknown:
    #print elem
    print ("done")
    i += 1
    check_hypothesis(plus, minus, elem)
#    if i == 3: break
print (cv_res)
TP=cv_res['1_1']
TN=cv_res['0_0']
FP=cv_res['0_1']
FN=cv_res['1_0']
accuracy=(TP+TN)/(TP+TN+FP+FN)
precision=TP/(TP+FP)
sensitivity=TP/(TP+FN)
specificity=TN/(FP+TN)
F1=2*TP/(2*TP+FP+FN)
NPV=TN/(TN+FN)
print(' min_conf=',min_conf,'min_sup=',min_sup,'\n',
      'accuracy=(TP+TN)/(TP+TN+FP+FN)=',accuracy,'\n',
      'Precision=TP/(TP+FP)=',precision,'\n',
      'Sensitivity=TP/(TP+FN)=',sensitivity,'\n',
      'Specificity=TN/(FP+TN)=',specificity,'\n',
      'F1=2*TP/(2*TP+FP+FN)=',F1,'\n',
      'NPV=TN/(TN+FN)=',NPV)
