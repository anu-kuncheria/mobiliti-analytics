import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import os
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


# 1. BPR like plots
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

#2. Pems validation Flow or Speed Plots
def plot_pems(day,linkid,stationid, *data, pems , flows = True):
    '''
    Returns flow or speed compariosn with PEMS dataset
    The order in which flows are given in determines the R2 labels - so double check.
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
        fig, ax = plt.subplots(figsize = (8,5))
        xloc, yloc = 0.63,0.15
        for f,l,c in zip(fdf,l,c):
            ax.plot(f.loc[linkid,"00:00":"23:45"].values*15*60, color = c,label = l,linewidth = 1.5)
            from scipy import stats
            #r square values
            x = f.loc[linkid,'00:00':'23:45'].values*15*60
            y = df_6['TotalFlow']
            slope, intercept, r_value,_,_ = stats.linregress(x.astype(float), y)
            ax.text(xloc,yloc,'R-square {}: {}'.format(l, np.round(r_value**2,4)),horizontalalignment='left',verticalalignment='bottom', transform=ax.transAxes )
            yloc-=.05


        ax.plot(df_6['TotalFlow'], label = 'Pems', color = 'orange' )
        ax.text(0.63,0.05,'Capacity(v/hr): {}'.format(int(fdf[0].loc[linkid, 'CAPACITY(veh/hour)'])),horizontalalignment='left',verticalalignment='bottom', transform=ax.transAxes)
        ax.axhline(y= int(fdf[0].loc[linkid, 'CAPACITY(veh/hour)']/4), color= 'slategray', linestyle='dashed',linewidth = 2)
        ax.set_xlabel("Time of day")
        ax.set_ylabel("Flow(veh per 15 min)")
        ax.xaxis.set_tick_params(rotation=90)
        ax.xaxis.set_major_locator(plt.MaxNLocator(24))

        plt.title ("Link:{}, {}".format(linkid, fdf[0].loc[linkid, 'ST_NAME']))
        plt.legend(loc='upper right')
        #plt.savefig("{}.png".format(title))
        #plt.show();
        return fig;

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
        #plt.show();
        return fig;

# 3. Simple Flows or speed plots for links
def plot_flow_speed(linkid, *data, flows = True):
    '''
    Returns flow or speed plots
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

    if flows == True:
        fig, ax = plt.subplots(figsize = (8,5))
        for f,l,c in zip(fdf,l,c):
            ax.plot(f.loc[linkid,"00:00":"23:45"].values*15*60, color = c,label = l,linewidth = 1.5)

        ax.text(30,100,'Capacity(v/hr): {}'.format(int(fdf[0].loc[linkid, 'CAPACITY(veh/hour)'])))
        ax.axhline(y= int(fdf[0].loc[linkid, 'CAPACITY(veh/hour)']/4), color='slategray', linestyle='dashed',linewidth = 2)
        ax.set_xlabel("Time of day")
        ax.set_ylabel("Flow(veh per 15 min)")
        ax.xaxis.set_tick_params(rotation=90)
        ax.xaxis.set_major_locator(plt.MaxNLocator(24))
        plt.title ("Link:{}, {}".format(linkid, fdf[0].loc[linkid, 'ST_NAME']))
        plt.legend(loc='upper right')
        #plt.savefig("{}.png".format(title))
        #plt.show();
        return fig;

    else:
        fig, ax = plt.subplots(figsize = (8,5))
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
        return fig;
