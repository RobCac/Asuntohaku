import json
import pandas as pd
import string
import requests
import datetime as dt



def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def create_query_for_graphQL(api_adress, destination, time = '"07:00:00"'):
    #creates the GraphQLrequest for traveltime between to locations in ReittiopasAPI format
    check_date = dt.datetime.now()
    query = """
    {{
    plan(
        fromPlace: "{starter}",
        toPlace: "{to}",
        date: "{Year}-{Month}-{Day}",
        time: {depart},
        numItineraries: 3,
    ) {{
        itineraries{{
        duration
        }}
    }}
    }}
    """.format(starter = str(api_adress), to = str(destination), Year = check_date.year, Month = check_date.month, Day = check_date.day, depart = str(time))
    return query



def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))




def route_length(apart_adress, home = "Kurtinmäenkuja 2, Espoo::60.178746,24.595081", work = "Valimotie 21, Helsinki::60.220108,24.87883" ):

    url = "https://api.digitransit.fi/geocoding/v1/search?text="
    url = url + apart_adress + "&layers=address&size=1"
    response = requests.get(url)
    coordinates = response.json()["bbox"]
    api_adress= apart_adress+"::"+str(coordinates[1]) + "," + str(coordinates[0])
    
    
    home_query = create_query_for_graphQL(api_adress,home)
    home_traveljson = run_query(home_query)
    home_durations = home_traveljson["data"]["plan"]["itineraries"]
    home_average_travel = 0
    for dictionary in home_durations:
        home_average_travel = home_average_travel + dictionary["duration"]
    home_average_travel = int(home_average_travel/(3*60))

    
    work_query = create_query_for_graphQL(api_adress,work)
    work_traveljson = run_query(work_query)
    work_durations = work_traveljson["data"]["plan"]["itineraries"]
    work_average_travel = 0
    for dictionary in work_durations:
        work_average_travel = work_average_travel + dictionary["duration"]
    work_average_travel = int(work_average_travel/(3*60))
    return home_average_travel, work_average_travel


def add_journeys_to_df(df_combined):
    df_combined.reindex(columns = df_combined.columns.tolist() + ['Reitti töihin'] + ['Reitti Kökkeliin'])
    #add new columns to the dataframe
    for index, row in df_combined.iterrows():
        #Iterate through the columns, using route_length to calculate the traveltimes and adding them to
        #the dataframe
        adress_string = row["Osoite"] + ", " + row["Kaupunki"]
        print("Adding routes from apartment number {s}...".format(s = index +1))
        a, b = route_length(adress_string)
        print("reitti kökkeliin %s", a)
        df_combined.loc[index, "Reitti Kökkeliin"], df_combined.loc[index, "Reitti töihin"] = a, b
        
        print("...done!")
    return(df_combined)


#route_length("valimotie 21, Helsinki")
