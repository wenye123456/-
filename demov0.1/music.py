import pygame

class MusicPlayer():
  def __init__(self):
    pygame.mixer.init()
    self.sound=pygame.mixer.Sound(R"src\vgmenuselect.wav")
    self.backgroundmusic=pygame.mixer.music.load(R"src\Christmas synths.ogg")
    self.explodemusic=pygame.mixer.Sound(R"src\boom6.wav")
    pygame.mixer.music.set_volume(0.01)
  def PlaySound(self):
    self.sound.play()
  def PlayBackgroundMusic(self):
    #pygame.mixer.music.set_volume(0.5)
    print(pygame.mixer.music.get_volume())
    pygame.mixer.music.play()
  def PlayExplode(self):
    self.explodemusic.play()
    pass

    