import mesa
import numpy as np

from helpers import (
    get_normed_heading_vector,
    get_distance,
    get_distances,
    fix_position,
)


class PanicAgent2(mesa.Agent):
    """An agent with a radius, friend set, resilience, exposure level and a panic level."""

    def __init__(self, unique_id, model, resilience, min_radius, min_velocity=0.1):
        super().__init__(unique_id, model)
        self.panic = 0
        self.radius = self.random.random() * 0.2 + min_radius
        self.velocity = self.random.random() * 0.2 + min_velocity
        self.resilience = resilience
        self.exposure = 0
        self.friends = set()
        self.w_exit = 0.5
        self.w_friends = 0.25
        self.w_neighbors = 0.25

    def move(self, unwanted_neighbors):
        exit = np.array((0, 0))
        pos = np.array(self.pos)

        # way towards the exit
        heading_vector_exit_norm = get_normed_heading_vector(pos, exit)
        distance_exit = get_distance(pos, exit)

        # way towards friends
        friends = list(self.friends)

        distances_friends = get_distances(pos, friends)
        closest_friend = friends[np.argmin(distances_friends)]
        closest_friend_distance = np.min(distances_friends)

        if closest_friend_distance == np.inf:
            heading_vector_friend_norm = heading_vector_exit_norm
        else:
            heading_vector_friend_norm = get_normed_heading_vector(
                pos, np.array(closest_friend.pos)
            )

        # way away from unwanted neighbors
        heading_vector_neighbors = np.array((0, 0))
        for n in unwanted_neighbors:
            heading_vector_neighbors = heading_vector_neighbors - (
                np.array(n.pos) - pos
            )

        magnitude = np.sqrt(np.sum(heading_vector_neighbors**2))
        if magnitude < 1e-2:
            heading_vector_neighbors_norm = np.array((0, 0))
        else:
            heading_vector_neighbors_norm = heading_vector_neighbors / magnitude

        new_pos = (
            pos
            + (
                self.w_exit * heading_vector_exit_norm
                + self.w_friends * heading_vector_friend_norm
                + self.w_neighbors * heading_vector_neighbors_norm
            )
            * self.radius
        )

        new_pos = fix_position(self.model, new_pos)

        self.model.space.move_agent(self, tuple(new_pos))

        if distance_exit < self.radius:
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)

    def step(self):
        neighbors = set(self.model.space.get_neighbors(self.pos, self.radius))

        unwanted_neighbors = list(neighbors.difference(self.friends))

        if len(unwanted_neighbors) > 1:
            self.exposure += 1
        else:
            self.exposure = 0
        if self.exposure > self.resilience:
            self.panic = 1

        if self.pos is not None:
            self.move(unwanted_neighbors)
