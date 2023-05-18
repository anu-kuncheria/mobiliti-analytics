from load_data import *
import utility as util

def leg_metrics():
    leg_simulation_one = util.preprocess_legs(sim_one_legspath)
    leg_simulation_two = util.preprocess_legs(sim_two_legspath)

    #Trips greater than 5 and 10 hours
    x = lambda sim,time_min : len(sim[sim['congested_ttmin']>time_min])
    sim1_time5, sim2_time5 = x(leg_simulation_one, 5*60), x(leg_simulation_two,5*60)
    sim1_time10,sim2_time10 = x(leg_simulation_two, 10*60), x(leg_simulation_two, 10*60)

    #Mean
    metrics = ['Number of Trips','Average Trip Distance(miles)', 'Average Travel Time(min)', 'Average Trip Delay(min)','Number of trips with TT > 5 hours','Number of trips with TT > 10 hours']
    
    sim1_metrics = ["{:,}".format(len(leg_simulation_one)),
                    np.round(util.get_mean(leg_simulation_one['total distance (m)'])*0.000621371, decimals = 1),
                    util.get_mean(leg_simulation_one['congested_ttmin']),
                    util.get_mean(leg_simulation_one['delay_ttmin']),
                    int(sim1_time5),
                    int(sim1_time10) ]
    
    sim2_metrics = ["{:,}".format(len(leg_simulation_two)),
                    np.round(util.get_mean(leg_simulation_two['total distance (m)'])*0.000621371, decimals = 1),
                    util.get_mean(leg_simulation_two['congested_ttmin']),
                    util.get_mean(leg_simulation_two['delay_ttmin']),
                    int(sim2_time5),
                    int(sim2_time10)]
    
    legssystemdf = pd.DataFrame(list(zip(metrics, sim1_metrics, sim2_metrics)),columns =[ 'Metric', sim_one_name, sim_two_name])
    print(legssystemdf)
    legssystemdf.to_csv(processed_path/f"legssystemdf_mean.csv", index = False)

    #Median and P95
    metrics = ['P50 Trip Distance(miles)', 'P50 Travel Time(min)', 'P50 Trip Delay(min)',
    'P95 Trip Distance(miles)', 'P95 Travel Time(min)', 'P95 Trip Delay(min)']

    sim1_metrics = [ np.round(util.get_median(leg_simulation_one['total distance (m)'])*0.000621371, decimals = 1),
                    util.get_median(leg_simulation_one['congested_ttmin']),
                    util.get_median(leg_simulation_one['delay_ttmin']),
                    np.round(util.p95(leg_simulation_one['total distance (m)'])*0.000621371, decimals = 1),
                    util.p95(leg_simulation_one['congested_ttmin']),
                    util.p95(leg_simulation_one['delay_ttmin'])]
    
    sim2_metrics = [np.round(util.get_median(leg_simulation_two['total distance (m)'])*0.000621371, decimals = 1),
                    util.get_median(leg_simulation_two['congested_ttmin']),
                    util.get_median(leg_simulation_two['delay_ttmin']),
                    np.round(util.p95(leg_simulation_two['total distance (m)'])*0.000621371, decimals = 1),
                    util.p95(leg_simulation_two['congested_ttmin']),
                    util.p95(leg_simulation_two['delay_ttmin'])]

    legssystemdf = pd.DataFrame(list(zip(metrics, sim1_metrics, sim2_metrics)),columns =[ 'Metric', sim_one_name, sim_two_name])
    print(legssystemdf)
    legssystemdf.to_csv(processed_path/f"legssystemdf_median.csv",index = False)

    #Distribution plot for data less than p95 for time and delay 
    
    #trip time
    data1 = util.p95_data(df = leg_simulation_one, col = 'congested_ttmin')
    data2 = util.p95_data(df = leg_simulation_two, col = 'congested_ttmin')
    util.histplot_two_data(data1, data2,label1 = sim_one_name , label2 = sim_two_name , 
                           xlabel = "Travel Time (min)", title = " Distribution of Trip Travel Times (P95)",
                           savename = "congested_tt", processed_path = processed_path ,alphas = 0.5, color1 = 'tab:blue', color2 = 'tab:orange')
    
    #trip delay
    data1 = util.p95_data(df = leg_simulation_one, col = 'delay_ttmin')
    data2 = util.p95_data(df = leg_simulation_two, col = 'delay_ttmin')
    util.histplot_two_data(data1, data2,label1 = sim_one_name , label2 = sim_two_name ,
                           xlabel = "Delay (min)", title = "Distribution of Trip Delay (P95)",
                           savename = "delay",processed_path = processed_path , alphas = 0.5, color1 = 'tab:blue', color2 = 'tab:orange' )

if __name__ == "__main__":
    #system_metrics_table()
    #system_metrics_functionalclass()
    leg_metrics()

