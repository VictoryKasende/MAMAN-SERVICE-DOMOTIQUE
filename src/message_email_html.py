import datetime
import pytz

def return_fString_html(etat_maison):
    # Obtenir la date et l'heure actuelles de la RDC
    tz_rdc = pytz.timezone('Africa/Kinshasa')
    now_rdc = datetime.datetime.now(tz_rdc)
    date_time_str = now_rdc.strftime("%d/%m/%Y %H:%M:%S")

    etat_lignes = ""
    for piece, etat in etat_maison.items():
        if piece not in ['temperature', 'humidite']:
            etat_lignes += f"<li>{piece.replace('_', ' ').title()} : {'allumé' if etat == 'on' else 'éteint'}</li>"
        else:
            etat_lignes += f"<li>{piece.title()} : {etat}</li>"

    message_email_html = f"""
        <html>
        <head>
            <style>
                .card {{
                    background-color: #fff;
                    border-radius: 10px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
                    width: 450px;
                    margin: 40px auto;
                    font-family: Arial, sans-serif;
                }}

                .card-header {{
                    background-color: #4CAF50;
                    color: #fff;
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
                    padding: 15px;
                    text-align: center;
                    font-size: 20px;
                    font-weight: bold;
                }}

                .card-body {{
                    padding: 25px;
                }}

                .card-body p {{
                    color: #555;
                    font-size: 16px;
                    line-height: 1.6;
                    margin-bottom: 15px;
                }}

                .card-body ul {{
                    list-style-type: none;
                    padding: 0;
                    margin: 0;
                }}

                .card-body li {{
                    margin-bottom: 10px;
                    font-size: 16px;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="card-header">Statistiques de la maison du {date_time_str}</div>
                <div class="card-body">
                    <p>Voici l'état de votre maison :</p>
                    <ul>
                        {etat_lignes}
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
    return message_email_html
