import networkx as nx
import plotly.graph_objects as go
import os
import re

def create_trace_for_nodes(graph, pos, node_color):
    x_values = [pos.get(key, (0, 0))[0] for key in graph.nodes()]
    y_values = [pos.get(key, (0, 0))[1] for key in graph.nodes()]

    node_trace = go.Scatter(
        x=x_values, y=y_values,
        mode='markers',
        marker=dict(
            color=node_color,
            size=10,
            line_width=2
        ),
        text=list(graph.nodes),
        hoverinfo='text'
    )

    return node_trace

def create_trace_for_edges(graph, pos, edge_color):
    edge_trace = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        arrow_annotation = dict(
            ax=x0,
            ay=y0,
            axref='x',
            ayref='y',
            x=x1,
            y=y1,
            xref='x',
            yref='y',
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=edge_color
        )
        edge_trace.append(arrow_annotation)

    return edge_trace

def create_frames(path, directed):
    all_nodes = set()
    all_graphs = []
    files = sorted((f for f in os.listdir(f'{path}') if re.search(r'timestep_(\d+).gexf', f)), key=lambda x: int(re.search(r'timestep_(\d+).gexf', x).group(1)))

    for file in files:  
        if file.endswith('.gexf'):
            G = nx.read_gexf(f'{path}/{file}') #type: ignore
            all_nodes.update(G.nodes())
            all_graphs.append(G)

    super_graph = nx.Graph()
    super_graph.add_nodes_from(all_nodes)
    pos = nx.spring_layout(super_graph) # type: ignore

    frames = []
    for i, G in enumerate(all_graphs):
        node_trace = create_trace_for_nodes(G, pos, 'blue')
        edge_trace = create_trace_for_edges(G, pos, 'gray') if directed else []

        frame = go.Frame(
            data=[node_trace],
            layout=go.Layout(
                title_text=files[i],
                annotations=edge_trace,
                xaxis=dict(range=[-1.5, 1.5]),  # ensuring all frames have the same axes
                yaxis=dict(range=[-1.5, 1.5])   # ensuring all frames have the same axes
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
           xaxis=dict(range=[-1.5, 1.5]),
            yaxis=dict(range=[-1.5, 1.5]),
            title=dict(text=files[0], font=dict(size=20)),
            hovermode="closest",
            updatemenus=[{
                "type": "buttons",
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 300, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}],
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                    }
                ],
            }],
            annotations=frames[0]['layout']['annotations'],
            sliders=sliders
        ),
        frames=frames
    )
    return fig

# Getting visualisation for experiments

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
    fig.write_html(f"{write_path}/network_visualisation.html")