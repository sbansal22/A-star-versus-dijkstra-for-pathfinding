import pandas as pd
# from geopy.geocoders import Nominatim


# def xlsx_to_pd():
#     data = pd.read_excel(r'St-Data-Original.xlsx')

#     df = pd.DataFrame(data)
#     st_name = df['St_name']
#     from_st = df['from']
#     to_st = df['to']
#     miles = df['miles']
#     # make lat and log as columns with default numbers here
#     df['st1_lat'] = 0.0 ; st1_lat = df['st1_lat']
#     df['st1_long'] = 0.0 ; st1_long = df['st1_long']
#     df['st2_lat'] = 0.0 ; st2_lat = df['st2_lat']
#     df['st2_long'] = 0.0 ; st2_long = df['st2_long']

#     return df


def check_dead_ends(df):
    df.drop(df.loc[df['to']=='Dead End'].index, inplace=True)


def querry_geopy(st1, st2, idx, df):
    # set up the geolocator and find lat/long
    geolocator = Nominatim(user_agent="google maps")
    st1_com = st1 + ', Bostn, Massachusetts'
    st2_com = st2 + ', Boston, Massachusetts'
    st1_loc = geolocator.geocode(st1_com)
    st2_loc = geolocator.geocode(st2_com)

    # check if querrying the lat/long of st1 or st2 fails
    if st1_loc is None or st2_loc is None:
        # # get rid of that row
        # df.drop(df.index[idx], inplace=True)
        # put a placeholder value that indicates Error
        df['st1_lat'][idx] = 'Querry Failed'
        df['st1_long'][idx] = 'Querry Failed'
        df['st2_lat'][idx] = 'Querry Failed'
        df['st2_long'][idx] = 'Querry Failed'
    
    else:
        # write the lat/long in the dataframe
        df['st1_lat'][idx] = st1_loc.latitude
        df['st1_long'][idx] = st1_loc.longitude
        df['st2_lat'][idx] = st2_loc.latitude
        df['st2_long'][idx] = st2_loc.longitude
    

def process_df():
    ### initialization ###
    data = pd.read_excel(r'St-Data-Original.xlsx')

    df = pd.DataFrame(data)
    st_name = df['St_name']
    from_st = df['from']
    to_st = df['to']
    miles = df['miles']
    # make lat and log as columns with default numbers here
    df['st1_lat'] = 0.0 ; st1_lat = df['st1_lat']
    df['st1_long'] = 0.0 ; st1_long = df['st1_long']
    df['st2_lat'] = 0.0 ; st2_lat = df['st2_lat']
    df['st2_long'] = 0.0 ; st2_long = df['st2_long']

    # find all dead_ends and delete rows that contain dead ends
    check_dead_ends(df)

    # find all streets that geopy cannot find the lat/long
    for idx in range(len(df.idx)):
        querry_geopy(from_st[idx], to_st[idx], idx, df)

    # delete all rows that geopy failed to pinpoint the lat/long
    df.drop(df.loc[df['st1_lat']=='Querry Failed'].index, inplace=True)
    df.drop(df.loc[df['st1_long']=='Querry Failed'].index, inplace=True)
    df.drop(df.loc[df['st2_lat']=='Querry Failed'].index, inplace=True)
    df.drop(df.loc[df['st2_long']=='Querry Failed'].index, inplace=True)


if __name__ == "__main__":
    # df_raw = xlsx_to_pd()
    # df_processed = querry_geopy()




    ### Below was used for testing ###
    data = {'Name':['Jai', 'Princi', 'Gaurav', 'Anuj'], 
        'Age':[27, 24, 22, 32], 
        'Address':['0', '0', 'Allahabad', 'Kannauj'], 
        'Qualification':['Msc', 'MA', 'MCA', 'Phd']} 
  
    # Convert the dictionary into DataFrame  
    df = pd.DataFrame(data) 

    # select two columns 
    print(df)

    def change(daf):
        # daf.drop('Age', axis=1, inplace=True)
        # daf['Name'][0] = 'HK'
        daf[daf.Address != '0']
        daf.drop(daf.loc[df['Address']=='0'].index, inplace=True)
        # return df

    change(df)
    print("--")
    print(df) 

