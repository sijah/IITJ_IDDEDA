# -*- coding: utf-8 -*-
"""DesignProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vXAOjVsvgsvxItAZgeu-WIKjEZnCRmHn

##INPUT:
"""

import re

inputs = []
outputs = {}
circuit = []
path = input("Enter path to input file: ")

with open(path) as f:

    line = f.readline()
    while line[0] == "#":
        line = f.readline()
    line = f.readline()

    while line.strip() != '':
        k = line[6:]
        k = k[:len(k)-2]
        inputs.append(k)
        line = f.readline()
    line = f.readline()

    while line.strip() != '':
        k = line[7:]
        k = k[:len(k)-2]
        outputs[k] = 1
        line = f.readline()
    line = f.readline()

    while line.strip() != '':
        l = re.split("\W+", line)
        l.remove('')
        circuit.append(l)
        line = f.readline()

print(inputs)
print(list(outputs.keys()))
print(circuit)

"""##Utilary Functions:"""

def createSubExp(x):

    l = []

    if x[1] == "NOT":
        return str("(" + "!" + x[0] + "+" + "!" + x[2] + ")" + "(" + x[0] + "+" + x[2] + ")")
    elif x[1] == "OR":
        m = [str("(!"+x[0]), ")"]
        for i in range(2, len(x)):
            l.append(str("(" + x[0] + "+" + "!" + x[i] + ")"))
            m.insert(-1, str("+"+x[i]))
        l.append(''.join(m))
        s = ''.join(l)
    elif x[1] == "AND":
        m = [str("("+x[0]), ")"]
        for i in range(2, len(x)):
            l.append(str("(" + "!" + x[0] + "+" + x[i] + ")"))
            m.insert(-1, str("+!"+x[i]))
        l.append(''.join(m))
        s = ''.join(l)
    elif x[1] == "NOR":
        m = [str("("+x[0]), ")"]
        for i in range(2, len(x)):
            l.append(str("(!" + x[0] + "+" + "!" + x[i] + ")"))
            m.insert(-1, str("+"+x[i]))
        l.append(''.join(m))
        s = ''.join(l)
    elif x[1] == "NAND":
        m = [str("(!"+x[0]), ")"]
        for i in range(2, len(x)):
            l.append(str("(" + x[0] + "+" + x[i] + ")"))
            m.insert(-1, str("+!"+x[i]))
        l.append(''.join(m))
        s = ''.join(l)
    elif x[1] == "XOR":
        return str("(" + "!" + x[2] + "+" + "!" + x[3] + "+" + "!" + x[0] + ")" + "(" + x[2] + "+" + x[3] + "+" + "!" + x[0] + ")" + "(" + "!" + x[2] + "+" + x[3] + "+" + x[0] + ")" + "(" + x[2] + "+" + "!" + x[3] + "+" + x[0] + ")")
    elif x[1] == "XNOR":
        return str("(" + "!" + x[2] + "+" + "!" + x[3] + "+" + x[0] + ")" + "(" + x[2] + "+" + x[3] + "+" + x[0] + ")" + "(" + "!" + x[2] + "+" + x[3] + "+" + "!" + x[0] + ")" + "(" + x[2] + "+" + "!" + x[3] + "+" + "!" + x[0] + ")")
    return s
    
def setOuputsinCNF(d):
    lis = []
    for i in d:
        if d[i] == 0:
            lis.append(str("(" + "!" + i + ")"))
        else:
            lis.append(str("(" + i + ")"))
    return ''.join(lis)

def dplltoanswer(p,q):
    d = {}
    for i in inputs:
        if q[i] in p:
            d[i] = 1
        elif -q[i] in p:
            d[i] = 0
        else:
            d[i] = 1
    return d

def removeElements(l,listOfElements):
    l2=[]
    for i in l:
        if i not in listOfElements:
            l2.append(i)
    return l2

def pos(s,d):
    temp = []
    b = []
    l = []
    k = 1
    v = 1
    for i in s:
        if i=='(':
            continue
        elif i.isalnum():
            temp.append(i)
        elif i=='!':
            k = -1
        elif i == ')' or '+':
            j = ''.join(temp)
            if j not in d:
                d[j] = v
                v = v + 1
            b.append(k*d[j])
            k = 1
            temp = []
            if i == ')':
                l.append(b)
                b = []
    return l

"""#DPLL:"""

def internal_dpll(l,s,a=-1,k=True,answers=[]):
    global Answers
    pol=1
    elements=[]
    if(a==len(s)):
        return
    elif(a>=0):
        if k:
            pol=1
        else :
            pol=pol*-1
        for i in l:
            if s[a]*pol in i:
                elements.append(i)
            elif s[a]*pol*-1 in i:
                #print("f",s[a]*pol*-1)
                if (s[a]*pol*-1)<0 and (s[a]*pol==max(abs(min(i)),abs(max(i)))):
                    return
                if (s[a]*pol*-1)>0 and (s[a]*pol*-1==max(abs(min(i)),abs(max(i)))):
                    return
                else:
                    continue
    l2=removeElements(l,elements)
    if(l2==[]):
        #print(answers[1:]+[s[a]*pol])
        Answers.append(answers[1:]+[s[a]*pol])
        return
    else:
        #a2=answers+[s[a]*pol]
        #print(l2)
        internal_dpll(l2,s,a+1,True,answers+[s[a]*pol]) 
        internal_dpll(l2,s,a+1,False,answers+[s[a]*pol]) 
        return

def DPLL(l,final_list=[]):
    count={}
    mySet=set()
    #unit propogation
    for i in reversed(l):
        if(len(i)==1):
            final_list.append(i[0])
    
    for i in l:
        for j in i:
            if j in count:
                pass
            elif -1*j not in count:
                if j not in count:
                    count[j]=True
                elif(count[i]==False):
                    continue
            elif -1*j in count:
                count[-1*j]=False
    for i in count:
        if count[i]==True:
            final_list.append(i)
    deleteElements=[]
    for i in l:
        for j in i:
            if (j in final_list):
                deleteElements.append(i)
            elif(-1*j in final_list) :
                if type(i) == type(None): 
                  continue
                elif type(j) == type(None): 
                  continue
                else:
                  i=i.remove(j)
            else:
                mySet.add(abs(j))
    
    l=removeElements(l,deleteElements)
    if([] in l):
      print("Unsatisfiable")
      return
    internal_dpll(l,list(mySet),-1,True,[])

"""#SOLUTION:"""

import random
m = int(input("Set all output literal values randomly? :"))
if m==1:
  for i in outputs:
    outputs[i] = random.randint(0,1)
  print("Note: To see the values that are set, go to the end of the printed CNF formula of the circuit (right below)")
else:
  k = int(input("Set all output literal values to 1? :"))
  if k==0:
    for i in outputs:
      outputs[i] = int(input("Set the value of "+i+" :"))

rawCNF = [''.join([createSubExp(i) for i in circuit]), setOuputsinCNF(outputs)]

finalCNF = ''.join(rawCNF)

print(finalCNF)

d={}
Answers=[]
l = pos(finalCNF,d)
#print(l)
#print(d)
f=[]
DPLL(l,f)
if Answers==[]:
  print("UnSatisfiable")

for i in range(len(Answers)):
  print(dplltoanswer(Answers[i]+f,d))