from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.core import CardMaker, TextureStage
from direct.gui.DirectGui import DirectButton  # Импортируем класс кнопки


# Принудительно включаем OpenAL для стабильного воспроизведения тяжелого файла
loadPrcFileData("", "audio-library-name p3openal_audio")
# Отключаем принудительное масштабирование текстур
Texture.setTexturesPower2(0)

class App6(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # шрифт
        self.font = loader.loadFont("Roboto/Roboto-Bold.ttf")

        cm = CardMaker("plane")
        cm.setFrameFullscreenQuad()

        plane = render2d.attachNewNode(cm.generate())

        # Загружаем видео и звук (раз отдельный пример работал так, оставляем его)
        movie = loader.loadTexture("material/video_ending.mp4")
        sound = loader.loadSfx("material/video_ending.mp4")

        plane.setTexture(movie)
        plane.setTexScale(TextureStage.getDefault(), movie.getTexScale())
        movie.setLoop(0)
        movie.synchronizeTo(sound)

        # Запускаем оба компонента
        sound.play()
        movie.play() # Обязательно активируем видеопоток
#parent=self.a2dBottomRight,
        # Кнопка в правом нижнем углу поверх видео
        self.btn_continue = DirectButton(
            text="Продолжить",
            text_font = self.font,
            scale=0.08,
            pos=(1, -1, 0.15),
            command=self.on_continue,  # Оставляем вызов метода
            sortOrder=10
        )

        # Регистрируем собственное событие для безопасного выхода
        self.accept("safe-exit-and-menu", self.exit_and_open_menu)

    def on_continue(self):
        # Просто отправляем сигнал. EventManager безопасно завершит клик
        messenger.send("safe-exit-and-menu")

    def exit_and_open_menu(self):
        import subprocess
        import sys
        import os

        print("Безопасно запускаем главный файл и выходим...")

        # Вычисляем путь к главному файлу на папку выше (замените 'main.py' на ваше имя, если нужно)
        main_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Whisper_Game.py"))

        # Запускаем главное меню как независимый процесс
        subprocess.Popen([sys.executable, main_script])

        # Полностью и безопасно закрываем текущую программу
        sys.exit(0)


# Этот блок заставит файл запуститься независимо, когда его вызовет Subprocess
if __name__ == "__main__":
    app = App6()
    app.run()
