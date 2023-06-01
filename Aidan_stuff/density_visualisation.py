import os
import re
import networkx as nx
import plotly.graph_objects as go

def create_density_frames(path):
    all_nodes = set()
    all_graphs = []
    files = sorted((f for f in os.listdir(f'{path}') if re.search(r'timestep_(\d+).gexf', f)), key=lambda x: int(re.search(r'timestep_(\d+).gexf', x).group(1)))
    densities = []

    for file in files:
        if file.endswith('.gexf'):
            G = nx.read_gexf(f'{path}/{file}') #type: ignore
            all_nodes.update(G.nodes())
            all_graphs.append(G)

            # Compute network density
            num_edges = G.number_of_edges()
            num_nodes = G.number_of_nodes()

            if num_nodes > 1:  # To avoid division by zero
                if G.is_directed():
                    max_possible_edges = num_nodes * (num_nodes - 1)
                else:
                    max_possible_edges = num_nodes * (num_nodes - 1) / 2

                density = num_edges / max_possible_edges
                densities.append(density)
            else:
                densities.append(None)

    trace_density = go.Scatter(
        x=list(range(len(densities))), 
        y=densities,
        mode='lines+markers',
        name='Density'
    )

    return [trace_density], files


def create_density_animation(data, files):
    fig = go.Figure(
        data=data,
        layout=go.Layout(
            xaxis=dict(title='Time Step'),
            yaxis=dict(title='Network Density'),
            title=dict(text=files[0], font=dict(size=20)),
            hovermode="closest"
        )
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
    data, files = create_density_frames(read_path)
    fig = create_density_animation(data, files)
    fig.write_html(f"{write_path}/density_visualisation.html")