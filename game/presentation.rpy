define bucks = Character("Ларри Бакс", who_color="#e4c49b", voice_tag="bucks")
define brando = Character("Молли Брандо", who_color="#e7afbc", voice_tag="brando")
define more = Character("Александр Морэ", who_color="#a6bdcf", voice_tag="more")
define secretary = Character("Секретарь · внутренняя связь", who_color="#a9c9bf", voice_tag="secretary")
define fazen = Character("Джейкоб Фазен", who_color="#c9b9cf")
define bolderik = Character("Ирвин Болдерик", who_color="#a6bdcf")
define narrator = Character(None, what_color="#d1c8bd")

default active_speaker = ""
default bucks_mood = "neutral"
default brando_mood = "neutral"
default more_mood = "neutral"
default visible_bucks = True
default visible_more = False
default chapter = "КАДРОВОЕ РЕШЕНИЕ"
default tribunal_brando_present = False
default tribunal_in_corridor = False

image bg office = Transform("images/office-scp-v2.png", size=(1920, 1080))

image bucks mog = Transform("images/bucks-mog.png", ysize=870, fit="contain")
image brando mog = Transform("images/brando-mog.png", ysize=870, fit="contain")
image fazen neutral = Transform("images/fazen.png", ysize=820, fit="contain")
image bolderik neutral = Transform("images/bolderik.png", ysize=850, fit="contain")
image fazen mog = Transform("images/fazen-mog.png", ysize=820, fit="contain")
image bolderik mog = Transform("images/bolderik-mog.png", ysize=850, fit="contain")

# Crop the sheet at runtime, preserving the original generated alpha and pixels.
init python:
    for person, expressions in {
        "bucks": ("neutral", "serious", "knowing"),
        "brando": ("neutral", "angry", "tired"),
        "more": ("neutral", "firm", "uneasy", "mog"),
    }.items():
        sheet = "images/more-v2.png" if person == "more" else "images/" + person + ".png"
        width, height = renpy.image_size(sheet)
        columns = len(expressions)
        boundaries = [round(width * i / columns) for i in range(columns + 1)]
        for index, expression in enumerate(expressions):
            crop = Crop((boundaries[index], 0, boundaries[index+1]-boundaries[index], height), sheet)
            renpy.image(person + " " + expression, Transform(crop, ysize=870, fit="contain"))

transform mog_pose_pop:
    subpixel True
    zoom 0.99
    easeout 0.14 zoom 1.035
    ease 0.20 zoom 1.0

screen cast_stage(tribunal=False):
    zorder -10
    if mog_ready:
        timer mog_delay action Function(mog_trigger_pending) repeat True
    if mog_speaker:
        # The video is drawn first, behind both the cast and the say screen.
        add "mog edit" xysize (1920, 1080)
        if not mog_first_cycle_done:
            timer mog_duration action Function(mog_mark_cycle)
    if tribunal:
        if tribunal_in_corridor:
            $ cast = (("bucks", 0.50, "knowing", True),)
        elif tribunal_brando_present:
            $ cast = (
                ("bucks", 0.14, "serious", True),
                ("brando", 0.38, "tired", True),
                ("fazen", 0.62, "neutral", True),
                ("bolderik", 0.86, "neutral", True),
            )
        else:
            $ cast = (
                ("bucks", 0.19, "serious", True),
                ("fazen", 0.51, "neutral", True),
                ("bolderik", 0.81, "neutral", True),
            )
    else:
        $ cast = (
            ("bucks", 0.17, bucks_mood, visible_bucks),
            ("brando", 0.50, brando_mood, True),
            ("more", 0.83, more_mood, visible_more),
        )
    for person, position, mood, visible in cast:
        if visible:
            if mog_speaker == person:
                add (person + " mog") at (mog_pose_pop if _preferences.transitions else Transform()):
                    xpos position xanchor 0.5 ypos 935 yanchor 1.0
            else:
                add (person + " " + mood):
                    xpos position xanchor 0.5 ypos 935 yanchor 1.0
                    matrixcolor BrightnessMatrix(0.0 if active_speaker == person else -0.14)

screen scene_header(location="КАБИНЕТ ДИРЕКТОРА"):
    zorder 10
    frame:
        background Solid("#0b0c10c9")
        xfill True ysize 58 padding (52, 0)
        hbox:
            yalign 0.5 spacing 22
            text "УВС—19F" size 20 bold True color "#d3b28c"
            text "/" size 20 color "#6f6761"
            text location size 17 color "#c5bdb2"
        text chapter xalign 1.0 yalign 0.5 size 17 color "#b7a38e"

screen say(who, what):
    style_prefix "novel"
    window:
        id "window"
        background Solid("#101014f4")
        xfill True yalign 1.0 ysize (284 if renpy.showing("bg bulletin_counter") else 344)
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
            text "[config.name]" size 38 bold True
            text gui.about
            text "Голоса Бакса, Брандо и Морэ синтезированы ИИ. Восемь записей секретаря предоставлены автором проекта. Иллюстрации созданы ИИ по авторскому референсу."
            text "Управление: щелчок, пробел или Enter — дальше; колесо вверх — назад; Esc — меню; H — скрыть текст; F — полный экран."
            text "Режим «Авто» дожидается окончания озвучки. Громкость речи, музыки и эффектов настраивается раздельно."
            text "История содержит ненормативную лексику."
            text "Движок Ren’Py [renpy.version_only].\n[renpy.license!t]" size 19

screen end_card(first_chapter=True):
    modal True
    add Solid("#101014")
    vbox:
        xalign 0.5 yalign 0.5 spacing 30
        text "УВС—19F / АРХИВ" xalign 0.5 size 20 color "#be9f79" kerning 3
        text "КОНЕЦ ЗАПИСИ" xalign 0.5 size 62 bold True color "#eee5d9"
        if first_chapter:
            text "«Ты ведь никогда не умел просто уйти»." xalign 0.5 size 28 color "#b7aca0"
        null height 35
        if first_chapter:
            textbutton "Перейти к главе 2" action Jump("chapter_two") xalign 0.5 style "archive_primary_button" default_focus True
        textbutton "Вернуться в главное меню" action Return() xalign 0.5 style "archive_secondary_button" default_focus (not first_chapter)

style novel_quick_button:
    padding (5, 9)
    background None
style novel_quick_button_text:
    size 16 color "#b0a89d" hover_color "#e5c49e" selected_color "#e5c49e"
init 5 python:
    gui.accent_color = "#c6a77d"
    gui.hover_color = "#f0cfa0"
    gui.idle_color = "#b9b0a5"
    gui.selected_color = "#eee5d9"
    gui.text_color = "#eee5d9"
    gui.interface_text_color = "#ded6cc"
    gui.main_menu_background = "images/office-scp-v2.png"
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
