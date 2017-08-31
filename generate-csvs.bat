@echo off

bin\convert_to_utf8 TREND.SI output.si
bin\preprocess output.si standard.csv --standard-preprocess

bin\time-sample standard.csv hourly.csv --sample-freq=1:00 --filter-irrelevant
bin\time-sample standard.csv 10-from-recruitment.csv --sample-start=recruitment --sample-offset=0:02 --sample-freq=0:10 --filter-irrelevant --reformat-time

bin\sample standard.csv pre-recruitment.csv --sample-param=recruitment --sample-period=pre --sample-offset=1 --filter-irrelevant
bin\sample standard.csv post-recruitment.csv --sample-param=recruitment --sample-period=post --sample-offset=2 --filter-irrelevant
bin\sample standard.csv over-recruitment.csv --sample-param=recruitment --sample-period=during --filter-irrelevant

bin\sample standard.csv pre-assessment.csv --sample-param=assessment --sample-period=pre --sample-offset=2 --filter-irrelevant
bin\sample standard.csv post-assessment.csv --sample-param=assessment --sample-period=post --sample-offset=2 --filter-irrelevant
bin\sample standard.csv over-assessment.csv --sample-param=assessment --sample-period=during --filter-irrelevant

del output.si