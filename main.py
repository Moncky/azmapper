# This is a sample Python script.
import boto3
import plotly.graph_objects as go

#Setup Sessions on the accoutns we want to compare
def left_session(profile, region):
    session = boto3.session.Session(profile_name=profile, region_name=region)
    client = session.client('ec2')
    return client

def right_session(profile, region):
    session = boto3.session.Session(profile_name=profile, region_name=region)
    client = session.client('ec2')
    return client

#Get a list of Availabiltiy Zones from the left session.  The number of AZ's in any one region is the same on
#All accounts so we only need to do this once
def zone_ids(session):
    #ec2 = setup_left_session(profile, region)  # Press ⌘F8 to toggle the breakpoint.
    response = session.describe_availability_zones()
    zone_ids = {}
    for az in response['AvailabilityZones']:
        name = az['ZoneName']
        zid = az['ZoneId']
        zone_ids[name] = zid
        #zone_ids[az] = az['ZoneId']
    return zone_ids

def match_zid(left, right):
    matches = set(left) & set(right)

if __name__ == '__main__':

    left = zone_ids(left_session('default', 'us-east-1'))
    right = zone_ids(right_session('otherprofile', 'us-east-1'))

    left_zid = []
    zones = []
    for k, v in left.items():
        zones.append(k)
        left_zid.append(v)

    right_zid = []
    for _, v in right.items():
        right_zid.append(v)


    match_zid(left_zid, right_zid)
    fig = go.Figure(data=[go.Table(
        header=dict(values=["", "left", "right"]),
        cells=dict(values=[zones,
                           left_zid,
                           right_zid
                           ]
                   ))
    ])

    # Look here for possible highlighting options
    #https://chart-studio.plotly.com/~empet/14689/table-with-cells-colored-according-to-th/#/

    fig.show()
