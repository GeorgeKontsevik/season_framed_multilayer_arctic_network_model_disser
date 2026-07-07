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
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This project contains research code for seasonal geospatial accessibility modeling in Arctic transport networks. It is intended for researchers and developers working with spatial analysis, transport-network modeling, and notebook-driven Python workflows. The repository centers on a reproducible analysis pipeline that combines preprocessing, network construction, provision calculation, and visualization, with results explored through notebooks and supporting Python modules. For a runnable entry point and local execution details, see Getting Started.

---

## Core Features

- Builds seasonal accessibility models over geospatial settlement, transport, infrastructure, and service data, giving researchers a workflow for analyzing how access changes by month.
- Converts processed settlement areas into a network model that combines transport links with service locations, enabling graph-based accessibility calculations.
- Incorporates monthly climate-driven conditions into the network, so transport accessibility can be evaluated across seasons rather than as a single static snapshot.
- Computes service provision and allocation results with optimization-based assignment, helping quantify covered demand, unmet demand, and service reach.
- Produces visual outputs such as multilayer network views, Sankey-style flow charts, circular flow charts, and temporal metric plots, making model results easier to inspect and communicate.

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

- Python environment from `environment.yml` or `requirements.txt`.
- Input data under `../data/`, organized as processed settlement folders such as `processed/<SETTL_NAME>/` with files like `df_settlements_<SETTL_NAME>.geojson`, `df_time_<SETTL_NAME>.geojson`, `infrastructure_<SETTL_NAME>.csv`, `df_<SERVICE_NAME>_<SETTL_NAME>.geojson`, and `df_climate_<SETTL_NAME>.csv`.
- Run the notebook from the `notebooks/` directory so the parent directory can be added to `sys.path` for `scripts/` imports.

### Quickstart

1. Set up the Python environment using the repository environment file or requirements file.
2. Open `notebooks/2_main.ipynb`.
3. Run the import cell, which appends the repository root to `sys.path` and loads the pipeline modules.
4. Ensure the data path in the notebook points to `../data/`.
5. Execute the main calculation cell to process the listed settlements and services.
6. Optionally run the plotting cells to generate multilayer, Sankey, and circular flow charts from `all_results`.

---

## Architecture

This repository is organized around a notebook-driven research workflow. The main analysis notebook (`notebooks/2_main.ipynb`) ties together preprocessing, graph construction, seasonal modeling, metric calculation, and plotting for multiple settlement and service combinations.

The Python code under `scripts/` is split into four main roles:

- `scripts/preprocesser` loads and cleans geospatial inputs, normalizes names and transport data, and prepares settlement, infrastructure, and service datasets for analysis.
- `scripts/model` builds the graph-based accessibility model and computes provision results, including the graph-to-city-model transformation used by the analysis pipeline.
- `scripts/calculator` runs the core analysis steps, such as block-scheme construction, transport probability handling, monthly mode calculations, and network statistics.
- `scripts/plotter` turns the computed graphs and summaries into visual outputs such as multilayer networks, Sankey-style flows, temporal plots, and heatmaps.

At a high level, the workflow is: read cleaned geospatial data, construct a transport network for each study area, attach seasonal temperature data, run accessibility/provision calculations for each month, and then generate figures and summary tables from the resulting graphs and records. The repository also includes precomputed inputs and example outputs under `new_data/`, `notebooks/`, and `plots/`, which support reproducing and reviewing the analysis.

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