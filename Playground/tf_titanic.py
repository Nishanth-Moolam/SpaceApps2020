import functools

import numpy as np
import tensorflow as tf
import pandas as pd

# obtain csv of data
TRAIN_DATA_URL = "https://storage.googleapis.com/tf-datasets/titanic/train.csv"
TEST_DATA_URL = "https://storage.googleapis.com/tf-datasets/titanic/eval.csv"
train_file_path = tf.keras.utils.get_file("train.csv", TRAIN_DATA_URL)
test_file_path = tf.keras.utils.get_file("eval.csv", TEST_DATA_URL)

# specify labels
LABEL_COLUMN = 'survived'
LABELS = [0, 1]

# for readability
np.set_printoptions(precision=3, suppress=True)

# save data in pd dataframe
train_features = pd.read_csv(train_file_path)
test_features = pd.read_csv(test_file_path)

train_labels = train_features.pop('survived')
test_labels = test_features.pop('survived')


# If we wish, we may use only certain parts of the dataframe (only numeric values)
temp_df = train_features[['age', 'n_siblings_spouses', 'parch', 'fare']]

# describes and saves mean and standard dev.
mean = temp_df.describe().T['mean']
std = temp_df.describe().T['std']

# It is always good practice to normalize numeric data
def normalize_data(data, mean, std):
  # Center the data
  return (data-mean)/std

# Normalized dataframe
df = normalize_data(temp_df, mean, std).head()

# Now we gotta deal with the categorical data


