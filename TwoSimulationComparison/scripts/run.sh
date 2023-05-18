
set -e  # exit immediately if a command exits with a non-zero status
pwd

python3 system.py
python3 analytics_differences.py
python3 timeseries.py
python3 report.py



