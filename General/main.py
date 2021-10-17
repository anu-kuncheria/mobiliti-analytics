import sys
from analysis_tools import *

dir = "../../../../2021-02-04-SFAddedFreightDemand"
subdir = "2021-02-03-sf_uet_000_links"
fpath = "avg_flow_rates.tsv"
spath = "avg_speeds.tsv"
fupath = "fuel_consumption.tsv"

#Loading network
network = Network()
npath = "../../../../networks_dataset_Mobiliti/Nov2019/for_drive/september2020"
nodes, links, _,  = network.load_citylinks(os.path.join(npath,'sf_nodes.csv'), os.path.join(npath,'sf_links.csv'))

#Reading flow and speed files in the format along with adding the link attributes
results = ReadingFiles()
flowdf = results.results_city_len(os.path.join(dir,subdir,fpath),links)
speeddf = results.results_city_len(os.path.join(dir,subdir,spath),links)
fueldf = results.read_file(os.path.join(dir,subdir,fupath))

#System level metrics
print("VMT is:",vmt(flowdf))
print("VHD is:",vhd(flowdf, speeddf))
print("Fuel consumption is:",fuel_gallons(fueldf))
flowdf = ADT(flowdf)
print(flowdf.groupby(['FUNC_CLASS'])[[ 'ADT']].sum())
#Morning peak analysis
cols_interest = ['link_id', '7:00', '7:15', '7:30', '7:45', '8:00', '8:15',
       '8:30', '8:45', '9:00', '9:15', '9:30', '9:45', 'ST_NAME', 'REF_IN_ID', 'NREF_IN_ID', 'FUNC_CLASS',
       'DIR_TRAVEL', 'NUM_PHYS_LANES', 'SPEED_KPH', 'LENGTH(meters)',
       'CAPACITY(veh/hour)', 'RAMP' ]
flowam = flowdf[cols_interest]
#VMT by FC
fc = [2,3,4,5]
vmtbyfc = []
for i in fc:
    flowam_fc = flowam[flowam[ 'FUNC_CLASS']==i]
    vmt = np.round(np.sum(flowam_fc.loc[:,'7:00':'9:45'].sum(axis = 1)*15*60*flowam_fc.loc[:,'LENGTH(meters)']*0.000621371))
    vmtbyfc.append(vmt)
print([i/1000000 for i in vmtbyfc]) #in million
