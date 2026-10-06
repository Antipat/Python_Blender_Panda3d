from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from direct.actor.Actor import Actor
from panda3d.core import *
from direct.task import Task
#from direct.filter.CommonFilters import CommonFilters
import sys
from moduls.scene_base import Scene
from moduls.Game3 import App3

RUS = ["", "Дом дяди уже где-то недалеко", "Где-то должен быть поворот", "", "А вот и поворот", "",

  "", "", "", "", "" ,"", "Выйти из машины. Нажми P" ]

ENG = ["", "Uncle's house is already somewhere nearby", "There must be a turn somewhere", "", "Here comes the turn", ""
 "", "", "", "", "", "", "Exit the car. Press P."]

Lang =[RUS, ENG]

COL = ("Cube", "Cube.001", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "Q1", "Q2")

class App2(Scene, ShowBase):

    def __init__(self):

        ShowBase.__init__(self)
        # шрифт
        self.font = loader.loadFont("Roboto/Roboto-Bold.ttf") #("cmr12.egg")

        # Отключаем камеру по умолчанию (свободный режим)
        self.disableMouse()

        # Ограничить до 30 FPS
        loadPrcFileData("", "clock-mode limited")
        loadPrcFileData("", "clock-frame-rate 60.0")
        base.camLens.setFar(1500.0)

        #render.setShaderAuto()


        self.effect1 = base.loader.loadSfx("sound/Vehicle_Car_Engine.wav")
        self.effect2 = base.loader.loadSfx("sound/Vehicle_Car_Drive.wav")
        self.effect3 = base.loader.loadSfx("sound/Vehicle_Car_Stop.wav")
        self.effect4 = base.loader.loadSfx("sound/car_collision.wav")

        self.effect1.setLoop(True)
        self.effect2.setLoop(True)
        self.effect2.play()
        self.effect2.setVolume(0.5) # Громкость от 0 до 1

        self.speekG = base.loader.loadSfx("sound/man0.wav")

        # Загрузка звука
        self.myMusic = base.loadMusic("sound/Mellody.wav")

        # Настройка
        self.myMusic.setVolume(2) # Громкость от 0 до 1
        self.myMusic.setLoop(True)  # Зациклить

        # Воспроизведение
        self.myMusic.play()

        # логика столкновения
        self.hitB = False

        self.vah = 0
        self.FileRead()
        self.numb = 2

        self.Quest = 0
        self.fuel = 0

       # Кнопка
        self.buttonPlay = self.loader.loadModel("model//Button3.glb")
        self.buttonPlay.setPos(0, 0, -5)
        self.btn0 = DirectButton(
         geom=self.buttonPlay, scale=0.1, pos=(-0.8,0,0.45), frameColor=(0, 0, 0, 0), command = self.PlayExit)

        # Кнопка рестарт
        self.buttonRest = self.loader.loadModel("model//Restart.glb")
        self.buttonRest.setPos(0, 0, 0.5)
        self.btn1 = DirectButton(
        geom=self.buttonRest,
        scale=0.1,pos=(-0.8,0,0.45), frameColor=(0, 0, 0, 0), command = self.RES)

        self.btn1.hide()
        self.btn0.hide()


##        #окружение освещения
##        dirLight = DirectionalLight("directional")
##        dirLight.setColor(Vec4(0.8, 0.8, 0.5, 1.0))
##        dirNode = render.attachNewNode(dirLight)
##        dirNode.setHpr(0, 60, 0)
##        render.setLight(dirNode)

#
        base.setBackgroundColor(0, 0.05, 0.1)

        # Имя тумана используется для отладки
        fog = Fog("SceneFog")

        # 2. Настраиваем цвет тумана (RGBA)
        # Здесь: светло-серый туман
        fog.setColor(0.2, 0.2, 0.1)

        # 3. Настраиваем дальность тумана (у экспоненциального тумана свои параметры)
        #fog.setExpDensity(0.001) # Для экспоненциального
        # Или линейный туман (начало, конец)
        fog.setLinearRange(0.0, 1800.0)

        # 4. Применяем туман к сцене (render)
        render.setFog(fog)

        self.frameActor = 0


        self.locS = self.loader.loadModel("model//Loc1.glb")
        self.locS.setPos(0, 0, 0)
        self.locS.setTransparency(TransparencyAttrib.MAlpha)
        self.locS.reparentTo(render)

        self.scene = self.loader.loadModel("model//Car.glb")
        self.scene.setPos(0, 0, 0)
        self.scene.setTransparency(TransparencyAttrib.MAlpha)
        self.scene.reparentTo(render)

        # 2. Добавление модели в сцену
        self.RUL = Actor("model/Rul.glb")
        self.RUL.reparentTo(self.scene)
        #self.my_actor.setScale(1, 1, 1) # Масштаб при необходимости
        self.RUL.setPos(0, 0, 0) # Позиция
        # Получаем список названий анимаций

##        animations_list = self.RUL.get_anim_names()
##
##        print("Доступные анимации:", animations_list)

        # 1. Создаем текстовую метку для отображения значения
        self.value_label = DirectLabel(
            text="Coord: 0, 0, 0",
            scale=0.1,
            pos=(0.2, 0, 0.65),
            text_fg=(1, 1, 1, 1),
            text_font = self.font,
            frameColor=(0, 0, 0, 0), # Прозрачный фон
            text_wordwrap=20.0,
            # Дополнительно можно выровнять текст, например, по центру
            text_align=TextNode.ACenter
        )

        # привязка модели к другой модели

##        self.s = self.loader.loadModel("model//cube.glb")
##        self.s.setPos(15, -10, 0)
##        #slightCube = self.scene.attachNewNode(self.s)
##        #self.s.reparentTo(render)
##
##        self.s.reparentTo(self.scene)
########

        # фары автомобиля
        self.spotlig(-10, -15, 3, 90, -10, 0, self.scene)
        self.spotlig(-10, -5, 3, 90, -10, 0, self.scene)
        # освещение салона автомобиля
        self.pointlig( 25, -15, 1, self.scene, 2)
        self.pointlig( 15, -5, 1, self.scene, 2)
####
##        # освещение заправки
##        self.spotlig(4335, -1200, 15, 150, 0, 0, self.locStop)
##        self.spotlig(4515, -1700, 15, 0, 0, 0, self.locStop)
##        self.spotlig(4515, -1200, 15, 0, 0, 0, self.locStop)
##        self.spotlig(4715, -1200, 15, 0, 0, 0, self.locStop)
##
##        self.spotlig(4615, -1200, 15, 45, 0, 0, self.locStop)
####        self.spotlig(4680, -1200, 15, -45, 0, 0, self.locStop)
####        self.spotlig(4680, -1200, 15, -75, 0, 0, self.locStop)

        base.graphicsEngine.renderFrame()

############
        # Инициализация фильтров
        filters = CommonFilters(base.win, base.cam)

        # Включение Bloom (эффект свечения)
        filters.setBloom()

        # Другие популярные фильтры:
        #filters.setCartoonInk(0.5, (0.1,1,0.2,1)) # Эффект комикса (обводка)
        #filters.setAmbientOcclusion() # Screen-space Ambient Occlusion (SSAO)
        filters.setBlurSharpen(amount=0.8) # Размытие или резкость
        filters.setGammaAdjust(1.1) #Гамма

        #filters.setSrgbEncode()
        #filters.delHighDynamicRange() # фильтр HDR

##############
################
        # 1. Инициализируем глобальный обходчик столкновений
        self.cTrav = CollisionTraverser()
        # Создаем очередь для хранения зарегистрированных столкновений
        self.collision_queue = CollisionHandlerQueue()

        # добавить сетку коллайдера
        self.collBox(self.scene)

###############

        # рассеянное освещение
        ambLight = AmbientLight("ambient")
        ambLight.setColor(Vec4(0.3, 0.3, 0.35, 0.7))
        # установка нового узла света
        ambNode = render.attachNewNode(ambLight)
        render.setLight(ambNode)

        ####
        # Смещение камеры
        self.cam.setPos(23,-14,2) #(23, -100, 20)
        self.cam.setHpr(94, -5, 0)

        self.cam.reparentTo(self.scene)

        # Для теста: заставим модель вращаться, свет должен вращаться вместе с ней
        #self.scene.hprInterval(10, (360, 0, 0)).loop()
#############
        # загружаем по настройкам
#        self.FileRead()
############
        # Настраиваем окно: прячем курсор и удерживаем его внутри
        props = WindowProperties()
        props.setCursorHidden(True)
        # M_confined удерживает мышь в пределах окна без изменения логики ОС
        props.setMouseMode(WindowProperties.M_confined)
        self.win.requestProperties(props)

        self.camera_sens = 0.5 # Чувствительность

        # Запускаем задачу во фрейме PostRender или Late, чтобы окно успело обновиться
        self.taskMgr.add(self.update_camera, "UpdateCameraTask")


        # 1. Словарь для хранения состояний
        self.keys = {
            "w": False, "a": False, "s": False, "d": False,
            "shift": False, "space": False, "e": False, "p":False
        }

        # 2. Привязка событий нажатия и отпускания
        for key in self.keys:
            self.accept(key, self.update_key, [key, True])
            self.accept(f"{key}-up", self.update_key, [key, False])

        # Добавляем задачу на каждый кадр
        self.taskMgr.add(self.update_game, "update_game")
        self.speed = 0
##
##        ################

        # Загружаем визуальную модель
        wall_np = loader.loadModel("model/Bar1.glb")
        wall_np.reparentTo(render)

        # Используем физику полигонов самой модели
        # Устанавливаем бит-маску столкновений (например, BitMask32.bit(1))
        wall_np.set_collide_mask(BitMask32.bit(1))
        wall_np.setTag('Collide', 'Polyset keep descend')

        # Скрыть модель
        wall_np.hide()

##        # Загружаем визуальную модель
##        wall_np1 = loader.loadModel("model/Bar2.glb")
##        wall_np1.reparentTo(render)
##
##        # Используем физику полигонов самой модели
##        # Устанавливаем бит-маску столкновений (например, BitMask32.bit(1))
##        wall_np1.set_collide_mask(BitMask32.bit(1))
##        wall_np1.setTag('Collide', 'Polyset keep descend')
##
##        # Скрыть модель
##        wall_np1.hide()

        ##########
        # Триггеры

        for i in range(1,10):
            Name = f"Trigerr{i}.glb"
            # Загружаем визуальную модель
            T1 = loader.loadModel(f"model/{Name}")
            T1.reparentTo(render)

            # Используем физику полигонов самой модели
            # Устанавливаем бит-маску столкновений (например, BitMask32.bit(1))
            T1.set_collide_mask(BitMask32.bit(1))
            T1.setTag('Collide', 'Polyset keep descend')
            # Скрыть модель
            T1.hide()

         # квестовые триггеры
        Name = f"TrigGame2.glb"
        # Загружаем визуальную модель
        self.T3 = loader.loadModel(f"model/{Name}")
        self.T3.reparentTo(render)

        # Используем физику полигонов самой модели
        self.T3.set_collide_mask(BitMask32.bit(1))
        self.T3.setTag('Collide', 'Polyset keep descend')
        self.T3.hide()
##
        # 5. Запускаем постоянную проверку в игровом цикле
        self.taskMgr.add(self.update_collisions, "CollisionTask")


    # отслеживаем касание
    def update_collisions(self, task):
        # Проверяем, есть ли столкновения в очереди
        if self.collision_queue.getNumEntries() > 0:
            # Сортируем столкновения от ближайшего к дальнему
            self.collision_queue.sortEntries()

            # Берем самое первое (ближайшее) столкновение
            entry = self.collision_queue.getEntry(0)

            # Получаем имена столкнувшихся узлов
            from_node = entry.getFromNode().getName()
            into_node = entry.getIntoNode().getName()
            print(f"ПРОИЗОШЛО СТОЛКНОВЕНИЕ! {from_node} врезался в {into_node}")
            if into_node == COL[0] or into_node == COL[1]:
                print(f"ПРОИЗОШЛО СТОЛКНОВЕНИЕ! {from_node} врезался в {into_node}")
                self.hitB = True
                self.scene.setPos(self.scene.getX()+20,self.scene.getY()+20, self.scene.getZ())
                self.effect4.play()

                if self.numb ==0:

                    self.btn1.show()
                    self.btn0.show()

                    self.numb +=1

                # Создаем объект свойств окна
                props = WindowProperties()

                # Устанавливаем видимость курсора (False означает "НЕ скрывать")
                props.setCursorHidden(False)

                # Применяем свойства к главному окну игры
                base.win.requestProperties(props)

            elif into_node == COL[2]:
                self.value_label['text'] = Lang[self.vah][0]
                self.speekG.play()
                self.GameSave(2, "val 3")
            elif into_node == COL[3]:
                self.value_label['text'] = Lang[self.vah][1]
                self.speekG.play()
            elif into_node == COL[4]:
                self.value_label['text'] = Lang[self.vah][2]
                self.speekG.play()
            elif into_node == COL[5]:
                self.value_label['text'] = Lang[self.vah][3]
                self.speekG.play()
            elif into_node == COL[6]:
                self.value_label['text'] = Lang[self.vah][4]
                self.speekG.play()
            elif into_node == COL[7]:
                self.value_label['text'] = Lang[self.vah][5]
                self.speekG.play()
            elif into_node == COL[8]:
                self.value_label['text'] = Lang[self.vah][6]
                self.speekG.play()
            elif into_node == COL[9]:
                self.value_label['text'] = Lang[self.vah][7]
                self.speekG.play()
                self.GameSave(0, f"pos ({self.scene.getX()},{self.scene.getY()}, {self.scene.getZ()})")
            elif into_node == COL[10]:
                self.value_label['text'] = Lang[self.vah][8]
                self.speekG.play()
            elif into_node == COL[11]:
                if self.fuel<=1:
                    self.value_label['text'] = Lang[self.vah][10]
                    self.Quest = 1
            elif into_node == COL[12]:
                self.value_label['text'] = Lang[self.vah][12]

                self.Quest = 2
        return task.cont


    def update_key(self, key, is_down):
        """Обновляет состояние клавиши в словаре"""
        self.keys[key] = is_down

    def update_game(self, task):
        """Проверяет комбинации клавиш каждый кадр"""
        # Пример: движение + ускорение

        if self.speed>0.1 :
            self.move(self.speed, 0)
            self.speed -=0.02
        elif self.speed<-0.1:
            self.move(self.speed, 0)
            self.speed +=0.02
        if self.hitB == False:
            if self.keys["w"]:
                self.numb = 0
                if self.speed>=-1.0:
                    self.speed -=0.1
                self.move(self.speed, 0)
                if self.keys["a"]:
                     self.rote(0.5)
                     # Проиграет анимацию с 10-го по 30-й кадр и остановится на 30-м
                     match self.frameActor:
                        case 0:
                            self.RUL.play("Rul", fromFrame=0, toFrame=30)
                            self.frameActor = 30
                        case 60:
                            self.RUL.play("Rul", fromFrame=0, toFrame=30)
                            self.frameActor = 30
                        case 90:
                            self.RUL.play("Rul", fromFrame=90, toFrame=60)
                            self.frameActor = 60
                        case 120:
                            self.RUL.play("Rul", fromFrame=0, toFrame=30)
                            self.frameActor = 30
                elif self.keys["d"]:
                    match self.frameActor:
                        case 0:
                            self.RUL.play("Rul", fromFrame=60, toFrame=90)
                            self.frameActor = 90
                        case 30:
                            self.RUL.play("Rul", fromFrame=30, toFrame=60)
                            self.frameActor = 60
                        case 60:
                            self.RUL.play("Rul", fromFrame=60, toFrame=90)
                            self.frameActor = 90
                        case 120:
                            self.RUL.play("Rul", fromFrame=60, toFrame=90)
                            self.frameActor = 90
                    self.rote(-0.3)
                print("Бег вперед!")

            elif self.keys["s"]:
                if self.speed<=1.0:
                    self.speed +=0.1
                self.move(self.speed, 0)
                print("Идти назад")
                if self.keys["a"]:
                     self.rote(0.5)
                     # Проиграет анимацию с 10-го по 30-й кадр и остановится на 30-м
                     match self.frameActor:
                        case 0:
                            self.RUL.play("Rul", fromFrame=0, toFrame=30)
                            self.frameActor = 30
                        case 60:
                            self.RUL.play("Rul", fromFrame=60, toFrame=30)
                            self.frameActor = 30
                        case 90:
                            self.RUL.play("Rul", fromFrame=90, toFrame=60)
                            self.frameActor = 60
                        case 120:
                            self.RUL.play("Rul", fromFrame=0, toFrame=30)
                            self.frameActor = 30
                elif self.keys["d"]:
                    match self.frameActor:
                        case 0:
                            self.RUL.play("Rul", fromFrame=60, toFrame=90)
                            self.frameActor = 90
                        case 30:
                            self.RUL.play("Rul", fromFrame=30, toFrame=60)
                            self.frameActor = 60
                        case 60:
                            self.RUL.play("Rul", fromFrame=60, toFrame=90)
                            self.frameActor = 90
                        case 120:
                            self.RUL.play("Rul", fromFrame=60, toFrame=90)
                            self.frameActor = 90
                    self.rote(-0.5)

            elif self.keys["a"]:
                self.rote(0.5)
                self.numb = 0
                # Проиграет анимацию с 10-го по 30-й кадр и остановится на 30-м
                match self.frameActor:
                     case 0:
                        self.RUL.play("Rul", fromFrame=0, toFrame=30)
                        self.frameActor = 30
                     case 60:
                        self.RUL.play("Rul", fromFrame=60, toFrame=30)
                        self.frameActor = 30
                     case 90:
                        self.RUL.play("Rul", fromFrame=90, toFrame=60)
                        self.frameActor = 60
                     case 120:
                        self.RUL.play("Rul", fromFrame=0, toFrame=30)
                        self.frameActor = 30

                print("Поворот влево")
            elif self.keys["d"]:
                self.rote(-0.5)
                self.numb = 0
                print("Поворот вправо")
                match self.frameActor:
                     case 0:
                        self.RUL.play("Rul", fromFrame=60, toFrame=90)
                        self.frameActor = 90
                     case 30:
                        self.RUL.play("Rul", fromFrame=30, toFrame=60)
                        self.frameActor = 60
                     case 60:
                        self.RUL.play("Rul", fromFrame=60, toFrame=90)
                        self.frameActor = 90
                     case 120:
                        self.RUL.play("Rul", fromFrame=60, toFrame=90)
                        self.frameActor = 90

                # Проиграет анимацию с 10-го по 30-й кадр и остановится на 30-м
                #self.RUL.play("Rul", fromFrame=60, toFrame=90)

            elif self.keys["e"]:
                if self.fuel<=100:
                    self.fuel += 1
                    self.value_label['text'] = f"Fuel = {self.fuel}"
                else:
                    self.value_label['text'] = Lang[self.vah][9]
                    self.Quest = 2
                    self.T2.hide()
                    self.T3.show()
            elif self.keys["p"]:
                if self.Quest == 2:
                    self.value_label['text'] = Lang[self.vah][10]
                    #self.taskMgr.removeAll()
                    #self.taskMgr.cleanup()
                    for task in self.taskMgr.getTasks():
                        self.taskMgr.remove(task)
                    base.destroy()
                    A = App3()
                    A.load()
                    self.Quest=3


            pos = self.scene.getPos()
            # Обновляем текст метки
            #self.value_label['text'] = f"Coord: {pos}"

        else:
            self.value_label['text'] = "Game Over"
        return task.cont


    def move(self, dx, dy):
        # Изменение позиции
        # Получить вектор "вперед" (локальная ось Y)
        self.scene.setPos(self.scene, dx, 0, 0)

    def rote(self, dH):
        # Изменение позиции
        self.scene.setH(self.scene.getH() + dH)
        #self.scene.setY(self.scene.getY() + dy)

    def update_camera(self, task):
        # Получаем размеры окна
        win_w = self.win.getXSize()
        win_h = self.win.getYSize()

        # Центр экрана в пикселях
        center_x = win_w // 2
        center_y = win_h // 2

        # Получаем данные мыши напрямую от устройства ввода (а не из Node)
        md = self.win.getPointer(0)
        mouse_x = md.getX()
        mouse_y = md.getY()

        # Вычисляем смещение в пикселях относительно центра
        delta_x = mouse_x - center_x
        delta_y = mouse_y - center_y

        # Если смещение есть (даже минимальное в 1 пиксель)
        if delta_x != 0 or delta_y != 0:
            h, p, r = self.camera.getHpr()

            if self.numb==0:
                # Изменяем углы (инверсия по Y для классического управления)
                self.cam.setH(90+h - delta_x * self.camera_sens)
                self.cam.setP(-10+p - delta_y* self.camera_sens)

                print(10+h - delta_x , " / ", -110+p - delta_y)

            # Возвращаем курсор строго в центр экрана

        if self.numb==2:
            self.win.movePointer(0, center_x, center_y)
        return Task.cont


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

            if "language" in lines[1]:
                n = (lines[1][9:16])
                print('n = ', n)
            if n == "English":
                self.vah = 1
            else:
                self.vah = 0


    def spotlig(self, x,y,z, h, p, r, obj):
         # освещение конусное
        sptLight = Spotlight("spot")
        sptLens = PerspectiveLens()
        sptLight.setLens(sptLens)
        sptLight.setAttenuation(VBase3(0, 0, 0.001)) # Затухание
        sptLight.setColor(Vec4(200.0, 200.0, 100, 1))
        sptLight.setShadowCaster(True)
        # 3. Прикрепляем свет к сцене и делаем его ребенком панды
        self.slnp = self.render.attachNewNode(sptLight)
        # СВЕТ ПРИВЯЗАН К ПАНДЕ:
        self.slnp.reparentTo(obj)

        # Позиционируем свет относительно панды (например, над головой)
        self.slnp.setPos(x, y, z)# В локальных координатах модели
        #self.slnp.lookAt(self.scene) # Свет смотрит на модель
        self.slnp.setHpr(h, p, r)

        # 4. Включаем свет
        self.render.setLight(self.slnp)

    def pointlig(self, x,y,z, obj, force):
        # 2. Создаем точечный свет (PointLight)
        plight = PointLight('plight')
        plight.setColor((force, force, force/2, 1)) # Желтоватый свет
        plight.setAttenuation((0, 0.02, 0.01))

        # Создаем узел для света
        self.plnp = self.scene.attachNewNode(plight)

        # --- ВАЖНО: Привязка ---
        # Делаем свет дочерним объектом модели, чтобы он двигался вместе с ней
        self.plnp.reparentTo(obj)
        # Устанавливаем позицию света относительно модели (например, чуть выше)
        self.plnp.setPos(x, y, z)

        # 3. Применяем свет к сцене
        self.render.setLight(self.plnp)

    #Коллайдер
    def collBox(self, sce):
        # Создаем узел для коллизий куба
        box_node = CollisionNode('box_node')
        # Добавляем куб: параметры - (центр, размер_по_X, размер_по_Y, размер_по_Z)
        box_shape = CollisionBox(Point3(-15, -20, -1), 10.0, 20.0, 10.0)
        box_node.add_solid(box_shape)

        # Прикрепляем к сцене
        box_np = sce.attach_new_node(box_node)
        box_np.set_pos(0, 10, 0) # Позиция блока

         # Прикрепляем коллизию к активной модели
        self.from_coll_np = sce.attachNewNode(box_node)
        # Настраиваем маски: объект ищет цели на канале 1, сам игнорирует входящие
        self.from_coll_np.node().setFromCollideMask(BitMask32.bit(1))
        self.from_coll_np.node().setIntoCollideMask(BitMask32.allOff())

        #box_np.show() # Раскомментируйте, чтобы увидеть границы куба для отладки

        # 4. Регистрируем активный объект в обходчике
        self.cTrav.addCollider(self.from_coll_np, self.collision_queue)

    def PlayExit(self):
        base.destroy()
        sys.exit()
        #base.userExit()

    def RES(self):
        self.btn1.hide()
        self.btn0.hide()
        self.numb = 2

        self.scene.setPos(0, 0, 0)
        self.hitB = False
        self.cam.setH(94* self.camera_sens)
        self.cam.setP(2 * self.camera_sens)

    # записываем данные в файл
    def GameSave(self, n, text):
        # Имя файла
        filename = 'Save.txt'
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


