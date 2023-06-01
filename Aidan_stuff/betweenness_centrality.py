import os
import re
import networkx as nx
import plotly.graph_objects as go
from collections import Counter

def create_frames(path):
    all_nodes = set()
    all_graphs = []
    files = sorted((f for f in os.listdir(f'{path}') if re.search(r'timestep_(\d+).gexf', f)), key=lambda x: int(re.search(r'timestep_(\d+).gexf', x).group(1)))

    frames = []
    for i, file in enumerate(files):
        if file.endswith('.gexf'):
            G = nx.read_gexf(f'{path}/{file}') #type: ignore
            all_nodes.update(G.nodes())
            all_graphs.append(G)
            centrality = nx.betweenness_centrality(G)
            min_centrality = min(centrality.values())
            max_centrality = max(centrality.values())
            centrality_sequence = sorted([centrality[n] for n in G.nodes()], reverse=True)
            centrality_count = Counter(centrality_sequence)
            cent, cnt = zip(*centrality_count.items())

            trace = go.Scatter(
                x=list(cent), 
                y=list(cnt),
                mode='markers'
            )
            frame = go.Frame(
                data=[trace],
                layout=go.Layout(
                    title_text=files[i],
                    xaxis=dict(title='Betweenness Centrality', range=[min_centrality, max_centrality]),
                    yaxis=dict(title='Count', range=[0, 50])
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
            yaxis=dict(title='Count', range=[0, 50]),
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
    frames, files = create_frames(read_path)
    sliders = create_slider(frames)
    fig = create_animation(frames, files, sliders)
    fig.write_html(f"{write_path}/betweenness_centrality_visualisation.html")
