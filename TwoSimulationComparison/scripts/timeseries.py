from load_data import *
import utility as util

# specify the links needed to plot the time series


def bridge_link_plots():
    bridge_links = {
        812618472: 'WB',
        812618491: 'EB',
        28435963: 'WB',
        28435955: 'EB',
        993980437: 'NB',
        993981645: 'SB',
        820792476: 'EB',
        821487631: 'WB'
    }

    fwy_links = {
        127821081: 'SB',
        945913434: 'NB'
    }  # I280, junipero serra fwy

    for linkid, direction in bridge_links.items():
        util.plot_flow_speed(linkid, simulation_one_flow, sim_one_name, "red", simulation_two_flow,
                             sim_two_name, "blue", flows=True, attr=direction, processed_path=processed_path)
        util.plot_flow_speed(linkid, simulation_one_speed, sim_one_name, "red", simulation_two_speed,
                             sim_two_name, "blue", flows=False, attr=direction, processed_path=processed_path)

    for linkid, direction in fwy_links.items():
        util.plot_flow_speed(linkid, simulation_one_flow, sim_one_name, "red", simulation_two_flow,
                             sim_two_name, "blue", flows=True, attr=direction, processed_path=processed_path)
        util.plot_flow_speed(linkid, simulation_one_speed, sim_one_name, "red", simulation_two_speed,
                             sim_two_name, "blue", flows=False, attr=direction, processed_path=processed_path)


def city_link_plots():
    # sample links with traffic signal and stop signs
    city_links = {
        23619797: 'TL',
        7000452377: 'SS',
        7000266147: ' ',
        946058264: ' '
    }

    clement_18th_sf = {
        7000005362: '',
        23600777: '',
        7000435385: 'SS',
        1159330156: 'SS'
    }

    clement_19th_sf = {
        23600776: 'SS',
        1159358435: 'SS',
        7000000918: 'SS',
        7000005361: 'SS'
    }

    for linkid, reg in city_links.items():
        if signals_bool == False:
            regulator = ' '
        else:
            regulator = reg
        util.plot_flow_speed(linkid, simulation_one_flow, sim_one_name, "red", simulation_two_flow,
                             sim_two_name, "blue", flows=True, attr=regulator, processed_path=processed_path)
        util.plot_flow_speed(linkid, simulation_one_speed, sim_one_name, "red", simulation_two_speed,
                             sim_two_name, "blue", flows=False, attr=regulator, processed_path=processed_path)

    for linkid, reg in clement_18th_sf.items():
        if signals_bool == False:
            regulator = ' '
        else:
            regulator = reg
        util.plot_flow_speed(linkid, simulation_one_flow, sim_one_name, "red", simulation_two_flow,
                             sim_two_name, "blue", flows=True, attr=regulator, processed_path=processed_path)
        util.plot_flow_speed(linkid, simulation_one_speed, sim_one_name, "red", simulation_two_speed,
                             sim_two_name, "blue", flows=False, attr=regulator, processed_path=processed_path)

    for linkid, reg in clement_19th_sf.items():
        if signals_bool == False:
            regulator = ' '
        else:
            regulator = reg
        util.plot_flow_speed(linkid, simulation_one_flow, sim_one_name, "red", simulation_two_flow,
                             sim_two_name, "blue", flows=True, attr=regulator, processed_path=processed_path)
        util.plot_flow_speed(linkid, simulation_one_speed, sim_one_name, "red", simulation_two_speed,
                             sim_two_name, "blue", flows=False, attr=regulator, processed_path=processed_path)


if __name__ == "__main__":
    bridge_link_plots()
    city_link_plots()
