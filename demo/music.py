import pygame

class MusicPlayer():
  def __init__(self):
    pygame.mixer.init()
    self.sound=pygame.mixer.Sound(R"src\vgmenuselect.wav")
    self.backgroundmusic=pygame.mixer.music.load(R"src\Riverside Ride.mp3")
    self.explodemusic=pygame.mixer.Sound(R"src\boom6.wav")
    pygame.mixer.music.set_volume(0.02)
  def PlaySound(self):
    self.sound.play()
  def PlayBackgroundMusic(self):
    #pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
  def PlayExplode(self):
    self.explodemusic.play()
    pass

    