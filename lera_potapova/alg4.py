import pprint
import sys
import functools

index = 1

q=open("C:\\lazy-learning-fca\\lera_potapova\\train10.csv","r")
train = [ a.strip().split(",") for a in q]
plus = [a for a in train if a[-1]=="positive"]
minus = [a for a in train if a[-1]=="negative"]

#print t
q.close()
w=open("C:\\lazy-learning-fca\\lera_potapova\\test10.csv","r")
unknown = [a.strip().split(",") for a in w]
w.close()

def phi(Group,obj):
    closure=[0]*9
    for i in range(9):
        B=0
        O=0
        X=0
        for j in range(len(obj)):
            if Group[obj[j]][i]=='b':
                B=B+1
            if Group[obj[j]][i]=='o':
                O=O+1
            if Group[obj[j]][i]=='x':
                X=X+1
        if B==len(obj):
            closure[i]='b'
        if O==len(obj):
            closure[i]='o'
        if X==len(obj):
            closure[i]='x'

    return closure

def psi(Group, closure):
    gen_obj=[]
    for i in range(10):
        C=0
        for j in range(9):
            if Group[i][j]==closure[j] or closure[j]==0:
                C=C+1
        if C==9:
            gen_obj=gen_obj+[0]
            gen_obj[-1]=i
    return gen_obj

def check(hypothesis,example):
    C=0
    for j in range(9):
        if hypothesis[j]==example[j] or hypothesis[j]==0:
            C=C+1
    if C==9:
        return 1
    else:
        return 0

def build_hypothesis(plus_context, minus_context):
    #разделим +контекст на группки по 10 элементов, и будем искать там гипотезы.
    #это делается для того, чтобы программа хотя бы сегодня закончила работу.
    i=0
    Plus_Hypothesis=[]
    while i<len(plus_context)-10:
        Group=[0]*10
        for j in range(10):
            Group[j]=plus_context[i+j+1]
        #сделали группу. Теперь надо внутри найти гипотезы
        k=1
        while k<1024:
            n=''
            N=k
            while k>0:
                y=str(k % 2)
                n=y + n
                k=int(k/2)
            if len(n)!=10:
                s=10-len(n)
                n='0'*s+n
            obj=[]
            for s in range(len(n)):
                if n[s]=='1':
                    obj=obj+[0]
                    obj[len(obj)-1]=s
            #выбрали подмножество в группе
            if obj!=[]:
                closure=phi(Group, obj)
                gen_obj=psi(Group,closure)
                T=0
                if len(obj)==len(gen_obj):
                    for s in range(len(obj)):
                        if obj[s]==gen_obj[s]:
                            T=T+1
                if T==len(obj):
                    Plus_Hypothesis=Plus_Hypothesis+[0]
                    Plus_Hypothesis[len(Plus_Hypothesis)-1]=closure
            k=N+1
            #нашли гипотезы в группе.
        i=i+10
    #нашли все такие маленькие положительные гипотезы
    #надо проверить, фальсифицируются ли они
    i=0
    True_plus_hypothesis=[]
    for i in range(len(Plus_Hypothesis)):
        C=0
        for elem in minus_context:
            C=check(Plus_Hypothesis[i],elem)
        if C==0:
            True_plus_hypothesis=True_plus_hypothesis+[0]
            True_plus_hypothesis[len(True_plus_hypothesis)-1]=Plus_Hypothesis[i]
    #теперь есть все хорошие гипотезы. Надо найти все плохие.
    i=0
    Minus_Hypothesis=[]
    while i<len(minus_context)-10:
        Group=[0]*10
        for j in range(10):
            Group[j]=minus_context[i+j+1]
        #сделали группу. Теперь надо внутри найти гипотезы
        k=0
        while k<1024:
            n=''
            N=k
            while k>0:
                y=str(k % 2)
                n=y + n
                k=int(k/2)
            if len(n)!=10:
                s=10-len(n)
                n='0'*s+n
            obj=[]
            for s in range(len(n)):
                if n[s]=='1':
                    obj=obj+[0]
                    obj[len(obj)-1]=s
            #выбрали подмножество в группе
            if obj!=[]:
                closure=phi(Group, obj)
                gen_obj=psi(Group,closure)
                T=0
                if len(obj)==len(gen_obj):
                    for s in range(len(obj)):
                        if obj[s]==gen_obj[s]:
                            T=T+1
                if T==len(obj):
                    Minus_Hypothesis=Minus_Hypothesis+[0]
                    Minus_Hypothesis[len(Minus_Hypothesis)-1]=closure
            k=N+1
            #нашли гипотезы в группе.
        i=i+10

    #нашли все такие маленькие положительные гипотезы
    #надо проверить, фальсифицируются ли они
    i=0
    True_minus_hypothesis=[]
    for i in range(len(Minus_Hypothesis)):
        C=0
        for elem in plus_context:
            C=check(Minus_Hypothesis[i],elem)
        if C==0:
            True_minus_hypothesis=True_minus_hypothesis+[0]
            True_minus_hypothesis[len(True_minus_hypothesis)-1]=Minus_Hypothesis[i]
    #Ура, есть положительные и отрицательные гипотезы. Теперь они будут голосоватm
    return [True_plus_hypothesis, True_minus_hypothesis]

#Все функции дописаны, теперь осталось проверить
[Plus,Minus]=build_hypothesis(plus,minus)
Q=0
for example in unknown:
    S_plus=0
    S_minus=0
    for i in range(len(Plus)):
        C=0
        C=check(Plus[i],example)
        if C==0:
            S_plus=S_plus+1

    for i in range(len(Minus)):
        C=0
        C=check(Minus[i],example)
        if C==0:
            S_minus=S_minus+1

    S_plus=S_plus/len(Plus)
    S_minus=S_minus/len(Minus)
    if S_plus>S_minus:
        print(example)
        print ("It is positive")
        if example[-1]=="positive":
            Q=Q+1
    if S_plus<S_minus:
        print(example)
        print("It is negative")
        if example[-1]=="positive":
            Q=Q+1
Q=Q/len(unknown)
print(Q)
