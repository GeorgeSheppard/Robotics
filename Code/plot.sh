### Have to change directory after running interface to get plot of what just happened, this script
### runs interface and then brings up the plot in one.

# This stops silent exceptions, will stop if anything throws
set -e

# This is what will be run
echo python2.7 interface.py $1
python2.7 interface.py $1

# Switch to analysis directory
echo cd Analysis
cd Analysis

# Run position angle file with same setup, Testing will plot latest testing file, real latest real data
echo python2.7 position_angle $1
python2.7 position_angle.py $1
