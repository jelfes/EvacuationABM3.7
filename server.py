import mesa

from model import PanicModel
from canvas import SimpleCanvas


def draw_agent(agent):
    # select color
    if agent.panic == 1:
        color = "red"
    else:
        color = "skyblue"

    drawing_params = {
        "Shape": "circle",
        "r": agent.radius * 5,
        "Filled": "true",
        "Color": color,
    }
    return drawing_params


panic_canvas = SimpleCanvas(draw_agent, 500, 500)

chart = mesa.visualization.ChartModule(
    [{"Label": "panic", "Color": "#0000FF"}], data_collector_name="datacollector"
)

num_agents = mesa.visualization.Slider(
    "Number of agents",
    value=100,
    min_value=2,
    max_value=600,
    step=1,
    description="Choose how many agents to include in the model",
)

min_group_size = mesa.visualization.Slider(
    name="min_group_size",
    value=1,
    min_value=1,
    max_value=3,
)

max_group_size = mesa.visualization.Slider(
    name="max_group_size", value=5, min_value=3, max_value=50
)

resilience = mesa.visualization.Slider(
    name="resilience", value=3, min_value=1, max_value=5
)


model_params = {
    "N": num_agents,
    "width": 10,
    "height": 10,
    "min_group_size": min_group_size,
    "max_group_size": max_group_size,
    "resilience": resilience,
    "min_radius": 0.5,
}

server = mesa.visualization.ModularServer(
    PanicModel, [panic_canvas, chart], "Panic Model", model_params
)

server.port = 8521
