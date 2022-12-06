import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
import os
import yaml
from utility import *

config_file = "config.yaml"
a_yaml_file = open(config_file)
config = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

network_path = config["analytics"]["network_path"]
links = config["analytics"]["city_links"]
nodes = config["analytics"]["city_nodes"]
sim_one_path = config["analytics"]["sim_one_path"]
sim_two_path = config["analytics"]["sim_two_path"]
sim_one_name = config["analytics"]["sim_one_name"]
sim_two_name = config["analytics"]["sim_two_name"]
fpath = config["analytics"]["fpath"]
spath = config["analytics"]["spath"]
fupath = config["analytics"]["fupath"]
sim_one_legspath = config["analytics"]["legs_one_path"]
sim_two_legspath = config["analytics"]["legs_two_path"]
processed_path = Path(config["analytics"]["processed_path"])
figures_path = config["analytics"]["processed_path"]
signals_bool = config["analytics"]["signalsrun"]

sf_links = pd.read_csv(os.path.join(network_path,links))
sf_nodes = pd.read_csv(os.path.join(network_path, nodes))

dfnames = {fpath:[simulation_one_flow,sim_one_path, simulation_two_flow,sim_two_path],
          spath:[simulation_one_speed,sim_one_path,simulation_two_speed, sim_two_path],
          fupath:[simulation_one_fuel,sim_one_path, simulation_two_fuel, sim_two_path]}

for k,v in dfnames.items():
    v[0] = results_city_len(read_file(os.path.join(v[1], k)),sf_links)
    v[2] = results_city_len(read_file(os.path.join(v[3], k)),sf_links)
