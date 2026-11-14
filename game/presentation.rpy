define bucks = Character("Ларри Бакс", who_color="#e4c49b", voice_tag="bucks")
define brando = Character("Молли Брандо", who_color="#e7afbc", voice_tag="brando")
define more = Character("Александр Морэ", who_color="#a6bdcf", voice_tag="more")
define secretary = Character("Секретарь · внутренняя связь", who_color="#a9c9bf", voice_tag="secretary")
define narrator = Character(None, what_color="#d1c8bd")

default active_speaker = ""
default bucks_mood = "neutral"
default brando_mood = "neutral"
default more_mood = "neutral"
default visible_bucks = True
default visible_more = False
default chapter = "КАДРОВОЕ РЕШЕНИЕ"

image bg office = Transform("images/office.png", size=(1920, 1080))

# Crop the sheet at runtime, preserving the original generated alpha and pixels.
init python:
    for person, expressions in {
        "bucks": ("neutral", "serious", "knowing"),
        "brando": ("neutral", "angry", "tired"),
        "more": ("neutral", "firm", "uneasy"),
    }.items():
        sheet = "images/" + person + ".png"
        width, height = renpy.image_size(sheet)
        boundaries = [round(width * i / 3) for i in range(4)]
        for index, expression in enumerate(expressions):
            crop = Crop((boundaries[index], 0, boundaries[index+1]-boundaries[index], height), sheet)
            renpy.image(person + " " + expression, Transform(crop, ysize=870, fit="contain"))

screen cast_stage():
    zorder -10
    if visible_bucks:
        add "bucks [bucks_mood]":
            xpos 0.17 xanchor 0.5 ypos 935 yanchor 1.0
            matrixcolor BrightnessMatrix(0.0 if active_speaker == "bucks" else -0.14)
    add "brando [brando_mood]":
        xpos 0.50 xanchor 0.5 ypos 935 yanchor 1.0
        matrixcolor BrightnessMatrix(0.0 if active_speaker == "brando" else -0.14)
    if visible_more:
        add "more [more_mood]":
            xpos 0.83 xanchor 0.5 ypos 935 yanchor 1.0
            matrixcolor BrightnessMatrix(0.0 if active_speaker == "more" else -0.14)

screen scene_header():
    zorder 10
    frame:
        background Solid("#0b0c10c9")
        xfill True ysize 58 padding (52, 0)
        hbox:
            yalign 0.5 spacing 22
            text "УВС—19F" size 20 bold True color "#d3b28c"
            text "/" size 20 color "#6f6761"
            text "КАБИНЕТ ДИРЕКТОРА" size 17 color "#c5bdb2"
        text chapter xalign 1.0 yalign 0.5 size 17 color "#b7a38e"

screen say(who, what):
    style_prefix "novel"
    window:
        id "window"
        background Solid("#101014f4")
        xfill True yalign 1.0 ysize 344
        add Solid("#8e6a47") xsize 1920 ysize 2
        vbox:
            xpos 100 ypos 30 xsize 1720 spacing 15
            if who:
                text who id "who" size 27 bold True
            else:
                text "ЗАПИСЬ РАЗГОВОРА" size 17 color "#a38e77" kerning 2
            text what id "what" size 30 line_spacing 7 color "#eee7dd" layout "greedy"
        text "▸" xalign 0.96 yalign 0.83 size 22 color "#bba180"

screen quick_menu():
    zorder 100
    if quick_menu:
        hbox:
            xalign 0.5 yalign 0.992 spacing 32
            style_prefix "novel_quick"
            textbutton "НАЗАД" action Rollback()
            textbutton "ИСТОРИЯ" action ShowMenu("history")
            textbutton "ГОЛОС ↻" action VoiceReplay()
            textbutton "АВТО" action Preference("auto-forward", "toggle")
            textbutton "СОХРАНИТЬ" action ShowMenu("save")
            textbutton "ЗАГРУЗИТЬ" action ShowMenu("load")
            textbutton "НАСТРОЙКИ" action ShowMenu("preferences")

screen main_menu():
    tag menu
    add "bg office"
    add Solid("#090b10bb")
    add "more neutral" xpos 0.87 xanchor 0.5 ypos 1100 yanchor 1.0 alpha 0.5
    add "brando neutral" xpos 0.68 xanchor 0.5 ypos 1130 yanchor 1.0
    add "bucks neutral" xpos 0.51 xanchor 0.5 ypos 1195 yanchor 1.0
    add Solid("#0c0d14ee") xpos 0 ypos 0 xsize 820 ysize 1080
    vbox:
        xpos 95 ypos 78 spacing 28
        text "УВС—19F  /  СЛУЖЕБНЫЙ АРХИВ" size 20 color "#cfb28c" kerning 2
        null height 47
        text "ПРИЧИНА\nОТКАЗА" font "DejaVuSans-Bold.ttf" size 92 line_spacing -14 color "#f1e8dd"
        text "Один кабинет. Три человека.\nВопрос, на который никто не хочет отвечать." size 25 color "#beb4aa" line_spacing 7
        null height 30
        vbox:
            spacing 7
            style_prefix "archive_menu"
            textbutton "Начать разговор" action Start() default_focus True
            textbutton "Загрузить запись" action ShowMenu("load")
            textbutton "Настройки" action ShowMenu("preferences")
            textbutton "Об игре" action ShowMenu("about")
            textbutton "Выход" action Quit(confirm=True)
    text "ЛИНЕЙНАЯ ВИЗУАЛЬНАЯ НОВЕЛЛА" xpos 100 ypos 980 size 16 kerning 2 color "#9a8e80"
    text "v[config.version]" xpos 100 ypos 1012 size 16 color "#796f66"

screen navigation():
    vbox:
        style_prefix "navigation"
        xpos gui.navigation_xpos yalign 0.5 spacing 14
        if not main_menu:
            textbutton "Продолжить" action Return()
            textbutton "История" action ShowMenu("history")
            textbutton "Сохранить" action ShowMenu("save")
        textbutton "Загрузить" action ShowMenu("load")
        textbutton "Настройки" action ShowMenu("preferences")
        textbutton "Об игре" action ShowMenu("about")
        if not main_menu:
            textbutton "Главное меню" action MainMenu()
        textbutton "Выход" action Quit(confirm=True)

screen about():
    tag menu
    use game_menu("Об игре", scroll="viewport"):
        vbox:
            spacing 22
            text "УВС-19F: Причина отказа" size 38 bold True
            text "Версия [config.version]" size 23
            text "Линейная постановка полного диалога о назначении начальника ОВС. Все реплики и ремарки перенесены из предоставленного автором текста."
            text "Персонажи: Ларри Бакс, Молли Брандо, Александр Морэ. Голос секретаря звучит по внутренней связи."
            text "Голоса синтезированы ИИ (Microsoft). Иллюстрации созданы ИИ по авторскому референсу."
            text "Управление: щелчок, пробел или Enter — дальше; колесо вверх — назад; Esc — меню; H — скрыть текст; F — полный экран."
            text "Режим «Авто» дожидается окончания озвучки. Громкость речи, музыки и эффектов настраивается раздельно."
            text "История содержит ненормативную лексику."
            text "Движок Ren’Py [renpy.version_only].\n[renpy.license!t]" size 19

screen end_card():
    modal True
    add Solid("#101014")
    vbox:
        xalign 0.5 yalign 0.5 spacing 30
        text "УВС—19F / АРХИВ" xalign 0.5 size 20 color "#be9f79" kerning 3
        text "КОНЕЦ ЗАПИСИ" xalign 0.5 size 62 bold True color "#eee5d9"
        text "«Ты ведь никогда не умел просто уйти»." xalign 0.5 size 28 color "#b7aca0"
        null height 35
        textbutton "Вернуться в главное меню" action Return() xalign 0.5 style "archive_menu_button" text_style "archive_menu_button_text" default_focus True

style novel_quick_button:
    padding (5, 9)
    background None
style novel_quick_button_text:
    size 16 color "#b0a89d" hover_color "#e5c49e" selected_color "#e5c49e"
style archive_menu_button:
    padding (20, 13)
    xminimum 490
    background None
    hover_background Solid("#b3957026")
style archive_menu_button_text:
    size 29 color "#d9d1c7" hover_color "#f2cfa0" selected_color "#f2cfa0"
    font "DejaVuSans.ttf"

init 5 python:
    gui.accent_color = "#c6a77d"
    gui.hover_color = "#f0cfa0"
    gui.idle_color = "#b9b0a5"
    gui.selected_color = "#eee5d9"
    gui.text_color = "#eee5d9"
    gui.interface_text_color = "#ded6cc"
    gui.main_menu_background = "images/office.png"
    gui.game_menu_background = Solid("#121217f9")

style navigation_button_text:
    size 26
    hover_color "#f0cfa0"
style game_menu_label_text:
    color "#c6a77d"
style history_text:
    size 28
style history_name_text:
    size 24

# Character defaults use the stock say styles; reset their fixed offsets inside
# the custom text container so long Russian lines use its full width.
style say_dialogue:
    xpos 0
    ypos 0
    xsize 1720
    size 30
    line_spacing 7
style say_label:
    xpos 0
    ypos 0
    size 27
