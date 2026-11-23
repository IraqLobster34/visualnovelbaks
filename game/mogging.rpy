# Rare, non-blocking edits attached to selected dialogue, never screen prediction.
default mog_speaker = ""
default mog_rolls = {}
default mog_duration = 5.25
default mog_music_was_paused = False
default mog_pending_speaker = ""
default mog_ready = False
default mog_delay = 0.08
default mog_first_cycle_done = False

init -20 python:
    import json

    with renpy.file("mog-quips.json") as quip_file:
        MOG_QUIPS = frozenset((quip["speaker"], quip["text"]) for quip in json.load(quip_file))
    MOG_SPEAKERS = frozenset(speaker for speaker, text in MOG_QUIPS)

    # The author's five-second "mentalist moment.mp4", converted to WebM.
    # A small decoding margin ensures the first cycle is complete before Auto.
    MOG_VIDEO_DURATION = 5.25
    renpy.music.register_channel("mog_edit", mixer="sfx", loop=True, movie=True)

    def mog_finish():
        if mog_speaker:
            renpy.music.stop(channel="mog_edit")
            renpy.music.set_pause(mog_music_was_paused, channel="music")
        store.mog_speaker = ""
        store.mog_pending_speaker = ""
        store.mog_ready = False
        store.mog_first_cycle_done = False

    def mog_start(speaker, duration=None):
        if speaker not in MOG_SPEAKERS:
            return
        mog_finish()
        store.mog_music_was_paused = renpy.music.get_pause(channel="music")
        renpy.music.set_pause(True, channel="music")
        renpy.music.set_volume(0.85, channel="mog_edit")
        store.mog_duration = MOG_VIDEO_DURATION if duration is None else duration
        store.mog_speaker = speaker

    def mog_trigger_pending():
        speaker = mog_pending_speaker
        if not mog_ready or speaker != active_speaker or renpy.is_skipping():
            mog_finish()
            return
        # Duration can be unavailable while a recording is first decoded.
        # Never start the edit over an unfinished spoken line.
        if renpy.music.get_playing(channel="voice"):
            return
        mog_start(speaker)

    def mog_arm_after_voice():
        if not mog_pending_speaker or mog_ready:
            return
        delay = 0.08
        if renpy.music.get_playing(channel="voice"):
            duration = renpy.music.get_duration(channel="voice")
            position = renpy.music.get_pos(channel="voice") or 0.0
            if duration is not None:
                delay += max(0.0, duration - position)
        store.mog_delay = delay
        store.mog_ready = True
        renpy.restart_interaction()

    def mog_mark_cycle():
        if not mog_speaker:
            return
        store.mog_first_cycle_done = True
        # Manual mode keeps looping. Auto dismisses only after a complete cycle;
        # do not dismiss a save/settings menu that is in another context.
        if _preferences.afm_enable and renpy.context_nesting_level() == 0:
            renpy.end_interaction(True)

    def mog_dialogue_callback(event, interact=True, what="", **kwargs):
        if not interact:
            return
        if event == "end":
            mog_finish()
        elif event == "begin":
            mog_finish()
            key = (active_speaker, what)
            if renpy.is_skipping() or key not in MOG_QUIPS:
                return
            # One exact 1-in-100 roll. Ren'Py's RNG and this cache both
            # participate in save/load and rollback, so revisiting a line
            # does not grant another attempt or change the speaking actor.
            if key not in mog_rolls:
                mog_rolls[key] = renpy.random.randrange(100) == 0
            if mog_rolls[key]:
                store.mog_pending_speaker = active_speaker
        elif event == "slow_done" and kwargs.get("last_segment", True):
            mog_arm_after_voice()

    config.all_character_callbacks.append(mog_dialogue_callback)

init 50 python:
    _mog_original_afm_callback = config.afm_callback

    def mog_afm_callback():
        if mog_pending_speaker or (mog_speaker and not mog_first_cycle_done):
            return False
        return _mog_original_afm_callback() if _mog_original_afm_callback else True

    config.afm_callback = mog_afm_callback

image mog edit = Movie(
    play="video/mog-edit.webm",
    channel="mog_edit",
    size=(1920, 1080),
    loop=True,
    start_image="images/office-scp-v2.png",
    image="images/office-scp-v2.png",
)
