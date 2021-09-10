# TranStack
A tool for stacking optical transmission curves of multiple surfaces
Using maplotlib and widgets a main plotting window is created with transmission curves for combinations (stacks) of 
surfaces  transmission/reflection curves stored in csv files and dynamically allocated by widget based controll pannels

chck TS_settings for user editable variables (wavelength range etx...)


TODO:
1. excel to csv
2. URL wget (thorlabs first as raw data is easily accessable)
3. dynamic widget spacing on controll pannel tiles (*bug 1)
4. save safety (*bug 2)

Known Bugs:
1. if more than 12 filter files are loaded the controll pannel entries are drawn outside the canvas
2. it is possable to overwrite files when saving a curve with no warning

