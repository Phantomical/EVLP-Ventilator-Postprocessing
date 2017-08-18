@echo off

python convert_to_csv/convert_to_csv.py convert_to_csv/trend.si convert_to_csv/output.csv
python remove_header/remove_header.py convert_to_csv/output.csv remove_header/output.csv
python remove_empty/remove_empty.py remove_header/output.csv remove_empty/output.csv
python reformat_hours/reformat_hours.py remove_empty/output.csv reformat_hours/output.csv
python calc_plateau_pressure/calc_plateau_pressure.py reformat_hours/output.csv calc_plateau_pressure/output.csv
