import mesa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from matplotlib.collections import PatchCollection


def get_panic_level(model: mesa.Model) -> float:
    """
    Calculate the mean panic level of a set of agents.

    Args:
        model (mesa.Model): Model that contains a set of agents with a panic variable.

    Returns:
        float: Mean panic level of all agents.
    """

    agent_panic = [agent.panic for agent in model.schedule.agents]

    if len(agent_panic) == 0:
        mean_panic_level = 0
    else:
        mean_panic_level = np.array(agent_panic).mean()

    return mean_panic_level


def get_num_agents(model: mesa.Model) -> float:
    """
    Calculate the number of agents that still remain in the model.

    Args:
        model (mesa.Model): Model that contains a set of agents.
    Returns:
        int: Number of agents.
    """

    return len(model.schedule.agents)


def get_normed_heading_vector(pos1: np.array, pos2: np.array) -> np.array:
    heading_vector = pos2 - pos1
    magnitude = get_distance(pos1, pos2)

    if magnitude < 1e-2:
        heading_vector_norm = np.array((0, 0))
    else:
        heading_vector_norm = heading_vector / magnitude

    return heading_vector_norm


def get_distance(pos1: np.array, pos2: np.array) -> float:
    distance = np.sqrt(np.sum((pos2 - pos1) ** 2))

    return distance


def get_distances(pos: np.array, lst: list) -> list:
    distances = []
    for agent in lst:
        if agent.pos is None:
            distances.append(np.inf)
        else:
            distances.append(get_distance(pos, np.array(agent.pos)))

    return distances


def plot_canvas(fig: plt.figure, ax: plt.axes, model: mesa.model):
    personal_cmap = {
        0: [0, 0, 0],
        1: [1, 1, 1],
    }

    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    circles = [
        patches.Circle(agent.pos, radius=agent.radius)
        for agent in model.schedule.agents
    ]
    panic = [agent.panic for agent in model.schedule.agents]
    # colors = [agent.group_number for agent in model.schedule.agents]

    if len(panic) == 0:
        mean_panic = 0
    else:
        mean_panic = np.mean(panic)

    c = PatchCollection(circles)
    # c.set_array(colors)
    c.set_array(panic)
    ax.add_collection(c)
    # ax.add_patch(circles[0])
    plt.title(f"Mean panic level: {mean_panic:.2f}")
    plt.grid()
    plt.show()


def fix_position(model: mesa.Model, pos: np.array) -> np.array:
    """
    Fix the position of an agent if it leaves the model space.
    """

    pos[0] = min(pos[0], model.space.width)
    pos[0] = max(pos[0], 0)

    pos[1] = min(pos[1], model.space.height)
    pos[1] = max(pos[1], 0)

    return pos
