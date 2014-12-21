__author__ = 'Marat Bakiev'

#import sys

#print(str(sys.argv[1]))

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

example = ['x','x','x','x','o','o','x','o','o','positive']

a = set([i+':'+str(k) for i,k in zip(attrib_names,example)])

print(a)