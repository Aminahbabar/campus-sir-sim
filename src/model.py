import numpy as np, networkx as nx
from agents import Agent, State

class Params:
    def __init__(self, N=1000, beta=0.23, gamma=0.1,
                 mask_effect=0.0, contact_mult=1.0,
                 isolation_days=0):
        self.N=N; self.beta=beta; self.gamma=gamma
        self.mask_effect=mask_effect
        self.contact_mult=contact_mult
        self.isolation_days=isolation_days

class Simulation:
    def __init__(self, params: Params, seed=7):
        rng = np.random.default_rng(seed)
        self.rng = rng
        self.params = params
        self.day = 0
        self.agents = [Agent(i, compliant=rng.random()<0.8) for i in range(params.N)]
        self.network = nx.watts_strogatz_graph(params.N, k=8, p=0.05, seed=seed)
        # seed one infection
        self.agents[0].state = State.I
        self.log = []

    def step(self):
        p = self.params
        new_infections = []
        for u,v in self.network.edges():
            a,b = self.agents[u], self.agents[v]
            pair = (a,b) if a.state==State.I and b.state==State.S else \
                   (b,a) if b.state==State.I and a.state==State.S else None
            if pair:
                inf, sus = pair
                beta_eff = p.beta * p.contact_mult * (1 - p.mask_effect if sus.compliant else 1.0)
                p_trans = 1 - np.exp(-beta_eff)
                if self.rng.random() < p_trans:
                    new_infections.append(sus.idx)
        for idx in new_infections:
            if self.agents[idx].state == State.S:
                self.agents[idx].state = State.I
                self.agents[idx].days_in_state = 0

        for a in self.agents:
            if a.state == State.I:
                if self.rng.random() < (1 - np.exp(-p.gamma)):
                    a.state = State.R
                    a.days_in_state = 0
            a.days_in_state += 1

        self.day += 1
        S = sum(a.state==State.S for a in self.agents)
        I = sum(a.state==State.I for a in self.agents)
        R = sum(a.state==State.R for a in self.agents)
        self.log.append((self.day,S,I,R))

    def run(self, days=120):
        for _ in range(days):
            self.step()
        return self.log
