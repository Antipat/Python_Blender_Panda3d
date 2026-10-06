from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from direct.actor.Actor import Actor
from panda3d.core import *
import sys

##from moduls.Game0 import App0
##from moduls.Game1 import App1
##from moduls.Game2 import App2
##from moduls.Game3 import App3
##from moduls.Game4 import App4
##from moduls.Game5 import App5

class Application(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        # Смещение камеры
        self.cam.setPos(20,-10,2)

        # 2. Добавление модели в сцену
        self.my_actor = Actor("model/Girl.glb")
        self.my_actor.reparentTo(self.render)
        self.my_actor.setScale(1, 1, 1) # Масштаб при необходимости
        self.my_actor.setPos(1, 0, 0) # Позиция
        self.my_actor.loop('girl_geroAction')

        self.my_actor1 = Actor("model/Kor1.glb")
        # 2. Добавление модели в сцену
        self.my_actor1.reparentTo(self.render)
        self.my_actor1.setScale(1, 1, 1) # Масштаб при необходимости
        self.my_actor1.setPos(1, 0, 0) # Позиция
        self.my_actor1.loop('Arm')

        self.my_actor2 = Actor("model/Kor2.glb")
        # 2. Добавление модели в сцену
        self.my_actor2.reparentTo(self.render)
        self.my_actor2.setScale(1, 1, 1) # Масштаб при необходимости
        self.my_actor2.setPos(1, 0, 0) # Позиция
        self.my_actor2.loop('Arm1')

        self.my_actor3 = Actor("model/Kor3.glb")
        # 2. Добавление модели в сцену
        self.my_actor3.reparentTo(self.render)
        self.my_actor3.setScale(1, 1, 1) # Масштаб при необходимости
        self.my_actor3.setPos(1, 0, 0) # Позиция
        self.my_actor3.loop('Arm2')

        self.my_actor4 = Actor("model/Kor4.glb")
        # 2. Добавление модели в сцену
        self.my_actor4.reparentTo(self.render)
        self.my_actor4.setScale(1, 1, 1) # Масштаб при необходимости
        self.my_actor4.setPos(1, 0, 0) # Позиция
        self.my_actor4.loop('Arm3')

        self.my_actor5 = Actor("model/Kor5.glb")
        # 2. Добавление модели в сцену
        self.my_actor5.reparentTo(self.render)
        self.my_actor5.setScale(1, 1, 1) # Масштаб при необходимости
        self.my_actor5.setPos(1, 0, 0) # Позиция
        self.my_actor5.loop('Arm4')

        self.my_actor6 = Actor("model/Kor6.glb")
        # 2. Добавление модели в сцену
        self.my_actor6.reparentTo(self.render)
        self.my_actor6.setScale(1, 1, 1) # Масштаб при необходимости
        self.my_actor6.setPos(1, 0, 0) # Позиция
        self.my_actor6.loop('Arm5')
##
        # рассеянное освещение
        ambLight = AmbientLight("ambient")
        ambLight.setColor(Vec4(0.2, 0.2, 0.25, 0.5))
        # установка нового узла света
        ambNode = render.attachNewNode(ambLight)
        render.setLight(ambNode)

        # 3. Привязка вашей 3D-модели (например, Actor'а) к физической ноде
        self.actor = Actor("model/Animetion_Gero.glb")
        self.actor.setScale(1)
        self.actor.reparentTo(self.render)
        self.actor.setPos(20, 0, 0)
        self.actor.loop( "AnimMan")


                # NPC
        # Привязка 3D-модели (например, Actor'а)
        self.people = Actor("model/People1.glb")
        self.people.setScale(0.2)
        self.people.reparentTo(render)
        self.people.loop("Game_engine|Game_engine|mixamo.com|Layer0.001")
        self.people.setPos(23, 0, 0)
        self.people.setLightOff()

        #  Привязка 3D-модели (например, Actor'а)
        self.people1 = Actor("model/People2.glb")
        self.people1.setScale(0.2)
        self.people1.reparentTo(render)
        self.people1.loop("Game_engine|Game_engine|mixamo.com|Layer0")
        self.people1.setPos(18, 0, 0)
        self.people1.setH(0)
         # Привязка 3D-модели (например, Actor'а)
        self.people2 = Actor("model/People3.glb")
        self.people2.setScale(1)
        self.people2.reparentTo(render)
        self.people2.loop("menl_vrag1|mixamo.com")
        self.people2.setPos(16, 0, 0)

         # Привязка 3D-модели (например, Actor'а)
        self.people3 = Actor("model/People4.glb")
        self.people3.setScale(1)
        self.people3.reparentTo(render)
        self.people3.loop("menl_vrag2|mixamo.com")
        self.people3.setPos(14, 0, 0)
        self.people3.setH(15)

        base.setBackgroundColor(0.2, 0.5, 0.5)

        # рассеянное освещение
        ambLight = AmbientLight("ambient")
        ambLight.setColor(Vec4(0.4, 0.4, 0.45, 0.7))
        # установка нового узла света
        ambNode = render.attachNewNode(ambLight)
        render.setLight(ambNode)



####        #окружение освещения
####        dirLight = DirectionalLight("directional")
####        dirLight.setColor(Vec4(0.1, 0.1, 0.2, 1.0))
####        dirNode = render.attachNewNode(dirLight)
####        dirNode.setHpr(0, 0, 0)
####        render.setLight(dirNode)
##
####        # точечное освещение
####        pntLight = PointLight("point")
####        pntLight.setColor(Vec4(1, 0, 0.0, 1.0))
####        # установка нового узла света
####        pntNode = render.attachNewNode(pntLight)
####        pntNode.setPos(20, 5, 3)
##
####        self.scene = self.loader.loadModel("model//cube.glb")
####        self.scene.setPos(20, 5, 6)
####        self.scene.reparentTo(render)
##
##        #self.panda.setLight(pntNode)
        # освещение конусное
        sptLight = Spotlight("spot")
        sptLens = PerspectiveLens()
        sptLight.setLens(sptLens)
        sptLight.setAttenuation(VBase3(0, 0, 0.01)) # Затухание
        sptLight.setColor(Vec4(1.0, 1.0, 0.8, 0.5))
        sptLight.setShadowCaster(True)
        # установка нового узла света
        sptNode = render.attachNewNode(sptLight)
        sptNode.setPos(20, -11, 1.5)
        render.setLight(sptNode)
        # автонастройка шейдеров - тени свет
        #render.setShaderAuto()

        # Загрузка звука
        self.myMusic = base.loadMusic("sound/Mellody.wav")

        # Настройка
        self.myMusic.setVolume(0.1) # Громкость от 0 до 1
        self.myMusic.setLoop(True)  # Зациклить

        # Воспроизведение
        self.myMusic.play()

        # загружаем по настройкам
        self.FileRead()


    def PlayGame(self):
        self.effect.play()
        base.destroy()


        gameApp = App0()
        gameApp.load()



    def PlaySetting(self):
        self.effect.play()
        self.Im.hide()
        self.L.hide()
        self.s.hide()
        self.d.hide()
        self.btn0.hide()
        self.btn1.hide()
        self.btn2.hide()
        self.btn3.hide()
        #font = loader.loadFont("GLIWA TYPE/GLIWA TYPE.otf")
        #0 текст поясненния
        self.textlabel = DirectLabel(
            text="screen resolution",
            scale=0.1,
            pos=(-0.9, 0, 0.6),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 1), # Прозрачный фон
            text_font = self.font
        )

        # 1. Создаем текстовую метку для отображения значения
        self.value_label = DirectLabel(
            text="Screen: 640x480",
            scale=0.1,
            pos=(0.2, 0, 0.65),
            text_fg=(1, 1, 1, 1),
            text_font = self.font,
            frameColor=(0, 0, 0, 1) # Прозрачный фон
        )

        # 2. Создаем ползунок (Slider)
        self.slider = DirectSlider(
            range=(0, 4),       # Диапазон значений (минимум, максимум)
            value=0,              # Начальное значение
            pageSize=1,          # Шаг при клике на трек
            command=self.show_value, # Функция, вызываемая при изменении
            scale=0.5,            # Размер ползунка
            pos=(0.2, 0, 0.6)         # Позиция на экране
        )

        #3 текст громкость
        self.textlabel1 = DirectLabel(
            text="Language",
            scale=0.1,
            pos=(-0.9, 0, 0.4),
            text_fg=(1, 1, 1, 1),
            text_font = self.font,
            frameColor=(0, 0, 0, 1) # Прозрачный фон
        )

        # Функция, которая срабатывает при выборе
        def set_item(arg):
            print(f"Выбран элемент: {arg}")
            self.FileSetting(1, f"language {arg}")


        # Создание выпадающего списка
        self.option = DirectOptionMenu(
            text="Выберите опцию",
            scale=0.1,
            items=["English", "Russia"],
            initialitem = 0, # Выбран первый элемент
            highlightColor = (0.65, 0.65, 0.65, 1),
            command = set_item,
            text_font = self.font
        )

        # Размещение на экране
        self.option.setPos(0, 0, 0.4)

         # Кнопка Возврата
        self.btn = DirectButton( text = " OK",
         scale=0.1, pos=(-0.8,0,0.2),  command = self.MainMenu)
        #pass

    def PlayExit(self):
        self.effect.play()
        base.destroy()
        sys.exit()
        #base.userExit()

    # Функция обратного вызова (callback)
    def show_value(self):
        scenWidth = ("640x480", "1280x720", "1366x768", "1920x1080", "2560x1440")
        # Получаем текущее значение
        current_val = self.slider['value']
        print(f"Текущее значение ползунка: {current_val}")

        self.vis = int(current_val)
        # перезаписываем первую строку файла
        self.FileSetting(0, f"vis {self.vis}")


        # Обновляем текст метки
        self.value_label['text'] = f"Screen: {scenWidth[self.vis]}"


    def togFullScreen(self, width, height, posX, posY, full):
    #def togFullScreen(self):
        winPro = WindowProperties()
        winPro.setOrigin(posX, posY)
        #winPro.clearSize()
        winPro.setSize(width, height)
        #winPro.setFullscreen(full)
        self.win.requestProperties(winPro)

    # разрешение экрана
    def screenF0(self):
        self.togFullScreen(640,480,100,200,0)
    def screenF1(self):
        self.togFullScreen(1280,720,0,25,0)
    def screenF2(self):
        self.togFullScreen(1366,768,0,25,0)
    def screenF3(self):
        self.togFullScreen(1920,1080,0,25,0)
    def screenF4(self):
        self.togFullScreen(2560,1440,0,25,0)

    # записываем данные в файл
    def FileSetting(self, n, text):
        # Имя файла
        filename = 'SetFile.txt'
        new_line_content = f"{text}\n"

        # 1. Читаем все строки из файла
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 2. Изменяем вторую строку (индекс 1, т.к. индексация с 0)
        # Проверяем, есть ли вторая строка
        if len(lines) >= n:
            lines[n] = new_line_content
        else:
            # Если строк меньше, можно добавить вторую или обработать ошибку
            lines.append(new_line_content)

        # 3. Перезаписываем файл с измененными данными
        with open(filename, 'w', encoding='utf-8') as file:
            file.writelines(lines)

    def FileRead(self):
        # Имя файла
        filename = 'SetFile.txt'

        # 1. Читаем все строки из файла
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            print('line = ', lines)
            if "vis" in lines[0]:
                n = int(lines[0][4])
                print('n = ', n)
                match n:
                    case 0:
                        self.screenF0()
                    case 1:
                        self.screenF1()
                    case 2:
                        self.screenF2()
                    case 3:
                        self.screenF3()
                    case 4:
                        self.screenF4()



    def MainMenu(self):
        self.effect.play()
        self.textlabel.hide()
        self.value_label.hide()
        self.slider.hide()
        self.textlabel1.hide()
        self.option.hide()
        self.btn.hide()

        self.Im.show()
        self.s.show()
        self.L.show()
        self.d.show()
        self.btn0.show()
        self.btn1.show()
        self.btn2.show()
        self.btn3.show()

        match self.vis:
            case 0:
                self.screenF0()
            case 1:
                self.screenF1()
            case 2:
                self.screenF2()
            case 3:
                self.screenF3()
            case 4:
                self.screenF4()

    def PlayLoading(self):
        self.effect.play()
        #Games = (App0(), App1(), App2(), App3(), App4(), App5())
        #self.GAMM = Games

         # Имя файла
        filename = 'Save.txt'
        #new_line_content = f"{text}\n"

        # 1. Читаем все строки из файла
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 2. Изменяем вторую строку (индекс 1, т.к. индексация с 0)
        # Проверяем, есть ли вторая строка
        if "val" in lines[2]:
            k = int(lines[2][4])
            print('k = ', k)
            base.destroy()

            match k:
                case 0:
                    print("нет сохранений")
                case 1:
                    A = App0()
                    A.load()
                case 2:
                    A = App1()
                    A.load()
                case 3:
                    A = App2()
                    A.load()
                case 4:
                    A = App3()
                    A.load()
                case 5:
                    A = App4()
                    A.load()
                case 6:
                    A = App5()
                    A.load()



##        if len(lines) >= n:
##            lines[n] = new_line_content
##        else:
##            # Если строк меньше, можно добавить вторую или обработать ошибку
##            lines.append(new_line_content)



        #pass












'''

SAS.glb
        # Создание перасонажа
        self.panda = Actor("panda",{'walk': "panda-walk"})
        self.panda.reparentTo(render)
        self.panda.loop("walk")
'''


