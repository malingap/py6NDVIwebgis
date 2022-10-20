import imp
import streamlit as st
import ee
from google.oauth2 import service_account
from ee import oauth

import leafmap.foliumap as leafmap
import geemap.foliumap as geemap
# Visualize the Digital Elevation Model (DEM) using Google Earth Engine Python API
# Author :

def get_auth():
    service_account_keys = st.secrets["ee_keys"]
    credentials = service_account.Credentials.from_service_account_info(service_account_keys, scopes=oauth.SCOPES)
    ee.Initialize(credentials)
    
    return "successfully sync to GEE"
# Import Google Earth Engine
#import ee

# Import Geemap
#import geemap

# Starting the Google authenticaiton
#ee.Authenticate()

# Initializing the google earth engine library
#ee.Initialize()
# try:
#         ee.Initialize()
# except Exception as e:
#         ee.Authenticate()
#         ee.Initialize()

def app():

    st.title("DEM")
    
    # Create the map object
    Map = geemap.Map()

    # Loading the country data
    all_countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017");

    # Filtering the Area of Interest(AOI) as Sri Lanka
    AOI = all_countries.filter(ee.Filter.eq('country_na', "Sri Lanka"));

    #region = AOI.geometry()
    #scale = 50
    #folder = 'DEM_M'
    #export_dem = 'SL_GeoTiff'

    #config ={'scale':scale, 'maxPixels':1.0E13, 'driveFolder':folder, 'region':region}
    #task = ee.batch.Export.image(AOI, export_dem, config)
    #task.start()

    # Import Digital Elevation Model (DEM) and Clip with the AOI
    dem = ee.Image('USGS/SRTMGL1_003').clip(AOI)

    # Visualizing colors for DEM
    viz_parameters = {
        'min': 0,
        'max': 4000,
        'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5'],
    }

    # Adding DEM Layer to the map
    Map.addLayer(dem, viz_parameters, 'SRTM Digital Elevation Model (DEM)')

    # Fix the zooming viewport to the Sri Lanka
    Map.centerObject(AOI, 7)

    # Adding the colors to Legend Bar
    # Define color palette for color bar
    colors = viz_parameters['palette']

    # Define min value
    vmin = viz_parameters['min']

    # Define max value
    vmax = viz_parameters['max']

    # Add the Legend bar to the map
    Map.add_colorbar(viz_parameters, label="Digital Elevation (m)", layer_name = "SRTM DEM", orientation = 'vertical', transparent_bg=True,)
    

    Map.to_streamlit(height=700)
