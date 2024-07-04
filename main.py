import requests
import paho.mqtt.client as mqtt
from src import configurations, content_system_ia, emails
import ast
from src import ThingEsp
from src import configurations
from src import emails

thing = ThingEsp.Client('Victory', 'DomotiqueWhats', 'victory2003')
url = "https://open-ai21.p.rapidapi.com/chatgpt"


# Configuration de votre client MQTT
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(configurations.user, configurations.password)
mqtt_client.connect(configurations.mqtt_broker, configurations.port, 60)

salon_temperature = None
salon_humidite = None
salon_etat = None
chambre_parents_etat = None
chambre_enfants_etat = None
couloir_etat = None
cuisine_etat = None
depot_etat = None
exterieur_etat = None
ventilateur_etat = None
projecteur_etat = None
alarme_etat = None
tout_etat = None

TOPIC_SALON = "maman_service/lampe/salon"
TOPIC_CHAMBRE_PARENTS = "maman_service/lampe/chambre_parents"
TOPIC_CHAMBRE_ENFANTS = "maman_service/lampe/chambre_enfants"
TOPIC_COULOIR = "maman_service/lampe/couloir"
TOPIC_CUISINE = "maman_service/lampe/cuisine"
TOPIC_DEPOT = "maman_service/lampe/depot"
TOPIC_EXTERIEUR = "maman_service/lampe/exterieur"
TOPIC_VENTILATEUR = "maman_service/ventilateur"
TOPIC_PROJECTEUR = "maman_service/projecteur"
TOPIC_SALON_TEMPERATURE = "maman_service/salon/temperature"
TOPIC_SALON_HUMIDITE = "maman_service/salon/humidite"
TOPIC_ALARME = "maman_service/alarme"
TOPIC_EMAIL = "maman_service/email/statistique/maison"
TOPIC_TOUT = "maman_service/lampes/tout"

TOPIC_SALON_ETAT = "maman_service/lampe/salon/etat"
TOPIC_CHAMBRE_PARENTS_ETAT = "maman_service/lampe/chambre_parents/etat"
TOPIC_CHAMBRE_ENFANTS_ETAT = "maman_service/lampe/chambre_enfants/etat"
TOPIC_COULOIR_ETAT = "maman_service/lampe/couloir/etat"
TOPIC_CUISINE_ETAT = "maman_service/lampe/cuisine/etat"
TOPIC_DEPOT_ETAT = "maman_service/lampe/depot/etat"
TOPIC_EXTERIEUR_ETAT = "maman_service/lampe/exterieur/etat"
TOPIC_VENTILATEUR_ETAT = "maman_service/ventilateur/etat"
TOPIC_PROJECTEUR_ETAT = "maman_service/projecteur/etat"
TOPIC_SALON_TEMPERATURE_ETAT = "maman_service/salon/temperature/etat"
TOPIC_SALON_HUMIDITE_ETAT = "maman_service/salon/humidite/etat"
TOPIC_ALARME_ETAT = "maman_service/alarme/etat"
TOPIC_TOUT_ETAT = "maman_service/maison/etat"


def on_message(client, userdata, msg):
    global salon_temperature
    global salon_humidite
    global salon_etat
    global chambre_parents_etat
    global chambre_enfants_etat
    global couloir_etat
    global cuisine_etat
    global depot_etat
    global exterieur_etat
    global ventilateur_etat
    global projecteur_etat
    global alarme_etat
    global tout_etat

    if msg.topic == TOPIC_SALON_TEMPERATURE:
        salon_temperature = msg.payload.decode()
        # print(salon_temperature)
    elif msg.topic == TOPIC_SALON_HUMIDITE:
        # print(salon_humidite)
        salon_humidite = msg.payload.decode()
    elif msg.topic == TOPIC_SALON_ETAT:
        salon_etat = msg.payload.decode()
        # print(f"État du salon : {salon_etat}")
    elif msg.topic == TOPIC_CHAMBRE_PARENTS_ETAT:
        chambre_parents_etat = msg.payload.decode()
        # print(f"État de la chambre des parents : {chambre_parents_etat}")
    elif msg.topic == TOPIC_CHAMBRE_ENFANTS_ETAT:
        chambre_enfants_etat = msg.payload.decode()
        # print(f"État de la chambre des enfants : {chambre_enfants_etat}")
    elif msg.topic == TOPIC_COULOIR_ETAT:
        couloir_etat = msg.payload.decode()
        # print(f"État du couloir : {couloir_etat}")
    elif msg.topic == TOPIC_CUISINE_ETAT:
        cuisine_etat = msg.payload.decode()
        # print(f"État de la cuisine : {cuisine_etat}")
    elif msg.topic == TOPIC_DEPOT_ETAT:
        depot_etat = msg.payload.decode()
        # print(f"État du déport : {depot_etat}")
    elif msg.topic == TOPIC_EXTERIEUR_ETAT:
        exterieur_etat = msg.payload.decode()
        # print(f"État de l'extérieur : {exterieur_etat}")
    elif msg.topic == TOPIC_VENTILATEUR_ETAT:
        ventilateur_etat = msg.payload.decode()
        # print(f"État du ventilateur : {ventilateur_etat}")
    elif msg.topic == TOPIC_PROJECTEUR_ETAT:
        projecteur_etat = msg.payload.decode()
        # print(f"État du projecteur : {projecteur_etat}")
    elif msg.topic == TOPIC_ALARME_ETAT:
        alarme_etat = msg.payload.decode()
        # print(f"État du projecteur : {projecteur_etat}")
    elif msg.topic == TOPIC_TOUT_ETAT:
        tout_etat_str = msg.payload.decode()
        tout_etat = ast.literal_eval(tout_etat_str)
        # print(f"État de la maison : {type(tout_etat)}")
    else:
        print(f"Message reçu sur le sujet {msg.topic} : {msg.payload.decode()}")


def response_ia(content_user, content_system):
    global url
    payload = {
        "messages": [
            {
                "role": "system",
                "content": content_system
            },
            {
                "role": "user",
                "content": content_user
            }
        ],
        "web_access": False
    }
    
    headers = {
        "x-rapidapi-key": "1912b97d24msh6ec09b4efbc569cp14cca6jsnaa2ebad48593",
        "x-rapidapi-host": "open-ai21.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    if 'status' in response_json and response_json['status']:
        return response_json['result'].strip()
    else:
        return "Vous avez depasse votre limite de messages pour aujourd'hui."


def handleResponse(query):
    global salon_temperature
    global salon_humidite
    global salon_etat
    global chambre_parents_etat
    global chambre_enfants_etat
    global couloir_etat
    global cuisine_etat
    global depot_etat
    global exterieur_etat
    global ventilateur_etat
    global projecteur_etat
    global alarme_etat
    global tout_etat

    topic = response_ia(query, content_system_ia.content_command)
    print(topic)

    if topic == f"{TOPIC_SALON}/on":
        mqtt_client.publish(TOPIC_SALON, "on")
        message = response_ia(content_user="la lampe du salon est allume", content_system=content_system_ia.content_response)
        return message
    elif topic == f"{TOPIC_SALON}/off":
        mqtt_client.publish(TOPIC_SALON, "off")
        return response_ia(content_user="la lampe du salon est eteinte", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_CHAMBRE_PARENTS}/on":
        mqtt_client.publish(TOPIC_CHAMBRE_PARENTS, "on")
        return response_ia(content_user="la lampe du chambre de parents est allume", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_CHAMBRE_PARENTS}/off":
        mqtt_client.publish(TOPIC_CHAMBRE_PARENTS, "off")
        return response_ia(content_user="la lampe du chambre de parents est eteinte", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_CHAMBRE_ENFANTS}/on":
        mqtt_client.publish(TOPIC_CHAMBRE_ENFANTS, "on")
        return response_ia(content_user="la lampe du chambre des enfants est allume", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_CHAMBRE_ENFANTS}/off":
        mqtt_client.publish(TOPIC_CHAMBRE_ENFANTS, "off")
        return response_ia(content_user="la lampe du chambre des enfants est eteinte", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_COULOIR}/on":
        mqtt_client.publish(TOPIC_COULOIR, "on")
        return response_ia(content_user="la lampe du couloir est allume", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_COULOIR}/off":
        mqtt_client.publish(TOPIC_COULOIR, "off")
        return response_ia(content_user="la lampe du couloir est eteinte", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_CUISINE}/on":
        mqtt_client.publish(TOPIC_CUISINE, "on")
        return response_ia(content_user="la lampe de la cuisine est allume", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_CUISINE}/off":
        mqtt_client.publish(TOPIC_CUISINE, "off")
        return response_ia(content_user="la lampe de la cuisine est eteinte", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_DEPOT}/on":
        mqtt_client.publish(TOPIC_DEPOT, "on")
        return response_ia(content_user="la lampe du dépôt est allume", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_DEPOT}/off":
        mqtt_client.publish(TOPIC_DEPOT, "off")
        return response_ia(content_user="la lampe du dépôt est eteinte", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_EXTERIEUR}/on":
        mqtt_client.publish(TOPIC_EXTERIEUR, "on")
        return response_ia(content_user="la lampe de l'extérieur est allume", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_EXTERIEUR}/off":
        mqtt_client.publish(TOPIC_EXTERIEUR, "off")
        return response_ia(content_user="la lampe de l'extérieur est eteinte", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_VENTILATEUR}/on":
        mqtt_client.publish(TOPIC_VENTILATEUR, "on")
        return response_ia(content_user="le ventilateur est allume", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_VENTILATEUR}/off":
        mqtt_client.publish(TOPIC_VENTILATEUR, "off")
        return response_ia(content_user="le ventilateur est eteint", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_PROJECTEUR}/on":
        mqtt_client.publish(TOPIC_PROJECTEUR, "on")
        return response_ia(content_user="le projecteur est allume", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_PROJECTEUR}/off":
        mqtt_client.publish(TOPIC_PROJECTEUR, "off")
        return response_ia(content_user="le projecteur est eteint", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_ALARME}/on":
        mqtt_client.publish(TOPIC_ALARME, "on")
        return response_ia(content_user="l'alarme est allume", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_ALARME}/off":
        mqtt_client.publish(TOPIC_ALARME, "off")
        return response_ia(content_user="l'alarme est eteint", content_system=content_system_ia.content_response)
    elif topic == f"{TOPIC_EMAIL}":
        message = response_ia(content_user="L'email du statistique de la maison a ete envoye", content_system=content_system_ia.content_response)
        emails.send_mail(tout_etat)
        print(tout_etat)
        return message
    elif topic == f"{TOPIC_TOUT}/on":
        mqtt_client.publish(TOPIC_SALON, "on")
        mqtt_client.publish(TOPIC_CHAMBRE_PARENTS, "on")
        mqtt_client.publish(TOPIC_CHAMBRE_ENFANTS, "on")
        mqtt_client.publish(TOPIC_COULOIR, "on")
        mqtt_client.publish(TOPIC_CUISINE, "on")
        mqtt_client.publish(TOPIC_DEPOT, "on")
        mqtt_client.publish(TOPIC_EXTERIEUR, "on")
        mqtt_client.publish(TOPIC_PROJECTEUR, "on")
        return response_ia(content_user="Toutes les lampes ont été allumées.", content_system=content_system_ia.content_response)

    elif topic == f"{TOPIC_TOUT}/off":
        mqtt_client.publish(TOPIC_SALON, "off")
        mqtt_client.publish(TOPIC_CHAMBRE_PARENTS, "off")
        mqtt_client.publish(TOPIC_CHAMBRE_ENFANTS, "off")
        mqtt_client.publish(TOPIC_COULOIR, "off")
        mqtt_client.publish(TOPIC_CUISINE, "off")
        mqtt_client.publish(TOPIC_DEPOT, "off")
        mqtt_client.publish(TOPIC_EXTERIEUR, "off")
        mqtt_client.publish(TOPIC_PROJECTEUR, "off")
        return response_ia(content_user="Tous les lampes ont été éteintes.", content_system=content_system_ia.content_response)
    elif topic == TOPIC_SALON_TEMPERATURE:
        if salon_temperature is not None:
            return response_ia(content_user=f"la température du salon est de {salon_temperature} degrés",
                               content_system=content_system_ia.content_response)
        else:
            return response_ia(content_user="Désolé, je n'ai pas d'informations sur la température du salon.",
                               content_system=content_system_ia.content_response)
    elif topic == TOPIC_SALON_HUMIDITE:
        if salon_humidite is not None:
            return response_ia(content_user=f"l'humidité du salon est de {salon_humidite}%",
                               content_system=content_system_ia.content_response)
        else:
            return response_ia(content_user="Désolé, je n'ai pas d'informations sur l'humidité du salon.",
                               content_system=content_system_ia.content_response)
    elif topic == TOPIC_SALON_ETAT:
        if salon_etat is not None:
            return response_ia(content_user=f"L'état du salon est : {salon_etat}",
                               content_system=content_system_ia.content_response)
        else:
            return response_ia(content_user="Désolé, je n'ai pas d'informations sur l'état du salon.",
                               content_system=content_system_ia.content_response)
    elif topic == TOPIC_CHAMBRE_PARENTS_ETAT:
        if chambre_parents_etat is not None:
            response_ia(content_user=f"L'état de la chambre des parents est : {chambre_parents_etat}",
                        content_system=content_system_ia.content_response)
        else:
            return response_ia(content_user="Désolé, je n'ai pas d'informations sur l'état de la chambre des parents.",
                               content_system=content_system_ia.content_response)
    elif topic == TOPIC_CHAMBRE_ENFANTS_ETAT:
        if chambre_enfants_etat is not None:
            return response_ia(content_user=f"L'état de la chambre des enfants est : {chambre_enfants_etat}",
                               content_system=content_system_ia.content_response)
        else:
            return response_ia(content_user="Désolé, je n'ai pas d'informations sur l'état de la chambre des enfants.",
                               content_system=content_system_ia.content_response)
    elif topic == TOPIC_COULOIR_ETAT:
        if couloir_etat is not None:
            return response_ia(content_user=f"L'état du couloir est : {couloir_etat}",
                               content_system=content_system_ia.content_response)
        else:
            return response_ia(content_user="Désolé, je n'ai pas d'informations sur l'état du couloir.",
                               content_system=content_system_ia.content_response)
    elif topic == TOPIC_CUISINE_ETAT:
        if cuisine_etat is not None:
            return response_ia(content_user=f"L'état de la cuisine est : {cuisine_etat}",
                               content_system=content_system_ia.content_response)
        else:
            return response_ia(content_user="Désolé, je n'ai pas d'informations sur l'état de la cuisine.",
                               content_system=content_system_ia.content_response)
    elif topic == TOPIC_DEPOT_ETAT:
        if depot_etat is not None:
            return response_ia(content_user=f"L'état du dépôt est : {depot_etat}",
                               content_system=content_system_ia.content_response)
        else:
            return response_ia(content_user="Désolé, je n'ai pas d'informations sur l'état du dépôt.",
                               content_system=content_system_ia.content_response)
    elif topic == TOPIC_EXTERIEUR_ETAT:
        if exterieur_etat is not None:
            return response_ia(content_user=f"L'état de l'extérieur est : {exterieur_etat}",
                               content_system=content_system_ia.content_response)
        else:
            return response_ia(content_user="Désolé, je n'ai pas d'informations sur l'état de l'extérieur.",
                               content_system=content_system_ia.content_response)
    elif topic == TOPIC_VENTILATEUR_ETAT:
        if ventilateur_etat is not None:
            return response_ia(content_user=f"L'état du ventilateur est : {ventilateur_etat}",
                               content_system=content_system_ia.content_response)
        else:
            return response_ia(content_user="Désolé, je n'ai pas d'informations sur l'état du ventilateur.",
                               content_system=content_system_ia.content_response)
    elif topic == TOPIC_PROJECTEUR_ETAT:
        if projecteur_etat is not None:
            return response_ia(content_user=f"L'état du projecteur est : {projecteur_etat}",
                               content_system=content_system_ia.content_response)
        else:
            return response_ia(content_user="Désolé, je n'ai pas d'informations sur l'état du projecteur.",
                               content_system=content_system_ia.content_response)
    elif topic == TOPIC_ALARME_ETAT:
        if alarme_etat is not None:
            return response_ia(content_user=f"L'état de l'alarme est : {alarme_etat}",
                               content_system=content_system_ia.content_response)
        else:
            return response_ia(content_user="Désolé, je n'ai pas d'informations sur l'état de l'alarme.",
                               content_system=content_system_ia.content_response)
    elif topic == TOPIC_TOUT_ETAT:
        response = ""
        if "salon" in tout_etat:
            response += f"L'etat du salon est : {tout_etat['salon']}\n"
        else:
            response += "Désolé, je n'ai pas d'informations sur l'état du salon"
        if "chambre_de_parents" in tout_etat:
            response += f"L'état de la chambre des parents est : {tout_etat['chambre_de_parents']}.\n"
        else:
            response += "Désolé, je n'ai pas d'informations sur l'état de la chambre des parents.\n"

        if "chambre_des_enfants" in tout_etat:
            response += f"L'état de la chambre des enfants est : {tout_etat['chambre_des_enfants']}.\n"
        else:
            response += "Désolé, je n'ai pas d'informations sur l'état de la chambre des enfants.\n"

        if "couloir" in tout_etat:
            response += f"L'état du couloir est : {tout_etat['couloir']}.\n"
        else:
            response += "Désolé, je n'ai pas d'informations sur l'état du couloir.\n"

        if "cuisine" in tout_etat:
            response += f"L'état de la cuisine est : {tout_etat['cuisine']}.\n"
        else:
            response += "Désolé, je n'ai pas d'informations sur l'état de la cuisine.\n"

        if "depot" in tout_etat:
            response += f"L'état du dépot est : {tout_etat['depot']}.\n"
        else:
            response += "Désolé, je n'ai pas d'informations sur l'état du dépot.\n"

        if "exterieur" in tout_etat:
            response += f"L'état de l'extérieur est : {tout_etat['exterieur']}.\n"
        else:
            response += "Désolé, je n'ai pas d'informations sur l'état de l'extérieur.\n"

        if "ventilateur" in tout_etat:
            response += f"L'état du ventilateur est : {tout_etat['ventilateur']}.\n"
        else:
            response += "Désolé, je n'ai pas d'informations sur l'état du ventilateur.\n"

        if "projecteur" in tout_etat:
            response += f"L'état du projecteur est : {tout_etat['projecteur']}.\n"
        else:
            response += "Désolé, je n'ai pas d'informations sur l'état du projecteur.\n"

        if "alarme" in tout_etat:
            response += f"L'état de l'alarme est : {tout_etat['alarme']}.\n"
        else:
            response += "Désolé, je n'ai pas d'informations sur l'état de l'alarme.\n"
        if "temperature" in tout_etat:
            response += f"la température du salon est de : {tout_etat['temperature']}degrés.\n"
        else:
            response += "Désolé, je n'ai pas d'informations sur la température du salon."
        if "humidite" in tout_etat:
            response += f"l'humidité du salon est de : {tout_etat['humidite']}degrés.\n"
        else:
            response += "Désolé, je n'ai pas d'informations sur l'humidité du salon."
        return response_ia(content_user=response,
                           content_system=content_system_ia.content_response)
    else:
        return response_ia(content_user="Désolé, je ne comprends pas cette commande.",
                           content_system=content_system_ia.content_response)


def main():
    mqtt_client.subscribe(TOPIC_SALON_TEMPERATURE)
    mqtt_client.subscribe(TOPIC_SALON_HUMIDITE)
    mqtt_client.subscribe(TOPIC_SALON_ETAT)
    mqtt_client.subscribe(TOPIC_CHAMBRE_PARENTS_ETAT)
    mqtt_client.subscribe(TOPIC_CHAMBRE_ENFANTS_ETAT)
    mqtt_client.subscribe(TOPIC_COULOIR_ETAT)
    mqtt_client.subscribe(TOPIC_CUISINE_ETAT)
    mqtt_client.subscribe(TOPIC_DEPOT_ETAT)
    mqtt_client.subscribe(TOPIC_EXTERIEUR_ETAT)
    mqtt_client.subscribe(TOPIC_VENTILATEUR_ETAT)
    mqtt_client.subscribe(TOPIC_PROJECTEUR_ETAT)
    mqtt_client.subscribe(TOPIC_ALARME_ETAT)
    mqtt_client.subscribe(TOPIC_TOUT_ETAT)

    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    thing.setCallback(handleResponse).start()


if __name__ == "__main__":
    main()
