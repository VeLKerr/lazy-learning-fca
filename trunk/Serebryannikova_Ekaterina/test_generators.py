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
    labels = {}
    global cv_res
    for e in context_plus:
        ei = make_intent(e)
        candidate_intent = ei & eintent
        closure = [ make_intent(i) for i in context_minus if make_intent(i).issuperset(candidate_intent)]
        closure_size = len([i for i in closure if len(i)])
    #    print closure
        #print closure_size * 1.0 / len(context_minus)
        res = functools.reduce(lambda x,y: x&y if x&y else x|y, closure,set())
        #print('res=',res)
        for cs in ['0','1']:
            if 'OVERALL:'+cs in res:
                labels[cs] = True
                labels[cs+'_res'] = candidate_intent
                labels[cs+'_total_weight'] = labels.get(cs+'_total_weight',0) +closure_size * 1.0 / len(context_minus) / len(context_plus)
    for e in context_minus:
        ei = make_intent(e)
        candidate_intent = ei & eintent
        closure = [ make_intent(i) for i in context_plus if make_intent(i).issuperset(candidate_intent)]
        closure_size = len([i for i in closure if len(i)])
        #print closure_size * 1.0 / len(context_plus)
        res = functools.reduce(lambda x,y: x&y if x&y else x|y, closure,set())
        for cs in ['1','0']:
            if 'OVERALL:'+cs in res:
                labels[cs] = True
                labels[cs+'_res'] = candidate_intent
                labels[cs+'_total_weight'] = labels.get(cs+'_total_weight',0) +closure_size * 1.0 / len(context_plus) / len(context_minus)
    #print (eintent)
    #print (labels)
    if labels.get("0",False) and labels.get("1",False):
       cv_res["contradictory"] += 1
       return
    if example[0] == "1" and labels.get("1",False):
       cv_res["1_1"] += 1
    if example[0] == "0" and labels.get("1",False):
       cv_res["0_1"] += 1
    if example[0] == "1" and labels.get("0",False):
       cv_res["1_0"] += 1
    if example[0] == "0" and labels.get("0",False):
       cv_res["0_0"] += 1

#sanity check:
#check_hypothesis(plus_examples, minus_examples, plus_examples[3])
i = 0
for elem in unknown:
    #print elem
    #print ("done")
    i += 1
    check_hypothesis(plus, minus, elem)
#    if i == 3: break
print (cv_res)
