# Source-Code for Submission "Groundings of Drifters in the Wadden Sea Inform the Transport of Floating Macroplastic"

Marc Schneiter, ORCID https://orcid.org/0009-0002-6450-4171

## Location of figures in the paper

| Name | Notebook number |
| - | - |
| Figure 1 | [2_1_plots_campaign_summary_example_trajectory](2_1_plots_campaign_summary_example_trajectory.ipynb) |
| Figure 2 | [2_1_plots_campaign_summary](2_1_plots_campaign_summary.ipynb) |
| Figure 3 | [2_1_plots_campaign_summary](2_1_plots_campaign_summary.ipynb) |
| Figure 4 | [2_1_plots_campaign_summary](2_1_plots_campaign_summary.ipynb) |
| Figure 5 | [2_1_grounding_statistic](2_1_grounding_statistic.ipynb) |
| Figure 6 | [2_1_grounding_events_characterization](2_1_grounding_events_characterization.ipynb) |
| Figure 7 | [2_1_grounding_events_characterization](2_1_grounding_events_characterization.ipynb) |
| Figure 8 | [2_1_grounding_events_characterization](2_1_grounding_events_characterization.ipynb) |
| Figure D1 | [2_1_grounding_events_characterization](2_1_grounding_events_characterization.ipynb) |

Remark: Figure D1 requires the execution of [2_1_grounding_events_characterization](2_1_grounding_events_characterization.ipynb) with different parameters

## Notebooks structure

* Parameters are set in a dedicated 'Parameters' section at the beginning of the notebooks
* The notebooks are run in the order 0 to 2
  * In the notebook '1_records_preprocessing.ipynb' different values for the parameters 'downsample_interval', 'downsample_random_dropout_fraction' were used, to generate trajectories for the grounding statistic evaluation. These are summarized in the table below, precomputed resampled trajectories are provided together with the input datasets and must be placed in the ./data/out/ directory
  * The notebook '2_0_datasets_preparation.ipynb' must not be run, it is used in the notebooks '2_1_*.ipynb'

| downsample_interval | downsample_random_dropout_fraction |
| - | - |
| 1 | 0.00 |
| 2 | 0.00 |
| 4 | 0.00 |
| 8 | 0.00 |
| 1 | 0.50 |
| 1 | 0.75 |
| 1 | 0.88 |

## Input Datasets

| Type | Name / Designator | Source / Provider | Open access | Link (last access) |
| - | - | - | - | - |
| Drifter trajectories | Wadden Sea drifter trajectories 2023 | Zenodo | X | https://zenodo.org/records/14199027 (2025-09-16) |
| Bathymetry | H1. Bathymetrie (2019)  | Waddenregister  | X | https://datahuiswadden.openearth.nl/geonetwork/srv/dut/catalog.search#/metadata/eRwjLet8Qhy_Xc9OHANsqw (2025-09-02) |
| Water-levels | swan_kuststrook_harmonie | MATROOS, Rijkswaterstaat  |  | https://iplo.nl/thema/water/applicaties-modellen/berichtgeving-crisismanagement/matroos (2025-09-19) |
| Wind | ERA5 wind uv hourly 10m | Copernicus Climate Change Service (C3S) | X | https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels (2025-09-02) |
| Grounding events | Manual codings | in directory ./data/in/ | - | - |

For questions about dataset availabilities, contact https://orcid.org/0009-0002-6450-4171

The approximate total size is 4GB

## Dependencies

The project uses the following python packages

    jupyterlab
    numpy
    pandas
    xarray
    netcdf4
    scipy
    geopy
    scikit-learn
    matplotlib
    cartopy

## Execution

The project can be run on a modern personal computer, the scripts are single threaded and complete execution requires less than 10GB of disk-space

Linux terminal commands to run with a conda environment

```console
conda create --name <ENVNAME>
conda activate <ENVNAME>
conda install conda-forge::jupyterlab numpy pandas conda-forge::xarray netcdf4 scipy geopy scikit-learn matplotlib cartopy

git clone <GITHUB>
cd <GITDIR>
jupyter-lab
```
