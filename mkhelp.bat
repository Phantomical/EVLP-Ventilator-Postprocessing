@echo off

echo Help for preprocess.py > help.txt
python ventilator_data/preprocess.py --help >> help.txt
echo Help for sample.py >> help.txt
python ventilator_data/sample.py --help >> help.txt
echo Help for time-sample.py >> help.txt
python ventilator_data/time-sample.py >> help.txt
