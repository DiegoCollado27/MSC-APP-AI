#Implementar un algoritmo de Q-Learning para resolver el dominio de Frozen Lake
#Analizar la evolución del proceso de aprendizaje, modificando parámetros como el parámetro de descuento, la razón de aprendizaje, o la estrategia de exploración y explotación.
import numpy as np
import gymnasium as gym
import random

# Configuración del entorno Frozen Lake
#env = gym.make('FrozenLake-v1', map_name="8x8", is_slippery=True, render_mode='human' if render else None)
env = gym.make('FrozenLake-v1')
n_states = env.observation_space.n
n_actions = env.action_space.n

# Parámetros de Q-learning
alpha = 0.8  # Tasa de aprendizaje
gamma = 0.95  # Factor de descuento
epsilon = 0.1  # Probabilidad de exploración

# Inicialización de la tabla Q con valores arbitrarios
Q = np.zeros((env.observation_space.n, env.action_space.n))

# Número de episodios
num_episodes = 10000

# Proceso de aprendizaje
for episode in range(num_episodes):
    state = env.reset()[0]
    total_reward = 0

    while True:
        # Estrategia de exploración/explotación (epsilon-greedy)
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()  # Exploración -> el agente está tomando una acción aleatoria para explorar nuevas posibilidade
        else:
        
            action = np.argmax(Q[state, :]) # Explotación -> el agente selecciona la acción que maximiza el valor de Q para el estado actual

        # Realizar la acción y obtener la siguiente observación y recompensa
        #result = env.step(action)
        #print(result)
        next_state, reward, done, _, info = env.step(action)

        # Actualizar la tabla Q utilizando la ecuación de Bellman
        Q[state,action] = Q[state,action] + alpha * (
                    reward + gamma * np.max(Q[next_state,:]) - Q[state,action]
                )

        total_reward += reward
        state = next_state

        if done:
            break

    if episode % 100 == 0:
        print(f"Episodio {episode}: Recompensa total = {total_reward}")

# Evaluar el agente entrenado
total_reward = 0
num_eval_episodes = 100

for _ in range(num_eval_episodes):
    state = env.reset()
    while True:
        action = np.argmax(Q[state, :])
        next_state, reward, done, _ = env.step(action)
        total_reward += reward
        state = next_state
        if done:
            break

average_reward = total_reward / num_eval_episodes
print(f"Recompensa promedio en {num_eval_episodes} episodios de evaluación: {average_reward}")