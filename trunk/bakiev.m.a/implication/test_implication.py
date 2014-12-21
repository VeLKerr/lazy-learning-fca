import pprint
import sys

#index = sys.argv[1]
index = 1

q=open("train"+index+".csv","r")
train = [ a.strip().split(",") for a in q]
plus = [a for a in train if a[-1]=="positive"]
minus = [a for a in train if a[-1]=="negative"]

#print t
q.close()
w=open("test"+index+".csv","r")
unknown = [a.strip().split(",") for a in w]
w.close()


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


cv_res = {
 "positive_positive": 0,
 "positive_negative": 0,
 "negative_positive": 0,
 "negative_negative": 0,
 "contradictory": 0,
}
    
def check_hypothesis(context_plus, context_minus, example):
    global cv_res
    eintent = make_intent(example)
    big_context = context_plus + context_minus
    labels = {}
    for e in big_context:
        ei = make_intent(e)
        candidate_intent = ei&eintent
        if not candidate_intent:
            continue
        #print 'candidate_intent'
        #print candidate_intent
        closure = [ make_intent(i) for i in big_context if make_intent(i).issuperset(candidate_intent)] 
#        print 'closure:'
#        print closure
        res = reduce(lambda x,y: x&y if x&y else x|y, closure)
        #print 'reduced:'
        #print res
        for cs in ['positive','negative']:
            if 'class:'+cs in res:
                labels[cs] = True
                labels[cs+'_res'] = candidate_intent
        
                #print 'classified as %s, reason:' % cs
                #print candidate_intent
                #print res
#    print labels
    if labels.get("positive",False) and labels.get("negative",False):
       cv_res["contradictory"] += 1
       return
    if example[-1] == "positive" and labels.get("positive",False):
       cv_res["positive_positive"] += 1
    if example[-1] == "negative" and labels.get("positive",False):
       cv_res["negative_positive"] += 1
    if example[-1] == "positive" and labels.get("negative",False):
       cv_res["positive_negative"] += 1
    if example[-1] == "negative" and labels.get("negative",False):
       cv_res["negative_negative"] += 1

    '''closure = []
    for candidate in context:
        cintent = make_intent(candidate)
        closure.append(cintent&eintent)
        if cintent.issubset(eintent):
            print "classified!"
            print cintent
            print eintent
    '''
#sanity check:
#check_hypothesis(plus_examples, minus_examples, plus_examples[3])

for elem in unknown:
#    print elem
    print("done")
    check_hypothesis(plus, minus, elem)

print(cv_res)
