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

b1 = [dp.Media(file = os.path.join(figures_path,"flow8am.png")),dp.Media(file = os.path.join(figures_path,"speed8am.png"))]
b2 = [dp.Media(file = os.path.join(figures_path,"flow4pm.png")),dp.Media(file = os.path.join(figures_path,"speed4pm.png"))]

t1 = [dp.Media(file = os.path.join(figures_path,"812618472flows.png")),dp.Media(file = os.path.join(figures_path,"812618472speed.png"))]
t2 = [dp.Media(file = os.path.join(figures_path,"812618491flows.png")),dp.Media(file = os.path.join(figures_path,"812618491speed.png"))]
t3 = [dp.Media(file = os.path.join(figures_path,"28435963flows.png")),dp.Media(file = os.path.join(figures_path,"28435963speed.png"))]
t4 = [dp.Media(file = os.path.join(figures_path,"28435955flows.png")),dp.Media(file = os.path.join(figures_path,"28435955speed.png"))]
t5 = [dp.Media(file = os.path.join(figures_path,"993980437flows.png")),dp.Media(file = os.path.join(figures_path,"993980437speed.png"))]
t6 = [dp.Media(file = os.path.join(figures_path,"993981645flows.png")),dp.Media(file = os.path.join(figures_path,"993981645speed.png"))]
t7 = [dp.Media(file = os.path.join(figures_path,"820792476flows.png")),dp.Media(file = os.path.join(figures_path,"820792476speed.png"))]
t8 = [dp.Media(file = os.path.join(figures_path,"821487631flows.png")),dp.Media(file = os.path.join(figures_path,"821487631speed.png"))]

c1 = [dp.Media(file = os.path.join(figures_path,"23619797flows.png")),dp.Media(file = os.path.join(figures_path,"23619797speed.png"))]
c2 = [dp.Media(file = os.path.join(figures_path,"7000452377flows.png")),dp.Media(file = os.path.join(figures_path,"7000452377speed.png"))]
c3 = [dp.Media(file = os.path.join(figures_path,"7000266147flows.png")),dp.Media(file = os.path.join(figures_path,"7000266147speed.png"))]
c4 = [dp.Media(file = os.path.join(figures_path,"946058264flows.png")),dp.Media(file = os.path.join(figures_path,"946058264speed.png"))]

s1 = [dp.Media(file = os.path.join(figures_path,"7000005362flows.png")),dp.Media(file = os.path.join(figures_path,"7000005362speed.png"))]
s2 = [dp.Media(file = os.path.join(figures_path,"23600777flows.png")),dp.Media(file = os.path.join(figures_path,"23600777speed.png"))]
s3 = [dp.Media(file = os.path.join(figures_path,"7000435385flows.png")),dp.Media(file = os.path.join(figures_path,"7000435385speed.png"))]
s4 = [dp.Media(file = os.path.join(figures_path,"1159330156flows.png")),dp.Media(file = os.path.join(figures_path,"1159330156speed.png"))]

sf1 = [dp.Media(file = os.path.join(figures_path,"23600776flows.png")),dp.Media(file = os.path.join(figures_path,"23600776speed.png"))]
sf2 = [dp.Media(file = os.path.join(figures_path,"1159358435flows.png")),dp.Media(file = os.path.join(figures_path,"1159358435speed.png"))]
sf3 = [dp.Media(file = os.path.join(figures_path,"7000000918flows.png")),dp.Media(file = os.path.join(figures_path,"7000000918speed.png"))]
sf4 = [dp.Media(file = os.path.join(figures_path,"7000005361flows.png")),dp.Media(file = os.path.join(figures_path,"7000005361speed.png"))]


d1 = [dp.Media(file = os.path.join(figures_path,"VMT_dodgeplot.png")),dp.Media(file = os.path.join(figures_path,"VHD_dodgeplot.png"))]
d2 = [dp.Media(file = os.path.join(figures_path,"Fuel_dodgeplot.png")),]
l1 = [dp.Table(meanlegsmetricsdf), dp.Table(medianlegsmetricsdf)]
l2 = [dp.Media(file = os.path.join(figures_path,"congested_tt_hist.png")),dp.Media(file = os.path.join(figures_path,"delay_hist.png"))]

def report():
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

if __name__ == "__main__":
  report()
