from data import *
from utility import *

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

    scatterplot_flowparams = [['08:00_x','08:00_y','Flow(veh/sec) at 8am','flow8am'],
    ['16:00_x','16:00_y','Flow(veh/sec) at 4pm','flow4pm'],
    ['13:00_x','13:00_y','Flow(veh/sec) at 1pm','flow1pm']]
    for params in scatterplot_flowparams:
        plotscatter(flow_filter[params[0]], flow_filter[params[1]],flow_filter['FUNC_CLASS'], title = params[2], savename = params[3],xlabel = sim_one_name ,ylabel = sim_two_name, processed_path = processed_path)

    scatterplot_speedparams = [['08:00_x','08:00_y','Speed (m/sec) at 8am','speed8am'],
        ['16:00_x','16:00_y','Speed (m/sec) at 4pm','speed4pm'],
        ['13:00_x','13:00_y','Speed (m/sec) at 1pm','speed1pm']]
    for params in scatterplot_speedparams:
        plotscatter(speed_filter[params[0]], speed_filter[params[1]],speed_filter['FUNC_CLASS'], title = params[2], savename = params[3],xlabel = sim_one_name ,ylabel = sim_two_name, processed_path = processed_path)


    #capacity congestion metric, speed congestion metric
    vc_params = {'08:00':[sim1_congestedmiles_8am_vc,sim2_congestedmiles_8am_vc,sim1_congestedmiles_8am_speedratio, sim2_congestedmiles_8am_speedratio],
    '16:00':[sim1_congestedmiles_4pm_vc,sim2_congestedmiles_4pm_vc, sim1_congestedmiles_4pm_speedratio, sim2_congestedmiles_4pm_speedratio], 
    '20:00':[sim1_congestedmiles_8pm_vc,sim2_congestedmiles_8pm_vc, sim1_congestedmiles_8pm_speedratio, sim2_congestedmiles_8pm_speedratio]}
    for time,var in vc_params.items():
        var[0] = congestion_metrics_time_vc(df = simulation_one_flow, timecolumn = time)
        var[1] = congestion_metrics_time_vc(df = simulation_two_flow, timecolumn = time)
        var[2] = congestion_metrics_time_speed(df = simulation_one_speed, timecolumn = time)
        var[3] = congestion_metrics_time_speed(df = simulation_two_speed, timecolumn = time)
   

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
    comparison()
