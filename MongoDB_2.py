import tkinter as tk
from tkinter import (
    ttk,
)
from pymongo import (
    MongoClient,
)
from tkinter import (
    font,
)


class MatchesApp:
    def __init__(
        self,
        root,
        key_prefix,
    ):
        self.root = root
        root.geometry(
            "1000x600"
        )
        root.configure(
            bg='#F6F2EA'
        )
        self.key_prefix = key_prefix
        self.root.title(
            "Футбольные матчи"
        )

        # Устанавливаем шрифт и стиль для всего текста на окне
        global_font = font.nametofont(
            "TkDefaultFont"
        )
        global_font.configure(
            size=12,
            family="Courier New",
        )
        root.option_add(
            "*Font",
            global_font,
        )

        # Подключение к MongoDB
        self.client = MongoClient(
            'localhost',
            27017,
        )
        self.db = self.client[
            '22305'
        ]
        self.matches_collection = self.db[
            key_prefix
            + "matches"
        ]

        # Кнопка для добавления данных
        add_button = tk.Button(
            root,
            text="Добавить",
            command=self.add_data_to_db,
        )
        add_button.pack()

        # Создаем таблицу
        columns = [
            "Дата проведения",
            "Хозяева",
            "Гости",
            "Счет",
            "Желтые карточки",
            "Красные карточки",
            "Мячи",
            "Пенальти",
            "Удары по воротам",
        ]
        self.tree = ttk.Treeview(
            root,
            columns=columns,
            show="headings",
        )

        # Configure the scrollbar
        scrollbar = ttk.Scrollbar(
            root,
            orient="vertical",
            command=self.tree.yview,
        )
        scrollbar.pack(
            side="right",
            fill="y",
        )
        self.tree.configure(
            yscrollcommand=scrollbar.set
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

        # Привязываем функцию к событию (выбор ячейки) для отображения данных по карточкам и голам
        self.tree.bind(
            "<ButtonRelease-1>",
            self.show_details,
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

        matches = (
            self.matches_collection.find()
        )
        for match in matches:
            yellow_cards_count = sum(
                1
                for card in match[
                    'fouls'
                ]
                if card[
                    'card'
                ]
                == 'yellow'
            )
            red_cards_count = sum(
                1
                for card in match[
                    'fouls'
                ]
                if card[
                    'card'
                ]
                == 'red'
            )
            goals_count = len(
                match[
                    'goals'
                ]
            )
            penalties_count = len(
                match[
                    'penalty'
                ]
            )

            self.tree.insert(
                "",
                "end",
                values=(
                    match[
                        'date'
                    ],
                    match[
                        'home team'
                    ],
                    match[
                        'away team'
                    ],
                    match[
                        'score'
                    ],
                    yellow_cards_count,
                    red_cards_count,
                    goals_count,
                    penalties_count,
                    match[
                        'home kicks'
                    ],
                    match[
                        'away kicks'
                    ],
                ),
            )

    def add_data_to_db(
        self,
    ):
        # Функция для добавления данных в базу данных
        date = self.entry_vars[
            0
        ].get()
        home_team = self.entry_vars[
            1
        ].get()
        away_team = self.entry_vars[
            2
        ].get()
        score = self.entry_vars[
            3
        ].get()
        yellow_cards_count = self.entry_vars[
            4
        ].get()
        red_cards_count = self.entry_vars[
            5
        ].get()
        goals_count = self.entry_vars[
            6
        ].get()
        penalties_count = self.entry_vars[
            7
        ].get()
        home_kicks = self.entry_vars[
            8
        ].get()
        away_kicks = self.entry_vars[
            9
        ].get()

        # Преобразуем данные к необходимому формату
        yellow_cards_list = [
            {
                "card": "yellow"
            }
            for _ in range(
                int(
                    yellow_cards_count
                )
            )
        ]
        red_cards_list = [
            {
                "card": "red"
            }
            for _ in range(
                int(
                    red_cards_count
                )
            )
        ]
        goals_list = [
            {
                "position": "Слева, в 20 метрах от ворот",
                "minute": "15",
                "author": "Mohamed Salah",
                "assist": "Jordan Henderson",
            }
            for _ in range(
                int(
                    goals_count
                )
            )
        ]
        penalties_list = [
            {
                "minute": "70",
                "whose fault": "Marcus Rashford",
                "converted": False,
            }
            for _ in range(
                int(
                    penalties_count
                )
            )
        ]

        # Добавляем данные в базу данных
        self.matches_collection.insert_one(
            {
                "date": date,
                "home team": home_team,
                "away team": away_team,
                "score": score,
                "fouls": yellow_cards_list
                + red_cards_list,
                "goals": goals_list,
                "penalty": penalties_list,
                "home kicks": home_kicks,
                "away kicks": away_kicks,
            }
        )

        # Перезагружаем данные и обновляем таблицу
        self.load_data()

    def show_details(
        self,
        event,
    ):
        # Получаем информацию о ячейке
        item_id = self.tree.identify_row(
            event.y
        )
        column_id = self.tree.identify_column(
            event.x
        )

        # Проверяем, что клик был в столбце "Желтые карточки", "Красные карточки", "Мячи", "Пенальти"
        if (
            column_id
            in (
                "#5",
                "#6",
                "#7",
                "#8",
            )
        ):
            # Определяем тип данных (желтые карточки, красные карточки, голы или пенальти)
            data_type = None
            if (
                column_id
                == "#5"
            ):
                data_type = 'yellow_card'
            elif (
                column_id
                == "#6"
            ):
                data_type = 'red_card'
            elif (
                column_id
                == "#7"
            ):
                data_type = 'goal'
            elif (
                column_id
                == "#8"
            ):
                data_type = 'penalty'

            # Получаем данные по соответствующему типу
            details = self.get_details(
                item_id,
                data_type,
            )

            # Определяем заголовок окна
            window_title = "Детали"
            if (
                data_type
                == 'yellow_card'
            ):
                window_title += " по желтым карточкам"
            elif (
                data_type
                == 'red_card'
            ):
                window_title += " по красным карточкам"
            elif (
                data_type
                == 'goal'
            ):
                window_title += " по голам"
            elif (
                data_type
                == 'penalty'
            ):
                window_title += " по пенальти"

            # Создаем новое окно для отображения данных
            details_window = tk.Toplevel(
                self.root
            )
            details_window.title(
                window_title
            )
            details_window.geometry(
                "1000x300"
            )

            # Создаем Treeview для отображения данных
            if (
                data_type
                == 'yellow_card'
                or data_type
                == 'red_card'
            ):
                columns = (
                    "ФИО",
                    "Минута",
                    "Причина",
                )
            elif (
                data_type
                == 'goal'
            ):
                columns = (
                    "Позиция",
                    "Минута",
                    "Автор",
                    "Ассистент",
                )
            elif (
                data_type
                == 'penalty'
            ):
                columns = (
                    "Минута",
                    "Кто забил",
                    "Попадание",
                )

            # Создаем Treeview для отображения данных
            details_tree = ttk.Treeview(
                details_window,
                columns=columns,
                show="headings",
            )
            for (
                col,
                width,
            ) in zip(
                columns,
                [
                    200,
                    200,
                    200,
                    200,
                ],
            ):  # Adjust the widths as needed
                details_tree.heading(
                    col,
                    text=col,
                )
                details_tree.column(
                    col,
                    width=width,
                    anchor=tk.CENTER,
                )

            details_tree.pack()
            # Вставляем данные в таблицу
            for detail in details:
                if (
                    data_type
                    == 'yellow_card'
                    or data_type
                    == 'red_card'
                ):
                    details_tree.insert(
                        "",
                        "end",
                        values=(
                            detail.get(
                                'player',
                                '',
                            ),
                            detail.get(
                                'minute',
                                '',
                            ),
                            detail.get(
                                'reason',
                                '',
                            ),
                        ),
                    )
                elif (
                    data_type
                    == 'goal'
                ):
                    details_tree.insert(
                        "",
                        "end",
                        values=(
                            detail.get(
                                'position',
                                '',
                            ),
                            detail.get(
                                'minute',
                                '',
                            ),
                            detail.get(
                                'author',
                                '',
                            ),
                            detail.get(
                                'assist',
                                '',
                            ),
                        ),
                    )
                elif (
                    data_type
                    == 'penalty'
                ):
                    details_tree.insert(
                        "",
                        "end",
                        values=(
                            detail.get(
                                'minute',
                                '',
                            ),
                            detail.get(
                                'whose fault',
                                '',
                            ),
                            detail.get(
                                'converted',
                                '',
                            ),
                        ),
                    )

    def get_details(
        self,
        item_id,
        data_type,
    ):
        # Получаем данные по соответствующему типу
        item_values = self.tree.item(
            item_id,
            "values",
        )
        if item_values:
            if (
                data_type
                == 'yellow_card'
            ):
                card_count = int(
                    item_values[
                        4
                    ]
                )
                card_details = (
                    []
                )
                matches = (
                    self.matches_collection.find()
                )
                for match in matches:
                    cards = [
                        card
                        for card in match[
                            'fouls'
                        ]
                        if card[
                            'card'
                        ]
                        == 'yellow'
                    ]
                    card_details.extend(
                        cards
                    )
                    if (
                        len(
                            card_details
                        )
                        >= card_count
                    ):
                        break
                return card_details
            elif (
                data_type
                == 'red_card'
            ):
                card_count = int(
                    item_values[
                        5
                    ]
                )
                card_details = (
                    []
                )
                matches = (
                    self.matches_collection.find()
                )
                for match in matches:
                    cards = [
                        card
                        for card in match[
                            'fouls'
                        ]
                        if card[
                            'card'
                        ]
                        == 'red'
                    ]
                    card_details.extend(
                        cards
                    )
                    if (
                        len(
                            card_details
                        )
                        >= card_count
                    ):
                        break
                return card_details
            elif (
                data_type
                == 'goal'
            ):
                goal_count = int(
                    item_values[
                        6
                    ]
                )
                goal_details = (
                    []
                )
                matches = (
                    self.matches_collection.find()
                )
                for match in matches:
                    goals = match[
                        'goals'
                    ]
                    goal_details.extend(
                        goals
                    )
                    if (
                        len(
                            goal_details
                        )
                        >= goal_count
                    ):
                        break
                return goal_details
            elif (
                data_type
                == 'penalty'
            ):
                penalty_count = int(
                    item_values[
                        7
                    ]
                )
                penalty_details = (
                    []
                )
                matches = (
                    self.matches_collection.find()
                )
                for match in matches:
                    penalties = match[
                        'penalty'
                    ]
                    penalty_details.extend(
                        penalties
                    )
                    if (
                        len(
                            penalty_details
                        )
                        >= penalty_count
                    ):
                        break
                return penalty_details
        return (
            []
        )


if (
    __name__
    == "__main__"
):
    key_prefix = "kvilina-"
    root = (
        tk.Tk()
    )
    app = MatchesApp(
        root,
        key_prefix,
    )
    root.mainloop()
