import time
import redis

client = redis.Redis(
    host='localhost',
    password='student',
    port=6379,
)

client.set(
    '22305-kvilina-sportsman-sportsman1',
    'Petrov Petr Petrovich',
)
client.set(
    '22305-kvilina-sportsman-sportsman2',
    'Sidiriva Mariay Petrovna',
)
client.set(
    '22305-kvilina-judge-judge1',
    'Ivanov Ivan Ivanovich',
)
client.set(
    '22305-kvilina-judge-judge2',
    'Sidorov Sidor Sidorevich',
)
client.set(
    '22305-kvilina-exercise-exercise2',
    'press',
)
client.set(
    '22305-kvilina-exercise-exercise1',
    'bench press',
)
client.set(
    '22305-kvilina-exercise-exercise3',
    'squats',
)
keys = client.keys(
    '*'
)
for (
    key
) in keys:
    if (
        "22305-kvilina"
        in str(
            key
        )
    ):
        print(
            key
        )
        print(
            client.get(
                key
            )
        )
client.close()
print()
