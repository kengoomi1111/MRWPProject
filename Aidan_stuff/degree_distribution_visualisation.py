import os
import re
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import networkx as nx
import plotly.graph_objects as go

def create_frames(path, directed):
    all_nodes = set()
    all_graphs = []
    files = sorted((f for f in os.listdir(f'{path}') if re.search(r'timestep_(\d+).gexf', f)), key=lambda x: int(re.search(r'timestep_(\d+).gexf', x).group(1)))

    for file in files:  
        if file.endswith('.gexf'):
            G = nx.read_gexf(f'{path}/{file}') #type: ignore
            all_nodes.update(G.nodes())
            all_graphs.append(G)

    frames = []
    for i, G in enumerate(all_graphs):
        degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
        degree_count = Counter(degree_sequence)
        deg, cnt = zip(*degree_count.items())

        trace = go.Scatter(
            x=deg, 
            y=cnt,
            mode='markers'
        )
        frame = go.Frame(
            data=[trace],
            layout=go.Layout(
                title_text=files[i],
                xaxis=dict(title='Degree'),
                yaxis=dict(title='Count')
            ),
            name=str(i)
        )
        frames.append(frame)
    return frames, files

def create_slider(frames):
    steps = []
    for i, frame in enumerate(frames):
        step = dict(
            method="animate",
            args=[
                [frame['name']],
                {"frame": {"duration": 0, "redraw": True},
                 "mode": "immediate",
                 "transition": {"duration": 0}}
            ],
            label=frame['name']
        )
        steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Frame: "},
        pad={"t": 50},
        steps=steps
    )]
    return sliders

def create_animation(frames, files, sliders):
    fig = go.Figure(
        data=[frames[0]['data'][0]],
        layout=go.Layout(
           xaxis=dict(title='Degree', range=[-50, 50]),
            yaxis=dict(title='Count', range=[-25, 25]),
            title=dict(text=files[0], font=dict(size=20)),
            hovermode="closest",
            updatemenus=[{
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 30, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}],
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                    }
                ],
            }],
            sliders=sliders
        ),
        frames=frames
    )
    return fig


# Experiments visualisations

experiments = { 0: ['undirected_binomial_graph_binomial_reallocation', False],
          1: ['undirected_binomial_graph_scalefree_reallocation', False],
          2: ['undirected_scalefree_graph_binomial_reallocation', False],
          3:['undirected_scalefree_graph_scalefree_reallocation', False],
          4: ['directed_binomial_graph_binomial_reallocation', True], 
          5: ['directed_binomial_graph_scalefree_reallocation', True],
          6: ['directed_scalefree_graph_binomial_reallocation', True],
          7: ['directed_scalefree_graph_scalefree_reallocation', True]}
for i in range(len(experiments)):
    print(f'Experiment {i}')
    name = experiments[i][0]
    directed = experiments[i][1]
    read_path = f'Aidan_stuff/experiment_data/{name}'
    write_path = f'Aidan_stuff/experiment_visualisation/{name}'
    os.makedirs(write_path, exist_ok=True)
    frames, files = create_frames(read_path, directed)
    sliders = create_slider(frames)
    fig = create_animation(frames, files, sliders)
    fig.write_html(f"{write_path}/degree_distribution_visualisation.html")