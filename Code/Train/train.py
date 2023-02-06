import cv2
import csv
import numpy as np
from sklearn import  svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle

def extract_hog_features(img):
    win_size = (28, 28)
    cell_size = (4, 4)
    block_size_in_cells = (2, 2)
    
    block_size = (block_size_in_cells[1] * cell_size[1], block_size_in_cells[0] * cell_size[0])
    block_stride = (cell_size[1], cell_size[0])
    nbins = 9  # Number of orientation bins
    hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, nbins)
    h = hog.compute(img)
    h = h.flatten()
    return h

def fetch_training_data(file_name):
    #INITIALIZATION
    trainFile = ("./"+file_name)
    labels = []
    hog_result = []
    img = np.array((28, 28), dtype=np.uint8)
    
    #READING FROM FILE
    with open(trainFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                labels.append(row[0])
                img = np.array(row[1:], dtype=np.uint8).reshape((28, 28))
                line_count += 1
                img = 255-img
                hog_result.append(extract_hog_features(img))
    
    #PREPARING TEST DATA
    hog_features = np.array(hog_result)
    labels = np.array(labels)
    train, test,train_labels, test_labels = train_test_split(hog_features, labels, train_size=0.8, random_state=42)
    return train, test,train_labels, test_labels


def train_svc(train, test,train_labels, test_labels):
    #INITIALIZATION
    clf = svm.SVC(max_iter=100)
    
    #TRAINING
    clf.fit(train, train_labels)
    score = clf.score(test, test_labels)*100
    
    #SAVING MODEL TO "SVC.sav"
    filename = 'SVC.sav'
    pickle.dump(clf, open(filename, 'wb'))

    print('SVM:')
    print('Accuracy: ', str(np.round(score,decimals=2))+'%')

def train_knn(train, test,train_labels, test_labels):
    #INITIALIZATION
    knn = KNeighborsClassifier(n_neighbors=6, weights = 'uniform')
    
    #TRAINING
    knn.fit(train, train_labels)
    score = knn.score(test, test_labels)*100
    
    #SAVING MODEL TO "KNN.sav"
    filename = 'KNN.sav'
    pickle.dump(knn, open(filename, 'wb'))


    print('KNN:')
    print('Accuracy: ', str(np.round(score,decimals=2))+'%')

def train_rf(train, test,train_labels, test_labels):
    #INITIALIZATION
    rf = RandomForestClassifier(n_estimators=100, max_features='auto', max_depth=None)
    
    #TRAINING
    rf.fit(train, train_labels)
    predictions = rf.predict(test)
    score = rf.score(test, test_labels)*100
    
    #SAVING MODEL TO "RF.sav"
    filename = 'RF.sav'
    pickle.dump(rf, open(filename, 'wb'))

    print('RF:')
    print('Accuracy: ', str(np.round(score,decimals=2))+'%')

def train_lr(train, test,train_labels, test_labels):
    #INITIALIZATION
    lr = LogisticRegression(warm_start=True, solver='liblinear', max_iter=100)
    
    #TRAINING
    lr.fit(train, train_labels)
    score = lr.score(test, test_labels)*100
    
    #SAVING MODEL TO "LR.sav"
    filename = 'LR.sav'
    pickle.dump(lr, open(filename, 'wb'))
    
    print('LR:')
    print('Accuracy: ', str(np.round(score,decimals=2))+'%')



###################### Training  ############
train, test,train_labels, test_labels = fetch_training_data("train.csv")
train_svc(train, test,train_labels, test_labels)
train_knn(train, test,train_labels, test_labels)
train_rf(train, test,train_labels, test_labels)
train_lr(train, test,train_labels, test_labels)