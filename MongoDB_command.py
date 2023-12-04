import pymongo
import json


client = pymongo.MongoClient(
    'localhost',
    27017,
)
db = client[
    '22305'
]

key_prefix = "kvilina-"

teams_collection = db[
    key_prefix
    + "teams"
]
matches_collection = db[
    key_prefix
    + "matches"
]
teams = teams_collection.find(
    {
        "$or": [
            {
                "name": "Liverpool"
            },
            {
                "name": "Manchester Unite"
            },
        ]
    }
)
matches = matches_collection.find(
    {
        "$or": [
            {
                "home team": "Liverpool"
            }
        ]
    }
)
for (
    team
) in (
    teams
):
    print(
        team
    )
for (
    match
) in matches:
    print(
        match
    )
teams_collection.insert_one(
    {
        "name": "Liverpool",
        "city": "Liverpool",
        "coach": "Jurgen Klopp",
        "lineup": [
            {
                "name": "Mohamed Salah",
                "position": "F",
            },
            {
                "name": "Virgil van Dijk",
                "position": "D",
            },
            {
                "name": "Jordan Henderson",
                "position": "M",
            },
            {
                "name": "Sadio Mane",
                "position": "F",
            },
            {
                "name": "Thiago Alcantara",
                "position": "M",
            },
            {
                "name": "Andrew Robertson",
                "position": "D",
            },
            {
                "name": "Fabinho",
                "position": "M",
            },
            {
                "name": "Trent Alexander-Arnold",
                "position": "D",
            },
            {
                "name": "Alisson Becker",
                "position": "GK",
            },
        ],
        "substitute": [
            {
                "name": "Roberto Firmino",
                "position": "F",
            },
            {
                "name": "Diogo Jota",
                "position": "F",
            },
            {
                "name": "James Milner",
                "position": "M",
            },
            {
                "name": "Joel Matip",
                "position": "D",
            },
            {
                "name": "Caoimhin Kelleher",
                "position": "GK",
            },
        ],
    }
)

teams_collection.insert_one(
    {
        "name": "Manchester United",
        "city": "Manchester",
        "coach": "Ralf Rangnick",
        "lineup": [
            {
                "name": "Cristiano Ronaldo",
                "position": "F",
            },
            {
                "name": "Harry Maguire",
                "position": "D",
            },
            {
                "name": "Bruno Fernandes",
                "position": "M",
            },
            {
                "name": "Marcus Rashford",
                "position": "F",
            },
            {
                "name": "Paul Pogba",
                "position": "M",
            },
            {
                "name": "Luke Shaw",
                "position": "D",
            },
            {
                "name": "Nemanja Matic",
                "position": "M",
            },
            {
                "name": "Aaron Wan-Bissaka",
                "position": "D",
            },
            {
                "name": "David de Gea",
                "position": "GK",
            },
        ],
        "substitute": [
            {
                "name": "Edinson Cavani",
                "position": "F",
            },
            {
                "name": "Jadon Sancho",
                "position": "F",
            },
            {
                "name": "Scott McTominay",
                "position": "M",
            },
            {
                "name": "Eric Bailly",
                "position": "D",
            },
            {
                "name": "Dean Henderson",
                "position": "GK",
            },
        ],
    }
)

# Добавление данных об играх
matches_collection.insert_one(
    {
        "home team": "Liverpool",
        "away team": "Manchester United",
        "date": "2023-11-05",
        "score": "2:1",
        "fouls": [
            {
                "card": "yellow",
                "player": "Harry Maguire",
                "minute": "25",
                "reason": "Фол",
            },
            {
                "card": "yellow",
                "player": "Jordan Henderson",
                "minute": "35",
                "reason": "Рукоприкладство",
            },
            {
                "card": "red",
                "player": "Marcus Rashford",
                "minute": "70",
                "reason": "Грубый фол",
            },
        ],
        "goals": [
            {
                "position": "Слева, в 20 метрах от ворот",
                "minute": "15",
                "author": "Mohamed Salah",
                "assist": "Jordan Henderson",
            },
            {
                "position": "По центру, в 10 метрах от ворот",
                "minute": "60",
                "author": "Cristiano Ronaldo",
                "assist": "Bruno Fernandes",
            },
            {
                "position": "Справа, в 18 метрах от ворот",
                "minute": "80",
                "author": "Sadio Mane",
                "assist": "Thiago Alcantara",
            },
        ],
        "penalty": [
            {
                "minute": "70",
                "whose fault": "Marcus Rashford",
                "converted": False,
            },
        ],
        "home kicks": "8",
        "away kicks": "10",
    }
)
