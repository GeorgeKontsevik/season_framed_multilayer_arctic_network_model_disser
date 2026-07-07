# arctic_access

Seasonal multilayer service accessibility for Arctic settlements.

## Scheme

```mermaid
flowchart LR
    A[Inputs] --> B[Run: notebooks/2_main.ipynb]
    B --> C[Checked outputs]
    C --> D[Paper / thesis use]
```

## Main Result

![Main result](plots/multilayer/multilayer_network_yakut_chuk_May.png)

## Run

Entrypoint: `notebooks/2_main.ipynb`

Human:

```bash
jupyter notebook notebooks/2_main.ipynb
```

Agent:

Run only after checking raw/processed data availability; inspect generated plots, not only notebook completion.

## Publication

See thesis publication bundle in `itmo-phd-thesis-template-en/Dissertation/publications/`.

## Next Steps / Heuristics

Heuristic: seasonal modes are explicit layers; report missing/duplicate routes honestly.
