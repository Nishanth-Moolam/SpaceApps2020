import tensorflow as tf 
import numpy as np 
import pandas as pd



#https://towardsdatascience.com/machine-learning-general-process-8f1b510bd8af
#https://towardsdatascience.com/how-to-create-your-first-machine-learning-model-4c8f745e4b8c

#https://www.youtube.com/watch?v=tPYj3fFJGjk


# Data types scalars
string = tf.Variable('This is a string', tf.string)
number = tf.Variable(324, tf.int16)
floating = tf.Variable(12.4, tf.float64)

# higher rank tensors
rank_1_tensor = tf.Variable(['hi', 'hello', 'world'], tf.string)
rank_2_tensor = tf.Variable([[1,2,3],[4,5,6]], tf.float64)

print (120*'#')

# Shape of tensor
print (rank_2_tensor.shape)

print (120*'#')

# Changing Shape
tensor1 = tf.ones([1,2,3])
tensor2 = tf.reshape(tensor1, [2,3,1])
tensor3 = tf.reshape(tensor2, [3,-1])

print(tensor1)
print (120*'#')
print(tensor2)
print (120*'#')
print(tensor3)

# Types of Tensors
'''
- Constant --> does not change
- Variable --> does change

'''

# Evaluating tensors
'''
with tf.Session() as sess:
    tensor.eval()

'''
print (120*'#')




