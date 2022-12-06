import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import os
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

# General Plotting
def map_node_geometry(links, linkcol, nodes, nodecol):
    return links[linkcol].map(nodes.set_index('NODE_ID')[nodecol])

def links_geom(links,nodes):
    """
    Adding geometry to the links file
    """
    colnamelist = [['ref_lat','REF_IN_ID','LAT'], ['ref_long','REF_IN_ID','LON'],
                  ['nref_lat','NREF_IN_ID','LAT'],['nref_long','NREF_IN_ID','LON']]
    for v in colnamelist:
        links[v[0]] = map_node_geometry(links,v[1],nodes,v[2])
    return links

def geom_shp(linksgeom, savename):
    """
    Creates links shapefile from links geometry csv (CRS is GC WGS 84, epsg 4326)
    """
    import shapely.geometry as geom
    linksgeom['geometry'] = linksgeom.apply(lambda x: geom.LineString([(x['ref_long'], x['ref_lat']) , (x['nref_long'], x['nref_lat'])]), axis = 1)
    crs = {"init": "epsg:4326"}
    linksgeom_gdf = gpd.GeoDataFrame(linksgeom, geometry = linksgeom.geometry, crs=crs)
    linksgeom_gdf.to_file(driver = 'ESRI Shapefile', filename= savename)

def kepler_geom(df, sf_links, sf_nodes):
    """
    Adding geometry to any dataframe,e.g, flows or speeds, from links and nodes file
    """
    df_geom = df.merge(sf_links, left_on = 'link_id', right_on = 'LINK_ID', how = 'left')
    
    colnamelist = [['ref_lat','REF_IN_ID','LAT'], ['ref_long','REF_IN_ID','LON'],
                  ['nref_lat','NREF_IN_ID','LAT'],['nref_long','NREF_IN_ID','LON']]
    for v in colnamelist:
        df_geom[v[0]] = map_node_geometry(df_geom,v[1],sf_nodes,v[2])
    return df_geom

def kepler_geom_withattributes(df_len, sfnodespath):
    """
    Adding geometry to any dataframe,e.g, flows or speeds,that already has link attributes in it.
    """
    sf_nodes = pd.read_csv(sfnodespath)
    colnamelist = [['ref_lat','REF_IN_ID','LAT'], ['ref_long','REF_IN_ID','LON'],
                  ['nref_lat','NREF_IN_ID','LAT'],['nref_long','NREF_IN_ID','LON']]
    for v in colnamelist:
        df_len[v[0]] = map_node_geometry(df_len,v[1],sf_nodes,v[2])
    return df_len

def kepler_legs(leg,nodespath):
    """
    Plotting legs file in Kepler
    """
    nodes = pd.read_csv(nodespath)

    colnamelist = [['ref_lat','start node','LAT'], ['ref_long','start node','LON'],
                  ['nref_lat','end node','LAT'],['nref_long','end node','LON']]
    for v in colnamelist:
        leg[v[0]] = map_node_geometry(leg,v[1],nodes,v[2])
    return leg

def shp_gjson(shp_path, json_path):
    """
    Converts a shapefile to geojson
    """
    shp = gpd.read_file(shp_path)
    shp.to_file(os.path.join(json_path), driver='GeoJSON')

def plot_speedflow_scatter(linkid,*data):
    """
    #BPR like plots
    Returns flow - speed diagram like BPR /MFD diagram
    The order of *data is flow,speed,label, color.
    Can input as many results as you need.
    >>>df_2result = [baselineflow50, baselinespeed50, 'Baseline50','red', uet_flow, uet_speed, 'UET','blue']
    >>> plot_speedflows(812618472,df_2result)
    """

    elem = [len(a) for a in data][0]
    fdf = []
    sdf = []
    l = []
    c = []
    for i in range(0,elem,4):
        f = data[0][i]
        f = f.set_index('link_id')
        fdf.append(f)
        s = data[0][i+1]
        s = s.set_index('link_id')
        sdf.append(s)
        lv = data[0][i+2]
        l.append(lv)
        cv = data[0][i+3]
        c.append(cv)

    fig, ax = plt.subplots(figsize = (5,3))
    for f,s,l,c in zip(fdf, sdf,l,c):
        ax.scatter(f.loc[linkid,"00:00":"23:45"].values, s.loc[linkid,"00:00":"23:45"].values,s =10, color = c,label = l)

    ax.axvline(x= fdf[0].loc[linkid, 'CAPACITY(veh/hour)']/3600, color= 'slategray', linestyle='dotted', label = 'Capacity')
    ax.set_xlabel("Flow (veh/s)")
    ax.set_ylabel("Speed (m/s)")
    plt.title ("Link:{}, {}".format(linkid, fdf[0].loc[linkid, 'ST_NAME']))
    plt.legend()
    #plt.savefig("{}.png".format(linkid))
    #plt.show();
    return fig

def plot_flow_speed(linkid, *data, flows = True, attr = "", processed_path):
    """
    #Flows or speed plots for links
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

#PeMS plots
def plot_pems_confidenceintervals_flow(title, linkid,stationid,normalday_flow,pems):
    """
    # Plot pems with confidence intervals
    normalday_flow ->
    normalday_flow = read_file(os.path.join(rootPath, "2022-03-26-sf_rsr_baseline_060_noscen_links","avg_flow_rates.tsv"))
    linkspath = " "
    sf_links = pd.read_csv(os.path.join(linkspath,'sf_links.csv'))
    normalday_flow = results_city_len(normalday_flow,sf_links)
    normalday_flow.set_index('link_id', inplace = True)
    """
    sub = pems[(pems['Station']== stationid)]
    meanflow = sub.groupby('time_minutes')['TotalFlow'].mean().to_frame().reset_index(drop = False)
    stdflow = sub.groupby('time_minutes')['TotalFlow'].agg('std').to_frame().reset_index(drop = False)
    stdflow2 = (sub.groupby('time_minutes')['TotalFlow'].agg('std')*2).to_frame().reset_index(drop = False)
    N = 3
    m= meanflow.groupby(meanflow.index // N).sum()
    s = stdflow.groupby(stdflow.index // N).sum()
    s2 = stdflow2.groupby(stdflow2.index // N).sum()

    linkflow = normalday_flow.loc[linkid, '00:00':'23:45'].values*15*60
    linkcapacity = normalday_flow.loc[linkid,'CAPACITY(veh/hour)']/4

    fig = plt.figure(figsize = (12,6))
    ax = fig.add_subplot(111)
    width = 0.3
    x = np.arange(len(m))
    ax.plot(x,m['TotalFlow'].values, color = 'orange', label = "Pems")
    ax.fill_between(x, m['TotalFlow']-s['TotalFlow'],m['TotalFlow']+ s['TotalFlow'], alpha=0.2, color = 'orange', label = "1 SD")
    ax.fill_between(x, m['TotalFlow']-s2['TotalFlow'],m['TotalFlow']+ s2['TotalFlow'], alpha=0.2, color = 'red', label = "2 SD")
    ax.plot(x,linkflow, color = 'green', label = "Simulation: Normal Day")
    ax.axhline(y= linkcapacity, color='slategray', linestyle='dashed',linewidth = 2, label = "Capacity(veh/15min)")

    #relative error and r-square
    from scipy import stats
    x = linkflow
    y = m['TotalFlow']
    slope, intercept, r_value,_,_ = stats.linregress(x.astype(float), y)
    adt_diff = (x.sum()-y.sum())/y.sum()*100

    ax.text(0.8,0.15,'R-square: {}'.format(np.round(r_value**2,4)),horizontalalignment='left',verticalalignment='bottom',transform=ax.transAxes)
    #ax.text(0.8,0.1,'ADT Diff (%): {}'.format(np.round(adt_diff,0)),horizontalalignment='left',verticalalignment='bottom',transform=ax.transAxes)
    plt.xlabel("Time")
    plt.ylabel("Flow (veh/15 minutes)")
    plt.title(title)
    plt.legend(loc = 'upper right')
    plt.savefig("{}_normalday.png".format(title))
    plt.show();

def plot_pems_confidenceintervals_speed(title, linkid,stationid,normalday_speed,pems):
    """
    # Plot pems with confidence intervals Speed
    normalday_speed ->
    normalday_speed = read_file(os.path.join(rootPath, "2022-03-26-sf_rsr_baseline_060_noscen_links","avg_speeds.tsv"))
    linkspath = ' '
    sf_links = pd.read_csv(os.path.join(linkspath,'sf_links.csv'))
    normalday_speed = results_city_len(normalday_speed,sf_links)
    normalday_speed.set_index('link_id', inplace = True)
    """
    sub = pems[(pems['Station']== stationid)]
    meanspeed = sub.groupby('time_minutes')['AvgSpeed'].mean().to_frame().reset_index(drop = False)
    stdspeed = sub.groupby('time_minutes')['AvgSpeed'].agg('std').to_frame().reset_index(drop = False)
    stdspeed2 = (sub.groupby('time_minutes')['AvgSpeed'].agg('std')*2).to_frame().reset_index(drop = False)
    N = 3
    m= meanspeed.groupby(meanspeed.index // N).mean()
    s = stdspeed.groupby(stdspeed.index // N).mean()
    s2 = stdspeed2.groupby(stdspeed2.index // N).mean()

    linkspeed = normalday_speed.loc[linkid, '00:00':'23:45'].values*2.23694 #mph
    linkfreespeed = normalday_speed.loc[linkid,'SPEED_KPH']*0.621371

    fig = plt.figure(figsize = (12,6))
    ax = fig.add_subplot(111)
    width = 0.3
    x = np.arange(len(m))
    ax.plot(x,m['AvgSpeed'].values, color = 'orange', label = "Pems")
    ax.fill_between(x, m['AvgSpeed']-s['AvgSpeed'],m['AvgSpeed']+ s['AvgSpeed'], alpha=0.2, color = 'orange', label = "1 SD")
    ax.fill_between(x, m['AvgSpeed']-s2['AvgSpeed'],m['AvgSpeed']+ s2['AvgSpeed'], alpha=0.2, color = 'red', label = "2 SD")
    ax.plot(x,linkspeed, color = 'green', label = "Simulation")
    ax.axhline(y= linkfreespeed, color='slategray', linestyle='dashed',linewidth = 2, label = "Free speed")

    #relative error and r-square
    from scipy import stats
    x = linkspeed
    y = m['AvgSpeed']
    slope, intercept, r_value,_,_ = stats.linregress(x.astype(float), y)

    ax.text(0.8,0.15,'R-square: {}'.format(np.round(r_value**2,4)),horizontalalignment='left',verticalalignment='bottom',transform=ax.transAxes)

    plt.xlabel("Time")
    plt.ylabel("Speed (mph)")
    plt.title(title)
    plt.legend(loc = 'upper right')
    #plt.savefig("{}_normalday.png".format(title))
    plt.show();

def plot_pems(day,linkid,stationid, *data, pems ,title ,  flows = True):
    """
    # Pems validation Flow or Speed Plots - single day
    Returns flow or speed comparison with PEMS dataset
    The order in which flows are given in determines the R2 labels - so double check.

    usuage:
    df_flow = [flow_sce_constdemand_len,"sce, no change in demand",'red', flow_c5s60_len,"sce, c5s60",'green']
    plot_pems(7,1080910205,402815,df_flow , pems = dist4df , flows = True)
    """

    elem = [len(a) for a in data][0]
    fdf = []
    l = []
    c = []
    for i in range(0,elem,3):
        f = data[0][i]
        f = f.set_index('link_id')
        fdf.append(f)
        lv = data[0][i+1]
        l.append(lv)
        cv = data[0][i+2]
        c.append(cv)

    #PEMS
    df_6 = pems[(pems['day']== day) & (pems['Station']== stationid)].set_index('timestamp').resample('15T').agg({'TotalFlow':np.sum,'AvgSpeed':np.mean })
    df_6.reset_index(inplace = True)

    if flows == True:
        fig, ax = plt.subplots(figsize = (15,8))
        xloc, yloc = 0.82,0.80
        linestyles = ['-','--','-.',':']
        for f,l,c,ls in zip(fdf,l,c, linestyles):
            ax.plot(f.loc[linkid,"00:00":"23:45"].values*15*60, color = c,label = l,linewidth = 3, alpha=0.7, linestyle=ls)
            from scipy import stats
            #r square values
            x = f.loc[linkid,'00:00':'23:45'].values*15*60
            y = df_6['TotalFlow']
            slope, intercept, r_value,_,_ = stats.linregress(x.astype(float), y)
            ax.text(xloc,yloc,'R-square {}: {}'.format(l, np.round(r_value**2,4)),horizontalalignment='left',verticalalignment='bottom', transform=ax.transAxes )
            yloc-=.05

        ax.axhline(y= int(fdf[0].loc[linkid, 'CAPACITY(veh/hour)']/4), color='brown', linestyle='dashed',linewidth = 1, label = 'Capacity (veh/15min')
        ax.plot(df_6['TotalFlow'], label = 'Pems', color = 'orange' )
        ax.axvline(x = 44, color = 'black', linestyle = '--', alpha = 0.7)
        ax.axvline(x = 80, color = 'black', linestyle = '--', alpha = 0.7)

        #ax.text(0.63,0.05,'Capacity(v/hr): {}'.format(int(fdf[0].loc[linkid, 'CAPACITY(veh/hour)'])),horizontalalignment='left',verticalalignment='bottom', transform=ax.transAxes)
        #ax.axhline(y= int(fdf[0].loc[linkid, 'CAPACITY(veh/hour)']/4), color= 'slategray', linestyle='dashed',linewidth = 2)
        ax.set_xlabel("Time of day")
        ax.set_ylabel("Flow(veh per 15 min)")

        ax.xaxis.set_tick_params(rotation=90)
        ax.xaxis.set_major_locator(plt.MaxNLocator(24))

        #title = "Link:{}, {}".format(linkid, fdf[0].loc[linkid, 'ST_NAME'])
        plt.title(title)
        plt.legend(loc='upper right')
        plt.savefig("{}.png".format(title))
        plt.show();
        #return fig;

    else:
        fig, ax = plt.subplots(figsize = (8,5))
        xloc, yloc = 0.63,0.15
        for f,l,c in zip(fdf,l,c):
            ax.plot(f.loc[linkid,"00:00":"23:45"].values*2.23694, color = c,label = l,linewidth = 1.5)
            #r square values
            x = f.loc[linkid,'00:00':'23:45']*2.23694
            y = df_6['AvgSpeed']
            from scipy import stats
            slope, intercept, r_value,_,_ = stats.linregress(x.astype(float), y)
            ax.text(xloc,yloc,'R-square {}: {}'.format(l,np.round(r_value**2,4)),horizontalalignment='left',verticalalignment='bottom', transform=ax.transAxes )
            yloc-=.05


        ax.plot(df_6['AvgSpeed'], label = 'Pems', color = 'orange' )
        ax.text(0.63,0.05,'Free Speed in Mobiliti(mph): {}'.format(int(fdf[0].loc[linkid, 'SPEED_KPH']*0.621371)),
                horizontalalignment='left',verticalalignment='bottom', transform=ax.transAxes )

        ax.axhline(y= int(fdf[0].loc[linkid, 'SPEED_KPH']*0.621371), color= 'slategray', linestyle='dashed',linewidth = 2)
        ax.set_xlabel("Time of day")
        ax.set_ylabel("Speed(mph)")
        ax.xaxis.set_tick_params(rotation=90)
        ax.xaxis.set_major_locator(plt.MaxNLocator(24))
        ax.yaxis.set_major_locator(MultipleLocator(5))
        ax.set_ylim(ymin=10)
        plt.title ("Link:{}, {}".format(linkid, fdf[0].loc[linkid, 'ST_NAME']))
        plt.legend(loc='upper right')
        #plt.savefig("{}.png".format(title))
        plt.show();
        #return fig;

#Other general plots
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

def plot_single(flowdf, linkid):
    """
    Plot flow or speeds
    """
    plt.figure(figsize = (8,6))
    plt.plot(((flowdf[flowdf['link_id'] ==  linkid].iloc[:,np.arange(1,97,4)])*2.24).T, label = 'Flow')
    plt.axhline(y= sf_links[sf_links['LINK_ID']== link_id]['SPEED_KPH'].values*0.621371, color='r', linestyle='dotted', label = 'free speed(mph)')
    plt.xticks(rotation=90)
    plt.title(" Flow for linkid: {}".format(linkid))
    plt.legend()
    plt.show();
