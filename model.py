import tensorflow as tf
import numpy as np 
import random
from collections import deque
from tensorflow.keras import layers



# Formule du Q-learning
LEARNING_RATE = 0.01 # alpha
FUTURE_REWARD = 0.95 # gamma
ESPILON_GREEDY = 0.95 # epsilon
MINIMUM_ESPILON = 0.1 # minimum epsilon
DECAY_ESPILON = 0.995 # décroissance epsilon 
BATCH_SIZE = 32 # Taille du batch
MEMORY_SIZE = 2000 # Taille memoire
UPDATE = 100 #Frequence mise a jour model

memory = deque(maxlen=MEMORY_SIZE)

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

#cree le model et stock dans une variable
model = create_model()

def choose_action(state):
    ''' Elle choisi un deplacement entre haut, gauche, droite, bas '''
    if np.random.rand() <= ESPILON_GREEDY:
        return random.randrange(4)
    else:
        value = model.predict(state)
        return np.argmax(value[0]) # l'action avec la plus haute valeur 
    


def train_model(): 
    ''' Entraine le model par rapport a la memoire'''
    if len(memory) < BATCH_SIZE:
        return
    batch = random.sample(memory, BATCH_SIZE)
    states, actions, rewards, next_states, dones = zip(*batch)
    states = np.array(states)
    actions = np.array(actions)
    rewards= np.array(rewards)
    next_states=np.array(next_states)
    dones = np.array(dones)
    
    next_value = model.predict(next_states)
    target_value = model.predict(states)
    for i in range(BATCH_SIZE):
        if dones[i]:
            target_value[i][actions[i]] = rewards[i]
        else:
            target_value[i][actions[i]] = rewards[i] + FUTURE_REWARD * np.max(next_value[i])
    model.fit(states,target_value,epochs=1, verbose=0)
    

def store_movement(state,action,reward,next_state,done):
    ''' Stock le mouvement dans la memoire'''
    memory.append((state,action,reward,next_state,done))
        
    
    
    
    


