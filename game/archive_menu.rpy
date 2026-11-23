transform archive_backdrop_drift:
    subpixel True
    align (0.5, 0.5)
    zoom 1.025
    ease 18.0 zoom 1.065
    ease 18.0 zoom 1.025
    repeat

transform archive_reveal(delay=0.0):
    subpixel True
    alpha 0.0
    yoffset 17
    pause delay
    easeout 0.32 alpha 1.0 yoffset 0

transform archive_arrow:
    subpixel True
    xoffset 0
    on hover, selected_hover:
        easeout 0.12 xoffset 6
    on idle, selected_idle:
        easeout 0.12 xoffset 0

image archive logo = Transform(Crop((127, 166, 1284, 735), "gui/game-logo-red.png"),
    xsize=602, ysize=345)

screen main_menu():
    tag menu
    on "show" action Function(mog_finish)

    add "bg office" at (archive_backdrop_drift if _preferences.transitions else Transform())
    add Solid("#11101a61")
    fixed:
        at (archive_reveal() if _preferences.transitions else Transform())
        add "more neutral" xpos 0.911 xanchor 0.5 ypos 1010 yanchor 1.0 zoom 0.93:
            matrixcolor BrightnessMatrix(-0.16)
        add "brando neutral" xpos 0.760 xanchor 0.5 ypos 1084 yanchor 1.0 zoom 1.04:
            matrixcolor BrightnessMatrix(-0.05)
        add "bucks neutral" xpos 0.568 xanchor 0.5 ypos 1140 yanchor 1.0 zoom 1.05
    add "gui/archive-shade.png" xysize (1920, 1080)

    hbox:
        xpos 104 ypos 92 spacing 17
        add Solid("#d9445b") xysize (23, 2) yalign 0.5
        text "УВС–19F / Служебный архив" size 21 color "#ead2d4" yalign 0.5

    vbox:
        xpos 104 ypos 161 spacing 22
        at (archive_reveal(0.05) if _preferences.transitions else Transform())
        add "archive logo" alt config.name
        text "От кабинета директора\nдо слушания в Трибунале.":
            xpos 2 size 27 line_spacing 4 color "#d4c6c6"

    vbox:
        xpos 106 ypos 615 spacing 11
        at (archive_reveal(0.10) if _preferences.transitions else Transform())
        button:
            style "archive_primary_button"
            xysize (410, 76)
            action Start()
            default_focus True
            fixed:
                text "Начать историю" style "archive_primary_button_text" yalign 0.5
                text "›" style "archive_primary_button_text" size 39 xalign 1.0 yalign 0.5:
                    at (archive_arrow if _preferences.transitions else Transform())
        button:
            style "archive_secondary_button"
            xysize (410, 69)
            action Show("chapter_picker")
            fixed:
                text "Выбрать главу" style "archive_secondary_button_text" yalign 0.5
                text "›" style "archive_secondary_button_text" size 36 xalign 1.0 yalign 0.5:
                    at (archive_arrow if _preferences.transitions else Transform())
        textbutton "Загрузить сохранение" action ShowMenu("load") style "archive_link_button"

    add Solid("#e9c9cb4d") xpos 104 ypos 956 xysize (1712, 1)
    hbox:
        xpos 104 ypos 989 spacing 29
        textbutton "Настройки" action ShowMenu("preferences") style "archive_footer_button"
        textbutton "Об игре" action ShowMenu("about") style "archive_footer_button"
        textbutton "Выход" action Quit(confirm=True) style "archive_footer_button"
    text "v[config.version]" xpos 1816 xanchor 1.0 ypos 1002 size 19 color "#d4c1c5"

screen chapter_picker():
    modal True
    zorder 50
    $ close_picker = Hide("chapter_picker", Dissolve(0.18) if _preferences.transitions else None)
    key "game_menu" action close_picker
    add Solid("#0b0b12bd") at (archive_reveal() if _preferences.transitions else Transform())

    frame:
        xalign 0.5 yalign 0.5 xysize (1376, 766)
        padding (58, 44)
        background Solid("#211a22")
        at (archive_reveal() if _preferences.transitions else Transform())

        vbox:
            spacing 22
            text "Выбрать главу" size 52 bold True color "#f5eee3"
            add Solid("#68454d") xysize (1260, 1)
            hbox:
                spacing 24
                use archive_chapter("Глава 1", "Кадровое решение",
                    "Разговор в кабинете директора", Start(), first=True)
                use archive_chapter("Глава 2", "Внутренний Трибунал",
                    "Заседание в переговорной Б-4", Start("chapter_two"))
            text "Недоступно" size 22 color "#bba9ad"
            hbox:
                spacing 24
                use archive_locked_chapter("Глава 3", "Ламперуж и Сович")
                use archive_locked_chapter("Глава 4", "Ларри находит новое пристанище")
                use archive_locked_chapter("Пролог", "Инцидент S65-028")

        textbutton "‹  Назад" action close_picker:
            style "archive_link_button"
            yalign 1.0

screen archive_chapter(number, title, description, start_action, first=False):
    button:
        style "archive_chapter_button"
        action start_action
        default_focus first
        xysize (618, 228)

        fixed:
            vbox:
                yalign 0.45 spacing 16
                text number size 21 color "#f5a6b1"
                text title size 38 bold True color "#f5eee3"
                text description size 23 color "#cec1b9"
            text "›" size 40 color "#f5a6b1" xalign 1.0 yalign 1.0:
                at (archive_arrow if _preferences.transitions else Transform())

screen archive_locked_chapter(number, title):
    frame:
        xysize (404, 150)
        padding (24, 18)
        background Solid("#2b252c")

        vbox:
            spacing 9
            text number size 20 color "#bba9ad"
            text title size 26 bold True color "#e4d4d7" xmaximum 356

style archive_primary_button is button:
    padding (25, 12)
    background Solid("#a8092e")
    hover_background Solid("#be1740")
    selected_background Solid("#be1740")
style archive_primary_button_text is button_text:
    font "DejaVuSans-Bold.ttf"
    size 27
    color "#fff5f1"
    hover_color "#fff5f1"
    selected_color "#fff5f1"

style archive_secondary_button is button:
    padding (25, 12)
    background Solid("#eee0cd1c")
    hover_background Solid("#eee0cd3d")
    selected_background Solid("#eee0cd3d")
style archive_secondary_button_text is button_text:
    size 27
    color "#f5eee3"
    hover_color "#fff2f1"
    selected_color "#fff2f1"

style archive_link_button is button:
    padding (0, 10)
    background None
style archive_link_button_text is button_text:
    size 24
    color "#d4c6c6"
    hover_color "#ffb5be"
    hover_underline True

style archive_footer_button is archive_link_button
style archive_footer_button_text is archive_link_button_text:
    size 22

style archive_chapter_button is button:
    padding (33, 25)
    background Solid("#302930")
    hover_background Solid("#53313f")
    selected_background Solid("#53313f")
