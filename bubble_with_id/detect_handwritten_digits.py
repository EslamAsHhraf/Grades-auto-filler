
import cv2
import numpy as np



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

def detect_digit(col,row,loaded_svc, loaded_knn, loaded_rf, loaded_lr ):

    img=cv2.imread('./contours/'+str(col)+'/'+str(row)+'.jpg')
    #VARIABLES INITIALIZATION
    svc_predictions = []
    knn_predictions = []
    rf_predictions = []
    lr_predictions = []
    final_predictions = []
    weights = [1,1,16,49,1,11,1,100,5,25]
    classifiers_respond = np.zeros(10)
    
    #PRE-PROCESSING
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (28,28), interpolation = cv2.INTER_LANCZOS4|cv2.INTER_NEAREST)
    img = cv2.GaussianBlur(img, (5,5),0)
    
    #HOG AND PREDICTION
    hog_of_img = np.array(extract_hog_features(img))
    hog_of_img = hog_of_img.reshape(1,-1)
    value_SVC = loaded_svc.predict(hog_of_img)
    value_KNN = loaded_knn.predict(hog_of_img)
    value_RF = loaded_rf.predict(hog_of_img)
    value_LR = loaded_lr.predict(hog_of_img)
    
    #FINALIZING RESULTS
    svc_predictions.append(value_SVC)
    knn_predictions.append(value_KNN)
    rf_predictions.append(value_RF)
    lr_predictions.append(value_LR)
    classifiers_respond[int(value_SVC)] = classifiers_respond[int(value_SVC)] + weights[int(value_SVC)]
    classifiers_respond[int(value_KNN)] = classifiers_respond[int(value_KNN)] + weights[int(value_KNN)]
    classifiers_respond[int(value_RF)] = classifiers_respond[int(value_RF)] + weights[int(value_RF)]
    classifiers_respond[int(value_LR)] = classifiers_respond[int(value_LR)] + weights[int(value_LR)]
    final_predictions.append([str(np.argmax(classifiers_respond))])
    return final_predictions[0][0]


