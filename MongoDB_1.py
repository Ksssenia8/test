import tkinter as tk
from tkinter import (
    ttk,
)
from pymongo import (
    MongoClient,
)


class FootballTeamsApp:
    def __init__(
        self,
        root,
        key_prefix,
    ):
        # Подключение к MongoDB
        self.client = MongoClient(
            'localhost',
            27017,
        )
        self.db = self.client[
            '22305'
        ]
        self.teams_collection = self.db[
            key_prefix
            + "teams"
        ]

        self.root = root
        self.key_prefix = key_prefix
        self.root.title(
            "Football Teams"
        )

        # Создаем Combobox для выбора команды
        self.team_var = (
            tk.StringVar()
        )
        teams = [
            team[
                'name'
            ]
            for team in self.teams_collection.find()
        ]
        self.team_combobox = ttk.Combobox(
            root,
            textvariable=self.team_var,
            values=teams
            + [
                "Новая команда"
            ],
            state="readonly",
        )
        self.team_combobox.set(
            "Выберите команду"
        )
        self.team_combobox.pack(
            pady=10
        )
        self.team_combobox.bind(
            "<<ComboboxSelected>>",
            self.load_team_data,
        )

        # Создаем entry-поля для ввода данных
        self.entry_labels = [
            "Город",
            "ФИО тренера",
            "Игрок",
            "Позиция",
            "Тип состава",
        ]
        self.entry_vars = [
            tk.StringVar()
            for _ in range(
                len(
                    self.entry_labels
                )
            )
        ]
        for (
            i,
            label,
        ) in enumerate(
            self.entry_labels
        ):
            tk.Label(
                root,
                text=label,
            ).pack()
            tk.Entry(
                root,
                textvariable=self.entry_vars[
                    i
                ],
            ).pack()

        # Кнопка для добавления данных
        add_button = tk.Button(
            root,
            text="Добавить",
            command=self.add_data_to_db,
        )
        add_button.pack()

        # Создаем таблицу
        columns = [
            "Название",
            "Город",
            "ФИО тренера",
            "Игрок",
            "Позиция",
            "Тип состава",
        ]
        self.tree = ttk.Treeview(
            root,
            columns=columns,
            show="headings",
        )
        for col in columns:
            self.tree.heading(
                col,
                text=col,
            )
            self.tree.column(
                col,
                width=100,
            )

        self.tree.pack(
            pady=20
        )

        # Загружаем данные из базы и отображаем их в таблице
        self.load_data()

    def load_team_data(
        self,
        event,
    ):
        selected_team = (
            self.team_var.get()
        )

        if (
            selected_team
            == "Новая команда"
        ):
            for var in (
                self.entry_vars
            ):
                var.set(
                    ""
                )
        else:
            team = self.teams_collection.find_one(
                {
                    "name": selected_team
                }
            )
            if team:
                self.entry_vars[
                    0
                ].set(
                    team[
                        'city'
                    ]
                )
                self.entry_vars[
                    1
                ].set(
                    team[
                        'coach'
                    ]
                )
            else:
                print(
                    f"Team {selected_team} not found."
                )

    def load_data(
        self,
    ):
        # Очищаем таблицу перед загрузкой новых данных
        for row in (
            self.tree.get_children()
        ):
            self.tree.delete(
                row
            )

        teams = (
            self.teams_collection.find()
        )
        for team in teams:
            try:
                print(
                    f"Processing team: {team}"
                )
                for player in team[
                    'lineup'
                ]:
                    print(
                        f"Lineup Player: {player}"
                    )
                    self.tree.insert(
                        "",
                        "end",
                        values=(
                            team[
                                'name'
                            ],
                            team[
                                'city'
                            ],
                            team[
                                'coach'
                            ],
                            player[
                                'name'
                            ],
                            player[
                                'position'
                            ],
                            'Основной',
                        ),
                    )
                for player in team[
                    'substitute'
                ]:
                    print(
                        f"Substitute Player: {player}"
                    )
                    self.tree.insert(
                        "",
                        "end",
                        values=(
                            team[
                                'name'
                            ],
                            team[
                                'city'
                            ],
                            team[
                                'coach'
                            ],
                            player[
                                'name'
                            ],
                            player[
                                'position'
                            ],
                            'Запасной',
                        ),
                    )
            except Exception as e:
                print(
                    f"Error processing team: {team}"
                )
                print(
                    f"Error details: {e}"
                )

    def add_data_to_db(
        self,
    ):
        # Функция для добавления данных в базу данных
        selected_team = (
            self.team_var.get()
        )
        city = self.entry_vars[
            0
        ].get()
        coach = self.entry_vars[
            1
        ].get()
        player_name = self.entry_vars[
            2
        ].get()
        position = self.entry_vars[
            3
        ].get()
        lineup_type = self.entry_vars[
            4
        ].get()

        if (
            lineup_type.lower()
            == 'основной'
        ):
            lineup_key = 'lineup'
        elif (
            lineup_type.lower()
            == 'запасной'
        ):
            lineup_key = 'substitute'
        else:
            print(
                "Неверный тип состава. Используйте 'Основной' или 'Запасной'."
            )
            return

        # Добавляем команду, если выбрано "Новая команда"
        if (
            selected_team
            == "Новая команда"
        ):
            self.teams_collection.insert_one(
                {
                    "name": player_name,  # Assuming the team name is used for the new team
                    "city": city,
                    "coach": coach,
                    lineup_key: [
                        {
                            "name": player_name,
                            "position": position,
                        }
                    ],
                }
            )
        else:
            # Добавляем данные в базу данных
            self.teams_collection.update_one(
                {
                    "name": selected_team
                },
                {
                    "$push": {
                        lineup_key: {
                            "name": player_name,
                            "position": position,
                        }
                    }
                },
            )

        # Перезагружаем данные и обновляем таблицу
        self.load_data()


if (
    __name__
    == "__main__"
):
    key_prefix = "kvilina-"
    root = (
        tk.Tk()
    )
    app = FootballTeamsApp(
        root,
        key_prefix,
    )
    root.mainloop()
