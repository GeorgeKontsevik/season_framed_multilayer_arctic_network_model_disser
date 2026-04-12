import networkx as nx
import pandas as pd
import geopandas as gpd
import numpy as np
import math
import tempfile
from pathlib import Path

import scripts.model.model as model  # Assuming model is a module that contains the calculate_provision function
from aggregated_spatial_pipeline.pandana_bridge import (
    build_graph_node_matrix_pandana_external,
    build_pairs_shortest_paths_pandana_external,
)

def calculate_base_demand(population, const_base_demand):
    """Calculate base demand from population with safety checks"""
    if population is None:
        return 0
    
    if isinstance(population, str):
        try:
            population = float(population)
        except (ValueError, TypeError):
            return 0
            
    try:
        return math.ceil((population / 1000) * const_base_demand)
    except (ValueError, TypeError):
        return 0

def create_adjacency_matrix(G):
    """
    Create full adjacency matrix from graph with shortest path distances between all nodes.
    
    Args:
        G: NetworkX graph
        
    Returns:
        pd.DataFrame: Full adjacency matrix with shortest path distances
    """
    with tempfile.TemporaryDirectory(prefix="pandana-adj-", dir="/tmp") as tmp_dir:
        tmp_root = Path(tmp_dir)
        graph_path = tmp_root / "graph.pkl"
        matrix_path = tmp_root / "matrix.parquet"
        pd.to_pickle(G, graph_path)
        return build_graph_node_matrix_pandana_external(
            graph_pickle_path=graph_path,
            output_path=matrix_path,
            weight_key="weight",
        )

def graph_to_city_model(G, service_radius, const_base_demand, service_name="hospital", adj_matrix=None):
    """
    Convert networkx graph or adjacency matrix to city_model format
    
    Args:
        G: NetworkX graph (for node attributes)
        service_radius: Maximum allowed service distance
        const_base_demand: Base demand per 1000 population
        service_name: Type of service to analyze
        adj_matrix: Optional pre-computed adjacency matrix
    """
    # Create blocks list with proper structure
    blocks = []
    
    for node, data in G.nodes(data=True):
        pop = data.get('population', 0)
        service_capacity = data.get(f'capacity_{service_name}', 0)
        
        block = {
            'id': data.get('id', node),
            'name': data.get('name', node),
            'geometry': data.get('geometry', None),
            'demand': calculate_base_demand(pop, const_base_demand),
            "population": pop,
            f'capacity_{service_name}': service_capacity,
            "demand_within": 0,
            "demand_without": 0,
            "capacity_left": 0,
        }
        blocks.append(block)

    # Use provided adjacency matrix or create from graph
    if adj_matrix is None:
        adj_matrix = create_adjacency_matrix(G)
    
    # Convert adjacency matrix to graph dict format
    graph_dict = {}
    for i in adj_matrix.index:
        graph_dict[i] = {}
        for j in adj_matrix.columns:
            if i != j and adj_matrix.loc[i, j] != float('inf'):
                graph_dict[i][j] = {'weight': adj_matrix.loc[i, j]}
    # print(graph_dict)
    city_model = {
        'epsg': G.graph.get('crs', None),
        'blocks': blocks,
        'graph': graph_dict,
        'service_types': {
            service_name: {
                'accessibility': service_radius,
                'demand': const_base_demand,
            },
        },
    }
    
    return city_model


def calculate_graph_provision(G, service_radius, const_base_demand, service_name="hospital", return_assignment=False, method="lp", **kwargs):
    """
    Calculate provision metrics for graph and create assignment edges
    
    Args:
        G: NetworkX graph
        service_radius: Maximum allowed service distance
        const_base_demand: Base demand per 1000 population
        service_name: Type of service to analyze
        return_assignment: Whether to return assignment details
        method: Provision method — "lp" / "lp_distance" (LP min distance) or "lp_coverage" (coverage matrix).
                model.calculate_provision supports "lp" and "iterative"; lp_distance/lp_coverage map to "lp".
        
    Returns:
        tuple: (G_with_assignments, provision_result, assignment_matrix)
            - G_with_assignments: Graph with assignment edges added
            - provision_result: DataFrame with provision metrics
            - assignment_matrix: DataFrame showing demand distribution
    """
    # model.calculate_provision supports "lp" and "iterative"; map pipeline methods
    model_method = "lp" if method in ("lp", "lp_distance", "lp_coverage") else method

    # Convert graph to city_model format
    # Create adjacency matrix first
    adj_matrix = create_adjacency_matrix(G)
    
    # Convert to city_model using the adjacency matrix
    city_model = graph_to_city_model(
        G, 
        service_radius, 
        const_base_demand, 
        service_name,
        adj_matrix=adj_matrix
    )

    # Calculate provision using model function
    result, assignments = model.calculate_provision(
        city_model=city_model, 
        service_type=service_name, 
        method=model_method,
    )

    # Create a fresh directed graph for service flows
    G_with_assignments = nx.DiGraph()
    
    # First add all nodes with their attributes
    for node, data in G.nodes(data=True):
        G_with_assignments.add_node(node, **data)
    
    # Add base network edges (undirected)
    for u, v, data in G.edges(data=True):
        G_with_assignments.add_edge(u, v, **data)
        G_with_assignments.add_edge(v, u, **data)
    
    # Create assignment matrix
    nodes = list(G_with_assignments.nodes())
    assignment_matrix = pd.DataFrame(
        assignments,
        index=nodes,
        columns=nodes
    )

    # print(assignment_matrix)
    
    # Add service flow assignments
    flow_pairs = []
    for i in assignment_matrix.index:
        for j in assignment_matrix.columns:
            flow = assignment_matrix.loc[i, j]
            if flow > 0:
                flow_pairs.append({"source": i, "target": j, "flow": float(flow)})

    if flow_pairs:
        with tempfile.TemporaryDirectory(prefix="pandana-flows-", dir="/tmp") as tmp_dir:
            tmp_root = Path(tmp_dir)
            graph_path = tmp_root / "graph.pkl"
            pd.to_pickle(G, graph_path)
            path_df = build_pairs_shortest_paths_pandana_external(
                graph_pickle_path=graph_path,
                pairs_df=pd.DataFrame(flow_pairs),
                weight_key="weight",
            )
        for _, row in path_df.iterrows():
            flow = float(row["flow"])
            path = row.get("path") or []
            total_weight = float(row.get("length", 0.0))
            if not path:
                continue
            i = row["source"]
            j = row["target"]
            G_with_assignments.add_edge(
                i,
                j,
                weight=total_weight,
                assignment=flow,
                path=path,
                is_service_flow=True,
                is_within=True if total_weight <= service_radius else False,
            )
            for k in range(len(path) - 1):
                u, v = path[k], path[k + 1]
                if G_with_assignments.has_edge(u, v):
                    G_with_assignments[u][v]['is_service_route'] = True
                    G_with_assignments[u][v]['service_flows'] = G_with_assignments[u][v].get('service_flows', 0) + flow
    # print(result)
    # Add provision values to graph nodes
    nx.set_node_attributes(G_with_assignments, {
        node: {
            'provision': result.loc[data['name'], 'provision'],
            'demand_within': result.loc[data['name'], 'demand_within'],
            'demand_without': result.loc[data['name'], 'demand_without'],
            'demand': result.loc[data['name'], 'demand'],
            'capacity_left': result.loc[data['name'], 'capacity_left']
        }
        for node, data in G_with_assignments.nodes(data=True)
    })
    
    if return_assignment:
        return G_with_assignments, result, assignment_matrix
    
    return G_with_assignments, result
