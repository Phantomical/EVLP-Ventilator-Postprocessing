@echo off

python ../convert_to_utf8/convert_to_utf8.py trend.si output.si
python preprocess.py output.si standard.csv --standard-preprocess

python time-sample.py standard.csv hourly.csv --sample-freq=1:00 --filter-irrelevant
python time-sample.py standard.csv 10-from-recruitment.csv --sample-start=recruitment --sample-offset=0:02 --sample-freq=0:10 --filter-irrelevant

python sample.py standard.csv pre-recruitment.csv --sample-param=recruitment --sample-period=pre --sample-offset=1 --filter-irrelevant
python sample.py standard.csv post-recruitment.csv --sample-param=recruitment --sample-period=post --sample-offset=2 --filter-irrelevant
python sample.py standard.csv over-recruitment.csv --sample-param=recruitment --sample-period=during --filter-irrelevant

python sample.py standard.csv pre-assessment.csv --sample-param=assessment --sample-period=pre --sample-offset=2 --filter-irrelevant
python sample.py standard.csv post-assessment.csv --sample-param=assessment --sample-period=post --sample-offset=2 --filter-irrelevant
python sample.py standard.csv over-assessment.csv --sample-param=assessment --sample-period=during --filter-irrelevant

del output.si