import tkinter as tk
from tkinter import (
    ttk,
)
from tkinter import (
    font,
)
from tkinter import (
    colorchooser,
)
import redis
import tkinter.messagebox as mb

client = redis.Redis(
    host='localhost',
    password='student',
    port=6379,
)


def save():
    user_ = (
        "22305-kvilina-"
        + user_choice.get()
    )
    old_settings = str(
        client.get(
            user_
        )
    ).split(
        ', '
    )
    # Проверяем ввели ли значение в поле шрифта: да - берем новый шрифт, нет - берем старый
    if (
        font_size_combobox.get()
        == ""
    ):
        old_settings[
            0
        ] = ''.join(
            old_settings[
                0
            ][
                1:
            ]
        )
        new_font = old_settings[
            0
        ].replace(
            "'",
            "",
        )
    else:
        new_font = (
            font_size_combobox.get()
        )
    # Проверяем ввели ли значение в поле начертания шрифта: да - берем новый тип начертания, нет - берем старый
    if (
        font_style_combobox.get()
        == ""
    ):
        new_type = old_settings[
            2
        ]
    else:
        new_type = (
            font_style_combobox.get()
        )
    # Проверяем ввели ли значение в поле цвета шрифта: да - берем новый цвет, нет - берем старый
    if (
        font_color_entry.get()
        == ""
    ):
        new_color = old_settings[
            3
        ].replace(
            "'",
            "",
        )
    else:
        new_color = (
            font_color_entry.get()
        )
    # Цвет не проверяем, т.к. там есть значение по умолчанию (то есть поле всегда не пустое)
    settings = (
        new_font
        + ", "
        + font_size_combobox.get()
        + ", "
        + new_type
        + ", "
        + new_color
    )
    client.set(
        user_,
        settings,
    )


def choose_font_color():
    color = colorchooser.askcolor()[
        1
    ]
    font_color_entry.delete(
        0,
        tk.END,
    )
    font_color_entry.insert(
        0,
        color,
    )


# Создаем главное окно
root = (
    tk.Tk()
)
root.title(
    "Настройки текстового сообщения"
)

# Устанавливаем красный фон
root.configure(
    bg='#F6F2EA'
)

# Устанавливаем размер окна 800x600
root.geometry(
    "800x600"
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

# Надпись "Выберите Пользователя"
user_choice_label = tk.Label(
    root,
    text="Выберите пользователя:",
)
user_choice_label.pack()

# Получаем список пользователей
users_list = (
    []
)
for (
    user
) in client.keys(
    '*'
):
    if (
        "22305-kvilina-nastroika"
        in str(
            user
        )
    ):
        user_replace = str(
            user
        ).replace(
            "22305-kvilina-",
            "",
        )
        user_replace = ''.join(
            user_replace[
                1:
            ]
        )
        users_list.append(
            user_replace.replace(
                "'",
                '',
            )
        )

user_choice = ttk.Combobox(
    root,
    values=users_list,
)
user_choice.pack()


def validation_person():
    if (
        user_choice.get()
        == ""
    ):
        error = "Выберите пользователя"
        mb.showwarning(
            "Ошибка",
            error,
        )
        raise Exception


# Надпись "Выберите шрифт"
font_name_label = tk.Label(
    root,
    text="Название шрифта:",
)
font_name_label.pack()

font_name_combobox = ttk.Combobox(
    root,
    values=font.families(),
)
font_name_combobox.pack()

font_size_label = tk.Label(
    root,
    text="Размер шрифта:",
)
font_size_label.pack()

font_size_combobox = ttk.Combobox(
    root,
    values=[
        str(
            i
        )
        for i in range(
            8,
            73,
        )
    ],
)
font_size_combobox.pack()

font_color_label = tk.Label(
    root,
    text="Цвет шрифта:",
)
font_color_label.pack()

font_color_entry = tk.Entry(
    root
)
font_color_entry.pack()

choose_color_button = tk.Button(
    root,
    text="Выбрать цвет",
    command=choose_font_color,
    bg="#A68E74",
    fg="white",
)
choose_color_button.pack()

font_style_label = tk.Label(
    root,
    text="Начертание:",
)
font_style_label.pack()

font_style_combobox = ttk.Combobox(
    root,
    values=[
        "normal",
        "bold",
        "italic",
    ],
)
font_style_combobox.pack()

save_button = tk.Button(
    root,
    text="Сохранить настройки",
    command=save,
    bg="#A68E74",
    fg="white",
)
save_button.pack()

text_entry_label = tk.Label(
    root,
    text="Введите текст:",
)
text_entry_label.pack()

text_entry = tk.Entry(
    root
)
text_entry.pack()

label_text = (
    tk.StringVar()
)
label = tk.Label(
    root,
    textvariable=label_text,
    font=(
        "Courier New",
        20,
        "normal",
    ),
    fg="black",
)
label.pack()


def update_label_text():
    # Получаем выбранные настройки пользователя
    selected_user = (
        user_choice.get()
    )

    # Получаем настройки шрифта
    font_name = (
        font_name_combobox.get()
    )
    font_size = int(
        font_size_combobox.get()
    )
    font_color = (
        font_color_entry.get()
    )
    font_style = (
        font_style_combobox.get()
    )

    # Обновляем настройки шрифта для надписи
    label.config(
        font=(
            font_name,
            font_size,
            font_style,
        ),
        fg=font_color,
    )
    label_text.set(
        text_entry.get()
    )


# Обработка изменения текста в поле ввода
text_entry.bind(
    "<KeyRelease>",
    lambda event: update_label_text(),
)

root.mainloop()
