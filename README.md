# season_framed_multilayer_arctic_network_model_disser

---

![License](https://img.shields.io/github/license/GeorgeKontsevik/season_framed_multilayer_arctic_network_model_disser?style=flat&logo=opensourceinitiative&logoColor=white&color=blue)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![folium](https://img.shields.io/badge/Folium-77B829.svg?style={0}&logo=Folium&logoColor=white)
![numpy](https://img.shields.io/badge/NumPy-013243.svg?style={0}&logo=NumPy&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?style={0}&logo=pandas&logoColor=white)
![plotly](https://img.shields.io/badge/Plotly-3F4F75.svg?style={0}&logo=Plotly&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikitlearn-F7931E.svg?style={0}&logo=scikit-learn&logoColor=white)
![scipy](https://img.shields.io/badge/SciPy-8CAAE6.svg?style={0}&logo=SciPy&logoColor=white)
![tqdm](https://img.shields.io/badge/tqdm-FFC107.svg?style={0}&logo=tqdm&logoColor=black)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This project provides research code for seasonal geospatial accessibility modeling in Arctic transport networks. It is aimed at researchers and developers working on spatial analysis, transport-network modeling, and notebook-driven Python workflows. The repository offers a Python-based analysis pipeline with supporting modules and notebooks for preprocessing, network modeling, and visualization. For a runnable entry point and local execution details, see Getting Started.

---

## Core Features

- Models seasonal accessibility across settlements, transport links, infrastructure, and service locations, giving researchers a way to study how access changes over time.
- Integrates monthly climate conditions into the network representation, so transport accessibility can be evaluated under different seasonal states.
- Computes service provision and allocation outcomes with optimization-based assignment, helping quantify covered demand, unmet demand, and reachable service capacity.
- Generates multilayer, Sankey-style, circular, and temporal network visualizations, making accessibility patterns and monthly changes easier to inspect and communicate.

---

## Installation

Install season_framed_multilayer_arctic_network_model_disser using one of the following methods:

**Build from source:**

1. Clone the season_framed_multilayer_arctic_network_model_disser repository:
```sh
git clone https://github.com/GeorgeKontsevik/season_framed_multilayer_arctic_network_model_disser
```

2. Navigate to the project directory:
```sh
cd season_framed_multilayer_arctic_network_model_disser
```

3. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

### Prerequisites

- A Python environment from `environment.yml` or `requirements.txt`.
- Input data available under `../data/`, with processed settlement folders such as `processed/<SETTL_NAME>/` containing files like `df_settlements_<SETTL_NAME>.geojson`, `df_time_<SETTL_NAME>.geojson`, `infrastructure_<SETTL_NAME>.csv`, `df_<SERVICE_NAME>_<SETTL_NAME>.geojson`, and `df_climate_<SETTL_NAME>.csv`.
- Run the notebook from the `notebooks/` directory so the parent directory can be added to `sys.path` for `scripts/` imports.

### Quickstart

1. Open `notebooks/2_main.ipynb`.
2. Run the import cell at the top of the notebook; it appends the repository root to `sys.path` and loads the pipeline modules.
3. Confirm the notebook data path is set to `../data/`.
4. Execute the main calculation cell to process the settlements and services listed in the notebook.
5. Run the plotting cells if you want to generate multilayer, Sankey, or circular flow charts from `all_results`.

---

## Architecture

This repository is organized around a notebook-driven research workflow. The main analysis notebook, `notebooks/2_main.ipynb`, orchestrates preprocessing, network construction, seasonal modeling, provision calculation, and figure generation for multiple settlement and service combinations.

At a high level, the pipeline reads cleaned geospatial inputs, builds a transport network for each study area, attaches monthly temperature data, and runs accessibility/provision calculations across months. The resulting graphs and records are then reused for multilayer, Sankey, circular flow, and temporal visualizations.

The Python code under `scripts/` is split into four main roles:

- `scripts/preprocesser` loads and cleans geospatial inputs, normalizes names and transport data, and prepares settlement, infrastructure, and service datasets.
- `scripts/model` defines the graph-based provision model and the graph-to-city-model transformation used by the analysis pipeline.
- `scripts/calculator` performs the core analysis steps, including block-scheme construction, transport probability handling, monthly mode calculations, and network statistics.
- `scripts/plotter` turns computed graphs and summaries into visual outputs such as multilayer networks, Sankey-style flows, temporal plots, and heatmaps.

The repository also includes precomputed inputs and generated outputs under `new_data/`, `notebooks/`, and `plots/`, which support reproducing and reviewing the analysis.

---

## API Reference

This project is notebook-driven and exposes its practical API through the `scripts/` modules used by `notebooks/2_main.ipynb`.

- `scripts.preprocesser.preprocesser.get_data(data_path, SETTL_NAME, transport_mode_name_mapper, transport_modes, SERVICE_NAME, specific_folder='processed/')` — loads settlement, transport, infrastructure, and service datasets for a settlement/service pair.
- `scripts.preprocesser.gcreator.make_g(...)` — builds the transport graph used in the main pipeline.
- `scripts.preprocesser.gcreator.add_temp_to_g(...)` — adds monthly temperature data to the graph.
- `scripts.preprocesser.huston.call_nasa(...)` — fetches or prepares monthly climate data for a settlement.
- `scripts.calculator.calculator_this_pipeline.make_block_scheme(...)` — creates the block scheme used for service analysis.
- `scripts.calculator.calculator_stat.create_agglomeration_network(...)` — constructs the agglomeration network object used for the monthly run.
- `net.run_all_steps(...)` — executes the monthly analysis loop and can return assignment results.
- `scripts.calculator.calculator_monthly_mode.create_df_modes_monthly_fixed(...)` — builds the monthly transport-mode dataframe.
- `scripts.plotter.plotter_transport_mode_prob.plot_transport_probability_legacy(...)` — renders the transport probability chart.
- `scripts.plotter.plotter_multilayer_service_network.plot_multilayer_network(...)` — plots the multilayer network view.
- `scripts.plotter.plotter_flow_sankey.create_clean_sankey(...)` — creates the Sankey flow chart.
- `scripts.plotter.plotter_circular_network_sankey_style.plot_circular_network_sankey_style(...)` — plots the circular Sankey-style flow chart.
- `scripts.plotter.plotter_multi_temporal_nx_plots.plot_temporal_service_evolution(...)` — plots temporal service evolution.
- `scripts.plotter.plotter_multi_temporal_nx_plots.calculate_temporal_metrics(...)` — calculates temporal metrics.
- `scripts.plotter.plotter_multi_temporal_nx_plots.plot_temporal_metrics(...)` — plots temporal metrics.
- `scripts.model.provision.calculate_graph_provision(...)` — calculates provision metrics for a graph and is passed into the main agglomeration network pipeline.
- `scripts.model.provision.graph_to_city_model(...)` — converts a NetworkX graph into the `city_model` structure used by the provision code.
- `scripts.model.provision.create_adjacency_matrix(...)` — builds a full adjacency matrix from a graph.
- `scripts.model.provision.calculate_base_demand(...)` — computes base demand from population.

Core constants imported from `scripts.preprocesser.constants` and used as configuration include `START_YEAR`, `MONTHS_IN_YEAR`, `CONST_BASE_DEMAND`, `transport_modes`, `transport_modes_color`, `service_radius_minutes`, `transport_mode_name_mapper`, `service_list`, `threshold`, and `month_order`.

---

## Examples

Examples of how this should work and how it should be used are available [here](https://github.com/GeorgeKontsevik/season_framed_multilayer_arctic_network_model_disser/tree/main/notebooks).

---

## Documentation

A detailed season_framed_multilayer_arctic_network_model_disser description is available [here](https://link.springer.com/article/10.1007/s41109-026-00783-6).

---

## Contributing

- **[Report Issues](https://github.com/GeorgeKontsevik/season_framed_multilayer_arctic_network_model_disser/issues)**: Submit bugs found or log feature requests for the project.

- **[Submit Pull Requests](https://github.com/GeorgeKontsevik/season_framed_multilayer_arctic_network_model_disser/tree/main/CONTRIBUTING.md)**: To learn more about making a contribution to season_framed_multilayer_arctic_network_model_disser.

---

## License

This project is protected under the MIT License. For more details, refer to the [LICENSE](https://github.com/GeorgeKontsevik/season_framed_multilayer_arctic_network_model_disser/tree/main/LICENSE) file.

---

## Citation

If you use this software, please cite it as it is written in the [CITATION](https://github.com/GeorgeKontsevik/season_framed_multilayer_arctic_network_model_disser/tree/main/CITATION.cff) file.

---