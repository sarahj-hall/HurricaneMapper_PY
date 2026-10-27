'''
Hurricane Mapping Tool
This selects a specific US hurricane from points data, creates a hurricane track, and selects the affected counties. 
The code also creates an interactive html map and graph of the hurricane track and impacted counties. 

Change the selected hurricane using the storm_season and storm_name variables 

Created by Sarah Hall, 10/6/2026
ENV 859, Duke University 
'''

# %% Project Set-Up
#import packages
import arcpy
from pathlib import Path

#creates path object for raw data folder 
raw_folder_path = Path.cwd().parent/'data'/'raw'
#creates path object for processed data folder
processed_folder_path = Path.cwd().parent/'data'/'processed'

#check that paths exist
print(raw_folder_path)
print(raw_folder_path.exists())
print(processed_folder_path)
print(processed_folder_path.exists())

#Allow arcpy to overwrite output
arcpy.env.overwriteOutput = True
#set default & scratch workspace
arcpy.env.workspace = str(raw_folder_path)

# Set Tool vars/parameters
#temp output for select tool
selected_points = "memory\\selected_points"
#temp output for points to line tool
storm_track = "memory\\Tracklines"
# US counties layer URL
usa_counties = 'https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Counties_Generalized_Boundaries/FeatureServer/0'

# %% Generate list of storms in each season 

#empty dictionary
storm_dict = {}

#create dictionary where key = year, value = storm names
for storm_season in range (2000,2004):
    storm_names = []

    #search cursor 
    cursor = arcpy.da.SearchCursor(
        'IBTrACS_NA.shp', 
        ['NAME'],
        where_clause= f'SEASON = {storm_season}')

    #for loop to record storm names
    for record in cursor:
        Name = record[0]
        if not Name in storm_names and Name != 'UNNAMED':
                storm_names.append(Name)

    del(cursor)

    storm_dict[storm_season] = storm_names

# %% Iterate and tally storm county counts

for storm_season in storm_dict.keys():
     storm_count_total = 0 
     
     for storm_name in storm_dict[storm_season]:
        #select tool 
        arcpy.analysis.Select(
            in_features = "IBTrACS_NA.shp",
            out_feature_class = selected_points,
            where_clause = f"SEASON = {storm_season} And NAME = '{storm_name}'"
        )
        #convert selected storm points to storm track
        arcpy.management.PointsToLine(
            Input_Features = selected_points,
            Output_Feature_Class = storm_track,
            Sort_Field= "ISO_TIME"
        )
        #Select counties that intersect hurricane track 
        select_output = arcpy.management.SelectLayerByLocation(
            in_layer = usa_counties,
            overlap_type= "INTERSECT",
            select_features= storm_track
            )

        #get count of intersecting counties & convert to int
        counties_count = int(arcpy.management.GetCount(select_output).getOutput(0))
        #increment the season counter
        storm_count_total += counties_count

    #print output to file


# %% Create a plot of people affected by state
''''
the_plot = (
    counties_lyr.
    groupby('STATE_NAME')
    .agg({'POPULATION':'sum'})
    .sort_values(by='POPULATION',ascending=False)
    .plot(
        kind='barh',
        title=f'{storm_name}-{storm_season}',
        legend=False,
        xlabel='People affected',
        ylabel=''
        )
)
'''