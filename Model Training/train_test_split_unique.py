import pandas as pd
import numpy as np
from random import randint

def generate_index(x_df, dup_df, test_indices):
    num_rows = x_df.shape[0]
    while True:
        random_index = randint(0, num_rows - 1)

        #TEST1: index should not be in test_indices already
        if test_indices[np.isin(test_indices, [random_index])].size == 0:
            #UNIQUE INDEX FOUND HERE
            #TEST 2: records in the index SHOULD NOT HAVE MORE THAN 1 RECORD in landmarks
            random_test = x_df.iloc[random_index]
            if (dup_df == random_test).all(axis=1).sum() == 0:
                return random_index
            
def train_test_split_unique(x_df, y_df):
    num_rows = x_df.shape[0]
    test_size = int(num_rows * 0.2)
    train_size = num_rows - test_size
    
    dup_df = x_df[x_df.duplicated(keep=False)]

    #Split test data here
    test_indices = np.array([test_size,])
    y_test = np.array([test_size,])
    
    test_indices_tmp = []
    y_test_tmp = []
    for i in range(0, test_size):
        random_index = generate_index(x_df, dup_df, test_indices)
        test_indices_tmp.append(random_index)
        y_test_tmp.append(y_df[random_index])

        test_indices = np.array(test_indices_tmp)
        y_test = np.array(y_test_tmp)

    X_test = pd.concat([X_test, x_df.iloc[test_indices]])
    
    #Split training data here
    train_indices = np.delete(np.arange(num_rows), test_indices, axis=0)

    X_train = pd.concat([X_train, x_landmarks_df_normalized.iloc[train_indices]])
    y_train = np.delete(y_landmarks_df, test_indices, axis=0)
    
    return X_train, X_test, y_train, y_test

    
    