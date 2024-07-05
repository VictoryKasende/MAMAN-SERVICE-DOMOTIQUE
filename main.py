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


etat_maison = {
    "salon_temperature": None,
    "salon_humidite": None,
    "salon_etat": None,
    "chambre_parents_etat": None,
    "chambre_enfants_etat": None,
    "couloir_etat": None,
    "cuisine_etat": None,
    "depot_etat": None,
    "exterieur_etat": None,
    "ventilateur_etat": None,
    "projecteur_etat": None,
    "alarme_etat": None,
    "tout_etat": None,
}

topics = {
    "salon_temperature": "maman_service/salon/temperature",
    "salon_humidite": "maman_service/salon/humidite",
    "salon_etat": "maman_service/lampe/salon/etat",
    "chambre_parents_etat": "maman_service/lampe/chambre_parents/etat",
    "chambre_enfants_etat": "maman_service/lampe/chambre_enfants/etat",
    "couloir_etat": "maman_service/lampe/couloir/etat",
    "cuisine_etat": "maman_service/lampe/cuisine/etat",
    "depot_etat": "maman_service/lampe/depot/etat",
    "exterieur_etat": "maman_service/lampe/exterieur/etat",
    "ventilateur_etat": "maman_service/ventilateur/etat",
    "projecteur_etat": "maman_service/projecteur/etat",
    "alarme_etat": "maman_service/alarme/etat",
    "tout_etat": "maman_service/maison/etat",
    "salon": "maman_service/lampe/salon",
    "chambre_parents": "maman_service/lampe/chambre_parents",
    "chambre_enfants": "maman_service/lampe/chambre_enfants",
    "couloir": "maman_service/lampe/couloir",
    "cuisine": "maman_service/lampe/cuisine",
    "depot": "maman_service/lampe/depot",
    "exterieur": "maman_service/lampe/exterieur",
    "ventilateur": "maman_service/ventilateur",
    "projecteur": "maman_service/projecteur",
    "alarme": "maman_service/alarme",
    "email": "maman_service/email/statistique/maison",
    "tout": "maman_service/lampes/tout"
}


def on_message(client, userdata, msg):
    global etat_maison

    filtered_topics = {k: v for k, v in topics.items() if k in etat_maison}
    topic_to_attr = {v: k for k, v in filtered_topics.items()}

    if msg.topic in topic_to_attr:
        attr = topic_to_attr[msg.topic]
        if attr == "tout_etat":
            etat_maison[attr] = ast.literal_eval(msg.payload.decode())
        else:
            etat_maison[attr] = msg.payload.decode()
        print(f"État mis à jour : {attr} = {etat_maison[attr]}")
    else:
        pass
        #print(f"Message reçu sur le sujet {msg.topic} : {msg.payload.decode()}")


def response_ia(content_user, content_system):
    global url
    payload = {
        "messages": [
            {"role": "system", "content": content_system},
            {"role": "user", "content": content_user}
        ],
        "web_access": False
    }

    headers = {
        "x-rapidapi-key": "1912b97d24msh6ec09b4efbc569cp14cca6jsnaa2ebad48593",
        "x-rapidapi-host": "open-ai21.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        if 'status' in response_json and response_json['status']:
            return response_json['result'].strip()

    return "Vous avez dépassé votre limite de messages pour aujourd'hui. Veuillez souscrire au premium."


def handleResponse(query):
    global etat_maison

    topic = response_ia(query, content_system_ia.content_command)
    print(topic)

    actions = {
        f"{topics['salon']}/on": ("on", "la lampe du salon est allumée"),
        f"{topics['salon']}/off": ("off", "la lampe du salon est éteinte"),
        f"{topics['chambre_parents']}/on": ("on", "la lampe de la chambre des parents est allumée"),
        f"{topics['chambre_parents']}/off": ("off", "la lampe de la chambre des parents est éteinte"),
        f"{topics['chambre_enfants']}/on": ("on", "la lampe de la chambre des enfants est allumée"),
        f"{topics['chambre_enfants']}/off": ("off", "la lampe de la chambre des enfants est éteinte"),
        f"{topics['couloir']}/on": ("on", "la lampe du couloir est allumée"),
        f"{topics['couloir']}/off": ("off", "la lampe du couloir est éteinte"),
        f"{topics['cuisine']}/on": ("on", "la lampe de la cuisine est allumée"),
        f"{topics['cuisine']}/off": ("off", "la lampe de la cuisine est éteinte"),
        f"{topics['depot']}/on": ("on", "la lampe du dépôt est allumée"),
        f"{topics['depot']}/off": ("off", "la lampe du dépôt est éteinte"),
        f"{topics['exterieur']}/on": ("on", "la lampe de l'extérieur est allumée"),
        f"{topics['exterieur']}/off": ("off", "la lampe de l'extérieur est éteinte"),
        f"{topics['ventilateur']}/on": ("on", "le ventilateur est allumé"),
        f"{topics['ventilateur']}/off": ("off", "le ventilateur est éteint"),
        f"{topics['projecteur']}/on": ("on", "le projecteur est allumé"),
        f"{topics['projecteur']}/off": ("off", "le projecteur est éteint"),
        f"{topics['alarme']}/on": ("on", "l'alarme est allumée"),
        f"{topics['alarme']}/off": ("off", "l'alarme est éteinte")
    }

    etats = {
        topics['salon_temperature']: ("salon_temperature", "la température du salon est de {} degrés"),
        topics['salon_humidite']: ("salon_humidite", "l'humidité du salon est de {}%"),
        topics['salon_etat']: ("salon_etat", "L'état du salon est : {}"),
        topics['chambre_parents_etat']: ("chambre_parents_etat", "L'état de la chambre des parents est : {}"),
        topics['chambre_enfants_etat']: ("chambre_enfants_etat", "L'état de la chambre des enfants est : {}"),
        topics['couloir_etat']: ("couloir_etat", "L'état du couloir est : {}"),
        topics['cuisine_etat']: ("cuisine_etat", "L'état de la cuisine est : {}"),
        topics['depot_etat']: ("depot_etat", "L'état du dépôt est : {}"),
        topics['exterieur_etat']: ("exterieur_etat", "L'état de l'extérieur est : {}"),
        topics['ventilateur_etat']: ("ventilateur_etat", "L'état du ventilateur est : {}"),
        topics['projecteur_etat']: ("projecteur_etat", "L'état du projecteur est : {}"),
        topics['alarme_etat']: ("alarme_etat", "L'état de l'alarme est : {}")
    }

    if topic in actions:
        action, message_content = actions[topic]
        mqtt_client.publish(topic.split('/')[0], action)
        return response_ia(content_user=message_content, content_system=content_system_ia.content_response)

    if topic in etats:
        attr, message_template = etats[topic]
        if etat_maison[attr] is not None:
            return response_ia(content_user=message_template.format(etat_maison[attr]), content_system=content_system_ia.content_response)
        else:
            return response_ia(content_user="Désolé, je n'ai pas d'informations sur ce paramètre.", content_system=content_system_ia.content_response)

    if topic == topics['email']:
        message = response_ia(content_user="L'email des statistiques de la maison a été envoyé.", content_system=content_system_ia.content_response)
        emails.main(etat_maison['tout_etat'])
        print(etat_maison['tout_etat'])
        return message

    if topic == f"{topics['tout']}/on":
        for key in ['salon', 'chambre_parents', 'chambre_enfants', 'couloir', 'cuisine', 'depot', 'exterieur', 'projecteur']:
            mqtt_client.publish(topics[key], "on")
        return response_ia(content_user="Toutes les lampes ont été allumées.", content_system=content_system_ia.content_response)

    if topic == f"{topics['tout']}/off":
        for key in ['salon', 'chambre_parents', 'chambre_enfants', 'couloir', 'cuisine', 'depot', 'exterieur', 'projecteur']:
            mqtt_client.publish(topics[key], "off")
        return response_ia(content_user="Toutes les lampes ont été éteintes.", content_system=content_system_ia.content_response)

    if topic == topics['tout_etat']:
        response = ""
        response_map = {
            "salon": "L'état du salon est : {}",
            "chambre_de_parents": "L'état de la chambre des parents est : {}",
            "chambre_des_enfants": "L'état de la chambre des enfants est : {}",
            "couloir": "L'état du couloir est : {}",
            "cuisine": "L'état de la cuisine est : {}",
            "depot": "L'état du dépôt est : {}",
            "exterieur": "L'état de l'extérieur est : {}",
            "ventilateur": "L'état du ventilateur est : {}",
            "projecteur": "L'état du projecteur est : {}",
            "alarme": "L'état de l'alarme est : {}",
            "temperature": "La température du salon est de : {} degrés",
            "humidite": "L'humidité du salon est de : {}%"
        }

        tout_etat = etat_maison['tout_etat'] if etat_maison['tout_etat'] else {}

        for key, template in response_map.items():
            if key in tout_etat:
                response += template.format(tout_etat[key]) + "\n"
            else:
                response += f"Désolé, je n'ai pas d'informations sur l'état de {key}.\n"

        return response_ia(content_user=response, content_system=content_system_ia.content_response)

    return response_ia(content_user="Désolé, je ne comprends pas cette commande.", content_system=content_system_ia.content_response)


def main():
    for key in etat_maison.keys():
        mqtt_client.subscribe(topics[key])

    mqtt_client.on_message = on_message
    mqtt_client.loop_start()

    thing.setCallback(handleResponse).start()


if __name__ == "__main__":
    main()

