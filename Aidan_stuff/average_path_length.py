import os
import re
import networkx as nx
import plotly.graph_objects as go

def create_frames(path):
    all_nodes = set()
    all_graphs = []
    files = sorted((f for f in os.listdir(f'{path}') if re.search(r'timestep_(\d+).gexf', f)), key=lambda x: int(re.search(r'timestep_(\d+).gexf', x).group(1)))
    avg_path_lengths = []

    for file in files:
        if file.endswith('.gexf'):
            G = nx.read_gexf(f'{path}/{file}') #type: ignore
            all_nodes.update(G.nodes())
            all_graphs.append(G)

            # Handle directed and undirected graphs differently
            if G.is_directed():
                components = nx.weakly_connected_components(G)
            else:
                components = nx.connected_components(G)

            total_path_length = 0
            total_nodes = 0

            # Calculate the weighted average of the average path length
            for component in components:
                if len(component) > 1:
                    # Create a subgraph and make it undirected for path length calculation
                    subgraph = G.subgraph(component).to_undirected()
                    path_length = nx.average_shortest_path_length(subgraph)
                    total_path_length += path_length * len(component)
                    total_nodes += len(component)

            # Calculate average path length
            if total_nodes > 0:
                avg_path_length = total_path_length / total_nodes
                avg_path_lengths.append(avg_path_length)
            else:
                avg_path_lengths.append(None)

    trace = go.Scatter(
        x=list(range(len(avg_path_lengths))), 
        y=avg_path_lengths,
        mode='lines+markers'
    )

    return [trace], files


def create_animation(data, files):
    fig = go.Figure(
        data=data,
        layout=go.Layout(
            xaxis=dict(title='Time Step'),
            yaxis=dict(title='Average Path Length'),
            title=dict(text=files[0], font=dict(size=20)),
            hovermode="closest"
        )
    )
    return fig

# Experiments visualisations
experiments = { 0: ['undirected_binomial_graph_binomial_reallocation_n100_c20', False],
          1: ['directed_binomial_graph_binomial_reallocation_n100_c20', False],
          2: ['undirected_binomial_graph_binomial_reallocation_n100_c20', False],
          3:['directed_binomial_graph_binomial_reallocation_n100_c20', False],
          4: ['undirected_binomial_graph_scalefree_reallocation_n100_c20', True], 
          5: ['directed_binomial_graph_scalefree_reallocation_n100_c20', True],
          6: ['undirected_scalefree_graph_scalefree_reallocation_n100_c20', True],
          7: ['directed_scalefree_graph_scalefree_reallocation_n100_c20', True],
          8: ['undirected_scalefree_graph_no_reallocation_n100_c20', True],
          9: ['directed_scalefree_graph_no_reallocation_n100_c20', True],
          10: ['undirected_scalefree_graph_no_reallocation_n100_c20', True],
          11: ['directed_scalefree_graph_no_reallocation_n100_c20', True],
              }

for i in range(len(experiments)):
    print(f'Experiment {i}')
    name = experiments[i][0]
    directed = experiments[i][1]
    read_path = f'Aidan_stuff/experiment_data/{name}'
    write_path = f'Aidan_stuff/experiment_visualisation/{name}'
    os.makedirs(write_path, exist_ok=True)
    data, files = create_frames(read_path)
    fig = create_animation(data, files)
    fig.write_html(f"{write_path}/average_path_length_visualisation.html")