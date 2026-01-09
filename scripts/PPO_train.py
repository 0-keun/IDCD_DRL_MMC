import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Normal, Categorical
from torch.utils.data.sampler import BatchSampler, SubsetRandomSampler

from MMC_env import MMCTuningEnv

# visualization On / Off
viz = False

# Set the hyperparameters
GAMMA = 0.99
LR = 3e-4
EPS_CLIP = 0.2
K_EPOCH = 4
BATCH_SIZE = 64
UPDATE_TIMESTEP = 2000

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =========================
# Actor-Critic (continuous)
# =========================
class ActorCritic(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=64):
        super().__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        # Policy head (logits for discrete actions)
        self.policy_head = nn.Linear(hidden_dim, action_dim)
        # Value head
        self.value_head = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        x = torch.tanh(self.fc1(x))
        logits = self.policy_head(x)        # [B, action_dim]
        value = self.value_head(x)          # [B, 1]
        return logits, value
# class ActorCritic(nn.Module):
#     def __init__(self, state_dim, action_dim, hidden_dim=64):
#         super(ActorCritic, self).__init__()
#         # Common layer
#         self.fc1 = nn.Linear(state_dim, hidden_dim)

#         # Policy network: mean of action
#         self.mu_head = nn.Linear(hidden_dim, action_dim)
#         # log_std는 파라미터로 두고 학습되게 함
#         self.log_std = nn.Parameter(torch.zeros(action_dim))

#         # Value function network
#         self.value_head = nn.Linear(hidden_dim, 1)
    
#     def forward(self, x):
#         x = torch.tanh(self.fc1(x))
#         mu = self.mu_head(x)               # [batch, action_dim]
#         std = torch.exp(self.log_std)      # [action_dim]
#         state_values = self.value_head(x)  # [batch, 1]
#         return mu, std, state_values

# =========================
# PPO Agent
# =========================
# class PPOAgent:
#     def __init__(self, state_dim, action_dim):
#         self.policy = ActorCritic(state_dim, action_dim).to(device)
#         self.optimizer = optim.Adam(self.policy.parameters(), lr=LR)
#         self.policy_old = ActorCritic(state_dim, action_dim).to(device)
#         self.policy_old.load_state_dict(self.policy.state_dict())
#         self.MseLoss = nn.MSELoss()
    
#     def select_action(self, state):
#         state = torch.FloatTensor(state).unsqueeze(0).to(device)  # [1, state_dim]
#         with torch.no_grad():
#             mu, std, _ = self.policy_old(state)
#         dist = Normal(mu, std)
#         action = dist.sample()                                    # [1, action_dim]
#         log_prob = dist.log_prob(action).sum(dim=-1)              # [1]

#         # env action space [-1,1] 가정하고 clamp
#         action_clamped = torch.clamp(action, -1.0, 1.0)

#         return action_clamped.squeeze(0).cpu().numpy(), log_prob.item()

class PPOAgent:
    def __init__(self, state_dim, action_dim):
        self.policy = ActorCritic(state_dim, action_dim).to(device)
        self.policy_old = ActorCritic(state_dim, action_dim).to(device)
        self.policy_old.load_state_dict(self.policy.state_dict())

        self.optimizer = optim.Adam(self.policy.parameters(), lr=LR)
        self.MseLoss = nn.MSELoss()

    def select_action(self, state):
        state = torch.FloatTensor(state).unsqueeze(0).to(device)

        with torch.no_grad():
            logits, _ = self.policy_old(state)

        dist = Categorical(logits=logits)
        action = dist.sample()              # scalar int
        log_prob = dist.log_prob(action)    # scalar

        return action.item(), log_prob.item()

    def compute_returns(self, rewards, dones, next_value):
        returns = []
        R = next_value
        for reward, done in zip(reversed(rewards), reversed(dones)):
            if done:
                R = 0
            R = reward + GAMMA * R
            returns.insert(0, R)
        return returns
    
    def update(self, memory):
        states = torch.FloatTensor(memory['states']).to(device)
        actions = torch.LongTensor(memory['actions']).to(device)
        old_log_probs = torch.FloatTensor(memory['log_probs']).unsqueeze(1).to(device)
        returns = torch.FloatTensor(memory['returns']).unsqueeze(1).to(device)

        with torch.no_grad():
            _, values = self.policy(states)
        advantages = returns - values
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        dataset_size = states.size(0)

        for _ in range(K_EPOCH):
            for idx in BatchSampler(
                SubsetRandomSampler(range(dataset_size)),
                BATCH_SIZE,
                False
            ):
                sampled_states = states[idx]
                sampled_actions = actions[idx]
                sampled_old_log_probs = old_log_probs[idx]
                sampled_returns = returns[idx]
                sampled_advantages = advantages[idx]

                logits, state_values = self.policy(sampled_states)
                dist = Categorical(logits=logits)

                new_log_probs = dist.log_prob(sampled_actions).unsqueeze(1)
                entropy = dist.entropy().mean()

                ratio = torch.exp(new_log_probs - sampled_old_log_probs)

                surr1 = ratio * sampled_advantages
                surr2 = torch.clamp(ratio, 1 - EPS_CLIP, 1 + EPS_CLIP) * sampled_advantages

                policy_loss = -torch.min(surr1, surr2).mean()
                value_loss = self.MseLoss(state_values, sampled_returns)

                loss = policy_loss + 0.5 * value_loss - 0.01 * entropy

                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
                self.optimizer.step()

        self.policy_old.load_state_dict(self.policy.state_dict())

# =========================
# Main training loop
# =========================
def main():
    if viz:
        env = MMCTuningEnv(render_mode="human")
    else:
        env = MMCTuningEnv()
    
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    agent = PPOAgent(state_dim, action_dim)
    
    max_episodes = 1000
    max_timesteps = 300
    timestep = 0
    
    memory = {'states': [], 'actions': [], 'log_probs': [], 'rewards': [], 'dones': []}

    # 전체 학습 동안의 전역 최적 설계 기록용
    global_best_cost = float("inf")
    global_best_L = None
    global_best_C = None
    
    for episode in range(1, max_episodes + 1):
        state, _ = env.reset()
        ep_reward = 0.0
        for t in range(max_timesteps):
            if viz:
                env.render()
            action, log_prob = agent.select_action(state)
            next_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            # env 내부에서 추적한 best가 전체(global)보다 좋으면 갱신
            if info["best_cost"] < global_best_cost:
                global_best_cost = info["best_cost"]
                global_best_L = info["best_L"]
                global_best_C = info["best_C"]
            
            memory['states'].append(state)
            memory['actions'].append(action)
            memory['log_probs'].append(log_prob)
            memory['rewards'].append(reward)
            memory['dones'].append(done)
            
            state = next_state
            ep_reward += reward
            timestep += 1
            
            # 일정 timestep마다 PPO 업데이트
            if timestep % UPDATE_TIMESTEP == 0:
                with torch.no_grad():
                    state_tensor = torch.FloatTensor(state).unsqueeze(0).to(device)
                    _, _, next_value = agent.policy_old(state_tensor)
                returns = agent.compute_returns(
                    memory['rewards'], memory['dones'], next_value.item()
                )
                memory['returns'] = returns
                
                agent.update(memory)
                
                memory = {'states': [], 'actions': [], 'log_probs': [], 'rewards': [], 'dones': []}
            
            if done:
                break
        
        print(f"Episode {episode}\tReward: {ep_reward:.4f}")
    
    # 모델 저장
    torch.save(agent.policy.state_dict(), './model/mmc-ppo-continuous.pth')
    print("A model is saved")

    # 🔹 학습 전체에서 찾은 최적 설계 출력
    print("\n=== Global Best Design (over all episodes) ===")
    print(f"Best cost : {global_best_cost:.6f}")
    print(f"Best L_arm: {global_best_L:.6e} H")
    print(f"Best C_arm: {global_best_C:.6e} F")

    env.close()

if __name__ == '__main__':
    main()
