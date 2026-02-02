import spritePro as s
import scene_manger 

s.get_screen((1000, 1000), "пьяница", "icon.jpg")
s.audio_manager.play_music("sounds\elevator-music-vanoss-gaming-background-music.mp3")
scene_manger.create_scenes()
# s.enable_debug(True)
while True:
    s.update(fill_color=(85, 89, 145))
    