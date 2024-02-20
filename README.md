## G-Tomo Sky Chart App

This folder contains the code to construct a night sky plot using the GTOMO dataset. 
There exists both a online interactive version using dash and an offline version which uses the matplotlib library. For an overview of the code and its functions please refer to the `AboutCodeStructure.txt` file in the repository. 

## Requirements

The required libraries to run the code can be found in the file `requirements.txt`

## Data

The dataset [`grid_lbdext_0.5deg_5pc.h5`](https://zenodo.org/records/10405177/files/grid_lbdext_0.5deg_5pc.h5?download=1) needs to be downloaded from the Zenodo G-Tomo repository [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10405177.svg)](https://doi.org/10.5281/zenodo.10405177) and copied to the folder `sda/data/`


## Executing the code

To run the offline code, run the 'Main_Integrated.py' file in your IDE. For the online verison run the DashApp.py file in your IDE and open the created link in your preferred browser. 

## Create and test locally 

    $ git clone https://gitlab.acri-cwa.fr/project-explore/nightsky-gtomo.git
    $ cd nightsky_gtomo
    $ cd sda
    $ docker-compose up --build
    
## Get involved! 

This project relies on contributions from the community. See: https://github.com/explore-platform/explore

### Become a contributor

If you have ideas or suggestions for content for this project, please check out our [contributors' guidelines](CONTRIBUTING.md) and our [roadmap](ROADMAP.md). Please note that by joining this project, you agree to follow the [code of conduct](CODE_OF_CONDUCT.md) in all interactions both on and offline.


## Acknowledgements

This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 101004214. 

<img src='sda/assets/EUflag.png' height='100' /> <img src='sda/assets/Explore_Logo_Standard.png' height='100' />

