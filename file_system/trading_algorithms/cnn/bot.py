import numpy as np
import tensorflow as tf
import os.path

class Bot:
    def __init__(self):
        self.name = "cnn"
        self.actions = []
        self.data = {}
        path = os.path.dirname(os.path.realpath(__file__))
        self.model = tf.keras.models.load_model(path + '/simple_lstm.h5')
        self.model.summary()
        self.positions = {}
        self.event_counter = 0


    #unix_time, ticker, new_price = event
    def handle_event(self, event):
        self.event_counter += 1
        unix_time, ticker, new_price = event
        if ticker not in self.data:
            self.data[ticker] = []
            self.positions[ticker] = "short"

        self.data[ticker].append(event)

        if self.event_counter % 10 == 0:
            self.algorithm()

    def algorithm(self):
        for ticker, events in self.data.items():
            if len(events) < 30: 
                continue

            x = np.array(events)
            x = x[-30:,2].astype(np.float)
            x_mean = x.mean()
            x_std = x.std()
            x = (x-x_mean)/x_std
            x = x[:,np.newaxis,np.newaxis]
            

            prediction = self.model.predict(x)[0]
            
            if prediction > x[-1] and self.positions[ticker] == "short":
                self.positions[ticker] = "long"
                self.actions.append([events[-1], self.positions[ticker]])
            elif prediction < x[-1] and self.positions[ticker] == "long":
                self.positions[ticker] = "short"
                self.actions.append([events[-1], self.positions[ticker]])
            
        return

