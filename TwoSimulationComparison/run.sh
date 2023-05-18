
set -e  # exit immediately if a command exits with a non-zero status

python3 scripts/system.py
python3 scripts/legs_metrics.py
python3 scripts/link_activity.py
python3 scripts/timeseries.py
python3 scripts/report.py



