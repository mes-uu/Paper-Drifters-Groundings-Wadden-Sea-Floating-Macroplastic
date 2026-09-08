# Source-Code for Submission "Groundings of Drifters in the Wadden Sea Inform the Transport of Floating Macroplastic"

## References, authors and funding

* Repository citation DOI https://doi.org/10.5281/zenodo.17865410

* Main author: Marc Schneiter, PhD candidate (m.e.schneiter-at-uu.nl) ORCID https://orcid.org/0009-0002-6450-4171

* Supervision PhD: Erik van Sebille (e.vansebille-at-uu.nl)

* Co-Supervision PhD: Rolf Hut (R.W.Hut-at-tudelft.nl)

* Author of coding file data/in/waddendrifters2023_grounding_events_manual_coding_validation.csv: Jimena Medina Rubio (j.medinarubio-at-uu.nl)

The research project is part of the Vici ENW programme ['Tracing Marine Macroplastics by Unraveling the Ocean's Multiscale Transport Processes'](https://www.nwo.nl/en/projects/vic222025)

## Location of figures in the paper

| Name | Notebook |
| - | - |
| Figure 1 | [2_1_campaign_summary_plots](2_1_campaign_summary_plots.ipynb) |
| Figure 2 | [2_1_campaign_summary_plots_example_trajectory](2_1_campaign_summary_plots_example_trajectory.ipynb) |
| Figure 3 | [2_1_campaign_summary_plots](2_1_campaign_summary_plots.ipynb) |
| Figure 4 | [2_1_campaign_summary_plots](2_1_campaign_summary_plots.ipynb) |
| Figure 5 | [2_1_grounding_detection](2_1_grounding_detection.ipynb) |
| Figure 6 | [2_1_grounding_events_characterization](2_1_grounding_events_characterization.ipynb) |
| Figure 7 | [2_1_grounding_events_characterization](2_1_grounding_events_characterization.ipynb) |
| Figure 8 | [2_1_grounding_events_characterization](2_1_grounding_events_characterization.ipynb) |
| Figure A1 | [2_1_campaign_summary_plots](2_1_campaign_summary_plots.ipynb) |
| Figure B1 | [2_1_campaign_summary_plots](2_1_campaign_summary_plots.ipynb) |
| Figure C1 | [2_1_campaign_summary_plots](2_1_campaign_summary_plots.ipynb) |
| Figure D1 | [2_1_campaign_summary_plots](2_1_campaign_summary_plots.ipynb) |
| Figure E1 | [2_1_campaign_summary_plots](2_1_campaign_summary_plots.ipynb) |
| Figure G1 | [2_1_grounding_events_characterization](2_1_grounding_events_characterization.ipynb) |
| Figure I1 | [2_1_grounding_events_characterization](2_1_grounding_events_characterization.ipynb) |
| Figure J1 | [2_1_grounding_events_characterization](2_1_grounding_events_characterization.ipynb) |

Remark: Figures E1,G1,I1,J1 require running [2_1_grounding_events_characterization](2_1_grounding_events_characterization.ipynb) with different parameters and/or small script modifications

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

* Remark: In this version the terms 'wetting' (W), 'drying' (D) and 'beaching' (B) are used interchangeably with 'grounding' (G) and 'resuspension' (R) in the source code, data labels, and ducumentation

## Input datasets

| Type | Name / Designator | Source / Provider | Open access | Link (website and dataset accessed YYYY-MM-DD) |
| - | - | - | - | - |
| Drifter trajectories | Wadden Sea drifter trajectories 2023 | Zenodo | X | https://zenodo.org/records/14199027 (2026-09-08) |
| Bathymetry | H1. Bathymetrie (2019)  | Waddenregister  | X | https://datahuiswadden.openearth.nl/ (2026-09-08) |
| Water-levels | swan_kuststrook_harmonie | MATROOS, Rijkswaterstaat  |  | https://iplo.nl/thema/water/applicaties-modellen/berichtgeving-crisismanagement/matroos (2026-09-08) |
| Wind | ERA5 wind uv hourly 10m | Copernicus Climate Change Service (C3S) | X | https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels (2026-09-08) |
| Grounding events | Manual codings | in directory ./data/in/ | - | - |
| (optional) Water-levels alternative [1] | waterinfo_rws | Rijkswaterstaat  | X | https://waterinfo.rws.nl/publiek/waterhoogte/ (2026-09-08) |

Detailed download instructions are provided as code documentation at the import statements. For questions about dataset availabilities, contact https://orcid.org/0009-0002-6450-4171

The approximate total size is 10GB

[1] This dataset will not reproduce the results discussed in the paper, it is a low-resolution open access alternative to 'swan_kuststrook_harmonie' that can be used by setting the parameter 'which_waterlevel_dataset' at the beginning of the notebook '2_0_datasets_preparation'

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
    pytz

## Execution

The project can be run on a modern personal computer, the scripts are single threaded and complete execution requires less than 10GB of disk-space

Linux terminal commands to run with a conda environment (tested 2026-05-19)

```console
conda config --add channels conda-forge
conda create --name <ENVNAME>
conda activate <ENVNAME>
conda install conda-forge::jupyterlab numpy pandas conda-forge::xarray netcdf4 scipy geopy scikit-learn matplotlib cartopy pytz

git clone <GITHUB>
cd <GITDIR>
jupyter-lab
```

## Version history of GitHub releases and publication stages

20 May 2026 Revision [TODO add link] | [Paper Revision Source-Code](https://github.com/mes-uu/Paper-Drifters-Groundings-Wadden-Sea-Floating-Macroplastic/releases/tag/Paper-Revision)

10 Dec 2025 [Preprint](https://egusphere.copernicus.org/preprints/2025/egusphere-2025-6170/) | [Paper Submission Source-Code](https://github.com/mes-uu/Paper-Drifters-Groundings-Wadden-Sea-Floating-Macroplastic/releases/tag/Paper-Submission)

## License

This project is released under the [Creative Commons - Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) license.