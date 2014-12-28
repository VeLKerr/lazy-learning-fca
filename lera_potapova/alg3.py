import pprint
import sys
import functools

index = 1

q=open("C:\\lazy-learning-fca\\lera_potapova\\train2.csv","r")
train = [ a.strip().split(",") for a in q]
plus = [a for a in train if a[-1]=="positive"]
minus = [a for a in train if a[-1]=="negative"]

#print t
q.close()
w=open("C:\\lazy-learning-fca\\lera_potapova\\test2.csv","r")
unknown = [a.strip().split(",") for a in w]
w.close()

def check_hypothesis(plus_context, minus_context, example):
    S_plus=0
    S_minus=0
    #пересекаем с плюс-контекстом по очереди
    for elem_plus in plus_context:
        closure=[0]*9 #заготовка для пересечения:
        for i in range(9):
            if elem_plus[i]==example[i]:
                closure[i]=elem_plus[i]
        #нашли замыкание, теперь смотрим, вкладывается ли оно в какой-то элемент из минус контекста
        #print(closure)
        T=0
        for i in range(len(closure)):
            if closure[i]!=0:
                T=T+1
        if T>=5:
            Vloz=0
            for elem_minus in minus_context:
                #проверяем на вхождение
                check=0
                for j in range(9):
                    if elem_minus[j]==closure[j] or closure[j]==0 :
                        check=check+1
                if check<9:
                #значит, не вкладывается
                    Vloz=Vloz+1
                if Vloz==len(minus_context):
                    S_plus=S_plus+1
    S_plus=S_plus/len(plus_context)
    for elem_minus in minus_context:
        closure=[0]*9 #заготовка для пересечения:
        for i in range(9):
            if elem_minus[i]==example[i]:
                closure[i]=elem_minus[i]
        #нашли замыкание, теперь смотрим, вкладывается ли оно в какой-то элемент из минус контекста
        T=0
        for i in range(len(closure)):
            if closure[i]!=0:
                T=T+1
        if T>=5:
            Vloz=0
            for elem_plus in plus_context:
                #проверяем на вхождение
                check=0
                for j in range(9):
                    if elem_plus[j]==closure[j] or closure[j]==0 :
                        check=check+1
                if check<9:
                #значит, не вкладывается
                    Vloz=Vloz+1
                if Vloz==len(plus_context):
                    S_minus=S_minus+1
    S_minus=S_minus/len(minus_context)
    Quality=0
    if S_plus>S_minus:
        print("It is positive")
        print("Really",example[-1])
        if example[-1]=="positive":
            Quality=Quality+1
    if S_plus<S_minus:
        print("It is negative")
        print("Really",example[-1])
        if example[-1]=="negative":
            Quality=Quality+1
    if S_plus==S_minus:
        print("I don't know, what it is")
    return Quality

Q=0
for elem in unknown:
    print (elem)
    Q=Q+check_hypothesis(plus, minus, elem)

Q=Q/len(unknown)
print(Q)

