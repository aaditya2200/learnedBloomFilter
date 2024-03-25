"""
This file contains the neural network "brain" to remember false positives
"""
from keras import Sequential
from keras.src.layers import Dense


class Brain:

    """
    Args to be added input_size, embedding_size, conv_layers, fully_connected_layers, dropout_p, optimizer, loss
    """
    def __init__(self):
        self.neural_network = model = Sequential([
            Dense(64, activation='relu', input_shape=(64,), name='input_layer'),
            Dense(32, activation='relu', name='hidden_layer'),
            Dense(1, activation='sigmoid', name='output_layer')
        ])

    def train_batch(self, x_train, y_train):
        self.neural_network.train_on_batch(x_train, y_train)

    def get_prediction(self, key):
        self.neural_network.predict(key)

