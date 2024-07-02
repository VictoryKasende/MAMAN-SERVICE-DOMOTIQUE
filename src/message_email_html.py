import main

message_email = """
<html>
<head>
    <style>
        .card {
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            width: 450px;
            margin: 40px auto;
            font-family: Arial, sans-serif;
        }

        .card-header {
            background-color: #4CAF50;
            color: #fff;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            padding: 15px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
        }

        .card-body {
            padding: 25px;
        }

        .card-body p {
            color: #555;
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 15px;
        }

        .card-body ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }

        .card-body li {
            margin-bottom: 10px;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="card-header">Statistiques de la maison</div>
        <div class="card-body">
            <p>Voici les statistiques de votre maison pour le mois dernier :</p>
            <ul>
                <li>Température moyenne : """ + str(main.salon_temperature) + """</li>
                <li>Humidité moyenne : """ + str(main.salon_humidite) + """</li> 
            </ul>
        </div>
    </div>
</body>
</html>

"""