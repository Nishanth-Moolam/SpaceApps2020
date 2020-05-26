import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.layers import Flatten, Dense, Dropout, Softmax
from tensorflow.keras.models import Sequential
from tensorflow.keras.losses import SparseCategoricalCrossentropy

# dataset
mnist = tf.keras.datasets.mnist

# Load data and convert to float
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
'''
# viewing the first image
plt.figure()
plt.imshow(x_train[2])
plt.colorbar()
plt.grid(False)
plt.show()
'''
# Build model by stacking layers
model = Sequential([

    # input dimension is flattened of 28x28 (pixels of the mnist images)
    Flatten(input_shape=(28, 28)),

    # creates a layers of neurons with 128 neurons (relu is rectified linear unit)
    Dense(128, activation='relu'),

    # randomly sets input units to zero to prevent overfitting
    Dropout(0.2),

    # Output layer of 10 (for 10 digits)
    Dense(10)
])

# loss fn
loss_fn = SparseCategoricalCrossentropy(from_logits=True)

# defines optimizer, loss fx and metrics, which are needed to train
model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

# trains the model
model.fit(x_train, y_train, epochs=5)

# evaluates the model with test data ( verbose just makes it print progress bar)
model.evaluate(x_test,  y_test, verbose=2)




