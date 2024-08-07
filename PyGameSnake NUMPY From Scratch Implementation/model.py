import numpy as np

class Linear_QNet:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights1 = np.random.randn(input_size, hidden_size) / np.sqrt(input_size)
        self.bias1 = np.zeros((1, hidden_size))
        self.weights2 = np.random.randn(hidden_size, output_size) / np.sqrt(hidden_size)
        self.bias2 = np.zeros((1, output_size))

    def forward(self, x):
        layer1 = np.dot(x, self.weights1) + self.bias1
        layer1_activation = np.maximum(layer1, 0)  # ReLU activation
        layer2 = np.dot(layer1_activation, self.weights2) + self.bias2
        return layer2

    def save(self, file_name='model.npz'):
        np.savez(file_name, w1=self.weights1, b1=self.bias1, w2=self.weights2, b2=self.bias2)

    def load(self, file_name='model.npz'):
        data = np.load(file_name)
        self.weights1 = data['w1']
        self.bias1 = data['b1']
        self.weights2 = data['w2']
        self.bias2 = data['b2']

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model

    def train_step(self, state, action, reward, next_state, done):
        state = np.array(state, dtype=np.float32)
        next_state = np.array(next_state, dtype=np.float32)
        action = np.array(action, dtype=np.int8)
        reward = np.array(reward, dtype=np.float32)

        if len(state.shape) == 1:
            state = np.expand_dims(state, 0)
            next_state = np.expand_dims(next_state, 0)
            action = np.expand_dims(action, 0)
            reward = np.expand_dims(reward, 0)
            done = (done,)

        # Get predicted Q values with current state
        pred = self.model.forward(state)

        # Q_new = r + y * max(next_predicted Q value)
        target = np.copy(pred)
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * np.max(self.model.forward(next_state[idx]))

            target[idx][np.argmax(action[idx])] = Q_new

        # Compute loss and gradients
        loss = np.mean((target - pred) ** 2)
        
        # Backpropagation (manually computing gradients)
        d_pred = 2 * (pred - target) / pred.shape[0]
        layer1 = np.dot(state, self.model.weights1) + self.model.bias1
        layer1_activation = np.maximum(layer1, 0)  # ReLU activation
        d_weights2 = np.dot(layer1_activation.T, d_pred)
        d_bias2 = np.sum(d_pred, axis=0, keepdims=True)
        d_hidden = np.dot(d_pred, self.model.weights2.T)
        d_hidden[layer1 <= 0] = 0  # ReLU derivative
        d_weights1 = np.dot(state.T, d_hidden)
        d_bias1 = np.sum(d_hidden, axis=0, keepdims=True)

        # Update weights and biases
        self.model.weights1 -= self.lr * d_weights1
        self.model.bias1 -= self.lr * d_bias1
        self.model.weights2 -= self.lr * d_weights2
        self.model.bias2 -= self.lr * d_bias2