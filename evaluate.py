__author__ = 'Sarath'

import numpy
import math
from sklearn import svm
from sklearn.metrics import accuracy_score
import sys

def svm_classifier(train_x, train_y, valid_x, valid_y, test_x, test_y):

    clf = svm.LinearSVC()
    clf.fit(train_x,train_y)
    pred = clf.predict(valid_x)
    va = accuracy_score(numpy.ravel(valid_y),numpy.ravel(pred))
    pred = clf.predict(test_x)
    ta = accuracy_score(numpy.ravel(test_y),numpy.ravel(pred))
    return va, ta


    
def tf(view1,view2,labels):

    perp = int(len(view1)/5)

    print ("view1 to view2")

    acc = 0
    for i in range(0,5):
        test_x = view2[i*perp:(i+1)*perp]
        test_y = labels[i*perp:(i+1)*perp]
        if i==0:
            train_x = view1[perp:len(view1)]
            train_y = labels[perp:len(view1)]
        elif i==4:
            train_x = view1[0:4*perp]
            train_y = labels[0:4*perp]
        else:
            train_x1 = view1[0:i*perp]
            train_y1 = labels[0:i*perp]
            train_x2 = view1[(i+1)*perp:len(view1)]
            train_y2 = labels[(i+1)*perp:len(view1)]
            train_x = numpy.concatenate((train_x1,train_x2))
            train_y = numpy.concatenate((train_y1,train_y2))
        va, ta = svm_classifier(train_x, train_y, test_x, test_y, test_x, test_y)
        acc += ta
    print (acc/5)


#detfile = open("res/tl_12.txt", "a")

#detfile.write(str(acc/5) + "\n")
#detfile.close()

    print ("view2 to view1")

    acc = 0
    for i in range(0,5):
        test_x = view1[i*perp:(i+1)*perp]
        test_y = labels[i*perp:(i+1)*perp]
        if i==0:
            train_x = view2[perp:len(view1)]
            train_y = labels[perp:len(view1)]
        elif i==4:
            train_x = view2[0:4*perp]
            train_y = labels[0:4*perp]
        else:
            train_x1 = view2[0:i*perp]
            train_y1 = labels[0:i*perp]
            train_x2 = view2[(i+1)*perp:len(view1)]
            train_y2 = labels[(i+1)*perp:len(view1)]
            train_x = numpy.concatenate((train_x1,train_x2))
            train_y = numpy.concatenate((train_y1,train_y2))
        va, ta = svm_classifier(train_x, train_y, test_x, test_y, test_x, test_y)
        acc += ta
    print (acc/5)

def transfer_learning_5fold(folder):

    view1 = numpy.load(folder+"test-view1.npy")
    view2 = numpy.load(folder+"test-view2.npy")
    labels = numpy.load(folder+"test-labels.npy")
    tf(view1,view2,labels)
def tl_12(folder1,folder2):
    view1 = numpy.load(folder1+"test-view1.npy")
    view2 = numpy.load(folder2+"test-view2.npy")
    labels = numpy.load(folder1+"test-labels.npy")
    tf(view1,view2,labels)
def tl_11(folder1,folder2):
    view1 = numpy.load(folder1+"test-view1.npy")
    view2 = numpy.load(folder2+"test-view1.npy")
    labels = numpy.load(folder1+"test-labels.npy")
    tf(view1,view2,labels)
def tl_22(folder1,folder2):
    view1 = numpy.load(folder1+"test-view2.npy")
    view2 = numpy.load(folder2+"test-view2.npy")
    labels = numpy.load(folder1+"test-labels.npy")
    tf(view1,view2,labels)
    



def compute_corr(x,y):
    corr = 0
    for i in range(0,len(x[0])):
        x1 = x[:,i] - (numpy.ones(len(x))*(sum(x[:,i])/len(x)))
        x2 = y[:,i] - (numpy.ones(len(y))*(sum(y[:,i])/len(y)))
        nr = sum(x1 * x2)/(math.sqrt(sum(x1*x1))*math.sqrt(sum(x2*x2)))
        corr+=nr
    print (corr)

#
#    detfile = open("res/corr_valid.txt", "a")
#
#    detfile.write(str(corr) + "\n")
#    detfile.close()


#    detfile = open("res/corr_test.txt","a")
#
#    detfile.write(str(corr) + "\n")
#    detfile.close()
def correlation(folder):
    print ("validation correlation")
    x = numpy.load(folder+"valid-view1.npy")
    y = numpy.load(folder+"valid-view2.npy")
    print x.shape,y.shape
    compute_corr(x,y)
    print ("test correlation")
    x = numpy.load(folder+"test-view1.npy")
    y = numpy.load(folder+"test-view2.npy")
    compute_corr(x,y)

def corr_12(folder1, folder2):
    print ("validation correlation")
    x = numpy.load(folder1+"valid-view1.npy")
    
    y = numpy.load(folder2+"valid-view2.npy")
    print x.shape,y.shape
    compute_corr(x,y)

    print ("test  correlation ")
    x = numpy.load(folder1+"test-view1.npy")
    y = numpy.load(folder2+"test-view2.npy")
    compute_corr(x,y)
def corr_11(folder1, folder2):
    print ("validation correlation ")
    x = numpy.load(folder1+"valid-view1.npy")
    y = numpy.load(folder2+"valid-view1.npy")
    compute_corr(x,y)

    print ("test  correlation ")
    x = numpy.load(folder1+"test-view1.npy")
    y = numpy.load(folder2+"test-view1.npy")
    compute_corr(x,y)
def corr_22(folder1, folder2):
    print ("validation correlation ")
    x = numpy.load(folder1+"valid-view2.npy")
    y = numpy.load(folder2+"valid-view2.npy")
    compute_corr(x,y)

    print ("test  correlation ")
    x = numpy.load(folder1+"test-view2.npy")
    y = numpy.load(folder2+"test-view2.npy")
    compute_corr(x,y)
    

job = sys.argv[1]

if job=="tl":
    transfer_learning_5fold(sys.argv[2]+"project/")
elif job=="corr":
    correlation(sys.argv[2]+"project/")
elif job=="tl12":
    tl_12(sys.argv[2]+"project/",sys.argv[3]+"project/")
elif job=="corr12":
    corr_12(sys.argv[2]+"project/",sys.argv[3]+"project/")
elif job=="tl11":
    tl_11(sys.argv[2]+"project/",sys.argv[3]+"project/")
elif job=="corr11":
    corr_11(sys.argv[2]+"project/",sys.argv[3]+"project/")
elif job=="corr22":
    corr_22(sys.argv[2]+"project/",sys.argv[3]+"project/")
elif job=="tl22":
    tl_22(sys.argv[2]+"project/",sys.argv[3]+"project/")

