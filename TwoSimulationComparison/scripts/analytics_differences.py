from data import *
from utility import *

def activityplot():
    # gdf links and nodes_path
    gdf_links, gdf_nodes = networkGeom(sf_links,sf_nodes,crs = "epsg:4326")

    #adt whole day
    simulation_one_flow['adt'] = (simulation_one_flow.loc[:,"00:00":"23:45"].sum(axis = 1)*15*60).astype(int)
    simulation_two_flow['adt'] = (simulation_two_flow.loc[:,"00:00":"23:45"].sum(axis = 1)*15*60).astype(int)

    pd.options.mode.chained_assignment = None
    simulation_one_flow['activity'] = np.where(simulation_one_flow['adt']>1, 'yes', 'no')
    simulation_two_flow['activity'] = np.where(simulation_two_flow['adt']>1, 'yes', 'no')
    # gdf
    gdf_links = gdf_links.merge(simulation_one_flow[['link_id', 'adt', 'activity']], left_on = 'LINK_ID', right_on = 'link_id')
    gdf_links = gdf_links.merge(simulation_two_flow[['link_id', 'adt', 'activity']], left_on = 'LINK_ID', right_on = 'link_id')
    gdf_links.rename(columns = { 'adt_x': 'adt_b60', 'activity_x':'activity_b60',  'adt_y':'adt_uet', 'activity_y':'activity_uet'}, inplace = True)

    width, height = 15,14
    fig1, (ax) = plt.subplots(1, 1, figsize=(width, height))
    gdf_links.plot(ax = ax, column = gdf_links['activity_b60'], legend = True,categorical=True)
    plt.show()
    fig1.savefig(processed_path / "b60activity.png", bbox_inches='tight')

    fig2, (ax) = plt.subplots(1, 1, figsize=(width, height))
    gdf_links.plot(ax = ax, column = gdf_links['activity_uet'], legend = True,categorical=True)
    plt.show()
    fig2.savefig(processed_path / "uetactivity.png", bbox_inches='tight')

def congestion_metrics_time_vc(df, timecolumn):
    df_sub = df[[timecolumn,'FUNC_CLASS','SPEED_KPH', 'LENGTH(meters)','CAPACITY(veh/hour)']]
    df_sub['vc'] = df_sub[timecolumn]*3600/df_sub['CAPACITY(veh/hour)']
    congestedmiles = df_sub[df_sub['vc']>=1]['LENGTH(meters)'].sum()*0.000621371
    return int(congestedmiles)

def congestion_metrics_time_speed(df, timecolumn):
    df_sub = df[[timecolumn,'FUNC_CLASS','SPEED_KPH', 'LENGTH(meters)','CAPACITY(veh/hour)']]
    df_sub['speed_freespeed_ratio'] = df_sub[timecolumn]*3.6/df_sub['SPEED_KPH']
    congestedmiles = df_sub[df_sub['speed_freespeed_ratio'] < 0.9]['LENGTH(meters)'].sum()*0.000621371 # 0.9 is taken instaed of 1 to cancel the effect of rounding off errors. 
    return int(congestedmiles)

def comparison():
    # 8am and 4pm
    flow_filter = pd.merge(simulation_one_flow[['link_id', '08:00','13:00','16:00','FUNC_CLASS']], simulation_two_flow[['link_id', '08:00','13:00','16:00']], left_on = 'link_id', right_on = 'link_id', how = 'left')
    speed_filter = pd.merge(simulation_one_speed[['link_id', '08:00','13:00','16:00','FUNC_CLASS']], simulation_two_speed[['link_id', '08:00','13:00','16:00']], left_on = 'link_id', right_on = 'link_id', how = 'left')

    f1 = plotscatter(flow_filter['08:00_x'], flow_filter['08:00_y'],flow_filter['FUNC_CLASS'], title = 'Flow(veh/sec) at 8am', savename = 'flow8am',xlabel = sim_one_name ,ylabel = sim_two_name, processed_path = processed_path)
    f2 = plotscatter(speed_filter['08:00_x'], speed_filter['08:00_y'],speed_filter['FUNC_CLASS'], title = 'Speed (m/sec) at 8am', savename = 'speed8am',xlabel = sim_one_name ,ylabel = sim_two_name, processed_path = processed_path)
    f3 = plotscatter(flow_filter['16:00_x'], flow_filter['16:00_y'],flow_filter['FUNC_CLASS'], title = 'Flow(veh/sec) at 4pm', savename = 'flow4pm',xlabel = sim_one_name ,ylabel = sim_two_name, processed_path = processed_path)
    f4 = plotscatter(speed_filter['16:00_x'], speed_filter['16:00_y'],speed_filter['FUNC_CLASS'], title = 'Speed (m/sec) at 4pm', savename = 'speed4pm',xlabel = sim_one_name ,ylabel = sim_two_name, processed_path = processed_path)
    f5 = plotscatter(flow_filter['13:00_x'], flow_filter['13:00_y'],flow_filter['FUNC_CLASS'], title = 'Flow(veh/sec) at 1pm', savename = 'flow1pm',xlabel = sim_one_name ,ylabel = sim_two_name, processed_path = processed_path)
    f6 = plotscatter(speed_filter['13:00_x'], speed_filter['13:00_y'],speed_filter['FUNC_CLASS'], title = 'Speed (m/sec) at 1pm', savename = 'speed1pm',xlabel = sim_one_name ,ylabel = sim_two_name, processed_path = processed_path)

    #capacity congestion metric
    sim1_congestedmiles_8am_vc = congestion_metrics_time_vc(df = simulation_one_flow, timecolumn = '08:00')
    sim2_congestedmiles_8am_vc = congestion_metrics_time_vc(df = simulation_two_flow, timecolumn = '08:00')
    sim1_congestedmiles_4pm_vc = congestion_metrics_time_vc(df = simulation_one_flow, timecolumn = '16:00')
    sim2_congestedmiles_4pm_vc = congestion_metrics_time_vc(df = simulation_two_flow, timecolumn = '16:00')
    sim1_congestedmiles_8pm_vc = congestion_metrics_time_vc(df = simulation_one_flow, timecolumn = '20:00')
    sim2_congestedmiles_8pm_vc = congestion_metrics_time_vc(df = simulation_two_flow, timecolumn = '20:00')
    
    #speed congestion metric
    sim1_congestedmiles_8am_speedratio = congestion_metrics_time_speed(df = simulation_one_speed, timecolumn = '08:00')
    sim2_congestedmiles_8am_speedratio  = congestion_metrics_time_speed(df = simulation_two_speed, timecolumn = '08:00')
    sim1_congestedmiles_4pm_speedratio = congestion_metrics_time_speed(df = simulation_one_speed, timecolumn = '16:00')
    sim2_congestedmiles_4pm_speedratio  = congestion_metrics_time_speed(df = simulation_two_speed, timecolumn = '16:00')
    sim1_congestedmiles_8pm_speedratio = congestion_metrics_time_speed(df = simulation_one_speed, timecolumn = '20:00')
    sim2_congestedmiles_8pm_speedratio  = congestion_metrics_time_speed(df = simulation_two_speed, timecolumn = '20:00')

    activitydf = pd.DataFrame(columns = ['Metric',sim_one_name, sim_two_name])
    activitydf['Metric'] = ['Miles active at 8am', 'Miles active at 4pm', 
    'Congested Miles (V/C > 1) at 8am','Congested Miles (V/C > 1) at 4pm','Congested Miles (V/C > 1) at 8pm',
    'Congested Miles (speed/freespeed < 0.9) at 8am','Congested Miles (speed/freespeed < 0.9) at 4pm','Congested Miles (speed/freespeed < 0.9) at 8pm']
    activitydf[sim_one_name] = [int(simulation_one_flow[simulation_one_flow['08:00']>0]['LENGTH(meters)'].sum()*0.000621371),
    int(simulation_one_flow[simulation_one_flow['16:00']>0]['LENGTH(meters)'].sum()*0.000621371),
    sim1_congestedmiles_8am_vc,sim1_congestedmiles_4pm_vc,sim1_congestedmiles_8pm_vc,
    sim1_congestedmiles_8am_speedratio,sim1_congestedmiles_4pm_speedratio,sim1_congestedmiles_8pm_speedratio ]
    
    activitydf[sim_two_name] = [int(simulation_two_flow[simulation_two_flow['08:00']>0]['LENGTH(meters)'].sum()*0.000621371), 
    int(simulation_two_flow[simulation_two_flow['16:00']>0]['LENGTH(meters)'].sum()*0.000621371),
    sim2_congestedmiles_8am_vc,sim2_congestedmiles_4pm_vc, sim2_congestedmiles_8pm_vc,
    sim2_congestedmiles_8am_speedratio,sim2_congestedmiles_4pm_speedratio,sim2_congestedmiles_8pm_speedratio ]

    activitydf.loc[:, sim_one_name] = activitydf[sim_one_name].map('{:,d}'.format) 
    activitydf.loc[:, sim_two_name] = activitydf[sim_two_name].map('{:,d}'.format) 
    activitydf.to_csv(processed_path/f"activitydf.csv", index = False)
    print(activitydf)

if __name__ == '__main__':
    #activityplot()
    comparison()
