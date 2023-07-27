import numpy as np
import pickle
class match_model:
    """ Class that represents a match_model """

    def __init__ (self, w: list, b: int):
        self.w = np.array(w)
        self.b = b

    def predict (self, data):
        """ 
        Parameters:
        data : numpy array
            Either a (m,) or (m,n) array contain the data used to make a prediction
        """

        shape = data.shape

        if len(shape) == 1:
            z = np.dot(self.w, data) + self.b
            return 1 / (1 + np.exp(-z))
        elif len(shape) == 2:
            predictions = []

            for row in data:
                z = np.dot(self.w, row) + self.b
                prediction = 1 / (1 + np.exp(-z))
                predictions.append(prediction)
            
            return np.array(predictions)