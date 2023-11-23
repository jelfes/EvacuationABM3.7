import mesa
import numpy as np

from agent import PanicAgent2
from helpers import get_panic_level, get_num_agents


class PanicModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(
        self,
        N,
        height,
        width,
        max_group_size,
        min_group_size,
        resilience,
        min_radius,
        min_velocity=0.1,
    ):
        self.num_agents = N
        self.space = mesa.space.ContinuousSpace(width, height, torus=True)
        self.schedule = mesa.time.RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            a = PanicAgent2(
                i,
                self,
                resilience=resilience,
                min_radius=min_radius,
                min_velocity=min_velocity,
            )
            self.schedule.add(a)
            # Add the agent to a random space cell
            x = self.random.uniform(0, width)
            y = self.random.uniform(0, height)
            self.space.place_agent(a, (x, y))

        self.friend_groups = []

        agents = self.schedule.agents.copy()

        while len(agents) > 0:
            group_size = min(
                [self.random.randint(min_group_size, max_group_size), len(agents)]
            )

            group = self.random.sample(agents, group_size)
            self.friend_groups.append(group)

            agents = list(set(agents).difference(set(group)))

        for i, group in enumerate(self.friend_groups):
            for agent in group:
                agent.friends = group
                agent.group_number = i

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "panic": get_panic_level,
                "num_agents": get_num_agents,
            },
            agent_reporters={
                "panic": "panic",
                "exporsure": "exposure",
                "position": "pos",
            },
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
