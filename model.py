import tensorflow as tf
import numpy as np 
from tensorflow.keras import layers

def create_model():
    ''' Cree le model '''
    model = tf.keras.Sequential([
        tf.keras.layer.Flatten(input_shape=(4,4)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(4, activation='softmax'), ##  nombre de deplacement possible
    ])
    # Sert a minimiser les erreurs 
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse') 
    return model






