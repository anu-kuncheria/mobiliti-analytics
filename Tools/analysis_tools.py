import pandas as pd
import numpy as np
import os

#A. Reading in files
class Network():
    def load_citylinks(self, nodepath, linkpath):
        nodes = pd.read_csv(nodepath)
        links = pd.read_csv(linkpath)
        print("Number of nodes:", len(nodes),"Number oflinks:", len(links))
        linkslength = links['LENGTH(meters)'].sum()*0.000621371  #miles
        return  nodes, links, linkslength

class ReadingFiles():
    def read_file(self, path):
        colnames = ['link_id', "00:00", "00:15", "00:30","00:45","1","1:15","1:30","1:45","2:00","2:15","2:30","2:45","3:00",
                   "3:15","3:30","3:45","4:00","4:15","4:30","4:45","5:00","5:15","5:30","5:45","6:00","6:15","6:30","6:45",
                    "7:00","7:15","7:30","7:45","8:00","8:15","8:30","8:45","9:00","9:15","9:30","9:45","10:00","10:15","10:30","10:45",
                   "11:00","11:15","11:30","11:45","12:00","12:15","12:30","12:45","13:00","13:15","13:30","13:45","14:00","14:15","14:30","14:45",
                   "15:00","15:15","15:30","15:45","16:00","16:15","16:30","16:45","17:00","17:15","17:30","17:45","18:00","18:15","18:30","18:45",
                   "19:00","19:15","19:30","19:45","20:00","20:15","20:30","20:45","21:00","21:15","21:30","21:45","22:00","22:15","22:30","22:45",
                    "23:00","23:15","23:30","23:45",'NAN']
        file = pd.read_csv(path, sep = '\t',header = 0, names = colnames)
        file.drop(file.columns[len(file.columns)-1], axis=1, inplace=True) #dropping the last Nan column
        return file

    #Add link attributes to the flow or speed
    def results_city_len(self,path, links):
        flow_c  = self.read_file(path).merge(links, left_on = 'link_id', right_on = 'LINK_ID', how = 'left')
        return flow_c

    # Filtering results for a city
    def resultscity_filter(self,path,citylinks):
        flow = self.read_file(path)
        flow_sub = flow[flow.link_id.isin(citylinks.LINK_ID)]
        return flow_sub


#B. Transportation Metrics
#1. VMT
def vmt(flowdf):
    '''Vehicle Miles Travelled.
    Flow df needs to have the link atrribute length in it'''
    vmt = np.sum(flowdf.iloc[:,1:97].sum(axis = 1)*15*60*flowdf.loc[:,'LENGTH(meters)']*0.000621371) #count*length of road VMT
    return np.round(vmt, decimals=0)

def vmtfc(flowdf):
    '''Vehicle Miles Travelled by Functional class.
    Flow df needs to have the link atrribute length in it'''
    fc_att = [1,2,3,4,5]
    vmtfc = []
    for fc in fc_att:
        flow_sub = flow_len[flow_len[ 'FUNC_CLASS']==fc]
        vmt = np.around(np.sum(flow_sub.iloc[:,1:97].sum(axis = 1)*15*60*flow_sub.loc[:,'LENGTH(meters)']*0.000621371))
        vmtfc.append(vmt)
    return vmtfc

#2. VHD
def vhd(flowdf, speeddf, delaydf = False):
    '''Input: flow and speed df with both having length attribute
       Output: VHD for whole area'''

    d_f = flowdf.copy()
    d_f.set_index('link_id', inplace = True)
    d_f.iloc[:, :96] = d_f.iloc[:, :96]*15*60  #flow to count

    d_time =  speeddf.copy()
    d_time.set_index('link_id', inplace = True)
    d_time.iloc[:, :96] = np.reciprocal(d_time.iloc[:, 0:96])
    d_time.iloc[:, :96] = d_time.iloc[:, :96].mul(d_time['LENGTH(meters)'], axis = 0)   #speed to time (in seconds)
    d_time['tt_free'] = d_time['LENGTH(meters)']/(d_time['SPEED_KPH']*0.277778)  # freeflow tt in seconds

    cols = d_time.columns.tolist()
    cols = cols[0:96] + [cols[-1]]
    d_delay = d_time[cols]
    d_delay = d_delay.sub(d_delay['tt_free'], axis = 0) #delay in seconds
    delay_count_df =d_delay.iloc[:,0:96].mul(d_f.iloc[:,0:96]) #vehicle seconds delay


    if delaydf == False:
        return delay_count_df.sum().sum()/3600 #VHD
    else:
        delay_count_df['VHD_link'] = delay_count_df.sum(axis = 1)/3600 # vehicle hours delay for each link
        delay_count_df.reset_index(inplace = True)
        return delay_count_df # hours

#3. Fuel
def fuel_gallons(fueldf):
    '''Fuel comsumption.'''
    time = fueldf.columns[1:97]
    fuel_b = []
    for i in time:
        fuel_b.append(fueldf[i].sum())
    fuelga = np.sum(fuel_b)*0.264172 #gallons
    return np.round(fuelga, decimals = 0)

#4. ADT Average daily traffic count
def ADT(flowdf):
 flowdf['ADT'] = np.round(flowdf.iloc[:,1:97].sum(axis = 1)*15*60,decimals=-1)
 return flowdf

#C. Visualisation Plots

#1. Dual plots for Flow and speed for a link
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
    ax2.set_ylabel('Speed(mph)', color=color)
    plt.plot(speeddf.loc[linkid,"00:00":"23:45"].values*2.23, label = 'Speed', color = color)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.axhline(y= sf_links[sf_links['LINK_ID']==linkid]['SPEED_KPH'].values*0.6213, color=color, linestyle='dotted', label = 'Free speed')

    fig.tight_layout()
    ax1.xaxis.set_major_locator(plt.MaxNLocator(11))
    ax1.legend(loc='lower left')
    ax2.legend(loc='upper right')
    plt.title("Flow and Speeds: {}".format(linkid))
    plt.show();


#2. Single plots for flow or speeds
def plot_single(flowdf, linkid):
    plt.figure(figsize = (8,6))
    plt.plot(((flowdf[flowdf['link_id'] ==  linkid].iloc[:,np.arange(1,97,4)])*2.24).T, label = 'Flow')
    plt.axhline(y= sf_links[sf_links['LINK_ID']== link_id]['SPEED_KPH'].values*0.621371, color='r', linestyle='dotted', label = 'free speed(mph)')
    plt.xticks(rotation=90)
    plt.title(" Flow for linkid: {}".format(linkid))
    plt.legend()
    plt.show();


#D. Miscellaneous
#1. For plotting in KEPLER
def kepler_geom_v3(flowdf):
    '''The df has len in it'''
    flowdf['ref_lat'] = flowdf['REF_IN_ID'].map(nodes.set_index('NODE_ID')['LAT'])
    flowdf['ref_long'] = flowdf['REF_IN_ID'].map(nodes.set_index('NODE_ID')['LON'])
    flowdf['nref_lat'] = flowdf['NREF_IN_ID'].map(nodes.set_index('NODE_ID')['LAT'])
    flowdf['nref_long'] = flowdf['NREF_IN_ID'].map(nodes.set_index('NODE_ID')['LON'])
    flowdf.to_csv("{}_kepler.csv".format(flowdf), index = False) #writes a csv file

#2. Unpacking TGZ file
import zipfile,fnmatch,os,tarfile
rootPath = "/Users/akuncheria/Documents/GSR-2021Feb/UCBerkeley_GSR/Results_Mobiliti/2021-02-04-SFAddedFreightDemand"
pattern = '*.tgz'
for root, dirs, files in os.walk(rootPath):
    for filename in fnmatch.filter(files, pattern):
        zip_ref = tarfile.open(os.path.join(rootPath,filename)) # create tarfile object and open
        zip_ref.extractall(os.path.join(root,  os.path.splitext(filename)[0])) # extract file to dir
        zip_ref.close() # close file
