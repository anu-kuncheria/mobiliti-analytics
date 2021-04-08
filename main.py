import sys
from general_tools import *


dir = "/Users/akuncheria/Documents/GSR-2021Feb/UCBerkeley_GSR/Results_Mobiliti/2021-02-04-SFAddedFreightDemand"
subdir = "2021-02-03-sf_uet_000_links"
fpath = "avg_flow_rates.tsv"
spath = "avg_speeds.tsv"
fupath = "fuel_consumption.tsv"

#Loading network
network = Network()
npath = "/Users/akuncheria/Documents/GSR-2021Feb/UCBerkeley_GSR/Networks_Dataset/networks_dataset_Mobiliti/Nov2019/for_drive/september2020"
nodes, links, _,  = network.load_citylinks(os.path.join(npath,'sf_nodes.csv'), os.path.join(npath,'sf_links.csv'))

#Reading flow and speed files in the format along with adding the link attributes
results = ReadingFiles()
flowdf = results.results_city_len(os.path.join(dir,subdir,fpath),links)
speeddf = results.results_city_len(os.path.join(dir,subdir,spath),links)
fueldf = results.read_file(os.path.join(dir,subdir,fupath))

#System level metrics
print("VMT is:",vmt(flowdf)  )
print("VHD is:",vhd(flowdf, speeddf) )
print("Fuel consumption is:",fuel_gallons(fueldf))
