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

window = (
    tk.Tk()
)
window.title(
    "Lab_Redis"
)
window.geometry(
    "1500x600"
)
window.minsize(
    1500,
    600,
)
window.config(
    bg='#abcdef'
)
window.wm_attributes(
    "-topmost",
    1,
)

# client = redis.Redis(host='192.168.112.103', password='student')
client = redis.Redis(
    host='localhost',
    password='student',
    port=1433,
    decode_responses=True,
)


#  Таблица с рейтингом спортсменов
def generate_table_athletes():
    global table_athletes
    table_athletes = ttk.Treeview(
        window,
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
                    "22305-barsukov-"
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

    # Сортируем, чтобы спортсмены шли в порядке убывания их суммарных баллов
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
        window,
        command=table_athletes.yview,
    )
    table_athletes.configure(
        yscrollcommand=scroll_pane_athletes.set
    )

    scroll_pane_athletes.place(
        relx=0.97,
        rely=0.02,
        relwidth=0.01,
        relheight=0.84,
    )

    # Линейка прокрутки для списка (горизонтальная)
    scroll_pane_athletes_horizontal = ttk.Scrollbar(
        window,
        orient=tk.HORIZONTAL,
        command=table_athletes.xview,
    )
    table_athletes.configure(
        xscrollcommand=scroll_pane_athletes_horizontal.set
    )

    scroll_pane_athletes_horizontal.place(
        relx=0.28,
        rely=0.85,
        relwidth=0.70,
        relheight=0.01,
    )

    # Фиксируем таблицу на плоскости
    table_athletes.place(
        relx=0.28,
        rely=0.02,
        relwidth=0.70,
        relheight=0.84,
    )


#  Таблица с оценками по каждому упражнению для конкретного судьи и спортсмена
def generate_table_for_judges(
    event,
):
    if (
        combobox_athletes.get()
        != ""
        and combobox_judges.get()
        != ""
    ):
        global table_for_judges
        table_for_judges = ttk.Treeview(
            window,
            show='headings',
        )
        heads_for_judges = (
            []
        )
        for exercise in exercises_dict:
            heads_for_judges.append(
                exercise
            )
        table_for_judges[
            'columns'
        ] = heads_for_judges

        for header_p in heads_for_judges:
            table_for_judges.heading(
                header_p,
                text=header_p,
                anchor='center',
            )
            table_for_judges.column(
                header_p,
                anchor='center',
            )

        for sportsman in athletes_dict:
            exercises_score = (
                {}
            )
            if combobox_athletes.get() in str(
                sportsman
            ):
                for exercise in exercises_dict:
                    exercises_score[
                        exercise
                    ] = 0
                sum_scores = 0
                for judge in judges_dict:
                    if combobox_judges.get() in str(
                        judge
                    ):
                        for exercise in exercises_dict:
                            find = (
                                "22305-barsukov-"
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
                            else:
                                exercises_score[
                                    exercise
                                ] += int(
                                    client.get(
                                        find
                                    )
                                )
                row = (
                    []
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
                table_for_judges.insert(
                    '',
                    'end',
                    values=row,
                )

        # Линейка прокрутки для списка
        scroll_pane_for_judges = ttk.Scrollbar(
            window,
            command=table_athletes.yview,
        )
        table_for_judges.configure(
            yscrollcommand=scroll_pane_for_judges.set
        )

        scroll_pane_for_judges.place(
            relx=0.97,
            rely=0.88,
            relwidth=0.01,
            relheight=0.10,
        )

        # Линейка прокрутки для списка (горизонтальная)
        scroll_pane_for_judges_horizontal = ttk.Scrollbar(
            window,
            orient=tk.HORIZONTAL,
            command=table_for_judges.xview,
        )
        table_for_judges.configure(
            xscrollcommand=scroll_pane_for_judges_horizontal.set
        )

        scroll_pane_for_judges_horizontal.place(
            relx=0.28,
            rely=0.97,
            relwidth=0.70,
            relheight=0.01,
        )

        # Фиксируем таблицу на плоскости
        table_for_judges.place(
            relx=0.28,
            rely=0.88,
            relwidth=0.70,
            relheight=0.10,
        )
    else:
        if (
            'table_for_judges'
            in locals()
            or 'table_for_judges'
            in globals()
        ):
            table_for_judges.delete(
                *table_for_judges.get_children()
            )


#  Ошибки
def validation():
    def show_error(
        message,
    ):
        error_window = tk.Toplevel(
            window
        )
        error_window.title(
            "Ошибка"
        )
        error_window.attributes(
            '-topmost',
            'true',
        )  # Сделать окно поверх других окон
        tk.Label(
            error_window,
            text=message,
            padx=20,
            pady=20,
        ).pack()
        tk.Button(
            error_window,
            text="OK",
            command=error_window.destroy,
        ).pack()

    if (
        combobox_judges.get()
        == ""
    ):
        show_error(
            "Заполните поле <Cудья>"
        )
        raise Exception

    if (
        combobox_exercises.get()
        == ""
    ):
        show_error(
            "Заполните поле <Упражнение>"
        )
        raise Exception

    if (
        combobox_athletes.get()
        == ""
    ):
        show_error(
            "Заполните поле <Спортсмен>"
        )
        raise Exception

    try:
        score = int(
            spinbox_scores.get()
        )
        if (
            score
            > 10
            or score
            < 0
        ):
            show_error(
                "Оценка должна быть в диапазоне от 0 до 10 включительно"
            )
            raise Exception
    except ValueError:
        show_error(
            "Введите корректное число для оценки"
        )
        raise Exception


#  Сохранение оценки в базу данных
def save():
    validation()
    key1 = (
        ""
    )
    for sportsman in athletes_dict:
        if combobox_athletes.get() in str(
            sportsman
        ):
            key1 = sportsman
    key2 = (
        ""
    )
    for judge in judges_dict:
        if combobox_judges.get() in str(
            judge
        ):
            key2 = judge
    key3 = (
        ""
    )
    for exercise in exercises_dict:
        if combobox_exercises.get() in str(
            exercise
        ):
            key3 = exercise
    print(
        athletes_dict
    )
    key = (
        "22305-barsukov-"
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
        spinbox_scores.get(),
    )
    #  Добавляем сообщение о добавлении значения в канал обновление_таблицы
    client.publish(
        "обновление_таблицы",
        "добавлено_новое_значение",
    )
    # table_athletes.delete(*table_athletes.get_children())
    # generate_table_athletes()
    # if 'table_for_judges' in locals() or 'table_for_judges' in globals():
    #     table_for_judges.delete(*table_for_judges.get_children())
    # generate_table_for_judges(None)


# Функция, которая будет вызываться в отдельном потоке для обработки сообщений в канале "обновление_таблицы"
def run_pubsub():
    for message in (
        pubsub.listen()
    ):
        if (
            message[
                "type"
            ]
            == "message"
        ):
            # Если в канале обновление_таблицы было сообщение, то обновляем таблицу со всеми спортсменами
            #  и таблицу с оценками для конкретного спортсмена и судьи
            table_athletes.delete(
                *table_athletes.get_children()
            )
            generate_table_athletes()
            if (
                'table_for_judges'
                in locals()
                or 'table_for_judges'
                in globals()
            ):
                table_for_judges.delete(
                    *table_for_judges.get_children()
                )
            generate_table_for_judges(
                None
            )


# Надпись "Судья"
judges_label = Label(
    window,
    text="Судья",
    font=(
        "Courier New",
        24,
        "bold",
    ),
    bg="#abcdef",
    fg="black",
)
judges_label.place(
    relx=0.02,
    rely=0.02,
    relwidth=0.24,
    relheight=0.05,
)
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
        "22305-barsukov-judge"
        in str(
            judge
        )
    ):
        judge_ = str(
            judge
        ).replace(
            "22305-barsukov-judge-",
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
# Выпадающий список с судьями
combobox_judges = ttk.Combobox(
    window,
    values=judges,
    width=35,
    state="readonly",
)
combobox_judges.place(
    relx=0.02,
    rely=0.07,
    relwidth=0.24,
    relheight=0.05,
)
combobox_judges.bind(
    "<<ComboboxSelected>>",
    generate_table_for_judges,
)

# Надпись "Упражнение"
exercises_label = Label(
    window,
    text="Упражнение",
    font=(
        "Courier New",
        24,
        "bold",
    ),
    bg="#abcdef",
    fg="black",
)
exercises_label.place(
    relx=0.02,
    rely=0.17,
    relwidth=0.24,
    relheight=0.05,
)
# Получаем список упражнений
exercises_dict = (
    {}
)
exercises = (
    []
)
# Берем только значения, начинающиеся с "22305-barsukov-exercise"
for exercise in client.keys(
    '*'
):
    if (
        "22305-barsukov-exercise"
        in str(
            exercise
        )
    ):
        exercise_ = str(
            exercise
        ).replace(
            "22305-barsukov-exercise-",
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
# Выпадающий список с упражнениями
combobox_exercises = ttk.Combobox(
    window,
    values=exercises,
    width=35,
    state="readonly",
)
combobox_exercises.place(
    relx=0.02,
    rely=0.22,
    relwidth=0.24,
    relheight=0.05,
)

# Надпись "Спортсмен"
athletes_label = Label(
    window,
    text="Спортсмен",
    font=(
        "Courier New",
        24,
        "bold",
    ),
    bg="#abcdef",
    fg="black",
)
athletes_label.place(
    relx=0.02,
    rely=0.32,
    relwidth=0.24,
    relheight=0.05,
)
# Получаем список спортсменов
athletes_dict = (
    {}
)
athletes = (
    []
)
# Берем только значения, начинающиеся с "22305-barsukov-exercise"
for sportsman in client.keys(
    '*'
):
    if "22305-barsukov-sportsman" in str(
        sportsman
    ) and "judge" not in str(
        sportsman
    ):
        sportsman_ = str(
            sportsman
        ).replace(
            "22305-barsukov-sportsman-",
            "",
        )
        # sportsman_ = ''.join(sportsman_[1:])
        # athletes_dict[client.get(sportsman)] = sportsman_.replace("'", '')
        athletes_dict[
            client.get(
                sportsman
            )
        ] = sportsman_
        print(
            client.get(
                sportsman
            )
        )
        athletes.append(
            client.get(
                sportsman
            )
        )
# Выпадающий список со спортсменами
combobox_athletes = ttk.Combobox(
    window,
    values=athletes,
    width=35,
    state="readonly",
)
combobox_athletes.place(
    relx=0.02,
    rely=0.37,
    relwidth=0.24,
    relheight=0.05,
)
combobox_athletes.bind(
    "<<ComboboxSelected>>",
    generate_table_for_judges,
)

# Надпись "Оценка"
scores_label = Label(
    window,
    text="Оценка",
    font=(
        "Courier New",
        24,
        "bold",
    ),
    bg="#abcdef",
    fg="black",
)
scores_label.place(
    relx=0.02,
    rely=0.47,
    relwidth=0.24,
    relheight=0.05,
)
# Вращающийся список
spinbox_scores = ttk.Spinbox(
    window,
    from_=0,
    to=10,
)
# Значение по умолчанию
spinbox_scores.set(
    0
)
spinbox_scores.place(
    relx=0.02,
    rely=0.52,
    relwidth=0.24,
    relheight=0.05,
)

# Кнопка для сохранения оценки
save_button = Button(
    window,
    text="Оценить",
    width=25,
    font=(
        "Courier New",
        20,
        "normal",
    ),
    command=save,
)
save_button.place(
    relx=0.02,
    rely=0.62,
    relwidth=0.24,
    relheight=0.05,
)

# Таблица со спортсменами
generate_table_athletes()

# Подписка на канал "обновление_таблицы"
pubsub = (
    client.pubsub()
)
pubsub.subscribe(
    "обновление_таблицы"
)

# Создание и запуск отдельного потока для подписки на сообщения
pub_thread = threading.Thread(
    target=run_pubsub,
    daemon=True,
)
pub_thread.start()


window.mainloop()
pubsub.unsubscribe(
    "обновление_таблицы"
)
client.close()
