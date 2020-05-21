import functools

import numpy as np
import tensorflow as tf
import pandas as pd

#----------------------------------------------------------------------------------------------

# obtain csv of data
TRAIN_DATA_URL = "https://storage.googleapis.com/tf-datasets/titanic/train.csv"
TEST_DATA_URL = "https://storage.googleapis.com/tf-datasets/titanic/eval.csv"
train_file_path = tf.keras.utils.get_file("train.csv", TRAIN_DATA_URL)
test_file_path = tf.keras.utils.get_file("eval.csv", TEST_DATA_URL)

# for readability
np.set_printoptions(precision=3, suppress=True)

#----------------------------------------------------------------------------------------------

# specifies label column
LABEL_COLUMN = 'survived'
LABELS = [0, 1]

# defines method to get dataset
def get_dataset(file_path, **kwargs):
  dataset = tf.data.experimental.make_csv_dataset(
      file_path,
      batch_size=64,                   # Artificially small to make examples easier to show.
      label_name=LABEL_COLUMN,
      na_value="?",
      num_epochs=1,
      ignore_errors=True, 
      **kwargs)
  return dataset

# print function formatting
def show_batch(dataset):
  for batch, label in dataset.take(1):
    for key, value in batch.items():
      print("{:20s}: {}".format(key,value.numpy()))

# gets datasets
raw_train_data = get_dataset(train_file_path)
raw_test_data = get_dataset(test_file_path)

#----------------------------------------------------------------------------------------------

'''
# examply using a subset of the columns
SELECT_COLUMNS = ['survived', 'age', 'n_siblings_spouses', 'parch', 'fare']
DEFAULTS = [0, 0.0, 0.0, 0.0, 0.0]
temp_dataset = get_dataset(train_file_path, 
                           select_columns=SELECT_COLUMNS,
                           column_defaults = DEFAULTS)

# puts 'survived' in labels batch, the rest in example batch
example_batch, labels_batch = next(iter(temp_dataset)) 

# pack functions
def pack(features, label):
  return tf.stack(list(features.values()), axis=-1), label

# packed dataset (with numeric)
packed_dataset = temp_dataset.map(pack)
'''

#----------------------------------------------------------------------------------------------

# creates a numeric featurs object
class PackNumericFeatures(object):
  def __init__(self, names):
    self.names = names

  def __call__(self, features, labels):
    numeric_features = [features.pop(name) for name in self.names]
    numeric_features = [tf.cast(feat, tf.float32) for feat in numeric_features]
    numeric_features = tf.stack(numeric_features, axis=-1)
    features['numeric'] = numeric_features

    return features, labels

#----------------------------------------------------------------------------------------------

# specifies numeric features
NUMERIC_FEATURES = ['age','n_siblings_spouses','parch', 'fare']

# packs numeric data
packed_train_data = raw_train_data.map(
    PackNumericFeatures(NUMERIC_FEATURES))

packed_test_data = raw_test_data.map(
    PackNumericFeatures(NUMERIC_FEATURES))

# pandas description (for getting mean and std)
desc = pd.read_csv(train_file_path)[NUMERIC_FEATURES].describe()

MEAN = np.array(desc.T['mean'])
STD = np.array(desc.T['std'])

# normalize numeric data
def normalize_numeric_data(data, mean, std):
  # Center the data
  return (data-mean)/std

normalizer = functools.partial(normalize_numeric_data, mean=MEAN, std=STD)

numeric_column = tf.feature_column.numeric_column('numeric', normalizer_fn=normalizer, shape=[len(NUMERIC_FEATURES)])
numeric_columns = [numeric_column]

# creates a tf dense layer with numeric data
numeric_layer = tf.keras.layers.DenseFeatures(numeric_columns)

#----------------------------------------------------------------------------------------------
# jesus feck, okay on to the categorical data

# outlines categorical outcomes
CATEGORIES = {
    'sex': ['male', 'female'],
    'class' : ['First', 'Second', 'Third'],
    'deck' : ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    'embark_town' : ['Cherbourg', 'Southhampton', 'Queenstown'],
    'alone' : ['y', 'n']
}

categorical_columns = []
for feature, vocab in CATEGORIES.items():
  cat_col = tf.feature_column.categorical_column_with_vocabulary_list(
        key=feature, vocabulary_list=vocab)
  categorical_columns.append(tf.feature_column.indicator_column(cat_col))

# categorical layer
categorical_layer = tf.keras.layers.DenseFeatures(categorical_columns)

#----------------------------------------------------------------------------------------------

# concatenates the numeric and categorical layers
preprocessing_layer = tf.keras.layers.DenseFeatures(categorical_columns+numeric_columns)

#----------------------------------------------------------------------------------------------
# Cool, now for the model

model = tf.keras.Sequential([
  preprocessing_layer,
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(1),
])

model.compile(
    loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
    optimizer='adam',
    metrics=['accuracy'])

train_data = packed_train_data.shuffle(500)
test_data = packed_test_data

model.fit(train_data, epochs=20)

test_loss, test_accuracy = model.evaluate(test_data, verbose = 0)

print('\n\nTest Loss {}, Test Accuracy {}'.format(test_loss, test_accuracy))

'''
predictions = model.predict(test_data)

# Show some results
for prediction, survived in zip(predictions[:10], list(test_data)[0][1][:10]):
  prediction = tf.sigmoid(prediction).numpy()
  print("Predicted survival: {:.2%}".format(prediction[0]),
        " | Actual outcome: ",
        ("SURVIVED" if bool(survived) else "DIED"))
'''





