import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import os
from shapely.geometry import Point
import shapely.geometry as geom

class Network():
    def load_citylinks(self, nodepath, linkpath):
        nodes = pd.read_csv(nodepath)
        links = pd.read_csv(linkpath)
        print("Number of nodes:", len(nodes),"Number oflinks:", len(links))
        linkslength = links['LENGTH(meters)'].sum()*0.000621371  #miles
        return  nodes, links, linkslength

class ReadingFiles():
    def generateColumnNames(self):
        """
        Generates column names for the mobiliti results output
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

    def read_file(self, path):
        colnames = self.generateColumnNames()
        file = pd.read_csv(path, sep = '\t',header = 0, names = colnames)
        file.drop(file.columns[len(file.columns)-1], axis=1, inplace=True) #dropping the last Nan column
        return file

    def results_city_len(self,path, links):
        flow_c  = self.read_file(path).merge(links, left_on = 'link_id', right_on = 'LINK_ID', how = 'left')
        return flow_c

    def resultscity_filter(self,path,citylinks):
        flow = self.read_file(path)
        flow_sub = flow[flow.link_id.isin(citylinks.LINK_ID)]
        return flow_sub

    def resultscity_filter_len(flow,citylinks):
        """
        Filtering flow or speed results for a city and adding link attributes to it.
        """
        flow_sub = flow[flow.link_id.isin(citylinks.LINK_ID)]
        flow_c  = flow_sub.merge(citylinks, left_on = 'link_id', right_on = 'LINK_ID', how = 'left')
        return flow_c

def len_network(links):
    return links['LENGTH(meters)'].sum()*0.000621371  #miles

def adt(flow):
    return flow.iloc[:,1:97].sum(axis = 1)*15*60

def vmt(flow):
    """
    Vehicle Miles Travelled.
    Flow df needs to have the link atrribute length in it
    """
    vmt = np.sum(flow.loc[:,"00:00":"23:45"].sum(axis = 1)*15*60*flow.loc[:,'LENGTH(meters)']*0.000621371) #count*length of road VMT
    return np.round(vmt, decimals=0)

def vmtfc(flow_len):
    """
    Vehicle Miles Travelled by Functional class.
    Flow df needs to have the link atrribute length in it
    """
    fc_att = [1,2,3,4,5]
    vmtfc = []
    for fc in fc_att:
        flow_sub = flow_len[flow_len[ 'FUNC_CLASS']==fc]
        vmt = np.around(np.sum(flow_sub.iloc[:,1:97].sum(axis = 1)*15*60*flow_sub.loc[:,'LENGTH(meters)']*0.000621371))
        vmtfc.append(vmt)
    return vmtfc

def fuel_gallons(fuel_city):
    time = fuel_city.columns[1:97]
    fuel_b = []
    for i in time:
        fuel_b.append(fuel_city[i].sum())
    fuelga = np.sum(fuel_b)*0.264172 #gallons
    return np.round(fuelga, decimals = 0)

def vht(flow, speed):
    d_f = flow.copy()
    d_f.set_index('link_id', inplace = True)
    d_f.iloc[:, 0:96] = d_f.iloc[:, :96]*15*60  #flow to count

    d_time =  speed.copy()
    d_time.set_index('link_id', inplace = True)
    d_time.iloc[:, :96] = np.reciprocal(d_time.iloc[:, 0:96])
    d_time.iloc[:, :96] = d_time.iloc[:, :96].mul(d_time['LENGTH(meters)'], axis = 0)   #speed to time

    a_vht =d_f.iloc[:,0:96].mul(d_time.iloc[:,0:96])
    vht = np.sum(a_vht.sum(axis = 1)/60/60) # VHT
    return np.round(vht, decimals = 0)

def vhtfc(flow, speed):
    fc = [1,2,3,4,5]
    vhtfc = []
    for i in fc:
        d_f = flow[flow['FUNC_CLASS']==i]
        d_f.set_index('link_id', inplace = True)
        d_f.iloc[:, 0:96] = d_f.iloc[:, :96]*15*60  #flow to count

        d_time = speed[speed['FUNC_CLASS']==i]
        d_time.set_index('link_id', inplace = True)
        d_time.iloc[:, :96] = np.reciprocal(d_time.iloc[:, 0:96])
        d_time.iloc[:, :96] = d_time.iloc[:, :96].mul(d_time['LENGTH(met'], axis = 0)   #speed to time

        a_vht =d_f.iloc[:,0:96].mul(d_time.iloc[:,0:96])
        vht = np.around(np.sum(a_vht.sum(axis = 1)/60/60))# VHT
        vhtfc.append(vht)
    return vhtfc

def add_len(delaydf,linksdf):
    """
    Adding the liks details to the Dealy dataframe
    """
    delaydf.reset_index(inplace = True)
    delaydf = delaydf.merge(linksdf, left_on = 'link_id', right_on = 'LINK_ID', how = 'left')
    return delaydf

def cliplinks(boundry_shp,gdf_sf_nodes,gdf_sflinks, cityname):
    print("Reading in", cityname)
    sj_poly = gpd.read_file(boundry_shp) #sj boundary from HERE
    print("CRS is", sj_poly.crs)
    print("CLipping Nodes....")
    clipped_sjnodes = gpd.clip(gdf_sf_nodes,sj_poly)
    print("Number of Nodes", len(clipped_sjnodes))
    print("Clipping Links....")
    clipped_sjlinks = gpd.clip(gdf_sflinks,sj_poly)
    print("Number of Links", len(clipped_sjlinks))
    #Saving the clipped SJ links and nodes as shapefile and csv
    #clipped_sjnodes.to_csv(cityname + '_nodes.csv', index = False)
    clipped_sjlinks.to_csv(cityname + '_links.csv', index = False)

def vhd(flow, speed, delaydf = False):
    """Input: flow and speed df with both having length attribute
       Output: VHD for whole area
     """
    d_f = flow.copy()
    d_f.set_index('link_id', inplace = True)
    d_f.loc[:,"00:00":"23:45"] = d_f.loc[:,"00:00":"23:45"]*15*60  #flow to count

    d_time =  speed.copy()
    d_time.set_index('link_id', inplace = True)
    d_time.loc[:,"00:00":"23:45"] = np.reciprocal(d_time.loc[:,"00:00":"23:45"])
    d_time.loc[:, "00:00":"23:45"] = d_time.loc[:,"00:00":"23:45"].mul(d_time['LENGTH(meters)'], axis = 0)   #speed to time (in seconds)

    d_time['tt_free'] = d_time['LENGTH(meters)']/(d_time['SPEED_KPH']*0.277778)  # freeflow tt in seconds

    d_delay = d_time[['00:00','00:15','00:30','00:45','1','1:15','1:30','1:45','2:00','2:15', '2:30','2:45','3:00','3:15', '3:30','3:45','4:00','4:15','4:30','4:45','5:00','5:15','5:30','5:45','6:00','6:15','6:30','6:45','7:00','7:15','7:30','7:45','8:00','8:15','8:30','8:45','9:00','9:15','9:30','9:45',
                      '10:00','10:15','10:30','10:45','11:00','11:15','11:30','11:45','12:00','12:15','12:30','12:45','13:00','13:15',
                      '13:30', '13:45','14:00', '14:15','14:30', '14:45', '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30', '16:45','17:00', '17:15','17:30',
                      '17:45','18:00','18:15', '18:30', '18:45', '19:00', '19:15', '19:30', '19:45', '20:00', '20:15', '20:30',
                      '20:45', '21:00', '21:15', '21:30', '21:45','22:00', '22:15','22:30', '22:45', '23:00', '23:15', '23:30', '23:45','tt_free']]

    d_delay = d_delay.sub(d_delay['tt_free'], axis = 0) #delay in seconds
    #delay multiply by count
    delay_count_df =d_delay.loc[:,"00:00":"23:45"].mul(d_f.loc[:,"00:00":"23:45"]) #vehicle seconds delay

    if delaydf == False:
        return np.round(delay_count_df.sum().sum()/3600 ,decimals=0)#VHD
    else:
        delay_count_df['VHD_link'] = delay_count_df.sum(axis = 1)/3600 # vehicle hours delay for each link
        delay_count_df.reset_index(inplace = True)
        return delay_count_df # hours

def vhd_evening(flow, speed, delaydf = False):
    """
    Input: flow and speed df with both having length attribute
    Output: VHD for Evening 3-7pm
    """
    d_f = flow.copy()
    d_f.set_index('link_id', inplace = True)
    d_f.iloc[:, :96] = d_f.iloc[:, :96]*15*60  #flow to count

    d_time =  speed.copy()
    d_time.set_index('link_id', inplace = True)
    d_time.iloc[:, :96] = np.reciprocal(d_time.iloc[:, 0:96])
    d_time.iloc[:, :96] = d_time.iloc[:, :96].mul(d_time['LENGTH(meters)'], axis = 0)   #speed to time (in seconds)

    d_time['tt_free'] = d_time['LENGTH(meters)']/(d_time['SPEED_KPH']*0.277778)  # freeflow tt in seconds

    d_delay = d_time[['00:00','00:15','00:30','00:45','1','1:15','1:30','1:45','2:00','2:15', '2:30','2:45','3:00','3:15', '3:30','3:45','4:00','4:15','4:30','4:45','5:00','5:15','5:30','5:45','6:00','6:15','6:30','6:45','7:00','7:15','7:30','7:45','8:00','8:15','8:30','8:45','9:00','9:15','9:30','9:45',
                      '10:00','10:15','10:30','10:45','11:00','11:15','11:30','11:45','12:00','12:15','12:30','12:45','13:00','13:15',
                      '13:30', '13:45','14:00', '14:15','14:30', '14:45', '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30', '16:45','17:00', '17:15','17:30',
                      '17:45','18:00','18:15', '18:30', '18:45', '19:00', '19:15', '19:30', '19:45', '20:00', '20:15', '20:30',
                      '20:45', '21:00', '21:15', '21:30', '21:45','22:00', '22:15','22:30', '22:45', '23:00', '23:15', '23:30', '23:45','tt_free']]

    d_delay = d_delay.sub(d_delay['tt_free'], axis = 0) #delay in seconds
    #delay multiply by count
    delay_count_df =d_delay.loc[:,"00:00":"23:45"].mul(d_f.loc[:,"00:00":"23:45"]) #vehicle seconds delay


    if delaydf == False:
        return np.round(delay_count_df.loc[:,'15:00':'18:45'].sum().sum()/3600 ,decimals=0)# Evening VHD
    else:
        delay_count_df['VHD_link'] = delay_count_df.loc[:,'15:00':'18:45'].sum(axis = 1)/3600 # vehicle hours delay for each link in the evening peak
        delay_count_df.reset_index(inplace = True)
        return delay_count_df[['link_id','VHD_link']] # hours

def links_geom(links, nodes):
    links['ref_lat'] = links['REF_IN_ID'].map(nodes.set_index('NODE_ID')['LAT'])
    links['ref_long'] = links['REF_IN_ID'].map(nodes.set_index('NODE_ID')['LON'])
    links['nref_lat'] = links['NREF_IN_ID'].map(nodes.set_index('NODE_ID')['LAT'])
    links['nref_long'] = links['NREF_IN_ID'].map(nodes.set_index('NODE_ID')['LON'])
    return links

def geom_shp(linksgeom, savename):
    """
    Create shapefile from geom csv (CRS is GC WGS 84, epsg 4326)
    """
    linksgeom['geometry'] = linksgeom.apply(lambda x: geom.LineString([(x['ref_long'], x['ref_lat']) , (x['nref_long'], x['nref_lat'])]), axis = 1)
    # create the GeoDatFrame
    crs = {"init": "epsg:4326"}
    linksgeom_gdf = gpd.GeoDataFrame(linksgeom, geometry = linksgeom.geometry, crs=crs)
    # save the GeoDataFrame
    linksgeom_gdf.to_file(driver = 'ESRI Shapefile', filename= savename)

#Visualisation
def link_dualplot(flowdf, speeddf, linkid):
    flowdf.set_index('link_id', inplace = True)
    speeddf.set_index('link_id', inplace = True)

    fig, ax1 = plt.subplots(figsize = (12,8))
    color = 'tab:blue'
    ax1.set_xlabel('Time of Day')
    ax1.set_ylabel('Flow (veh/hour)', color=color)
    ax1.plot(flowdf.columns[0:96].values, flowdf.loc[linkid,"00:00":"23:45"].values*3600, label = 'Flow',color = color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.axhline(y= sf_links[sf_links['LINK_ID']== linkid]['CAPACITY(veh/hour)'].values, color= color, linestyle='dotted', label = 'Capacity')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:orange'
    ax2.set_ylabel('Speed(mph)', color=color)  # we already handled the x-label with ax1
    plt.plot(speeddf.loc[linkid,"00:00":"23:45"].values*2.23, label = 'Speed', color = color)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.axhline(y= sf_links[sf_links['LINK_ID']==linkid]['SPEED_KPH'].values*0.6213, color=color, linestyle='dotted', label = 'Free speed')

    fig.tight_layout()
    ax1.xaxis.set_major_locator(plt.MaxNLocator(11))
    ax1.legend(loc='lower left')
    ax2.legend(loc='upper right')
    plt.title("Flow and Speeds: {}".format(linkid))
    plt.show();

#Plot flow or speeds
def plot_single(flowdf, linkid):
    plt.figure(figsize = (8,6))
    plt.plot(((flowdf[flowdf['link_id'] ==  linkid].iloc[:,np.arange(1,97,4)])*2.24).T, label = 'Flow')
    plt.axhline(y= sf_links[sf_links['LINK_ID']== link_id]['SPEED_KPH'].values*0.621371, color='r', linestyle='dotted', label = 'free speed(mph)')
    plt.xticks(rotation=90)
    plt.title(" Flow for linkid: {}".format(linkid))
    plt.legend()
    plt.show();

#PLOTTING IN kepler
def kepler_geom(df, sjcity_links, sfnodespath):
    df_g = df.merge(sjcity_links, left_on = 'link_id', right_on = 'LINK_ID', how = 'left')
    sf_nodes = pd.read_csv(sfnodespath)

    df_g['ref_lat'] = df_g['REF_IN_ID'].map(sf_nodes.set_index('NODE_ID')['LAT'])
    df_g['ref_long'] = df_g['REF_IN_ID'].map(sf_nodes.set_index('NODE_ID')['LON'])
    df_g['nref_lat'] = df_g['NREF_IN_ID'].map(sf_nodes.set_index('NODE_ID')['LAT'])
    df_g['nref_long'] = df_g['NREF_IN_ID'].map(sf_nodes.set_index('NODE_ID')['LON'])
    df_g.to_csv(index = False)
    return df_g

def kepler_geom_v3(df_len):
    '''The df has len in it'''
    sf_nodes = pd.read_csv("/Users/akuncheria/Documents/GSR-2021Feb/UCBerkeley_GSR/Networks_Dataset/networks_dataset_Mobiliti/Nov2019/for_drive/september2020/sf_nodes.csv")
    df_len['ref_lat'] = df_len['REF_IN_ID'].map(sf_nodes.set_index('NODE_ID')['LAT'])
    df_len['ref_long'] = df_len['REF_IN_ID'].map(sf_nodes.set_index('NODE_ID')['LON'])
    df_len['nref_lat'] = df_len['NREF_IN_ID'].map(sf_nodes.set_index('NODE_ID')['LAT'])
    df_len['nref_long'] = df_len['NREF_IN_ID'].map(sf_nodes.set_index('NODE_ID')['LON'])
    return df_len

#plotting lesgs in KEPLER
def kepler_legs(leg):
    sf_nodes = pd.read_csv("/Users/akuncheria/Documents/GSR-2021Feb/UCBerkeley_GSR/Networks_Dataset/networks_dataset_Mobiliti/Nov2019/for_drive/september2020/sf_nodes.csv")

    leg['ref_lat'] = leg['start node'].map(sf_nodes.set_index('NODE_ID')['LAT'])
    leg['ref_long'] = leg['start node'].map(sf_nodes.set_index('NODE_ID')['LON'])
    leg['nref_lat'] = leg['end node'].map(sf_nodes.set_index('NODE_ID')['LAT'])
    leg['nref_long'] = leg['end node'].map(sf_nodes.set_index('NODE_ID')['LON'])
    return leg

# shapefile to geojson
def shp_gjson(shp_path, json_path):
    import geopandas as gpd
    shp = gpd.read_file(shp_path)
    shp.to_file(os.path.join(json_path), driver='GeoJSON')

def preproces1(legs_path):
    ''' Takes in a legs file path and return a legs dataframe '''
    l1 = pd.read_csv(legs_path, sep = '\t')
    # converting to date time object - takes a long time
    l1['congestedtt'] = pd.to_datetime(l1['duration (congested)'],errors = 'coerce')
    l1['congested_ttsec'] = l1['congestedtt'].dt.hour*3600+ l1['congestedtt'].dt.minute*60 + l1['congestedtt'].dt.second

    #l1['startt'] = pd.to_datetime(l1['start time (actual)'],errors = 'coerce')
    #l1['startt_hr'] = l1['startt'].dt.hour
    #l1['delaytt'] = pd.to_datetime(l1['delay'],errors = 'coerce')
    #l1['delay_ttmin'] = l1['delaytt'].dt.hour*60+ l1['delaytt'].dt.minute
    return l1

def networkGeom(links,nodes, crs = "epsg:4326"):
    nodes['geom'] = [Point(xy) for xy in zip(nodes.LON, nodes.LAT)]
    gdf_nodes = gpd.GeoDataFrame(nodes, geometry=nodes.geom, crs = crs)
    links['ref_lat'] = links['REF_IN_ID'].map(nodes.set_index('NODE_ID')['LAT'])
    links['ref_long'] = links['REF_IN_ID'].map(nodes.set_index('NODE_ID')['LON'])
    links['nref_lat'] = links['NREF_IN_ID'].map(nodes.set_index('NODE_ID')['LAT'])
    links['nref_long'] = links['NREF_IN_ID'].map(nodes.set_index('NODE_ID')['LON'])
    links['geometry'] = links.apply(lambda x: geom.LineString([(x['ref_long'], x['ref_lat']) , (x['nref_long'], x['nref_lat'])]), axis = 1)
    gdf_links = gpd.GeoDataFrame(links, geometry = links.geometry, crs = crs)
    return gdf_links, gdf_nodes
