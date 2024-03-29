import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
import os
import yaml
import utility as util

config_file = "scripts/config.yaml"
a_yaml_file = open(config_file)
config = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

network_path = config["analytics"]["network_path"]
links = config["analytics"]["city_links"]
nodes = config["analytics"]["city_nodes"]

sim_one_name = config["analytics"]["sim_one_name"]
sim_two_name = config["analytics"]["sim_two_name"]
sim_one_path = config["analytics"]["sim_one_path"]
sim_two_path = config["analytics"]["sim_two_path"]
fpath = config["analytics"]["fpath"]
spath = config["analytics"]["spath"]
fupath = config["analytics"]["fupath"]

sim_one_legspath = config["analytics"]["legs_one_path"]
sim_two_legspath = config["analytics"]["legs_two_path"]

signals_bool = config["analytics"]["signalsrun"]

sf_links = pd.read_csv(os.path.join(network_path, links))
sf_nodes = pd.read_csv(os.path.join(network_path, nodes))

processed_path = Path(config["analytics"]["processed_path"])
if not os.path.exists(processed_path):
    os.mkdir(processed_path)

# adding length attributes to flow and speed files
file_paths = {
    "simulation_one_flow": os.path.join(sim_one_path, fpath),
    "simulation_two_flow": os.path.join(sim_two_path, fpath),
    "simulation_one_speed": os.path.join(sim_one_path, spath),
    "simulation_two_speed": os.path.join(sim_two_path, spath),
    "simulation_one_fuel": os.path.join(sim_one_path, fupath),
    "simulation_two_fuel": os.path.join(sim_two_path, fupath)
}

length_attributes = {}
for key, file_path in file_paths.items():
    length_attributes[key] = util.results_city_len(
        util.read_file(file_path), sf_links)

simulation_one_flow, simulation_two_flow = length_attributes[
    "simulation_one_flow"], length_attributes["simulation_two_flow"]
simulation_one_speed, simulation_two_speed = length_attributes[
    "simulation_one_speed"], length_attributes["simulation_two_speed"]
simulation_one_fuel, simulation_two_fuel = length_attributes[
    "simulation_one_fuel"], length_attributes["simulation_two_fuel"]

report_upload_name = config["report"]["report_upload_name"]
