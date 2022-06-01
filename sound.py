from pygame import mixer
import os

mixer.init()

bgmusic = mixer.Sound("./audio/music.mpeg")
bgmusic.set_volume(0.1)

#bgmusic = mixer.music.load(os.path.join("audio", 'music.mp3'))
#bgmusic = mixer.music.set_volume(0.4)

missile = mixer.Sound("./audio/missile.wav")
expl = mixer.Sound("./audio/explosion2.ogg")
exlp2 = mixer.Sound("./audio/explosion.wav" )
powerup = mixer.Sound("./audio/powerup.wav" )