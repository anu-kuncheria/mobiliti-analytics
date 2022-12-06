import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import json
import os
from shapely.geometry import Point
import shapely.geometry as geom
import csv

# Data Loading
def unzipfiles_folder(rootPath, pattern = '*.tgz'):
    import zipfile,fnmatch,os,tarfile
    for root, dirs, files in os.walk(rootPath):
        for filename in fnmatch.filter(files, pattern):
            zip_ref = tarfile.open(os.path.join(rootPath,filename)) # create tarfile object and open
            zip_ref.extractall(os.path.join(root,  os.path.splitext(filename)[0])) # extract file to dir
            zip_ref.close() # close file

def round_2decimals(number):
    return np.round(number, decimals = 2)

def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(list_of_elem)

def network_geom(links,nodes, crs = "epsg:4326"):
    """
    Converts links and nodes pandas file to geodataframe
    """
    nodes['geom'] = [Point(xy) for xy in zip(nodes.LON, nodes.LAT)]
    gdf_nodes = gpd.GeoDataFrame(nodes, geometry=nodes.geom, crs = crs)

    links['ref_lat'] = links['REF_IN_ID'].map(nodes.set_index('NODE_ID')['LAT'])
    links['ref_long'] = links['REF_IN_ID'].map(nodes.set_index('NODE_ID')['LON'])
    links['nref_lat'] = links['NREF_IN_ID'].map(nodes.set_index('NODE_ID')['LAT'])
    links['nref_long'] = links['NREF_IN_ID'].map(nodes.set_index('NODE_ID')['LON'])
    links['geometry'] = links.apply(lambda x: geom.LineString([(x['ref_long'], x['ref_lat']) , (x['nref_long'], x['nref_lat'])]), axis = 1)
    gdf_links = gpd.GeoDataFrame(links, geometry = links.geometry, crs = crs)
    return gdf_links, gdf_nodes

def generate_column_names():
    """
    Generates column names for the mobiliti results output.
    """
    result = ['link_id','00:00']
    minc, hourc = 0,0
    for i in range(0,95):
        minc +=1
        if minc % 4 == 0:
            minc = 0
            hourc +=1
        mindigit =  "00" if minc==0 else str(minc*15)
        result.append('%02d'%hourc + ':' + mindigit)
    result.append('unnamed')
    return result

def read_file(path):
    """
    Reading flow and speed files in a readable format
    """
    colnames = generate_column_names()
    file = pd.read_csv(path, sep = '\t',header = None, names =colnames)
    file.drop(file.columns[len(file.columns)-1], axis=1, inplace=True) #dropping the last Nan column
    return file

def load_citylinks(nodepath, linkpath):
    nodes = pd.read_csv(nodepath)
    links = pd.read_csv(linkpath)
    print("nodes:", len(nodes),"links:", len(links))
    return  nodes, links

def results_city_len(flow,links):
    """
    Add link attributes to the flow or speed
    """
    flow_c  = flow.merge(links, left_on = 'link_id', right_on = 'LINK_ID', how = 'left')
    return flow_c

def resultscity_filter(flow,citylinks):
    """
    Filtering results for a city
    """
    flow_sub = flow[flow.link_id.isin(citylinks.LINK_ID)]
    return flow_sub

def resultscity_filter_len(flow,citylinks):
    """
    Filtering flow or speed results for a city and adding link attributes to the flow and speed
    """
    flow_sub = flow[flow.link_id.isin(citylinks.LINK_ID)]
    flow_c  = flow_sub.merge(citylinks, left_on = 'link_id', right_on = 'LINK_ID', how = 'left')
    return flow_c

def len_network(links):
    """
    Total length of the network in miles
    """
    return links['LENGTH(meters)'].sum()*0.000621371  #miles

# Transportation Metrics
def adt(flow):
    return flow.iloc[:,1:97].sum(axis = 1)*15*60

def vmt(flow):
    """ Vehicle Miles Travelled.
    Flow df needs to have the link atrribute length in it
    """
    vmt = np.sum(flow.loc[:,"00:00":"23:45"].sum(axis = 1)*15*60*flow.loc[:,'LENGTH(meters)']*0.000621371) #count*length of road VMT
    return int(vmt)

def vmtfc(flow_len):
    """ Vehicle Miles Travelled by Functional class.
    Flow df needs to have the link atrribute length in it
    """

    fc_att = [1,2,3,4,5]
    vmtfc = []
    for fc in fc_att:
        flow_sub = flow_len[flow_len[ 'FUNC_CLASS']==fc]
        vmt = np.sum(flow_sub.iloc[:,1:97].sum(axis = 1)*15*60*flow_sub.loc[:,'LENGTH(meters)']*0.000621371)
        vmtfc.append(int(vmt))
    return vmtfc

def vhd(flow, speed, delaydf = False):
    """ Input: flow and speed df with both having length attribute
       Output: VHD for whole area
    """

    d_f = flow.copy()
    d_f.set_index('link_id', inplace = True)
    d_f.iloc[:, :96] = d_f.iloc[:, :96]*15*60  #flow to count

    d_time =  speed.copy()
    d_time.set_index('link_id', inplace = True)
    d_time.iloc[:, :96] = np.reciprocal(d_time.iloc[:, 0:96])
    d_time.iloc[:, :96] = d_time.iloc[:, :96].mul(d_time['LENGTH(meters)'], axis = 0)   #speed to time (in seconds)

    d_time['tt_free'] = d_time['LENGTH(meters)']/(d_time['SPEED_KPH']*0.277778)  # freeflow tt in seconds
    d_delay = d_time.iloc[:, np.r_[0:96,-1]]
    d_delay = d_delay.sub(d_delay['tt_free'], axis = 0) #delay in seconds
    #delay multiply by count
    delay_count_df =d_delay.iloc[:,0:96].mul(d_f.iloc[:,0:96]) #vehicle seconds delay

    if delaydf == False:
        return int(delay_count_df.sum().sum()/3600)#VHD
    else:
        delay_count_df['VHD_link'] = delay_count_df.sum(axis = 1)/3600 # vehicle hours delay for each link
        delay_count_df.reset_index(inplace = True)
        return delay_count_df # hours

def vhdfc(flow, speed):
    """ Input: flow and speed df with both having length attribute
       Output: VHD for whole area
    """

    fc_att = [1,2,3,4,5]
    vhdfc = []
    for fc in fc_att:
        d_f = flow.copy()
        d_f = d_f[d_f[ 'FUNC_CLASS']==fc]
        d_f.set_index('link_id', inplace = True)
        d_f.iloc[:, :96] = d_f.iloc[:, :96]*15*60  #flow to count

        d_time =  speed.copy()
        d_time = d_time[d_time[ 'FUNC_CLASS']==fc]
        d_time.set_index('link_id', inplace = True)
        d_time.iloc[:, :96] = np.reciprocal(d_time.iloc[:, 0:96])
        d_time.iloc[:, :96] = d_time.iloc[:, :96].mul(d_time['LENGTH(meters)'], axis = 0)   #speed to time (in seconds)

        d_time['tt_free'] = d_time['LENGTH(meters)']/(d_time['SPEED_KPH']*0.277778)  # freeflow tt in seconds
        d_delay = d_time.iloc[:, np.r_[0:96,-1]]
        d_delay = d_delay.sub(d_delay['tt_free'], axis = 0) #delay in seconds
        #delay multiply by count
        delay_count_df =d_delay.iloc[:,0:96].mul(d_f.iloc[:,0:96]) #vehicle seconds delay
        vhdtotal = int(delay_count_df.sum().sum()/3600)#VHD
        vhdfc.append(vhdtotal)
    return vhdfc

def fuel_gallons(fuel):
    """
    Fuel consumption in gallons
    """
    fuelga = fuel.loc[:, '00:00': '23:45'].sum().sum()*0.264172 # gallons
    return np.round(fuelga, decimals = 0)

def fuel_gallons_fc(fuel_len):
    fc_att = [1,2,3,4,5]
    fuega_fc = []
    for fc in fc_att:
        fuel_sub = fuel_len[fuel_len[ 'FUNC_CLASS']==fc]
        fuelga = fuel_sub.loc[:, '00:00': '23:45'].sum().sum()*0.264172 # gallons
        fuega_fc.append(int(fuelga))
    return fuega_fc

def preproces_legs(legs_path):
    """
    Takes in a legs file path and return a legs dataframe
    """
    l1 = pd.read_csv(legs_path, sep = '\t')

    # converting to date time object - takes a long time
    l1['congestedtt'] = pd.to_datetime(l1['duration (congested)'],errors = 'coerce')
    l1['congested_ttsec'] = l1['congestedtt'].dt.hour*3600+ l1['congestedtt'].dt.minute*60 + l1['congestedtt'].dt.second

    l1['startt'] = pd.to_datetime(l1['start time (actual)'],errors = 'coerce')
    l1['startt_hr'] = l1['startt'].dt.hour

    l1['delaytt'] = pd.to_datetime(l1['delay'],errors = 'coerce')
    l1['delay_ttmin'] = l1['delaytt'].dt.hour*60+ l1['delaytt'].dt.minute

    return l1

#Pems Data
def highwaylinks_pemsstation():
    #PeMS highway links and sensors
    pemspath = "/Users/akuncheria/Documents/GSR-2021Feb/UCBerkeley_GSR/PEMS/data" # janes matching of Mobiliti links and PeMS sensor
    pems_stations = pd.read_csv(os.path.join(pemspath, "janes_links_for_pems_sensors11-2022.csv"))
    print(len(pems_stations))
    highways = pd.read_csv(os.path.join(pemspath, "mobiliti_highways.csv"))
    joined = pd.merge(pems_stations,highways, left_on = 'link_id', right_on = 'LINK_ID', how = 'right')
    return joined
