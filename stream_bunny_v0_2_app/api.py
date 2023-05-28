import requests

def get_stream(imdb_id):

    url = "https://streaming-availability.p.rapidapi.com/get/basic"

    querystring = {"country":"us","imdb_id":f'tt{imdb_id}',"output_language":"en"}

    headers = {
        'x-rapidapi-host': "streaming-availability.p.rapidapi.com",
        # 'x-rapidapi-key': "2b0bb807b2msh8f81f82877e9118p17629cjsn1b5858449268" #matthew api key
        # 'x-rapidapi-key': "9e6924077bmsh537baf971b723ddp1165e9jsn8c35b01cf3eb" #joseph api key
        'x-rapidapi-key': "2b0bb807b2msh8f81f82877e9118p17629cjsn1b5858449268", #michael
        # 'x-rapidapi-key': "c86b5de4cbmsh1b9d84199107c8dp14c37bjsnaad1fa143ed3" #joseph's wife, emily
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    noRec = []
    if "no records are found" in response.text: #if response.text == "message" then skip everything else & return an empty array
        return noRec
    ret1 = response.json()["streamingInfo"] #this is the place to check response
    stream_arr = []
    # stream_arr = {}
    for stream, value in ret1.items():
        stream_arr.append(
            {
                'stream':stream,
                'stream_link':value['us']['link']
                })
        # stream_arr = {'stream':stream, 'stream_link':value['us']['link']}
    print(stream_arr)
    return stream_arr

#/get/basic