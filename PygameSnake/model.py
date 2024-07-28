# Import the necessary libraries
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

# Define a class for the Q-network
class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        # Define the first linear layer
        self.linear1 = nn.Linear(input_size, hidden_size)
        # Define the second linear layer
        self.linear2 = nn.Linear(hidden_size, output_size)

    # Define the forward pass
    def forward(self, x):
        # Pass the input through the first linear layer and apply ReLU activation function
        x = F.relu(self.linear1(x))
        # Pass the result through the second linear layer
        x = self.linear2(x)
        return x

    # Define a method to save the model
    def save(self, file_name='model.pth'):
        # Define the path to the folder where the model will be saved
        model_folder_path = './model'
        # If the folder does not exist, create it
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        # Join the folder path and the file name
        file_name = os.path.join(model_folder_path, file_name)
        # Save the model
        torch.save(self.state_dict(), file_name)


# Define a class for the Q-learning trainer
class QTrainer:
    def __init__(self, model, lr, gamma):
        # Initialize learning rate, discount factor, and model
        self.lr = lr
        self.gamma = gamma
        self.model = model
        # Define the optimizer
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        # Define the loss function
        self.criterion = nn.MSELoss()

    # Define a method to perform a training step
    def train_step(self, state, action, reward, next_state, done):
        # Convert the inputs to tensors
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        # If the state is a 1D tensor (a single state), add an extra dimension
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # Get the Q-values for the current state
        pred = self.model(state)

        # Initialize the target Q-values as the predicted Q-values
        target = pred.clone()
        # Update the target Q-value for the action taken
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new

        # Zero the gradients
        self.optimizer.zero_grad()
        # Compute the loss
        loss = self.criterion(target, pred)
        # Backpropagate the error
        loss.backward()

        # Update the weights
        self.optimizer.step()