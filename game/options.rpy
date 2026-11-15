define config.name = "УВС-19F: Причина отказа"
define config.version = "0.2.0"

define gui.about = renpy.file("release-notes.txt").read().decode("utf-8").strip()
define config.window_title = "УВС-19F · Причина отказа"
define config.window_icon = "images/window_icon.png"
define config.save_directory = "Uvs19F-PrichinaOtkaza"
define config.has_sound = True
define config.has_music = True
define config.has_voice = True
define config.default_language = "russian"
define config.default_text_cps = 42
define config.default_afm_time = 8
define config.default_wait_for_voice = True
define config.end_splash_transition = Dissolve(0.5)
define config.enter_transition = Dissolve(0.18)
define config.exit_transition = Dissolve(0.18)
define config.intra_transition = Dissolve(0.12)
define config.after_load_transition = Dissolve(0.3)
define config.window = "auto"
define config.window_show_transition = Dissolve(0.15)
define config.window_hide_transition = Dissolve(0.15)
define config.main_menu_music = "audio/soundtrack.mp3"
default preferences.fullscreen = False
default preferences.music_volume = 0.25
default preferences.sound_volume = 0.6
default preferences.voice_volume = 1.0
default persistent.finished = False

init python:
    renpy.music.register_channel("ambience", "sfx", loop=True)
    build.name = "Uvs19F"
    build.executable_name = "Uvs19F"
    build.directory_name = "Uvs19F-" + config.version
    build.include_update = False
    build.classify("game/cache/**", None)
    build.classify("**.bak", None)
    build.classify("game/saves/**", None)
    build.classify("game/voice/**.part.mp3", None)
    build.classify("game/testcases.rpy", None)
    build.classify("game/testcases.rpyc", None)
    build.classify("game/**", "all")
    build.classify("README.txt", "all")
    build.classify("CREDITS.txt", "all")
    build.classify("**", None)

# Saves made before the soundtrack change can contain the old audio queue.
label after_load:
    stop sound
    stop ambience
    if renpy.get_screen("cast_stage"):
        play music "audio/soundtrack.mp3" loop if_changed fadein 1.0 volume 0.45
    return
