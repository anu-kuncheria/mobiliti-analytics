import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import os
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

#1.Plot pems with confidence intervals
def plot_pems_confidenceintervals_flow(title, linkid,stationid,normalday_flow,pems):
    """
    normalday_flow ->
    normalday_flow = read_file(os.path.join(rootPath, "2022-03-26-sf_rsr_baseline_060_noscen_links","avg_flow_rates.tsv"))
    path = "/Users/akuncheria/Documents/GSR-2021Feb/UCBerkeley_GSR/Networks_Dataset/networks_dataset_Mobiliti/Nov2019/for_drive/July2021"
    sf_links = pd.read_csv(os.path.join(path,'sf_links.csv'))
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
    
#1.2 Plot pems with confidence intervals Speed
def plot_pems_confidenceintervals_speed(title, linkid,stationid,normalday_speed,pems):
    """
    normalday_speed ->
    normalday_speed = read_file(os.path.join(rootPath, "2022-03-26-sf_rsr_baseline_060_noscen_links","avg_speeds.tsv"))
    path = "/Users/akuncheria/Documents/GSR-2021Feb/UCBerkeley_GSR/Networks_Dataset/networks_dataset_Mobiliti/Nov2019/for_drive/July2021"
    sf_links = pd.read_csv(os.path.join(path,'sf_links.csv'))
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

# 2. BPR like plots
def plot_speedflow_scatter(linkid,*data):
    '''
    Returns flow - speed diagram like BPR /MFD diagram
    The order of *data is flow,speed,label, color.
    Can input as many results as you need.
    >>>df_2result = [baselineflow50, baselinespeed50, 'Baseline50','red', uet_flow, uet_speed, 'UET','blue']
    >>> plot_speedflows(812618472,df_2result)
    '''
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

#3. Pems validation Flow or Speed Plots - single day
def plot_pems(day,linkid,stationid, *data, pems ,title ,  flows = True):
    '''
    Returns flow or speed comparison with PEMS dataset
    The order in which flows are given in determines the R2 labels - so double check.
    
    usuage:
    df_flow = [flow_sce_constdemand_len,"sce, no change in demand",'red', flow_c5s60_len,"sce, c5s60",'green']
    plot_pems(7,1080910205,402815,df_flow , pems = dist4df , flows = True)
    '''
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
    
# 4. Simple Flows or speed plots for links
def plot_flow_speed(linkid, *data, flows = True):
    '''
    Returns flow or speed plots. 
    Usuage:
    -> data contains flow, label and color attributes. 
    plot_flow_speed(1080910205,flow_normal_loi,"normal", "red", flow_sce_constdemand_loi, "change", "blue", flows = True)
    '''
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
        linestyles = ['-','--','-.',':']
        for f,l,c, ls in zip(fdf,l,c, linestyles):
            ax.plot(f.loc[linkid,"00:00":"23:45"].values*15*60, color = c,label = l,linewidth = 1.5,linestyle=ls)

        ax.text(30,100,'Capacity(v/hr): {}'.format(int(fdf[0].loc[linkid, 'CAPACITY(veh/hour)'])))
        ax.axhline(y= int(fdf[0].loc[linkid, 'CAPACITY(veh/hour)']/4), color='slategray', linestyle='dashed',linewidth = 2)
        ax.axvline(x = 44, color = 'black', linestyle = '--', alpha = 0.7)
        ax.axvline(x = 80, color = 'black', linestyle = '--', alpha = 0.7)
        
        ax.set_xlabel("Time of day")
        ax.set_ylabel("Flow(veh per 15 min)")
        ax.xaxis.set_tick_params(rotation=90)
        ax.xaxis.set_major_locator(plt.MaxNLocator(24))
        plt.title ("Link:{}, {}".format(linkid, fdf[0].loc[linkid, 'ST_NAME']))
        plt.legend(loc='upper right')
        #plt.savefig("{}.png".format(title))
        #plt.show();
        #return fig;

    else:
        fig, ax = plt.subplots(figsize = (10,8))
        for f,l,c in zip(fdf,l,c):
            ax.plot(f.loc[linkid,"00:00":"23:45"].values*2.23694, color = c,label = l,linewidth = 1.5)

        ax.text(5,20,'Free Speed in Mobiliti(mph): {}'.format(int(fdf[0].loc[linkid, 'SPEED_KPH']*0.621371)))
        ax.axhline(y= int(fdf[0].loc[linkid, 'SPEED_KPH']*0.621371), color= 'slategray', linestyle='dashed',linewidth = 2)
        ax.set_xlabel("Time of day")
        ax.set_ylabel("Speed(mph)")
        ax.xaxis.set_tick_params(rotation=90)
        ax.xaxis.set_major_locator(plt.MaxNLocator(24))
        plt.title ("Link:{}, {}".format(linkid, fdf[0].loc[linkid, 'ST_NAME']))
        plt.legend(loc='upper right')
        #plt.savefig("{}.png".format(title))
        #plt.show();
        #return fig;
