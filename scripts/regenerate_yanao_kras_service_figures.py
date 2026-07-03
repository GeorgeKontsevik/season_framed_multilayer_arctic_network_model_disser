from pathlib import Path
import sys

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(REPO_ROOT))

import scripts.model.provision as provision
from scripts.calculator.calculator_monthly_mode import create_df_modes_monthly_fixed
from scripts.calculator.calculator_stat import create_agglomeration_network
from scripts.calculator.calculator_this_pipeline import make_block_scheme
from scripts.calculator.calculator_transport_prob import get_transport_probability
from scripts.plotter.plotter_flow_sankey import create_clean_sankey
from scripts.plotter.plotter_multilayer_service_network import plot_multilayer_network
from scripts.plotter.plotter_transport_mode_prob import plot_transport_probability_legacy
from scripts.preprocesser.constants import (
    CONST_BASE_DEMAND,
    MONTHS_IN_YEAR,
    START_YEAR,
    month_order,
    service_list,
    service_radius_minutes,
    settl_list,
    threshold,
    transport_mode_name_mapper,
    transport_modes,
    transport_modes_color,
)
from scripts.preprocesser.gcreator import add_temp_to_g, make_g
from scripts.preprocesser.huston import call_nasa
from scripts.preprocesser.preprocesser import get_data


DATA = ROOT / "data"
PLOTS = ROOT / "plots"
THESIS = REPO_ROOT / "itmo-phd-thesis-template-en" / "images" / "ch4" / "arctic"


def networkx_adjacency_matrix(graph):
    """Original arctic implementation, used here only for figure reproduction."""
    nodes = sorted(graph.nodes())
    matrix = pd.DataFrame(float("inf"), index=nodes, columns=nodes)
    np.fill_diagonal(matrix.values, 0)
    for source in nodes:
        for target, distance in nx.single_source_dijkstra_path_length(graph, source, weight="weight").items():
            matrix.loc[source, target] = distance
    return matrix


def networkx_pair_paths(*, graph_pickle_path, pairs_df, weight_key, **_kwargs):
    graph = pd.read_pickle(graph_pickle_path)
    rows = []
    for row in pairs_df.to_dict("records"):
        try:
            path = nx.shortest_path(graph, row["source"], row["target"], weight=weight_key)
            length = nx.path_weight(graph, path, weight=weight_key)
        except nx.NetworkXNoPath:
            path, length = [], float("inf")
        rows.append({**row, "length": length, "path": path})
    return pd.DataFrame(rows)


def calculate(settl_name: str) -> dict:
    provision.create_adjacency_matrix = networkx_adjacency_matrix
    provision.build_pairs_shortest_paths_pandana_external = networkx_pair_paths
    threshold_temperatures = plot_transport_probability_legacy(
        transport_modes,
        transport_modes_color,
        get_transport_probability,
        threshold,
        temps=None,
        font_size=12,
    )
    plt.close("all")
    results = {settl_name: {}}
    for service in service_list:
        settlements, services, transport, _ = get_data(
            f"{DATA}/",
            settl_name,
            transport_mode_name_mapper,
            transport_modes,
            service,
        )
        blocks = make_block_scheme(settlements, services, service_name=service)
        graph = make_g(transport, transport_modes, blocks, settlements)
        monthly_climate = call_nasa(blocks, f"df_climate_{settl_name}.csv")
        graph = add_temp_to_g(graph, monthly_climate)
        network = create_agglomeration_network(
            graph=graph,
            threshold=threshold,
            probability_function=get_transport_probability,
            provision_calculator=provision.calculate_graph_provision,
        )
        network.run_all_steps(
            range(12),
            service_radius_minutes=service_radius_minutes[settl_name],
            base_demand=CONST_BASE_DEMAND,
            service_name=service,
            return_assignment=True,
        )
        results[settl_name][service] = {
            "net": network,
            "stats": network.stats,
            "graphs": network.stats.graphs,
            "records": network.stats.records,
            "results": network.stats.results,
            "G_undirected": graph,
            "df_modes_monthly": create_df_modes_monthly_fixed(
                graph,
                transport_modes,
                threshold_temperatures,
                START_YEAR,
                MONTHS_IN_YEAR=MONTHS_IN_YEAR,
            ),
        }
    return results


def save_multilayer_figures(results: dict, settl_name: str) -> list[Path]:
    written = []
    for month in (4, 7):
        fig = plot_multilayer_network(
            results,
            settl_name,
            service_list,
            month=month,
            figsize=(15, 30),
        )
        name = f"multilayer_network_{settl_name}_{month_order[month]}.png"
        target = PLOTS / "multilayer" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(target, bbox_inches="tight", dpi=200)
        thesis_name = f"{settl_name}_multilayer_may.png" if month == 4 else f"{settl_name}_multilayer_aug.png"
        thesis_path = THESIS / thesis_name
        fig.savefig(thesis_path, bbox_inches="tight", dpi=200)
        written.extend([target, thesis_path])
        plt.close(fig)
    return written


def main() -> None:
    written = []
    results_by_region = {}
    for settl_name in settl_list:
        print(f"Rendering multilayer figures for {settl_name}")
        results = calculate(settl_name)
        results_by_region[settl_name] = results
        written.extend(save_multilayer_figures(results, settl_name))

    results = results_by_region["yanao_kras"]
    graphs = results["yanao_kras"]["marina"]["stats"].graphs[4:10]
    sankey = create_clean_sankey(graphs, service_name="marina", month_start=4)
    sankey_thesis = THESIS / "yanao_kras_marina_sankey.png"
    sankey_plot = PLOTS / "sankey" / "yanao_flow_marina.png"
    sankey.write_image(sankey_thesis, width=1400, height=700, scale=1)
    sankey.write_image(sankey_plot, width=1400, height=700, scale=1)
    written.extend([sankey_thesis, sankey_plot])

    for path in written:
        assert path.exists() and path.stat().st_size > 50_000, path
        print(f"{path} | {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
