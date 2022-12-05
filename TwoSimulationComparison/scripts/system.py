from data import *
from utility import *

data_simulations = [[sim_one_name,simulation_one_flow,simulation_one_speed,simulation_one_fuel],
[sim_two_name, simulation_two_flow,simulation_two_speed, simulation_two_fuel]]

def system_metrics():
    names, vmts, vhds, fuel = ([] for i in range(4))
    for d in data_simulations:
        names.append(d[0])
        vmts.append(int(vmt(d[1])/1000))
        vhds.append(vhd(d[1], d[2]))
        fuel.append(int(fuel_gallons(d[3])/1000))

    systemdf = pd.DataFrame(list(zip(names,vmts, vhds, fuel)),
               columns =[ 'Name', 'VMT (thousand miles)', 'VHD', 'Fuel Consumption (thousand gallons)'])
    systemdf.loc[:, 'VMT (thousand miles)'] = systemdf['VMT (thousand miles)'].map('{:,}'.format) #to format numbers with commas
    systemdf.loc[:, 'VHD'] = systemdf['VHD'].map('{:,}'.format)
    systemdf.loc[:, 'Fuel Consumption (thousand gallons)'] = systemdf['Fuel Consumption (thousand gallons)'].map('{:,}'.format)
    print(systemdf)
    return systemdf

def system_metrics_functionalclass():
    vmt_params = []
    vhd_params = []
    fuel_params = []
    for d in data_simulations:
        vmt_params.append(int(val/1000000) for val in vmtfc(d[1]))
        vhd_params.append(int(val/1000) for val in vhdfc(d[1],d[2]))
        fuel_params.append(int(val/1000) for val in fuel_gallons_fc(d[3]))
   
    dodged_barplot(vmt_params[0],vmt_params[1],'VMT', sim_one_name, sim_two_name, 'Functional class', 'VMT (in million miles)',processed_path)
    dodged_barplot(vhd_params[0],vhd_params[1],'VHD',sim_one_name, sim_two_name,'Functional class', 'VHD (in thousand hours)',processed_path)
    dodged_barplot(fuel_params[0],fuel_params[1],'Fuel', sim_one_name, sim_two_name, 'Functional class', 'Fuel Consumption (in thousand gallons)',processed_path)
   
def leg_level_metrics():
    leg_simulation_one = preprocess_legs(sim_one_legspath)
    leg_simulation_two = preprocess_legs(sim_two_legspath)

    #Trips greater than 5 hours
    sim1_time5 = len(leg_simulation_one[leg_simulation_one['congested_ttmin']>5*60])
    sim2_time5 = len(leg_simulation_two[leg_simulation_two['congested_ttmin']>5*60])
    sim1_time10 = len(leg_simulation_one[leg_simulation_one['congested_ttmin']>10*60])
    sim2_time10 = len(leg_simulation_two[leg_simulation_two['congested_ttmin']>10*60])

    #Mean
    metrics = ['Average Trip Distance(miles)', 'Average Travel Time(min)', 'Average Trip Delay(min)','Number of trips with TT > 5 hours','Number of trips with TT > 10 hours']
    sim1_metrics = [np.round(get_mean(leg_simulation_one['total distance (m)'])*0.000621371, decimals = 1),
    get_mean(leg_simulation_one['congested_ttmin']),
    get_mean(leg_simulation_one['delay_ttmin']),
    int(sim1_time5),
    int(sim1_time10) ]

    sim2_metrics = [np.round(get_mean(leg_simulation_two['total distance (m)'])*0.000621371, decimals = 1),
    get_mean(leg_simulation_two['congested_ttmin']),
    get_mean(leg_simulation_two['delay_ttmin']),
    int(sim2_time5),
    int(sim2_time10)]
    legssystemdf = pd.DataFrame(list(zip(metrics, sim1_metrics, sim2_metrics)),columns =[ 'Metric', sim_one_name, sim_two_name])
    print(legssystemdf)
    legssystemdf.to_csv(processed_path/f"legssystemdf_mean.csv", index = False)

    #Median and P95
    metrics = ['P50 Trip Distance(miles)', 'P50 Travel Time(min)', 'P50 Trip Delay(min)',
    'P95 Trip Distance(miles)', 'P95 Travel Time(min)', 'P95 Trip Delay(min)']
    sim1_metrics = [np.round(get_median(leg_simulation_one['total distance (m)'])*0.000621371, decimals = 1),
    get_median(leg_simulation_one['congested_ttmin']),
    get_median(leg_simulation_one['delay_ttmin']),
    np.round(p95(leg_simulation_one['total distance (m)'])*0.000621371, decimals = 1),
    p95(leg_simulation_one['congested_ttmin']),
    p95(leg_simulation_one['delay_ttmin'])]

    sim2_metrics = [np.round(get_median(leg_simulation_two['total distance (m)'])*0.000621371, decimals = 1),
    get_median(leg_simulation_two['congested_ttmin']),
    get_median(leg_simulation_two['delay_ttmin']),
    np.round(p95(leg_simulation_two['total distance (m)'])*0.000621371, decimals = 1),
    p95(leg_simulation_two['congested_ttmin']),
    p95(leg_simulation_two['delay_ttmin'])]

    legssystemdf = pd.DataFrame(list(zip(metrics, sim1_metrics, sim2_metrics)),columns =[ 'Metric', sim_one_name, sim_two_name])
    print(legssystemdf)
    legssystemdf.to_csv(processed_path/f"legssystemdf_median.csv",index = False)

    #histplot of p95 data
    #travel time
    p95_congested_tt_sim_one = p95(leg_simulation_one['congested_ttmin'])  
    p95_congested_tt_sim_two = p95(leg_simulation_two['congested_ttmin']) 
    data1 = leg_simulation_one[leg_simulation_one['congested_ttmin'] < p95_congested_tt_sim_one]['congested_ttmin']
    data2 = leg_simulation_two[leg_simulation_two['congested_ttmin'] < p95_congested_tt_sim_two]['congested_ttmin']
    histplot_two_data(data1, data2,label1 = sim_one_name , label2 = sim_two_name , 
                        xlabel = "Travel Time (min)", title = " Distribution of Trip Travel Times (P95)",
                        savename = "congested_tt", processed_path = processed_path ,alphas = 0.5, color1 = 'tab:blue', color2 = 'tab:orange')
    
    #delay
    p95_delay_sim_one = p95(leg_simulation_one['delay_ttmin']) 
    p95_delay_sim_two = p95(leg_simulation_two['delay_ttmin']) 
    data1 = leg_simulation_one[leg_simulation_one['delay_ttmin'] < p95_delay_sim_one]['delay_ttmin']
    data2 = leg_simulation_two[leg_simulation_two['delay_ttmin'] < p95_delay_sim_two]['delay_ttmin']
    histplot_two_data(data1, data2,label1 = sim_one_name , label2 = sim_two_name , 
                        xlabel = "Delay (min)", title = "Distribution of Trip Delay (P95)",
                        savename = "delay",processed_path = processed_path , alphas = 0.5, color1 = 'tab:blue', color2 = 'tab:orange' )

if __name__ == "__main__":
    system_metrics()
    system_metrics_functionalclass()
    leg_level_metrics()

