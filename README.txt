This is a collection of scripts to postprocess
data retrieved from a Maquet Servo-i ventilator
using the Ventilator Record Card (VRC).

Instructions for Use:
1. Copy the TREND.SI file that you wish to process into the folder
   with the generate-csvs.bat file. (This should be the main folder)
    NOTE: On the VRC these can be found in VENT/YYYYMMDD.NNN/NO_NAME
	      folder. If you have given the patient a name in the ventilator
	      then the folder will be named something else.
2. Run generate-csvs.bat
3. A series of .csv files should show up in the folder.

Troubleshooting:
If there are errors:
- Ensure that any other csv files in the folder are not opened in excel.
- If that doesn't work, remove all csv files in the main folder
- Otherwise get a new copy of the scripts

Produced Files:
10-from-recruitment.csv
	Samples data points in between recruitments. There is one sample
	taken every 10 minutes.
hourly.csv
	Contains samples taken each hour of EVLP. This usually won't 
	line up with assessments or recruitments very well.
over-assessment.csv
	Contains all data points that have been determined to be within
	assessments (%O2 is greater than 80%)
over-recruitment.csv
	Contains all data points that are determined to be during
	recruitments. (Tidal Volume is greater than 300 mL)
	WARNING: This will stop working if used for subjects that
	         have a weight that is drastically different from
             approx. 30 kg.'
post-assessment.csv
	Contains data points sampled 2 minutes after assessment is
	determined to have ended.
post-recruitment.csv
	Contains data points sampled 2 minutes after recruitment is
	determined to have ended.
pre-assessment.csv
	Contains data points sampled 2 minutes before assessment is
	determined to have started.
post-recruitment.csv
	Contains data points sampled 2 minutes before recruitment is
	determined to have started.
standard.csv
	Contains all data points that had data from the original trend.si
	file.

Notes:
- The calculation of recruitment times assumes that the weight of the
  subject is around 30 kg. If using a subject with a different weight
  and therefore different tidal volume the recruitment calculations
  may not work.
- If it is desired to get additional views on the data the scripts
  can be invoked on their own and passed different parameters.
  For information on the parameters the various scripts support
  see help.txt or pass --help as a parameter to any of the scripts.
- If you wish to modify the program the sources will be required,
  a python3 version, and pyinstaller. (NOTE: As of the current date,
  2017-08-31, the version of pyinstaller that can be installed via
  pip, 3.2.1, is unable to package the scripts. The dev version does
  work however.)
