import datapane as dp
import key
dp.login(token = key.datapane_key)

from system import system_metrics_table
from load_data import *
from utility import *

#Load processed data
systemdf = system_metrics_table()
mean_legsmetricsdf = pd.read_csv(os.path.join(processed_path, "legssystemdf_mean.csv"))
median_legsmetricsdf = pd.read_csv(os.path.join(processed_path, "legssystemdf_median.csv"))
activitydf = pd.read_csv(os.path.join(processed_path, "activitydf.csv"))

data_figures = {
    "vmt_vhd" :["VMT_dodgeplot.png","VHD_dodgeplot.png"],
    "fuel" : ["Fuel_dodgeplot.png"],
    "trip_distribution" : ["congested_tt_hist.png","delay_hist.png"],
    "scatter_8am" : ["flow8am.png","speed8am.png"],
    "scatter_4pm" : ["flow4pm.png", "speed4pm.png"],

    "t1" : ["812618472flows.png","812618472speed.png"],
    "t2" : ["812618491flows.png","812618491speed.png"],
    "t3" : ["28435963flows.png","28435963speed.png"],
    "t4" : ["28435955flows.png","28435955speed.png"],
    "t5" : ["993980437flows.png","993980437speed.png"],
    "t6" : ["993981645flows.png","993981645speed.png"],
    "t7" : ["820792476flows.png","820792476speed.png"],
    "t8" : ["821487631flows.png","821487631speed.png"],
    "c1" : ["23619797flows.png","23619797speed.png"],
    "c2" : ["7000452377flows.png","7000452377speed.png"],
    "c3" : ["7000266147flows.png","7000266147speed.png"],
    "c4" : ["946058264flows.png","946058264speed.png"],
    "s1" : ["7000005362flows.png","7000005362speed.png"],
    "s2" : ["23600777flows.png","23600777speed.png"],
    "s3" : ["7000435385flows.png","7000435385speed.png"],
    "s4" : ["1159330156flows.png","1159330156speed.png"],
    "sf1" : ["23600776flows.png","23600776speed.png"],
    "sf2" : ["1159358435flows.png","1159358435speed.png"],
    "sf3" : ["7000000918flows.png","7000000918speed.png"],
    "sf4" : ["7000005361flows.png","7000005361speed.png"]
    }

#generating datapane blocks
for key, figure in data_figures.items():
    try:
        data_figures[key] = [dp.Media(file = os.path.join(processed_path, figure[0])),dp.Media(file = os.path.join(processed_path, figure[1]))]
    except:
        data_figures[key] = [dp.Media(file = os.path.join(processed_path, figure[0])), ]

legs_block = [dp.Table(mean_legsmetricsdf), dp.Table(median_legsmetricsdf)]

print(data_figures["vmt_vhd"])

if __name__ == "__main__":
    report_content = dp.View(
        dp.Text('**1. System Metrics**'),
        dp.Table(systemdf),
        dp.Text('**2. System Metrics by Functional Class**'),
        dp.Group(columns = 2, blocks = data_figures["vmt_vhd"]),
        dp.Group(columns = 2, blocks = data_figures["fuel"]),
        dp.Text('**3. Trip Legs Metrics**'),
        dp.Group(columns = 2, blocks = legs_block),
        dp.Group(columns = 2, blocks = data_figures["trip_distribution"]),
        dp.Text('**4. Links with Activity and Congestion**'),
        dp.Text('Active links have a flow greater than 0. Congested links have v/c higher than 0.75 .'),
        dp.Table(activitydf),
        dp.Text("**5. Flow and Speed Comparison of Links at 8am**"),
        dp.Group(columns = 2, blocks = data_figures["scatter_8am"]),
        dp.Text("**6. Flow and Speed Comparison of Links at 4pm**"),
        dp.Group(columns = 2, blocks = data_figures["scatter_4pm"]),

        dp.Text('**7. Time series plots for Bridges and City links**'),
        dp.Text('**7.1 Bridge links in each direction**'),
        dp.Group(columns = 2, blocks = data_figures["t1"]),
        dp.Group(columns = 2, blocks = data_figures["t2"]),
        dp.Group(columns = 2, blocks = data_figures["t3"]),
        dp.Group(columns = 2, blocks = data_figures["t4"]),
        dp.Group(columns = 2, blocks = data_figures["t5"]),
        dp.Group(columns = 2, blocks = data_figures["t6"]),
        dp.Group(columns = 2, blocks = data_figures["t7"]),
        dp.Group(columns = 2, blocks = data_figures["t8"]),
        dp.Text('**7.2 City links**'),
        dp.Group(columns = 2, blocks = data_figures["c1"]),
        dp.Group(columns = 2, blocks = data_figures["c2"]),
        dp.Group(columns = 2, blocks = data_figures["c3"]),
        dp.Group(columns = 2, blocks = data_figures["c4"]),
        dp.Text('SF Intersections - Clement and 18th'),
        dp.Group(columns = 2, blocks = data_figures["s1"]),
        dp.Group(columns = 2, blocks = data_figures["s2"]),
        dp.Group(columns = 2, blocks = data_figures["s3"]),
        dp.Group(columns = 2, blocks = data_figures["s4"]),
        dp.Text('SF Intersections - Clement and 17th'),
        dp.Group(columns = 2, blocks = data_figures["sf1"]),
        dp.Group(columns = 2, blocks = data_figures["sf2"]),
        dp.Group(columns = 2, blocks = data_figures["sf3"]),
        dp.Group(columns = 2, blocks = data_figures["sf4"])
        )
    
    dp.upload_report(report_content, name = report_upload_name)  
