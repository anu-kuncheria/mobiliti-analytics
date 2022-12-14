import datapane as dp
dp.login(token = ' ')
from system import system_metrics
from data import *
from utility import *

systemdf = system_metrics()
meanlegsmetricsdf = pd.read_csv(os.path.join(figures_path, "legssystemdf_mean.csv"))
medianlegsmetricsdf = pd.read_csv(os.path.join(figures_path, "legssystemdf_median.csv"))
activitydf = pd.read_csv(os.path.join(figures_path, "activitydf.csv"))

report_upload_name = config["report"]["report_upload_name"]

data_figures = {
b1:["flow8am.png","speed8am.png"],
b2:["flow4pm.png", "speed4pm.png"],
t1:["812618472flows.png","812618472speed.png"],
t2:["812618491flows.png","812618491speed.png"],
t3 :["28435963flows.png","28435963speed.png"],
t4 :["28435955flows.png","28435955speed.png"],
t5 :["993980437flows.png","993980437speed.png"],
t6 :["993981645flows.png","993981645speed.png"],
t7 :["820792476flows.png","820792476speed.png"],
t8:["821487631flows.png","821487631speed.png"],
c1:["23619797flows.png","23619797speed.png"],
c2:["7000452377flows.png","7000452377speed.png"],
c3:["7000266147flows.png","7000266147speed.png"],
c4:["946058264flows.png","946058264speed.png"],
s1:["7000005362flows.png","7000005362speed.png"],
s2:["23600777flows.png","23600777speed.png"],
s3:["7000435385flows.png","7000435385speed.png"],
s4:["1159330156flows.png","1159330156speed.png"],
sf1:["23600776flows.png","23600776speed.png"],
sf2:["1159358435flows.png","1159358435speed.png"],
sf3:["7000000918flows.png","7000000918speed.png"],
sf4:["7000005361flows.png","7000005361speed.png"],
d1:["VMT_dodgeplot.png","VHD_dodgeplot.png"],
d2:["Fuel_dodgeplot.png"],
l2:["congested_tt_hist.png","delay_hist.png"]
}

for variable, figures in data_figures.items():
    try:
        variable = [dp.Media(file = os.path.join(figures_path, figures[0])),dp.Media(file = os.path.join(figures_path, figures[1]))]
    except:
        variable = [dp.Media(file = os.path.join(figures_path, figures[0])), ]

l1 = [dp.Table(meanlegsmetricsdf), dp.Table(medianlegsmetricsdf)]

if __name__ == "__main__":
    p1 = dp.Report(
    dp.Text('**1. System Metrics**'),
    dp.Table(systemdf),
    dp.Text('**2. System Metrics by Functional Class**'),
    dp.Group(columns = 2, blocks = d1),
    dp.Group(columns = 2, blocks = d2),
    dp.Text('**3. Trip Legs Metrics**'),
    dp.Group(columns = 2, blocks = l1),
    dp.Group(columns = 2, blocks = l2),
    dp.Text('**4. Links with Activity and Congestion**'),
    dp.Text('Active links have a flow greater than 0. Congested links have v/c higher than 1.'),
    dp.Table(activitydf),
    dp.Text("**5. Flow and Speed Comparison of Links at 8am**"),
    dp.Group(columns = 2, blocks = b1),
    dp.Text("**6. Flow and Speed Comparison of Links at 4pm**"),
    dp.Group(columns = 2, blocks = b2),

    dp.Text('**7. Time series plots for Bridges and City links**'),
    dp.Text('**7.1 Bridge links in each direction**'),
    dp.Group(columns = 2, blocks = t1),
    dp.Group(columns = 2, blocks = t2),
    dp.Group(columns = 2, blocks = t3),
    dp.Group(columns = 2, blocks = t4),
    dp.Group(columns = 2, blocks = t5),
    dp.Group(columns = 2, blocks = t6),
    dp.Group(columns = 2, blocks = t7),
    dp.Group(columns = 2, blocks = t8),
    dp.Text('**7.2 City links**'),
    dp.Group(columns = 2, blocks = c1),
    dp.Group(columns = 2, blocks = c2),
    dp.Group(columns = 2, blocks = c3),
    dp.Group(columns = 2, blocks = c4),
    dp.Text('SF Intersections - Clement and 18th'),
    dp.Group(columns = 2, blocks = s1),
    dp.Group(columns = 2, blocks = s2),
    dp.Group(columns = 2, blocks = s3),
    dp.Group(columns = 2, blocks = s4),
    dp.Text('SF Intersections - Clement and 17th'),
    dp.Group(columns = 2, blocks = sf1),
    dp.Group(columns = 2, blocks = sf2),
    dp.Group(columns = 2, blocks = sf3),
    dp.Group(columns = 2, blocks = sf4),
    )
    p1.upload(name= report_upload_name )


