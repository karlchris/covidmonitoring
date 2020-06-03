#import needed libraries
from twilio.rest import Client
import pandas as pd
import requests
from datetime import datetime

#copied from twilio API 
account_sid = <YOUR_ACCOUNT_SID> #please change it to your own
auth_token = <YOUR_AUTH_TOKEN> #please change it to your own
client = Client(account_sid, auth_token) 
 
def send_message(receiver, message):
    message = client.messages.create( 
                                from_='whatsapp:+14155238886',  
                                body=message,      
                                to=f'whatsapp:{receiver}' 
                            )
    return message

#receiver number
receiver_list = ['+6281XXXXXXX','+6281XXXXXXX']

#get content covid report in Indonesia
url = "https://services5.arcgis.com/VS6HdKS0VfIhv8Ct/arcgis/rest/services/COVID19_Indonesia_per_Provinsi/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"
data_json = requests.get(url).json()

df = []
for row in range(len(data_json["features"])):
    df.append(data_json["features"][row]["attributes"])
df = pd.DataFrame(df)
df = df.drop(['FID','Kode_Provi'], axis=1)
data = df.sort_values(['Kasus_Meni'], ascending=False)[:5]

#present the data by translating the dataframe to string
province = data["Provinsi"].tolist()
current_timestamp = str(datetime.now())
messages = f"THIS is UPDATED REPORT up to {current_timestamp}"
for prov in province:
    each_row = data[data["Provinsi"] == prov]

    message_partition = f"""

    [{prov}]
    Kasus Positif = {str(each_row['Kasus_Posi'].tolist()[0])}
    Meningkat sebanyak {str(each_row['Kasus_Meni'].tolist()[0])}
    Total pasien sembuh sebanyak {str(each_row['Kasus_Semb'].tolist()[0])}
    """

    messages = messages + message_partition
