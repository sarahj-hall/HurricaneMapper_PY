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
raw_folder_path = Path.cwd().parent/'Data'/'Raw'

#creates path object for storm point data (since i have a nested folder)
storm_points_folder = raw_folder_path/'IBTrACS_NA'

#creates path object for processed data folder
processed_folder_path = Path.cwd().parent/'Data'/'Processed'

#check that paths exist
print(raw_folder_path)
print(raw_folder_path.exists())
print(processed_folder_path)
print(processed_folder_path.exists())

#Allow arcpy to overwrite output
arcpy.env.overwriteOutput = True
#set default & scratch workspace
arcpy.env.workspace = str(storm_points_folder)

# %% PseudoCode

#iterate over the years 2000-20024

#for a given year
    #generate a collection of named storms for that year from the points feature class
        #for each storm in this list
        #select the points for this storm -> convert to track
        #select county features intersecting the storm track 
        #count number of county features 
        #add year table to list of tables 
    #merge yearly tables into single table 
    #plot

# %% Generate list of storms in each season 
hurricane_names = []

storm_points_folder



# %%  Set Tool vars/parameters

#storm year
storm_season = "2024"
#storm name
storm_name = "HELENE"
#temp output for select tool
selected_points = "memory\\selected_points"
#temp output for points to line tool
storm_track = "memory\\Tracklines"
# US counties layer URL
usa_counties = 'https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Counties_Generalized_Boundaries/FeatureServer/0'

# %% Select points
#select tool 
arcpy.analysis.Select(
    in_features = "IBTrACS_NA.shp",
    out_feature_class = selected_points,
    where_clause = f"SEASON = {storm_season} And NAME = '{storm_name}'"
)

#check the selected points 
arcpy.management.GetCount(selected_points)

# %% convert selected storm points to storm track
arcpy.management.PointsToLine(
    Input_Features = selected_points,
    Output_Feature_Class = storm_track,
    Sort_Field= "ISO_TIME"
)

# %% Select counties that intersect hurricane track & export 

#Select counties that intersect hurricane track 
select_results = arcpy.management.SelectLayerByLocation(
    in_layer = usa_counties,
    select_features= storm_track
    )

#get count of intersecting counties & convert to int
counties_count = int(arcpy.management.GetCount(select_results).getOutput(0))


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