import pygame

class Music():
  def __init__(self):
    pygame.mixer.init()
    self.sound=pygame.mixer.Sound(R"src\key_pickup.mp3")
    self.backgroundmusic=pygame.mixer.music.load(R"src\Christmas synths.ogg")
    pygame.mixer.music.set_volume(0.01)
  def PlaySound(self):
    self.sound.play()
  def PlayBackgroundMusic(self):
    #pygame.mixer.music.set_volume(0.5)
    print(pygame.mixer.music.get_volume())
    pygame.mixer.music.play()
    