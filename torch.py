import torch 
import torch.nn as nn 

#this does not work yet but is a sceleton that will be filled later.
#still need to figure out how get pytorch up and running. 

#tetris game
class TetrisModel(nn.Module):
    
    def __init__(self): 
        super(TetrisModel, self).__init__()
        self.layer1 = nn.Linear(input_features, 128) #input_features match the size of state vector from the Tetris game
        self.layer2 = nn.Linear(128, 256)
        self.layer3 = nn.Linear(256, output_features) #output_features should match the number of possible actions

    
    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = torch.relu(self.layer2(x))
        x = self.layer3(x)

        return x

#training the model
def training (model, game, episodes, optimizer, criterion):
    for episode in range(episodes):
        state = game.reset()
        
        while not game.is_over():
            state_tensor = torch.tensor(state, dtype=torch.float32)
            predictions = model(state_tensor)
            action = torch.argmax(predictions).item()

            next_state, reward, done = game.step(action)

            next_state_tensor = torch.tensor(next_state, dtype=torch.float32)
            target = reward + torch.max(model(next_state_tensor))

            loss = criterion(predictions, [action], target)
            optimizer.zero_grad() 
            loss.backward() 
            optimizer.step()

            state = next_state

    print(f"Episode: {episode}, Loss: {loss.item()}")

    #model, opptimizer, criterion = TetrisModel(), torch.optim.Adam(), nn.MSELoss()
    model = TetrisModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    #train the model
    training(model, game, 1000, optimizer, criterion)   


