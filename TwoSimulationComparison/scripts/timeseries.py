from data import *
from utility import *

def bridge_plots():
    bridge_links = {812618472: 'WB',812618491:'EB',28435963:'WB',28435955:'EB',993980437:'NB',993981645:'SB',820792476:'EB',821487631:'WB'}
    for b, a in bridge_links.items():
        plot_flow_speed(b,simulation_one_flow,sim_one_name, "red", simulation_two_flow, sim_two_name, "blue", flows = True,attr = a ,  processed_path = processed_path)
        plot_flow_speed(b,simulation_one_speed,sim_one_name, "red", simulation_two_speed,sim_two_name, "blue",flows = False, attr = a, processed_path = processed_path)
    
    fwy_links = { 127821081:'SB', 945913434:'NB'} # I280, junipero serra fwy
    for b, a in fwy_links.items():
        plot_flow_speed(b,simulation_one_flow,sim_one_name, "red", simulation_two_flow, sim_two_name, "blue", flows = True,attr = a ,  processed_path = processed_path)
        plot_flow_speed(b,simulation_one_speed,sim_one_name, "red", simulation_two_speed,sim_two_name, "blue",flows = False, attr = a, processed_path = processed_path)
    

def city_plots(): 
    city_links = {23619797: 'TL',7000452377: 'SS',7000266147:' ', 946058264: ' ' }
    for c,a in city_links.items():
        if signals_bool == False:
            regulator = ' '
        else:
            regulator = a 
        plot_flow_speed(c,simulation_one_flow,sim_one_name, "red", simulation_two_flow,sim_two_name, "blue", flows = True, attr = regulator, processed_path = processed_path)
        plot_flow_speed(c,simulation_one_speed,sim_one_name, "red", simulation_two_speed,sim_two_name, "blue",flows = False, attr = regulator, processed_path = processed_path)

    clement_18th_sf = {7000005362:'', 23600777:'', 7000435385:'SS', 1159330156:'SS'}
    for c,a in clement_18th_sf.items():
        if signals_bool == False:
            regulator = ' '
        else:
            regulator = a 
        plot_flow_speed(c,simulation_one_flow,sim_one_name, "red", simulation_two_flow,sim_two_name, "blue", flows = True, attr = a, processed_path = processed_path)
        plot_flow_speed(c,simulation_one_speed,sim_one_name, "red", simulation_two_speed,sim_two_name, "blue",flows = False, attr = a, processed_path = processed_path)

    clement_19th_sf = {23600776:'SS', 1159358435:'SS', 7000000918:'SS', 7000005361:'SS'}
    for c,a in clement_19th_sf.items():
    
        if signals_bool == False:
            regulator = ' '
        else:
            regulator = a 
        plot_flow_speed(c,simulation_one_flow,sim_one_name, "red", simulation_two_flow,sim_two_name, "blue", flows = True, attr = a, processed_path = processed_path)
        plot_flow_speed(c,simulation_one_speed,sim_one_name, "red", simulation_two_speed,sim_two_name, "blue",flows = False, attr = a, processed_path = processed_path)

if __name__ == "__main__":
    bridge_plots()
    city_plots()
