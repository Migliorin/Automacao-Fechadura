from paho.mqtt import client as mqtt_client
from graphql import get_pwd


broker = '10.0.0.190'
port = 1883
topic = "foobar"
# generate client ID with pub prefix randomly
client_id = f'IA_Operador'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client_, userdata_, msg):
        dict_rvc = eval(msg.payload.decode())
        print(f"Received `{dict_rvc}` from `{msg.topic}` topic")

        pwd = get_pwd(dict_rvc['name'])['data']['persons']

        if(len(pwd) == 0 ):
            name = dict_rvc['name']
            msg_res = f'acesso negado para {name}'
            publish(client,msg_res)
        else:
            pwd = pwd[0]['pwd']
            if(pwd == dict_rvc['senha']):

                print("Send response")
                name = dict_rvc['name']
                msg_res = f'acesso liberado para {name}'
                publish(client,msg_res)
            else:
                name = dict_rvc['name']
                msg_res = f'acesso negado para {name}'
                publish(client,msg_res)

    client.subscribe(topic)
    client.on_message = on_message

def publish(client,msg):
    result = client.publish('response', msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

run()