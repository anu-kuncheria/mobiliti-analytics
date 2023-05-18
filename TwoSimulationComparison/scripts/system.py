from load_data import *
import utility as util

data_simulations = [
                    [sim_one_name,simulation_one_flow,simulation_one_speed,simulation_one_fuel],
                    [sim_two_name, simulation_two_flow,simulation_two_speed, simulation_two_fuel]
                     ]

def system_metrics_table():
    names, vmts, vhds, fuel = ([] for i in range(4))
    
    for d in data_simulations:
        names.append(d[0])
        vmts.append(int(util.vmt(d[1])/1000))
        vhds.append(util.vhd(d[1], d[2]))
        fuel.append(int(util.fuel_gallons(d[3])/1000))

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
        vmts = util.vmtfc(d[1])
        vhds = util.vhdfc(d[1],d[2])
        fuels = util.fuel_gallons_fc(d[3])

        vmt_params.append([int(val/1000000) for val in vmts])
        vhd_params.append([int(val/1000) for val in vhds])
        fuel_params.append([int(val/1000) for val in fuels])
    
    #writing bar plots
    util.dodged_barplot(vmt_params[0], vmt_params[1], 'VMT', sim_one_name, sim_two_name, 'Functional class', 'VMT (in million miles)', processed_path)
    util.dodged_barplot(vhd_params[0], vhd_params[1],'VHD', sim_one_name, sim_two_name, 'Functional class', 'VHD (in thousand hours)', processed_path)
    util.dodged_barplot(fuel_params[0], fuel_params[1], 'Fuel', sim_one_name, sim_two_name, 'Functional class', 'Fuel Consumption (in thousand gallons)', processed_path)
   
if __name__ == "__main__":
    #system_metrics_table()
    system_metrics_functionalclass()

