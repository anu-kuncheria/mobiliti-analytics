import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import shapely.geometry as geom
import seaborn as sns


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

def generateColumnNames():
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
    colnames = generateColumnNames()
    file = pd.read_csv(path, sep = '\t',header = None, names =colnames)
    file.drop(file.columns[len(file.columns)-1], axis=1, inplace=True) #dropping the last Nan column
    return file

def results_city_len(flow,links):
    flow_c  = flow.merge(links, left_on = 'link_id', right_on = 'LINK_ID', how = 'left')
    return flow_c

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

def results_city_len(flow,links):
    flow_c  = flow.merge(links, left_on = 'link_id', right_on = 'LINK_ID', how = 'left')
    return flow_c

def generateColumnNamesFigures():
    """
    Generates column names for the mobiliti results output.
    """
    result = ['00:00']
    minc, hourc = 0,0
    for i in range(0,95):
        minc +=1
        if minc % 4 == 0:
            minc = 0
            hourc +=1
        mindigit =  "00" if minc==0 else str(minc*15)
        result.append('%02d'%hourc + ':' + mindigit)
    return result


def plot_flow_speed(linkid, *data, flows = True, attr = "", processed_path):
    """
    Returns flow or speed plots.
    Usuage:
    -> data contains flow, label and color attributes.
    plot_flow_speed(1080910205,flow_normal_loi,"normal", "red", flow_sce_constdemand_loi, "change", "blue", flows = True)
    """

    elem = len([len(a) for a in data])
    fdf = []
    l = []
    c = []
    for i in range(0,elem,3):
        f = data[i]
        f = f.set_index('link_id')
        fdf.append(f)
        lv = data[i+1]
        l.append(lv)
        cv = data[i+2]
        c.append(cv)

    if flows == True:
        fig, ax = plt.subplots(figsize = (10,8))
        for f,l,c in zip(fdf,l,c):
            ax.plot(f.loc[linkid,"00:00":"23:45"].values*15*60, color = c,label = l,linewidth = 1.5)

        ax.text(30,100,'Capacity(v/hr): {}'.format(int(fdf[0].loc[linkid, 'CAPACITY(veh/hour)'])))
        ax.axhline(y= int(fdf[0].loc[linkid, 'CAPACITY(veh/hour)']/4), color='slategray', linestyle='dashed',linewidth = 2)
        ax.set_xlabel("Time of day")
        ax.set_ylabel("Flow(veh per 15 min)")
        pos = list(range(0,96,4))
        ax.set_xticks(pos)
        ax.set_xticklabels([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
        ax.xaxis.set_tick_params(rotation=90)

        plt.title ("Link:{}, {}, {}".format(linkid, fdf[0].loc[linkid, 'ST_NAME'], attr))
        plt.legend(loc='upper right')
        plt.savefig(processed_path /"{}flows.png".format(linkid))
        #plt.show();
        #return fig;

    else:
        fig, ax = plt.subplots(figsize = (10,8))
        for f,l,c in zip(fdf,l,c):
            ax.plot(f.loc[linkid,"00:00":"23:45"].values*2.23694, color = c,label = l,linewidth = 1.5)

        ax.text(5,20,'Free Speed in Mobiliti(mph): {}'.format(int(fdf[0].loc[linkid, 'SPEED_KPH']*0.621371)))
        ax.axhline(y= fdf[0].loc[linkid, 'SPEED_KPH']*0.621371, color= 'slategray', linestyle='dashed',linewidth = 2)
        ax.set_xlabel("Time of day")
        ax.set_ylabel("Speed(mph)")

        pos = list(range(0,96,4))
        ax.set_xticks(pos)
        ax.set_xticklabels([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
        ax.xaxis.set_tick_params(rotation=90)

        #ax.xaxis.set_major_locator(plt.MaxNLocator(24))
        plt.title ("Link:{}, {}, {}".format(linkid, fdf[0].loc[linkid, 'ST_NAME'], attr))
        plt.legend(loc='upper right')
        plt.savefig(processed_path /"{}speed.png".format(linkid))
        #plt.show();
        #return fig;

def format_commas_twodecimal(num):
    return "{0:,.2f}".format(num) #string

def addlabels(x,y, width = 0):
    for i in x:
        plt.text(i+width,y[i-1],y[i-1],ha = 'center')
        #plt.text(i+width,y[i],y[i],ha = 'center')

def dodged_barplot(values1, values2,title, label1, label2, xlabel, ylabel,processed_path):
    N = len(values1)
    assert len(values1) == len(values2)

    ind = np.arange(1, N+1)  # the x locations for the groups
    width = 0.35       # the width of the bars
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind,values1, width, color='royalblue', label = label1)
    addlabels(ind,values1,width = 0)
    rects2 = ax.bar(ind+width, values2, width, color='seagreen', label = label2)
    addlabels(ind,values2,width = width )
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.savefig(processed_path /"{}_dodgeplot.png".format(title))
    return fig

def preprocess_legs(legs_path):
    """ Takes in a legs file path and return a legs dataframe
    """
    l1 = pd.read_csv(legs_path, sep = '\t')
    # converting to date time object - expensive step
    l1['congestedtt'] = pd.to_datetime(l1['duration (congested)'],errors = 'coerce',format = "%H:%M:%S.%f")
    l1['congested_ttmin'] = l1['congestedtt'].dt.hour*60+ l1['congestedtt'].dt.minute + l1['congestedtt'].dt.second/60
    # l1['startt'] = pd.to_datetime(l1['start time (actual)'],errors = 'coerce',format = "%d:%H:%M:%S.%f")
    # l1['startt_hr'] = l1['startt'].dt.hour
    l1['delaytt'] = pd.to_datetime(l1['delay'],errors = 'coerce',format = "%H:%M:%S.%f")
    l1['delay_ttmin'] = l1['delaytt'].dt.hour*60+ l1['delaytt'].dt.minute + l1['delaytt'].dt.second/60
    return l1

def get_median(pdseries):
    return np.round(np.nanmedian(pdseries), decimals = 1)

def get_mean(pdseries):
    return np.round(np.nanmean(pdseries), decimals = 1)

def p95(array):
    arr =array[np.logical_not(np.isnan(array))] #remove null if any
    return np.round(np.percentile(arr,95), decimals = 1)

def boxplot(pdseries1, pdseries2, title,processed_path,savename):
    fig = plt.figure()
    plt.boxplot(pdseries1)
    plt.boxplot(pdseries2)
    plt.title(title)
    plt.legend()
    plt.savefig(processed_path /"{}_boxplot.png".format(savename))

def histplot_two_data(data1, data2,label1, label2 , xlabel, title,savename,processed_path, alphas = 0.5, color1 = 'tab:blue', color2 = 'tab:orange'):
    plt.figure()
    plt.hist(data1 ,alpha = alphas, label = label1, color = color1 )
    plt.hist( data2, alpha = alphas, label = label2, color = color2)
    plt.legend(loc='upper right')
    plt.xlabel(xlabel)
    plt.title(title)
    plt.legend()
    plt.savefig(processed_path /"{}_hist.png".format(savename))

def plotscatter(x,y,z, title, savename, xlabel,ylabel,processed_path):
    fig1 = plt.figure(figsize=(8,6))
    sns.scatterplot(x,y, hue = z ,figure=fig1,palette=['green','orange','brown','dodgerblue','red'], legend='full')
    plt.xlabel(xlabel,figure=fig1 )
    plt.ylabel(ylabel,figure=fig1)
    plt.title(title)
    plt.legend()
    fig1.savefig(processed_path / savename, bbox_inches='tight')
