import tkinter as tk
from tkinter import (
    ttk,
)
from tkinter import (
    Label,
)
import pymongo

# Подключение к базе данных
client = pymongo.MongoClient(
    "localhost",
    27017,
)
db = client[
    "22305"
]
matches_collection = db[
    "kvilina-matches"
]  # Замените на имя вашей коллекции

# Получение списка ключей из коллекции
keys_list = [
    "goals",
    "fouls",
    "penalty",
]


def on_click_show_list():
    key = (
        combo_query_keys.get()
    )
    sign = (
        combo_query_sign.get()
    )
    a_count = (
        entry_count.get()
    )
    write_count = (
        0
    )
    table_answer.grid_forget()
    for item in (
        table_answer.get_children()
    ):
        table_answer.delete(
            item
        )
    if (
        sign
        == ">"
    ):
        ag_sign = "$gt"
    elif (
        sign
        == "<"
    ):
        ag_sign = "$lt"
    elif (
        sign
        == "<="
    ):
        ag_sign = "$lte"
    else:
        ag_sign = "$gte"
    players = (
        {}
    )
    matches = db[
        "kvilina-matches"
    ].find(
        {}
    )
    for item in matches:
        try:
            a = item[
                key
            ]
            for goal in a:
                try:
                    if (
                        key
                        == "goals"
                    ):
                        count = players.get(
                            goal[
                                "author"
                            ]
                        )
                        if (
                            count
                            is None
                        ):
                            count = 0
                        players.update(
                            {
                                goal[
                                    "author"
                                ]: count
                                + 1
                            }
                        )
                    elif (
                        key
                        == "fouls"
                    ):
                        count = players.get(
                            goal[
                                "player"
                            ]
                        )
                        if (
                            count
                            is None
                        ):
                            count = 0
                        players.update(
                            {
                                goal[
                                    "player"
                                ]: count
                                + 1
                            }
                        )
                    else:
                        count = players.get(
                            goal[
                                "whose fault"
                            ]
                        )
                        if (
                            count
                            is None
                        ):
                            count = 0
                        players.update(
                            {
                                goal[
                                    "whose fault"
                                ]: count
                                + 1
                            }
                        )
                except:
                    continue
        except:
            continue
    players = sorted(
        players.items(),
        key=lambda x: x[
            1
        ],
        reverse=True,
    )
    answer = (
        []
    )
    for item in players:
        if (
            sign
            == ">"
        ):
            if item[
                1
            ] > int(
                a_count
            ):
                answer.append(
                    item
                )
        if (
            sign
            == ">="
        ):
            if item[
                1
            ] >= int(
                a_count
            ):
                answer.append(
                    item
                )
        if (
            sign
            == "<"
        ):
            if item[
                1
            ] < int(
                a_count
            ):
                answer.append(
                    item
                )
        if (
            sign
            == "<="
        ):
            if item[
                1
            ] <= int(
                a_count
            ):
                answer.append(
                    item
                )
    if (
        len(
            answer
        )
        > 0
    ):
        for item in answer:
            table_answer.insert(
                "",
                "end",
                values=(
                    item[
                        0
                    ],
                    item[
                        1
                    ],
                ),
            )
        table_answer.grid(
            row=(
                combo_query_keys.grid_info()
            )[
                "row"
            ]
            + 1,
            columnspan=3,
            column=1,
        )
    query = (
        ""
    )
    if (
        key
        == "goals"
    ):
        query = db[
            "kvilina-matches"
        ].aggregate(
            [
                {
                    "$unwind": "$goals"
                },
                {
                    "$group": {
                        "_id": {
                            "author": "$goals.author",
                            "match_id": "$_id",
                        },
                        "goalsCount": {
                            "$sum": 1
                        },
                    }
                },
                {
                    "$group": {
                        "_id": "$_id.author",
                        "totalGoals": {
                            "$sum": "$goalsCount"
                        },
                    }
                },
                {
                    "$match": {
                        "totalGoals": {
                            ag_sign: int(
                                a_count
                            )
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "player": "$_id",
                        "totalGoals": 1,
                    }
                },
                {
                    "$count": "count"
                },
            ]
        )
    elif (
        key
        == "fouls"
    ):
        query = db[
            "kvilina-matches"
        ].aggregate(
            [
                {
                    "$unwind": "$fouls"
                },
                {
                    "$group": {
                        "_id": {
                            "author": "$fouls.player",
                            "match_id": "$_id",
                        },
                        "foulsCount": {
                            "$sum": 1
                        },
                    }
                },
                {
                    "$group": {
                        "_id": "$_id.author",
                        "totalFouls": {
                            "$sum": "$foulsCount"
                        },
                    }
                },
                {
                    "$match": {
                        "totalFouls": {
                            ag_sign: int(
                                a_count
                            )
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "player": "$_id",
                        "totalFouls": 1,
                    }
                },
                {
                    "$count": "count"
                },
            ]
        )
    elif (
        key
        == "penalty"
    ):
        query = db[
            "kvilina-matches"
        ].aggregate(
            [
                {
                    "$unwind": "$penalty"
                },
                {
                    "$group": {
                        "_id": {
                            "author": "$penalty.whose_fault",
                            "match_id": "$_id",
                        },
                        "penaltyCount": {
                            "$sum": 1
                        },
                    }
                },
                {
                    "$group": {
                        "_id": "$_id.author",
                        "totalPenalties": {
                            "$sum": "$penaltyCount"
                        },
                    }
                },
                {
                    "$match": {
                        "totalPenalties": {
                            ag_sign: int(
                                a_count
                            )
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "player": "$_id",
                        "totalPenalties": 1,
                    }
                },
                {
                    "$count": "count"
                },
            ]
        )
    for item in query:
        label9 = Label(
            main_window,
            text="Количество: "
            + str(
                item[
                    "count"
                ]
            ),
        )
        label9.grid(
            row=(
                table_answer.grid_info()
            )[
                "row"
            ]
            + 1
        )


# Создание окна
main_window = (
    tk.Tk()
)
main_window.title(
    "Футбольный поиск"
)

# Создание и размещение элементов интерфейса
key_label = tk.Label(
    main_window,
    text="Ключ:",
)
key_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
)

# Создание выпадающего списка с ключами из базы данных
combo_query_keys = ttk.Combobox(
    main_window,
    values=keys_list,
)
combo_query_keys.grid(
    row=0,
    column=1,
    padx=10,
    pady=10,
)

comparison_label = tk.Label(
    main_window,
    text="Сравнение:",
)
comparison_label.grid(
    row=0,
    column=2,
    padx=10,
    pady=10,
)
combo_query_sign = ttk.Combobox(
    main_window,
    values=[
        ">",
        ">=",
        "=",
        "<=",
        "<",
    ],
)
combo_query_sign.grid(
    row=0,
    column=3,
    padx=10,
    pady=10,
)

value_label = tk.Label(
    main_window,
    text="Значение:",
)
value_label.grid(
    row=0,
    column=4,
    padx=10,
    pady=10,
)
entry_count = tk.Entry(
    main_window
)
entry_count.grid(
    row=0,
    column=5,
    padx=10,
    pady=10,
)

search_button = tk.Button(
    main_window,
    text="Поиск",
    command=on_click_show_list,
)
search_button.grid(
    row=0,
    column=6,
    padx=10,
    pady=10,
)

table_answer = ttk.Treeview(
    main_window,
    columns=(
        "Player",
        "TotalGoals",
    ),
)
table_answer.heading(
    "#0",
    text="Player",
)
table_answer.heading(
    "#1",
    text="TotalGoals",
)
table_answer.grid(
    row=1,
    column=0,
    columnspan=7,
    padx=10,
    pady=10,
)

# Запуск главного цикла
main_window.mainloop()
