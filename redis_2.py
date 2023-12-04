from tkcalendar import (
    Calendar,
    DateEntry,
)
import redis
from tkinter import *
from tkinter import (
    ttk,
    messagebox,
)
from tkinter import (
    font,
)
import webcolors
import tkinter as tk
import tkinter.messagebox as mb
import threading

# Создаем окно приложения
root = (
    tk.Tk()
)
root.title(
    "Монитор спортивных соревнований"
)
root.configure(
    bg="#F6F2EA"
)  # Задний фон серый
root.geometry(
    "1000x600"
)
client = redis.Redis(
    host='localhost',
    password='student',
    port=6379,
)

# Задаем список спортсменов (ваш список ФИО спортсменов здесь)
# sporters = ["Спортсмен 1", "Спортсмен 2", "Спортсмен 3", "Спортсмен 4"]

# Создаем список судей (ваш список судей здесь)
# judges = ["Судья 1", "Судья 2", "Судья 3", "Судья 4"]

# Задаем список упражнений (ваш список упражнений здесь)
# exercises = ["Упражнение 1", "Упражнение 2", "Упражнение 3", "Упражнение 4"]

# Получаем список cудей
judges_dict = (
    {}
)
judges = (
    []
)
# Берем только значения, начинающиеся с "22305-barsukov-judge"
for (
    judge
) in client.keys(
    '*'
):
    if (
        "22305-kvilina-judge"
        in str(
            judge
        )
    ):
        judge_ = str(
            judge
        ).replace(
            "22305-kvilina-judge-",
            "",
        )
        # judge_ = ''.join(judge_[1:])
        # judges_dict[client.get(judge)] = judge_.replace("'", '')
        judges_dict[
            client.get(
                judge
            )
        ] = judge_
        judges.append(
            client.get(
                judge
            )
        )
# Создаем Combobox для выбора судьи
judge_label = Label(
    root,
    text="Судья",
    bg="#A68E74",
)
judge_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
)
judge_combobox = ttk.Combobox(
    root,
    values=judges,
)
judge_combobox.grid(
    row=1,
    column=0,
    padx=10,
    pady=10,
)
judge_combobox.set(
    judges[
        0
    ]
)


# Задаем шрифт для всего текста
global_font = font.nametofont(
    "TkDefaultFont"
)
global_font.configure(
    family="Courier New",
    size=9,
)
root.option_add(
    "*Font",
    global_font,
)

# Метка "Выбрать баллы"
font_size_label = tk.Label(
    root,
    text="Выбрать баллы:",
    bg="#A68E74",
)
font_size_label.config(
    font=global_font
)
font_size_label.grid(
    row=0,
    column=1,
    padx=10,
    pady=10,
)
# Создаем Combobox для выбора баллов
font_size_combobox = ttk.Combobox(
    root,
    values=[
        str(
            i
        )
        for i in range(
            1,
            11,
        )
    ],
)
font_size_combobox.grid(
    row=1,
    column=1,
    padx=10,
    pady=10,
)
font_size_combobox.set(
    "1"
)


# Получаем список спортсменов
athletes_dict = (
    {}
)
athletes = (
    []
)
for sportsman in client.keys(
    '*'
):
    if "22305-kvilina-sportsman" in str(
        sportsman
    ) and "judge" not in str(
        sportsman
    ):
        sportsman_ = str(
            sportsman
        ).replace(
            "22305-kvilina-sportsman-",
            "",
        )
        # sportsman_ = ''.join(sportsman_[1:])
        # athletes_dict[client.get(sportsman)] = sportsman_.replace("'", '')
        athletes_dict[
            client.get(
                sportsman
            )
        ] = sportsman_
        athletes.append(
            client.get(
                sportsman
            )
        )

sportsman_label = Label(
    root,
    text="Спортсмен",
    bg="#A68E74",
)
sportsman_label.grid(
    row=0,
    column=3,
    padx=10,
    pady=10,
)
sporter_combobox = ttk.Combobox(
    root,
    values=athletes,
)
sporter_combobox.grid(
    row=1,
    column=3,
    padx=10,
    pady=10,
)
sporter_combobox.set(
    athletes[
        0
    ]
)


# Получаем список упражнений
exercises_dict = (
    {}
)
exercises = (
    []
)
for exercise in client.keys(
    '*'
):
    if "22305-kvilina-exercise" in str(
        exercise
    ) and (
        "judge"
        not in str(
            exercise
        )
    ):
        exercise_ = str(
            exercise
        ).replace(
            "22305-kivlina-exercise-",
            "",
        )
        # exercise_ = ''.join(exercise_[1:])
        # exercises_dict[client.get(exercise)] = exercise_.replace("'", '')
        exercises_dict[
            client.get(
                exercise
            )
        ] = exercise_
        exercises.append(
            client.get(
                exercise
            )
        )
# Создаем Combobox для выбора упражнений
exercise_label = Label(
    root,
    text="Упражнения",
    bg="#A68E74",
)
exercise_label.grid(
    row=0,
    column=5,
    padx=10,
    pady=10,
)
exercise_combobox = ttk.Combobox(
    root,
    values=exercises,
)
exercise_combobox.grid(
    row=1,
    column=5,
    padx=10,
    pady=10,
)
exercise_combobox.set(
    exercises[
        0
    ]
)

# Таблица со спортсменами

# Функция для добавления баллов к спортсмену
# def add_scores():
#     selected_judge = judge_combobox.get()
#     selected_score = int(font_size_combobox.get())
#     selected_sporter = sporter_combobox.get()
#     selected_exercise = exercise_combobox.get()
#
#     # Находим спортсмена в таблице и обновляем его баллы
#     for item in tree.get_children():
#         values = tree.item(item, "values")
#         if values[0] == selected_sporter:
#             # Обновляем баллы
#             for i in range(1, len(values) - 1):
#                 if values[i] == selected_exercise:
#                     # Найдено выбранное упражнение, обновляем баллы для судьи
#                     values[i + 1] = str(int(values[i + 1]) + selected_score)
#                     tree.item(item, values=values)
#                     break


#  Таблица с рейтингом спортсменов
def generate_table_athletes():
    global table_athletes
    table_athletes = ttk.Treeview(
        root,
        show='headings',
    )
    heads_athletes = (
        []
    )
    heads_athletes.append(
        'Sportsman'
    )
    for exercise in exercises_dict:
        heads_athletes.append(
            exercise
        )
    heads_athletes.append(
        'Sum'
    )
    table_athletes[
        'columns'
    ] = heads_athletes

    for header_p in heads_athletes:
        table_athletes.heading(
            header_p,
            text=header_p,
            anchor='center',
        )
        table_athletes.column(
            header_p,
            anchor='center',
        )

    rows = (
        []
    )
    for sportsman in athletes_dict:
        exercises_score = (
            {}
        )
        for exercise in exercises_dict:
            exercises_score[
                exercise
            ] = 0
        sum_scores = 0
        for judge in judges_dict:
            for exercise in exercises_dict:
                find = (
                    "22305-kvilina-"
                    + athletes_dict[
                        sportsman
                    ]
                    + "-"
                    + judges_dict[
                        judge
                    ]
                    + "-"
                    + exercises_dict[
                        exercise
                    ]
                )
                element = client.get(
                    find
                )
                if (
                    element
                    == None
                ):
                    exercises_score[
                        exercise
                    ] += 0
                    sum_scores += 0
                else:
                    exercises_score[
                        exercise
                    ] += int(
                        client.get(
                            find
                        )
                    )
                    sum_scores += exercises_score[
                        exercise
                    ]
        row = (
            []
        )
        # sportsman = ''.join(str(sportsman)[1:])
        # row.append(sportsman.replace("'", ''))
        row.append(
            sportsman
        )
        for exercise in exercises_dict:
            row.append(
                exercises_score[
                    exercise
                ]
            )
        row.append(
            sum_scores
        )
        rows.append(
            row
        )
    rows = sorted(
        rows,
        key=lambda x: x[
            len(
                exercises_dict
            )
            + 1
        ],
        reverse=True,
    )

    for row in rows:
        table_athletes.insert(
            '',
            'end',
            values=row,
        )

    # Линейка прокрутки для списка
    scroll_pane_athletes = ttk.Scrollbar(
        root,
        command=table_athletes.yview,
    )
    table_athletes.configure(
        yscrollcommand=scroll_pane_athletes.set
    )

    scroll_pane_athletes.place(
        relx=0.82,
        rely=0.14,
        relwidth=0.01,
        relheight=0.84,
    )

    # Линейка прокрутки для списка (горизонтальная)
    scroll_pane_athletes_horizontal = ttk.Scrollbar(
        root,
        orient=tk.HORIZONTAL,
        command=table_athletes.xview,
    )
    table_athletes.configure(
        xscrollcommand=scroll_pane_athletes_horizontal.set
    )

    scroll_pane_athletes_horizontal.place(
        relx=0.02,
        rely=0.97,
        relwidth=0.80,
        relheight=0.01,
    )

    # Фиксируем таблицу на плоскости
    table_athletes.place(
        relx=0.02,
        rely=0.14,
        relwidth=0.80,
        relheight=0.84,
    )


#  Сохранение оценки в базу данных
def save():
    key1 = (
        ""
    )
    for sportsman in athletes_dict:
        if sporter_combobox.get() in str(
            sportsman
        ):
            key1 = sportsman
    key2 = (
        ""
    )
    for judge in judges_dict:
        if judge_combobox.get() in str(
            judge
        ):
            key2 = judge
    key3 = (
        ""
    )
    for exercise in exercises_dict:
        if exercise_combobox.get() in str(
            exercise
        ):
            key3 = exercise
    print(
        key1
    )
    print(
        key2
    )
    print(
        key3
    )
    key = (
        "22305-kvilina-"
        + athletes_dict[
            key1
        ]
        + "-"
        + judges_dict[
            key2
        ]
        + "-"
        + exercises_dict[
            key3
        ]
    )
    client.set(
        key,
        font_size_combobox.get(),
    )
    #  Добавляем сообщение о добавлении значения в канал обновление_таблицы
    table_athletes.delete(
        *table_athletes.get_children()
    )
    generate_table_athletes()


# Кнопка для сохранения баллов
add_button = ttk.Button(
    root,
    text="Сохранить баллы",
    command=save,
)
add_button.config(
    style="TButton"
)
add_button.grid(
    row=0,
    column=len(
        judges
    )
    + 6,
    padx=10,
    pady=10,
)

# Вызываем функцию для создания таблицы рейтинга спортсменов
generate_table_athletes()


root.mainloop()
