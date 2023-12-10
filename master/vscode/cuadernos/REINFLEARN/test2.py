import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
import matplotlib.pyplot as plt
import cv2
from collections import deque, namedtuple
from itertools import count
import math

# Preprocesamiento de las imágenes del juego
def preprocess_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.resize(image, (84, 84), interpolation=cv2.INTER_AREA)
    return image / 255.0

# Apilar frames para dar contexto temporal
def stack_frames(stacked_frames, frame, is_new_episode, stack_size=4):
    frame = preprocess_image(frame)

    if is_new_episode:
        stacked_frames = deque([np.zeros((84, 84), dtype=np.float32) for _ in range(stack_size)], maxlen=4)
        for _ in range(stack_size):
            stacked_frames.append(frame)
    else:
        stacked_frames.append(frame)

    stacked_state = np.stack(stacked_frames, axis=0)
    return torch.from_numpy(stacked_state).float().to(device), stacked_frames  # Convertir a tensor y mover al dispositivo

# Definición de la red neuronal
class DQN(nn.Module):
    def __init__(self, input_shape, num_actions):
        super(DQN, self).__init__()
        self.conv1 = nn.Conv2d(input_shape[0], 32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)

        self.fc = nn.Linear(self.feature_size(input_shape), 512)
        self.out = nn.Linear(512, num_actions)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc(x))
        return self.out(x)

    def feature_size(self, input_shape):
        return self.conv3(self.conv2(self.conv1(torch.zeros(1, *input_shape)))).view(1, -1).size(1)

# Función para seleccionar acciones
def select_action(state, epsilon, policy_net):
    if random.random() > epsilon:
        with torch.no_grad():
            return policy_net(state.unsqueeze(0)).max(1)[1].view(1, 1)
    else:
        return torch.tensor([[random.randrange(n_actions)]], device=device, dtype=torch.long)


# Transición para almacenar en memoria
Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))

# Optimizar modelo
def optimize_model():
    if len(memory) < batch_size:
        return

    transitions = random.sample(memory, batch_size)
    batch = Transition(*zip(*transitions))

    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)), dtype=torch.bool, device=device)
    non_final_next_states = torch.cat([s.float().unsqueeze(0) for s in batch.next_state if s is not None]).to(device)

    state_batch = torch.cat([s.float().unsqueeze(0) for s in batch.state]).to(device)
    action_batch = torch.cat(batch.action).to(device)
    reward_batch = torch.cat(batch.reward).to(device)

    state_action_values = policy_net(state_batch).gather(1, action_batch)

    next_state_values = torch.zeros(batch_size, device=device)
    next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()
    expected_state_action_values = (next_state_values * gamma) + reward_batch

    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    optimizer.zero_grad()
    loss.backward()
    for param in policy_net.parameters():
        param.grad.data.clamp_(-1, 1)
    optimizer.step()

# Hiperparámetros y configuración inicial
batch_size = 64
gamma = 0.95
epsilon_start = 0.9
epsilon_end = 0.01
epsilon_decay = 500
target_update = 100

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

env = gym.make('SpaceInvaders-v4', render_mode='rgb_array')
env.reset()

init_screen = env.render()
screen_height, screen_width, _ = init_screen.shape

n_actions = env.action_space.n
policy_net = DQN((4, 84, 84), n_actions).to(device)
target_net = DQN((4, 84, 84), n_actions).to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.RMSprop(policy_net.parameters())
criterion = nn.SmoothL1Loss()
memory = deque([], maxlen=10000)

steps_done = 0
episode_durations = []

# Entrenamiento del agente
from tqdm import tqdm

# Entrenamiento del agente
num_episodes = 2
for i_episode in tqdm(range(num_episodes), desc="Training Progress"):
    env.reset()
    state, stacked_frames = stack_frames(None, env.render(), True)

    for t in count():
        epsilon = epsilon_end + (epsilon_start - epsilon_end) * math.exp(-1. * steps_done / epsilon_decay)
        action = select_action(state, epsilon, policy_net)
        observation, reward, done, _, info = env.step(action.item())

        reward = torch.tensor([reward], device=device, dtype=torch.float)

        if not done:
            next_state, stacked_frames = stack_frames(stacked_frames, env.render(), False)
            next_state = next_state.to(device)
        else:
            next_state = None

        memory.append(Transition(state, action, next_state, reward))

        state = next_state

        optimize_model()
        if done:
            episode_durations.append(t + 1)
            break
    if i_episode % target_update == 0:
        target_net.load_state_dict(policy_net.state_dict())

print('Training complete')


# Mostrar métricas
plt.figure()
plt.plot(episode_durations)
plt.show()


# Demostrar agente entrenado
env = gym.make('SpaceInvaders-v4', render_mode='human')
env.reset()  # Reinicia el entorno

# Inicializa stacked_frames con imágenes en negro al principio
# Asegúrate de que la imagen tenga 3 canales (RGB)
initial_image = np.zeros((84, 84, 3), dtype=np.float32)  # Imagen en negro con 3 canales
state, stacked_frames = stack_frames(None, initial_image, True)


done = False

while not done:
    env.render()  # Renderiza cada paso del juego para visualización
    action = select_action(state, 0, policy_net)  # Epsilon 0 para la mejor acción
    _, _, done, _, _ = env.step(action.item())

    # Como estamos en modo 'human', no podemos obtener la imagen del entorno
    # Así que no actualizamos 'state' aquí

env.close()





