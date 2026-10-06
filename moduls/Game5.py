from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import ActorInterval, Sequence

from direct.task import Task
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import *
from panda3d.fx import FisheyeLens # импортируем фишай-линзу

from panda3d.core import SequenceNode
from panda3d.core import CardMaker, NodePath, ColorBlendAttrib
from panda3d.physics import LineParticleRenderer
from panda3d.core import BitMask32
from panda3d.core import Vec3, Vec4
import sys
from panda3d.bullet import *
from moduls.scene_base import Scene
from moduls.Game6 import App6


from panda3d.core import Texture, TextureStage

RUSB = ["Войди в дом","Принять душ", "Идти в спальню", "Нужно поспать", "Я проголодался, нужно пойти на кухню", "Приготовить завтрак",
        "Пора отправиться в кабинет дяди", "Прочитать дневник", "Нужно осмотреть чердак"]
ENGB = ["Enter the house", "Take a shower", "Go to the bedroom", "Need to sleep","I'm hungry, need to go to the kitchen", "Make breakfast",
        "Time to head to Uncle's study", "Read the diary", "Need to check the attic"]

RUSC = ["Чем я могу быть вам полезен, Джон?", "Я хотел бы поприветствовать вас в нашем городке", "Спасибо, мне очень приятно", "Я сочувствую вашей утрате и хочу предостеречь о прогулках по лесу ночью",
        "Хорошо шериф, я буду осторожен и не стану гулять по темноте", "Ваш дядя был отличным человеком, это нелепая смерть", "Да он был очень добрый, но любил одиночество", "Если что вот мой номер телефона. Хорошего вам дня"
        ]
ENGC = ["How can I help you, John?", "I wanted to welcome a new citizen to our town.", "Thank you, I appreciate it.", "I’m sorry for your loss, and I want to warn you about walking in the woods at night.",
        "All right, Sheriff; I’ll be careful and won’t walk around after dark.", "Your uncle was a great man—it was a senseless death.",
         "Yes, he was very kind, but he loved his solitude.", "Here’s my phone number, just in case. Have a good day."
         ]

LangB =[RUSB, ENGB]
LangC =[RUSC, ENGC]

DayNight = ((0, 0.05, 0.1),(0, 0.35, 0.6))

class App5(Scene, ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        # шрифт
        self.font = loader.loadFont("Roboto/Roboto-Bold.ttf")

        # 1. Создаем текстовую метку для отображения значения
        self.value_label = DirectLabel(
            text="",
            scale=0.1,
            pos=(0.2, 0, 0.65),
            text_fg=(1, 1, 1, 1),
            text_font = self.font,
            frameColor=(0, 0, 0, 0), # Прозрачный фон
            text_wordwrap=20.0,
            # Дополнительно можно выровнять текст, например, по центру
            text_align=TextNode.ACenter
        )

        # поле для диалога
        self.dialog_label = DirectLabel(
            text="",
            scale=0.1,
            pos=(-0.5, 0, -0.5),
            text_fg=(1, 1, 1, 1),
            text_font = self.font,
            frameColor=(0, 0, 0, 1), # Прозрачный фон
            text_wordwrap=20.0,
            # Дополнительно можно выровнять текст, например, по центру
            text_align=TextNode.ACenter
        )

        # Создаем лист бумаги, но сразу её скрываем (hide)
        self.interact_page = OnscreenImage(
            image='material//leaf.png', # Путь к вашей картинке (PNG/TGA)
            pos=(0, 0, 0),            # Позиция на экране (X, Y, Z)
            scale=0.5                    # Масштаб иконки
        )
        self.interact_page.hide()

        # Отключаем камеру по умолчанию (свободный режим)
        #self.disableMouse()

        # кнопка закрытия игры
        self.btnClose = DirectButton( text = "Close Game", scale=0.1, pos=(-0.8,0,0.0), frameColor=(1, 0, 0, 1), command = self.PlayExit)
        self.btnClose.hide()

        # туман и окружение_ ночь день
        self.moon = 0
        base.setBackgroundColor(DayNight[self.moon])

        # Имя тумана используется для отладки
        fog = Fog("SceneFog")

        # 2. Настраиваем цвет тумана (RGBA)
        # Здесь: светло-серый туман
        fog.setColor(0.2, 0.2, 0.1)

        # 3. Настраиваем дальность тумана (у экспоненциального тумана свои параметры)
        fog.setExpDensity(0.002) # Для экспоненциального
        # Или линейный туман (начало, конец)
        #fog.setLinearRange(0.0, 1000.0)

        # 4. Применяем туман к сцене (render)
        render.setFog(fog)

        self.numb = 2
        self.act = 0
        self.level = 0
        self.CamPOS = (0,0,0)
        self.CamHpr = (0,0,0)
        # диалог
        self.dialog = 0
        self.vah = 0
        self.n = 3
        self.newScene = False
        self.Scene = False
        self.close = False
        self.Deed1 = True
        self.Deed2 = True
        self.zombie_alive = True
        self.npc_speed = 10       # Скорость бега NPC (подберите под анимацию)
        self.stop_distance = 10.0   # Дистанция, ближе которой NPC перестанет бежать к игроку

        self.rot = self.cam.getH()

        self.FileRead()
        self.GameSave(2, "val 6")

        # привязка частиц
        # --- ОБЯЗАТЕЛЬНО ДЛЯ ЧАСТИЦ ---
        base.enableParticles() # Включает менеджер эффектов частиц
        #self.enablePhysics()   # Включает физический менеджер (убирает ошибку NoneType)

##        self.loader = loader
##        self.taskMgr = taskMgr

                # 1. Загружаем шрифт (если не загружен ранее)
        self.font = loader.loadFont("Roboto/Roboto-Bold.ttf")

        # 2. Создаем фоновую картинку заставки вместо черного фона
        # Используйте форматы PNG, JPG или TGA
        self.loading_bg = OnscreenImage(
            image='material/loading_screen.png', # Укажите ваш путь к картинке
            pos=(0, 0, 0),                       # Центр экрана
            scale=(1.333, 1, 1)                  # Пропорции (подгоните под формат окна,
                                                 # например 1.333 для 4:3 или 1.777 для 16:9)
        )

        # 3. Создаем скроллбар ПОВЕРХ картинки
        self.progress_bar = DirectWaitBar(
            parent=self.loading_bg, # Привязываем к картинке, чтобы они удалились вместе
            text="Загрузка ресурсов...",
            text_font=self.font,
            text_fg=(1, 1, 1, 1),   # Цвет текста (белый)
            text_scale=0.05,

            # Настройка внешнего вида полосы для атмосферности:
            frameColor=(0.1, 0.1, 0.1, 0.7),  # Полупрозрачный серый фон полосы (RGBA)
            barColor=(0.8, 0.2, 0.2, 1),      # Цвет заполнения (например, темно-красный)

            range=100,
            value=0,
            pos=(0, 0, -0.7),       # Смещаем полосу в самый низ экрана, чтобы не перекрывать арт
            scale=0.8
        )

        # Принудительно отрисуем первый кадр, чтобы заставка мгновенно появилась
        base.graphicsEngine.renderFrame()


        # Принудительно отрисуем один кадр, чтобы скроллбар сразу появился на экране
        base.graphicsEngine.renderFrame()


        # Список, куда будут складываться готовые текстуры
        self.fire_texture_sequence = []

        # Запускаем фоновую загрузку, чтобы окно НЕ зависало
        #self.preload_fire_textures_async()


        # речь героя
        self.speekG = base.loader.loadSfx("sound/man0.wav")
        # речь NPC
        self.speekNPC1 = base.loader.loadSfx("sound/womenvoice.mp3")
        self.speekNPC2 = base.loader.loadSfx("sound/man1.mp3")
        # настройка громкости женского голоса
        self.speekNPC1.setVolume(2)
        # тестирование проигрывание речь
        #self.speekNPC1.play()
        #self.speekNPC2.play()
        #self.speekG.play()


        # звуки напряжения и устрашения
        self.muz1 = base.loader.loadSfx("sound/whisperV.mp3")
        self.muz2 = base.loader.loadSfx("sound/vyisadka.mp3")
        self.muz3 = base.loader.loadSfx("sound/WeirdPe.mp3")
        self.muz4 = base.loader.loadSfx("sound/death_2.mp3")
        # настройка громкости женского голоса
        self.muz1.setVolume(2)

        # звук шагов
        self.stepWalk= base.loader.loadSfx("sound/Footsteps_Walk1.wav")
        self.stepWalk.setLoop(True)
        self.stepWalk.setPlayRate(0.5)
        #тест шагов
        #self.stepWalk.play()

        # Загрузка звука
        self.myMusic = base.loadMusic("sound/Mellody.wav")

        # Настройка
        self.myMusic.setVolume(0.5) # Громкость от 0 до 1
        self.myMusic.setLoop(True)  # Зациклить

        # Воспроизведение
        self.myMusic.play()

        self.progress_bar['value'] = 20 # Устанавливаем процент
        base.graphicsEngine.renderFrame() # МГНОВЕННО ОБНОВЛЯЕМ ЭКРАН

        # 1. Инициализация физического мира Bullet
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

        # Добавляем задачу обновления физики в цикл рендеринга
        self.taskMgr.add(self.updatePhysics, "UpdatePhysics")


        house_shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        house_node = BulletRigidBodyNode("House")
        house_node.addShape(house_shape)
        # Говорим движку сообщать о контактах с полом
        house_node.notify_collisions(True)

        house_np = self.render.attachNewNode(house_node)
        house_np.setPos(0, 0, -10)
        self.world.attachRigidBody(house_node)

        # --- ЗАГРУЗКА ВСЕХ 250 ОПТИМИЗИРОВАННЫХ КАДРОВ ---
        self.fire_texture_sequence = []
        for i in range(1, 251):
            texture_name = f"material/m/fire{i:04d}.png"
            try:
                # Теперь картинки весят по 60 КБ, загрузка займет доли секунды!
                tex = self.loader.loadTexture(texture_name)
                self.fire_texture_sequence.append(tex)
            except OSError:
                pass
        print(f"--> Огонь успешно инициализирован. Загружено кадров: {len(self.fire_texture_sequence)}")

        self.progress_bar['value'] = 30 # Устанавливаем процент
        base.graphicsEngine.renderFrame() # МГНОВЕННО ОБНОВЛЯЕМ ЭКРАН

        # Создание персонажа (модель + физика)
        height = 17.5
        radius = 4

        # Задаем форму для обнаружения столкновений
        shape = BulletCapsuleShape(radius, height - 2 * radius, ZUp)

        # Создаем контроллер персонажа
        self.char_node = BulletCharacterControllerNode(shape, 0.4, "Player")
        self.char_node.setGravity(9.81)
        self.char_node.setMaxSlope(45.0) # Максимальный угол подъема по лестнице/склону

        # Добавляем ноду в физический мир
        self.char_np = self.render.attachNewNode(self.char_node)
        self.char_np.setPos(-50, -30, 10)
        self.world.attachCharacter(self.char_node)

        # 3. Привязка вашей 3D-модели (например, Actor'а) к физической ноде
        self.actor = Actor("model/Animetion_Gero.glb")
        self.actor.setScale(10)
        self.actor.reparentTo(self.char_np)
        self.actor.setZ(-8)

        self.posCh = self.char_np.get_pos(self.render)

        # анимация IDLE
        self.actor.loop("AnimMan", fromFrame=0, toFrame=133)

        # Включаем блендинг для плавных переходов
        self.actor.enableBlend()

        # Переменная, чтобы помнить, какая анимация СЕЙЧАС играет
        self.current_state = ""

        # Смещение камеры
        # self.cam.reparentTo(self.render)
        self.cam.reparentTo(self.char_np)
        self.cam.setPos(0, 20, 10)
        self.cam.setH(180)

        # пещера
        self.house: NodePath = self.loader.loadModel("model//Cave1.glb")
        self.house.setPos(10, 0, -10)
        self.house.setScale(10)
        self.house.reparentTo(render)
        self.house.flattenLight()
        # создание сложного коллайдера дома
        self.MeshCol(self.house)


        self.progress_bar['value'] = 55 # Устанавливаем процент
        base.graphicsEngine.renderFrame() # МГНОВЕННО ОБНОВЛЯЕМ ЭКРАН

##        # Триггеры сцены
        #self.door = self.BoxTrigger(0, 0, 10, 30, 10, 20, 0, 0, 0 , "Door")
        self.BoxTrigger(-220, -210, -10, 10, 10, 10, 0, 0, 0 , "OUTPUT")
        self.BoxTrigger(-600, 50, -10, 100, 30, 30, 0, 0, 0 , "Cave")

        # Зомби
        self.Zomb1 = Actor("model/ZOMBI1.glb")
        self.Zomb1.setScale(12)
        self.Zomb1.reparentTo(render)
        self.Zomb1.setPos(-160, -225, -10)
        self.Zomb1.setHpr(90, 0, 0)
        self.branch_collider1=self.KinematicColl(self.Zomb1)
        # 1. Задаем ОДНО ТОЧНОЕ имя трека, который мы хотим запустить
        self.target_anim = "menl_vrag2.001|mixamo.com|Layer0"

        # Запускаем анимацию в бесконечный цикл движения
        self.Zomb1.loop(self.target_anim, fromFrame=0, toFrame=123)
        self.Zomb1.getGeomNode().node().setFinal(True)
        self.Zomb1.update()

        # ветка1
        self.Zomb2 = Actor("model/ZOMBI2.glb")
        # привязка модели к кости NPC
        attach_joint2 = self.Zomb1.exposeJoint(None, "modelRoot", "spine_02")

        # 4. Привязываем ветви к этой кости
        self.Zomb2.reparentTo(attach_joint2)
        self.Zomb2.setScale(render, 0.1)
        self.Zomb2.setHpr(180, 40, 45)
        self.Zomb2.setPos(0.4, 0.1, 0)

        # 1. Задаем ОДНО ТОЧНОЕ имя трека, который мы хотим запустить
        self.target_anim = "Armature|Armature|Armature|ArmatureAction"

        # 2. Запускаем анимацию в бесконечный цикл
        self.Zomb2.loop(self.target_anim)
        self.Zomb2.getGeomNode().node().setFinal(True)
        self.Zomb2.update()

        # ветка2
        self.Zomb3 = Actor("model/ZOMBI3.glb")
        #attach_joint3 = self.Zomb1.controlJoint(None, "modelRoot", "head")
        attach_joint3 = self.Zomb1.exposeJoint(None, "modelRoot", "head")

        # 4. Привязываем ветви к этой кости
        self.Zomb3.reparentTo(attach_joint3)
        self.Zomb3.setScale(render, 0.05)
        self.Zomb3.setHpr(180, 40, 45)
        self.Zomb3.setPos(0.4, 0.1, -2)

        # 1. Задаем ОДНО ТОЧНОЕ имя трека, который мы хотим запустить
        self.target_anim = "Armature|Armature|Armature|ArmatureAction.001"

        # 2. Запускаем анимацию в бесконечный цикл
        self.Zomb3.loop(self.target_anim)
        self.Zomb3.getGeomNode().node().setFinal(True)
        self.Zomb3.update()

        # ветка3
        self.Zomb4 = Actor("model/ZOMBI4.glb")
        #attach_joint4 = self.Zomb1.controlJoint(None, "modelRoot", "head")
        attach_joint4 = self.Zomb1.exposeJoint(None, "modelRoot", "head")
        # 4. Привязываем ветви к этой кости
        self.Zomb4.reparentTo(attach_joint4)
        self.Zomb4.setScale(render, 0.05)
        self.Zomb4.setHpr(180, 40, 45)
        self.Zomb4.setPos(0.4, 0.1, -2)

        # 1. Задаем ОДНО ТОЧНОЕ имя трека, который мы хотим запустить
        self.target_anim = "Armature|Armature|Armature|ArmatureAction.001"

        # 2. Запускаем анимацию в бесконечный цикл
        self.Zomb4.loop(self.target_anim)
        self.Zomb4.getGeomNode().node().setFinal(True)
        self.Zomb4.update()

        self.progress_bar['value'] = 75 # Устанавливаем процент
        base.graphicsEngine.renderFrame() # МГНОВЕННО ОБНОВЛЯЕМ ЭКРАН

        # Зомби 2
        self.Zomb11 = Actor("model/ZOMBI1.glb")
        self.Zomb11.setScale(12)
        self.Zomb11.reparentTo(render)
        self.Zomb11.setPos(-700, 100, -10)
        self.Zomb11.setHpr(90, 0, 0)
        self.branch_collider1=self.KinematicColl(self.Zomb11)
        # 1. Задаем ОДНО ТОЧНОЕ имя трека, который мы хотим запустить
        self.target_anim1 = "menl_vrag2.001|mixamo.com|Layer0"

        # Запускаем анимацию в бесконечный цикл движения
        self.Zomb11.loop(self.target_anim1, fromFrame=0, toFrame=123)
        self.Zomb11.getGeomNode().node().setFinal(True)
        self.Zomb11.update()

        # ветка1
        self.Zomb21 = Actor("model/ZOMBI2.glb")
        # привязка модели к кости NPC
        attach_joint21 = self.Zomb11.exposeJoint(None, "modelRoot", "spine_02")

        # 4. Привязываем ветви к этой кости
        self.Zomb21.reparentTo(attach_joint21)
        self.Zomb21.setScale(render, 0.1)
        self.Zomb21.setHpr(180, 40, 45)
        self.Zomb21.setPos(0.4, 0.1, 0)

        # 1. Задаем ОДНО ТОЧНОЕ имя трека, который мы хотим запустить
        self.target_anim1 = "Armature|Armature|Armature|ArmatureAction"

        # 2. Запускаем анимацию в бесконечный цикл
        self.Zomb21.loop(self.target_anim1)
        self.Zomb21.getGeomNode().node().setFinal(True)
        self.Zomb21.update()

        # ветка2
        self.Zomb31 = Actor("model/ZOMBI3.glb")
        #attach_joint3 = self.Zomb1.controlJoint(None, "modelRoot", "head")
        attach_joint31 = self.Zomb11.exposeJoint(None, "modelRoot", "head")

        # 4. Привязываем ветви к этой кости
        self.Zomb31.reparentTo(attach_joint31)
        self.Zomb31.setScale(render, 0.05)
        self.Zomb31.setHpr(180, 40, 45)
        self.Zomb31.setPos(0.4, 0.1, -2)

        # 1. Задаем ОДНО ТОЧНОЕ имя трека, который мы хотим запустить
        self.target_anim1 = "Armature|Armature|Armature|ArmatureAction.001"

        # 2. Запускаем анимацию в бесконечный цикл
        self.Zomb31.loop(self.target_anim1)
        self.Zomb31.getGeomNode().node().setFinal(True)
        self.Zomb31.update()

        # ветка3
        self.Zomb41= Actor("model/ZOMBI4.glb")
        #attach_joint4 = self.Zomb1.controlJoint(None, "modelRoot", "head")
        attach_joint41 = self.Zomb11.exposeJoint(None, "modelRoot", "head")
        # 4. Привязываем ветви к этой кости
        self.Zomb41.reparentTo(attach_joint41)
        self.Zomb41.setScale(render, 0.05)
        self.Zomb41.setHpr(180, 40, 45)
        self.Zomb41.setPos(0.4, 0.1, -2)

        # 1. Задаем ОДНО ТОЧНОЕ имя трека, который мы хотим запустить
        self.target_anim1 = "Armature|Armature|Armature|ArmatureAction.001"

        # 2. Запускаем анимацию в бесконечный цикл
        self.Zomb41.loop(self.target_anim1)
        self.Zomb41.getGeomNode().node().setFinal(True)
        self.Zomb41.update()

        self.progress_bar['value'] = 95 # Устанавливаем процент
        base.graphicsEngine.renderFrame() # МГНОВЕННО ОБНОВЛЯЕМ ЭКРАН

        # корни/ветки
         # Привязка 3D-модели (например, Actor'а)
        self.base1 = Actor("model/BASe1.glb")
        #self.base1:NodePath = self.loader.loadModel("model/BASe1.glb")
        self.base1.setScale(10)
        self.base1.setPos(-700, 100, -10)
        self.base1.setH(-90)
        self.base1.reparentTo(render)
        self.base1.loop("Armature|Armature|ArmatureAction")
        self.base1.setLightOff()
        self.branch_collider1=self.KinematicColl(self.base1)
        # 3. СРАЗУ СКРЫВАЕМ И ВЫКЛЮЧАЕМ (пока акт не равен 22)
        #self.base1.hide()  # Прячем визуальную модель
        self.world.removeRigidBody(self.branch_collider1)  # Отключаем физику


        # Привязка 3D-модели (например, Actor'а)
        self.base2 = Actor("model/BASe1.glb")
        #self.base1:NodePath = self.loader.loadModel("model/BASe1.glb")
        self.base2.setScale(10)
        self.base2.setPos(-700, 150, -10)
        self.base2.setH(-90)
        self.base2.reparentTo(render)
        # Создаем интервал для конкретного диапазона кадров
        anim_interval = self.base2.actorInterval(
            "Armature|Armature|ArmatureAction",
            startFrame=250,
            endFrame=0
        )

        # Оборачиваем в Sequence и зацикливаем (loop)
        self.base2_loop = Sequence(anim_interval)
        self.base2_loop.loop()
        self.base2.setLightOff()
        self.branch_collider2=self.KinematicColl(self.base2)
        # 3. СРАЗУ СКРЫВАЕМ И ВЫКЛЮЧАЕМ (пока акт не равен 22)
        #self.base2.hide()  # Прячем визуальную модель
        self.world.removeRigidBody(self.branch_collider2)  # Отключаем физику

        # Привязка 3D-модели (например, Actor'а)
        self.base3 = Actor("model/BASe1.glb")
        #self.base1:NodePath = self.loader.loadModel("model/BASe1.glb")
        self.base3.setScale(10)
        self.base3.setPos(-750, 0, -10)
        self.base3.setH(-90)
        self.base3.reparentTo(render)
        self.base3.loop("Armature|Armature|ArmatureAction")
        self.base3.setLightOff()
        self.branch_collider3=self.KinematicColl(self.base3)
        #self.base3.hide()  # Прячем визуальную модель
        self.world.removeRigidBody(self.branch_collider3)



        # корни/ветки
         # Привязка 3D-модели (например, Actor'а)
        self.base4 = Actor("model/BASe1.glb")
        #self.base1:NodePath = self.loader.loadModel("model/BASe1.glb")
        self.base4.setScale(10)
        self.base4.setPos(-750, 50, -10)
        self.base4.setH(-90)
        self.base4.reparentTo(render)
        # Создаем интервал для конкретного диапазона кадров
        anim_interval = self.base4.actorInterval(
            "Armature|Armature|ArmatureAction",
            startFrame=250,
            endFrame=0
        )

        # Оборачиваем в Sequence и зацикливаем (loop)
        self.base4_loop = Sequence(anim_interval)
        self.base4_loop.loop()
        self.base4.setLightOff()
        self.branch_collider4=self.KinematicColl(self.base4)

        #self.base4.hide()  # Прячем визуальную модель
        self.world.removeRigidBody(self.branch_collider4)

        # Привязка 3D-модели (например, Actor'а)
        self.base5 = Actor("model/BASe1.glb")
        #self.base1:NodePath = self.loader.loadModel("model/BASe1.glb")
        self.base5.setScale(10)
        self.base5.setPos(-720, 70, -10)
        self.base5.setH(90)
        self.base5.reparentTo(render)
        self.base5.loop("Armature|Armature|ArmatureAction")
        self.base5.setLightOff()
        self.branch_collider5=self.KinematicColl(self.base5)
        #self.base5.hide()  # Прячем визуальную модель
        self.world.removeRigidBody(self.branch_collider5)


        # Привязка 3D-модели (например, Actor'а)
        self.base6 = Actor("model/BASe1.glb")
        #self.base1:NodePath = self.loader.loadModel("model/BASe1.glb")
        self.base6.setScale(10)
        self.base6.setPos(-650, 60, -10)
        self.base6.setH(90)
        self.base6.reparentTo(render)
        self.base6.loop("Armature|Armature|ArmatureAction")
        self.base6.setLightOff()
        # создание сложного коллайдера дома
        self.branch_collider6=self.KinematicColl(self.base6)
        #self.base6.hide()  # Прячем визуальную модель
        self.world.removeRigidBody(self.branch_collider6)


        # Привязка 3D-модели (например, Actor'а)
        self.flower = Actor("model/Flowers1.glb")
        #self.base1:NodePath = self.loader.loadModel("model/BASe1.glb")
        self.flower.setScale(15)
        self.flower.setPos(-600, 60, -8)
        self.flower.reparentTo(render)
        self.flower.setLightOff()
        # создание сложного коллайдера дома



        # Заведем флаг-маркер, чтобы включить ветку только один раз
        self.branch_activated = False


        # --- БЛОК ДИАГНОСТИКИ (Пожалуйста, пришлите то, что он выведет!) ---
        print("\n=== НАЧАЛО ДИАГНОСТИКИ PANDA3D ===")

##        # Проверяем реальное число кадров именно у target_anim
##        total_frames = self.base1.getNumFrames("Armature|Armature|ArmatureAction")
##        print(f"1. Количество кадров в треке '{self.target_anim}': {total_frames}")
##
##        # Выводим ВСЕ доступные треки, которые Panda3D смогла прочитать из файла
##        all_anims = self.base1.getAnimNames()
##        print(f"2. Все доступные треки в модели: {all_anims}")

##        # Проверяем, считает ли сам движок, что анимация проигрывается в памяти
##        controls = self.people2.getAnimControls(target_anim)
##        is_playing = controls.isPlaying() if controls else "Ошибка: трек не найден в памяти"
##        print(f"3. Статус воспроизведения в памяти: {is_playing}")

        print("=== КОНЕЦ ДИАГНОСТИКИ ===\n")

        self.progress_bar['value'] = 100 # Устанавливаем процент
        base.graphicsEngine.renderFrame() # МГНОВЕННО ОБНОВЛЯЕМ ЭКРАН

        # рассеянное освещение
        ambLight = AmbientLight("ambient")
        ambLight.setColor(Vec4(0.8, 0.8, 0.85, 0.7))
        # установка нового узла света
        ambNode = render.attachNewNode(ambLight)
        render.setLight(ambNode)

         # Инициализация фильтров
        self.filters = CommonFilters(base.win, base.cam)

        # Включение Bloom (эффект свечения)
        self.filters.setBloom()

        # Другие популярные фильтры:
        #filters.setCartoonInk(0.5, (0.1,1,0.2,1)) # Эффект комикса (обводка)
        #filters.setAmbientOcclusion() # Screen-space Ambient Occlusion (SSAO)
        self.filters.setBlurSharpen(amount=0.8) # Размытие или резкость
        self.filters.setGammaAdjust(1.1) #Гамма


        # освещение заправки
        #self.spotlig(-200, -200, 50, 0, -35, 0, self.house)
        #self.spotlig(-70, -260, 15, 0, 0, 0, self.ground)

        self.p1 = self.pointlig(-600, 100, 25, self.house, 50)
        self.p2 = self.pointlig(-700, 50, 30, self.house, 100)
        self.p3 = self.pointlig(-600, -30, 65, self.house, 100)

        self.BoxC(-100,-600,0, 3000, 2,15, 0, 0, 0 , Name = "House")
        self.Barier2 = self.BoxC(0,-300,0, 2, 2000,15, 0, 0, 0 , Name = "House")

        self.BoxC(-800,-300,0, 2, 2000,15, 0, 0, 0 , Name = "House")
        self.BoxC(0, 300,0, 5000, 2,15, 0, 0, 0 , Name = "House")

        #self.create_rain()
##        # Создаст коробку дождя 80х80 метров и высотой 50 метров вокруг игрока
##        self.rain_system = TextureRain(player=self.char_np, area_size=80.0, rain_height=50.0)

        # 1. Создаем ноду визуальной отладки
        debug_node = BulletDebugNode("Debug")
        debug_node.showWireframe(True)       # Показывать сетку столкновений
        debug_node.showConstraints(True)     # Показывать ограничения (если есть)
        #debug_node.showBoundingBoxes(False)  # Скрыть габаритные контейнеры (чтобы не спамить)

        # 2. Привязываем её к сцене
        debug_np = self.render.attachNewNode(debug_node)
        debug_np.show()

        # 3. Передаем ноду отладки в физический мир Bullet
        self.world.setDebugNode(debug_np.node())

         # 3. Словарь для отслеживания состояния клавиш
        self.key_map = {"forward": False, "backward": False, "left": False, "right": False }

        # Привязка клавиш (Event Handling)
        self.accept("w", self.set_key, ["forward", True])
        self.accept("w-up", self.set_key, ["forward", False])
        self.accept("s", self.set_key, ["backward", True])
        self.accept("s-up", self.set_key, ["backward", False])
        self.accept("a", self.set_key, ["left", True])
        self.accept("a-up", self.set_key, ["left", False])
        self.accept("d", self.set_key, ["right", True])
        self.accept("d-up", self.set_key, ["right", False])
        self.accept("e", self.on_space_pressed)
        self.accept("escape", self.close_game)


        # Скорость движения и поворота
        self.move_speed = 25.0
        self.turn_speed = 90.0 # Градусов в секунду

        self.camera_sens = 0.1 # Чувствительность
        # 4. Запуск цикла обновлений
        self.taskMgr.add(self.update, "UpdatePhysicsAndMovement")
        # Запускаем задачу во фрейме PostRender или Late, чтобы окно успело обновиться
        self.taskMgr.add(self.update_camera, "UpdateCameraTask")

        self.accept('mouse3', self.shoot_sphere)

        # Список, где мы будем хранить летящие сферы и их направления
        self.flying_spheres = []

        # === КОНЕЦ ЗАГРУЗКИ ===
        # Удаляем экран загрузки, когда всё готово
        self.loading_bg.destroy()

        # Не забываем запустить постоянную задачу для обновления движения сфер
        #self.taskMgr.add(self.update_spheres_task, "UpdateSpheres")



    def updatePhysics(self, task):
        dt = globalClock.getDt()
        self.world.doPhysics(dt)

        print(self.act, " act")
        print(self.level, " level")

        # 2. Проверяем контакты КОНКРЕТНО для нашего игрока
        result = self.world.contactTest(self.char_node)

        # 2. Проверяем контакты КОНКРЕТНО для нашего игрока
        result = self.world.contactTest(self.char_node)

        # 3. Если контакты есть, перебираем их
        if result.getNumContacts() > 0:
            for contact in result.getContacts():
                # Получаем узел, с которым столкнулся игрок
                node0 = contact.getNode0()
                node1 = contact.getNode1()

                # Находим, какой из узлов НЕ является игроком
                other_node = node1 if node0 == self.char_node else node0

                # Печатаем имя объекта, которого коснулись
                #print(f"Игрок касается объекта: {other_node.getName()}")
                if other_node.getName() == "OUTPUT":
                     self.act =1
                     self.value_label['text'] = "Тут Зомби"
                     self.muz2.play()
                     self.Deed1=False
                     self.level=0

                if other_node.getName() == "Cave":
                     self.act = 2
                     self.value_label['text'] = "Ты будешь с нами. Стань одним из нас!"
                     self.muz1.play()
                     self.Deed2=False

                     if self.level==0:
                        self.level=1
                        self.BoxTrigger(0, 0, 10, 30, 10, 20, 0, 0, 0 , "Door")



##                if other_node.getName() == "Door":
##                    print("Игрок коснулся пещеры. Переходим в App6...")
##                    self.taskMgr.destroy()
##
##                    # 3. Закрываем текущее окно
##                    base.destroy()
##                    # Полностью стираем старый контекст, чтобы освободить звуковую карту и шину GPU
##                    import builtins
##                    if hasattr(builtins, 'base'):
##                        del builtins.base
##
##                    A = App6()
##                    A.load()
                if other_node.getName() == "Door":
                    print("Игрок коснулся пещеры. Переходим в App6 через новый процесс...")

                    import subprocess
                    import sys
                    import os

                    # 1. Запускаем Game6.py в новом, абсолютно чистом процессе Python
                    # Передаем sys.executable (путь к вашему Python) и путь к файлу скрипта
                    script_path = os.path.join("moduls", "Game6.py") # проверьте правильность пути к Game6.py
                    subprocess.Popen([sys.executable, script_path])

                    self.taskMgr.destroy()
                    base.destroy()

                    # 2. Мгновенно убиваем текущий процесс App5 с физикой, очищая всю память
                    sys.exit()



        # Обходим все зафиксированные физические контакты игрока
        for contact in result.getContacts():
            # Извлекаем оба узла, участвующих в столкновении
            n0 = contact.getNode0()
            n1 = contact.getNode1()

            # Нам нужен тот узел, который НЕ является нашим игроком
            other_node = n1 if n0 == self.char_node else n0

            # Проверяем имя коллайдера ветки
            if other_node.getName() == "Base1":
                print("Игрок коснулся анимированной ветки Base1!")

                # Ваша логика (например, вывод текста на экран):
                self.dialog_label['text'] = "Вас обратили в зомби"
                self.char_np.setPos(-50, -30, 10)
                break # Выходим из цикла, так как касание уже зафиксировано


        return task.cont

    def on_space_pressed(self):
        # Находим узел по имени (например, 'my_collider_name')
        collider_np = render.find("**/B")

        if self.act == 3 and self.level<3:
            pass
##            self.KAN.hide()
##            self.value_label['text'] = "Кто-то проник во двор"
##            self.dialog_label['text'] = "Нажмите ПКМ, чтобы облить бензином зомби."
##            self.Deed =False
##            self.level=2
##            self.Zomb1.show()
##            self.Zomb2.show()
##            self.Zomb3.show()
##            self.Zomb4.show()

##        if self.act == 3 and self.level ==3:
##            self.act=4

        # переход на новую сцену
        if self.newScene == True and self.numb ==3:
            for task in self.taskMgr.getTasks():
                self.taskMgr.remove(task)
            base.destroy()
            A = App6()
            A.load()

    def close_game(self):
        self.close = not self.close
        if self.close ==True:
            self.btnClose.show()
            self.numb =1
        else:
            self.btnClose.hide()
            self.numb =0

    def PlayExit(self):
        for task in self.taskMgr.getTasks():
            self.taskMgr.remove(task)
        base.destroy()
        sys.exit()

    def set_key(self, key, value):
        """Записывает, нажата клавиша или отпущена"""
        self.key_map[key] = value

    def update(self, task):
        dt = globalClock.getDt()
        move_vec = Vec3(0, 0, 0)
        new_state = "idle"

        # Поворот персонажа (A/D)
        if self.key_map["left"]:
            new_state = "turn_left"
            self.numb=0
            #self.char_np.setH(self.char_np.getH() + self.turn_speed * dt)
            move_vec.setX(self.move_speed)
        if self.key_map["right"]:
            new_state = "turn_right"
            self.numb=0
            move_vec.setX(-self.move_speed)
            #self.char_np.setH(self.char_np.getH() - self.turn_speed * dt)

        # Движение вперед/назад (W/S) относительно направления персонажа

        if self.key_map["forward"]:
            new_state = "walk"
            self.numb=0
            move_vec.setY(-self.move_speed)
        if self.key_map["backward"]:
            new_state = "walk_back"
            self.numb=0
            move_vec.setY(self.move_speed)

        # Передаем вектор движения в Bullet (respect_camera=True учитывает поворот ноды)
        #self.char_node.setLinearMovement(move_vec, respect_camera=True)
        self.char_node.set_linear_movement(move_vec, True)

        # Возвращает объект Point3(x, y, z) в глобальных координатах сцены (render)
        global_pos = self.char_np.get_pos(self.render)

        if self.act == 4:
            self.value_label['text'] = "Электричество появилось. Возвращайтесь домой"

        # ==========================================================
        # ЛОГИКА ПРЕСЛЕДОВАНИЯ: NPC (people2) идет за игроком (char_np)
        # ==========================================================
        # Начинаем погоню/сопровождение, например, с 3-го акта (настройте под сюжет)
        if self.act == 1 and hasattr(self, 'Zomb1') and hasattr(self, 'char_np') and self.Deed1 == False: # and getattr(self, 'zombie_alive', True):

            # 1. Получаем позиции игрока и NPC в глобальных координатах
            player_pos = self.char_np.getPos(render)
            npc_pos = self.Zomb1.getPos(render)

            # 2. Считаем вектор направления от NPC к игроку
            direction = player_pos - npc_pos
            # Оставляем движение только на плоскости XY (чтобы NPC не взлетал/не смотрел в землю)
            direction.setZ(0)

            # Вычисляем расстояние между ними
            distance = direction.length()

            self.dialog_label['text']= f"Дистанция до NPC: {distance:.2f}"

            # 3. Если игрок отошел дальше, чем stop_distance — NPC идет к нему
            if self.stop_distance < distance < self.stop_distance+200:
                # Нормализуем вектор (делаем его длину равной 1), чтобы скорость была равномерной
                direction.normalize()

                # Поворачиваем NPC лицом к игроку
                self.Zomb1.lookAt(player_pos)
                # Корректируем наклон головы, чтобы NPC смотрел ровно перед собой
                self.Zomb1.setP(0)
                self.Zomb1.setR(0)
                self.Zomb1.setH(self.Zomb1.getH() + 180)

                # Вычисляем новую позицию шага
                new_pos = npc_pos + direction * self.npc_speed * dt
                self.Zomb1.setPos(render, new_pos)


            else:
                # Игрок близко — NPC останавливается и переходит в Idle-анимацию
                pass

        if self.act == 2 and hasattr(self, 'Zomb11') and hasattr(self, 'char_np') and self.Deed2 == False: # and getattr(self, 'zombie_alive', True):

            # 1. Получаем позиции игрока и NPC в глобальных координатах
            player_pos = self.char_np.getPos(render)
            npc_pos = self.Zomb11.getPos(render)

            # 2. Считаем вектор направления от NPC к игроку
            direction = player_pos - npc_pos
            # Оставляем движение только на плоскости XY (чтобы NPC не взлетал/не смотрел в землю)
            direction.setZ(0)

            # Вычисляем расстояние между ними
            distance = direction.length()

            self.dialog_label['text']= f"Дистанция до NPC: {distance:.2f}"

            # 3. Если игрок отошел дальше, чем stop_distance — NPC идет к нему
            if self.stop_distance < distance < self.stop_distance+200:
                # Нормализуем вектор (делаем его длину равной 1), чтобы скорость была равномерной
                direction.normalize()

                # Поворачиваем NPC лицом к игроку
                self.Zomb11.lookAt(player_pos)
                # Корректируем наклон головы, чтобы NPC смотрел ровно перед собой
                self.Zomb11.setP(0)
                self.Zomb11.setR(0)
                self.Zomb11.setH(self.Zomb1.getH() + 180)

                # Вычисляем новую позицию шага
                new_pos = npc_pos + direction * self.npc_speed * dt
                self.Zomb11.setPos(render, new_pos)


            else:
                # Игрок близко — NPC останавливается и переходит в Idle-анимацию
                pass


        # Этот блок находится внутри вашего таска update
        if self.Deed1 == True and self.act == 1:

           # ОБЯЗАТЕЛЬНО сбрасываем флаг сразу, чтобы код сработал строго 1 раз!
            #self.Deed = False

            # ГЛАВНОЕ РЕШЕНИЕ: ставим флаг, который навсегда заблокирует блок погони выше
            self.zombie_alive = False

            # Удаляем физику
            if hasattr(self, 'branch_collider1') and self.branch_collider1:
                self.world.removeRigidBody(self.branch_collider1)

            self.Zomb1.setHpr(0, 45, 90)
            # Переключаем анимацию через loop на ваши проверенные кадры
            self.Zomb1.loop(self.target_anim, fromFrame=130, toFrame=300)
            self.Zomb1.getGeomNode().node().setFinal(True)
            self.Zomb1.update()

            # Скрываем остальных зомби
##            self.Zomb2.hide()
##            self.Zomb3.hide()
##            self.Zomb4.hide()

            # Таймер скрытия (170 кадров при 30 FPS ~ 5.6 секунд)
            def hide_zombie_callback(task):
                if not self.Zomb1.isEmpty():
##                    self.Zomb1.hide()
                    self.Zomb1.stop()
                return task.done

            self.taskMgr.doMethodLater(5.6, hide_zombie_callback, "HideZombieTask")

        # Этот блок находится внутри вашего таска update
        if self.Deed2 == True and self.act == 2:

            # Удаляем физику
            if hasattr(self, 'branch_collider1') and self.branch_collider1:
                self.world.removeRigidBody(self.branch_collider1)

            self.Zomb11.setHpr(0, 45, 90)
            # Переключаем анимацию через loop на ваши проверенные кадры
            self.Zomb11.loop(self.target_anim, fromFrame=130, toFrame=300)
            self.Zomb11.getGeomNode().node().setFinal(True)
            self.Zomb11.update()

            # Таймер скрытия (170 кадров при 30 FPS ~ 5.6 секунд)
            def hide_zombie_callback(task):
                if not self.Zomb11.isEmpty():
                    self.Zomb11.stop()
                return task.done

            self.dialog_label['text']= f"Нужно срочно выбираться от сюда. Иначу я стану как они."

            self.taskMgr.doMethodLater(5.6, hide_zombie_callback, "HideZombieTask")



        # 2. Если состояние изменилось — переключаем диапазон кадров
        if new_state != self.current_state:
            self.current_state = new_state
            print (new_state)

            # Запоминаем новое состояние
            self.current_state = new_state

            # Сначала полностью останавливаем анимацию, очищая старые границы
            self.actor.stop()

            if new_state == "idle":
                self.actor.loop("AnimMan",
                fromFrame=0, toFrame=133)
                self.stepWalk.stop()

            elif new_state == "walk":
                self.actor.loop(
                "AnimMan",
                fromFrame=150, toFrame=180)
                self.stepWalk.play()

            elif new_state == "walk_back":
                self.actor.loop(
                "AnimMan",
                 fromFrame=192, toFrame=230)
                self.stepWalk.play()

            elif new_state == "turn_left":
                self.actor.loop(
                "AnimMan",
                 fromFrame=295, toFrame=328)
                self.stepWalk.play()

            elif new_state == "turn_right":
                self.actor.loop(
                "AnimMan",
                fromFrame=250, toFrame=283)
                self.stepWalk.play()

        #print(global_pos)
        # Шаг физического мира
        self.world.doPhysics(dt)
        return task.cont

    # коллайдер параллелепипед
    def BoxC(self, x,y,z, sx, sy,sz, rz, ry, rx , Name = "House"):
        # Для простоты используем форму коробки (для стен используйте TriMesh)
        house_shape = BulletBoxShape(Vec3(sx, sy, sz))
        house_node = BulletRigidBodyNode(Name)
        house_node.addShape(house_shape)
        house_np = self.render.attachNewNode(house_node)
        house_np.setPos(x, y, z)
        house_np.set_hpr(rz, ry, rx) #
        self.world.attachRigidBody(house_node)
        house_node.notify_collisions(True)

        # ВАЖНО: возвращаем этот узел наружу!
        return house_np

    # триггер
    def BoxTrigger(self, x,y,z, sx, sy,sz, rz, ry, rx , Name = "House"):
        # Для простоты используем форму коробки (для стен используйте TriMesh)
        house_shape = BulletBoxShape(Vec3(sx, sy, sz))
        house_node = BulletGhostNode(Name)
        house_node.addShape(house_shape)
        house_np = self.render.attachNewNode(house_node)
        house_np.setPos(x, y, z)
        house_np.set_hpr(rz, ry, rx) #
        self.world.attachGhost(house_node)


    # сложный коллайдер
    def MeshCol(self, obj, Name = "ComplexMeshBody"):
        # 3. Подготавливаем полигональную сетку (Triangle Mesh)
        mesh = BulletTriangleMesh()

        # Извлекаем геометрию из загруженного узла модели
        for geom_node in obj.findAllMatches('**/+GeomNode'):
            geom = geom_node.node().getGeom(0)
            if geom:
                mesh.addGeom(geom) # Добавляем геометрию в меш Bullet

        # 4. Создаем физическую форму (Shape) на основе меша
        # dynamic=False для статических объектов (уровни, стены), True — для динамических
        shape = BulletTriangleMeshShape(mesh, dynamic=False)

        # 5. Создаем физический узел тела и привязываем к нему форму
        body_node = BulletRigidBodyNode(Name)
        body_node.addShape(shape)
        body_node.notify_collisions(True)

        # Делаем тело статическим (масса = 0)
        body_node.setMass(0)

        # Привязываем физический узел к дереву сцены
        body_np = render.attachNewNode(body_node)
        body_np.setPos(obj.getPos())
        body_np.setHpr(obj.getHpr())

        # Прикрепляем визуальную модель к физическому телу для симуляции
        #obj.reparentTo(body_np)

        self.world.attachRigidBody(body_node)

    def KinematicColl(self, obj, Name = "Base1"):
        # Предположим, из listJoints() мы узнали, что главная гнущаяся часть называется 'Bone.001'
        joint_name = 'Root'

        # 1. Находим кость в модели
        joint_np = obj.exposeJoint(None, 'modelRoot', joint_name)

        # 2. Создаем для нее простую форму (например, коробку шириной 2, длиной 2, высотой 10)
        # Размеры подбирайте под визуальный размер части ветки
        box_shape = BulletBoxShape((5, 5, 20))

        body_node = BulletRigidBodyNode(Name)
        body_node.addShape(box_shape)
        body_node.setKinematic(True) # Обязательно кинематический!

        # 3. Привязываем физический узел прямо к кости ветки
        bone_collider_np = joint_np.attachNewNode(body_node)

        # Добавляем в физический мир
        self.world.attachRigidBody(body_node)

        return body_node


    def update_camera(self, task):
        # Если запущен диалог или управление заблокировано, ничего не делаем
        if self.dialog != 0:
            return Task.cont

        # Получаем размеры окна
        win_w = self.win.getXSize()
        win_h = self.win.getYSize()

        # Центр экрана в пикселях
        center_x = win_w // 2
        center_y = win_h // 2

        # Получаем данные мыши напрямую
        md = self.win.getPointer(0)
        mouse_x = md.getX()
        mouse_y = md.getY()

        # Вычисляем смещение относительно центра
        delta_x = mouse_x - center_x
        delta_y = mouse_y - center_y

        # Если мышь сдвинулась и активен нужный режим (numb == 0)
        if self.numb == 0:
            if delta_x != 0 or delta_y != 0:
                # 1. Поворачиваем персонажа по горизонтали с учетом чувствительности
                char_h = self.char_np.getH()
                new_char_h = char_h - delta_x * self.camera_sens
                self.char_np.setH(new_char_h)

                # 2. Получаем текущие углы камеры для изменения наклона (Pitch)
                h, p, r = self.cam.getHpr()
                new_p = p - delta_y * self.camera_sens
                new_p = max(-85.0, min(85.0, new_p)) # Ограничение наклона

                # ИСПРАВЛЕНИЕ: Фиксируем локальный Heading камеры на 180 градусов.
                # Это компенсирует изначальный разворот модели персонажа.
                # Камера останется на своем месте от третьего лица и будет смотреть в спину.
                self.cam.setHpr(180.0, new_p, 0)

            # Возвращаем курсор в центр экрана каждый кадр
            self.win.movePointer(0, center_x, center_y)

        return Task.cont






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

    def Dialog1(self):
        self.dialog = 2
        self.value_label['text'] = LangB[self.vah][0]
        self.dialog_label['text'] = LangB[self.vah][1]
        self.btn0.hide()
        self.btn1.hide()
        self.speekG.play()



    def Dialog2(self):
        self.dialog = 3
        self.value_label['text'] = LangC[self.vah][0]
        self.dialog_label['text'] = LangC[self.vah][1]
        self.btn1.hide()
        self.btn0.hide()
        self.speekNPC2.play()

    # конусное освещение
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
        # СВЕТ ПРИВЯЗАН К ОБЪЕКТУ:
        self.slnp.reparentTo(obj)

        # Позиционируем свет относительно панды (например, над головой)
        self.slnp.setPos(x, y, z)# В локальных координатах модели
        #self.slnp.lookAt(self.scene) # Свет смотрит на модель
        self.slnp.setHpr(h, p, r)
        # 4. Включаем отображение контура (пирамиды) источника света
        # sptLight.showFrustum()

        # 4. Включаем свет
        self.render.setLight(self.slnp)
    # точечное освещение
    def pointlig(self, x,y,z, obj, force):
        # 2. Создаем точечный свет (PointLight)
        plight = PointLight('plight')
        plight.setColor((force, force, force/2, 1)) # Желтоватый свет
        plight.setAttenuation((0, 0.02, 0.01))

        # Создаем узел для света
        self.plnp = obj.attachNewNode(plight)

        # --- ВАЖНО: Привязка ---
        # Делаем свет дочерним объектом модели, чтобы он двигался вместе с ней
        self.plnp.reparentTo(obj)
        # Устанавливаем позицию света относительно модели (например, чуть выше)
        self.plnp.setPos(x, y, z)

        # 3. Применяем свет к сцене
        self.render.setLight(self.plnp)

        # 3. Создаем визуальный контур (сферу)
        # Загружаем базовую модель сферы из встроенных ассетов Panda3D
##        light_sphere = loader.loadModel("models/misc/sphere")
##        light_sphere.reparentTo(self.plnp)
##
##        # Масштабируем сферу под радиус действия вашего света
##        light_sphere.setScale(10)
##
##        # Делаем сферу полупрозрачной сеткой (wireframe), чтобы она не перекрывала сцену
##        light_sphere.setRenderModeWireframe()
##        light_sphere.setTextureOff(1)
##        light_sphere.setLightOff(1)

        return self.plnp

    def enable_fisheye(self):
        # 1. Создаем линзу «рыбьего глаза»
        self.spy_lens = FisheyeLens()

        # 2. Настраиваем поле зрения (FOV). Чем больше угол, тем сильнее искажение по краям.
        # Для эффекта глазка отлично подходит 120-150 градусов. Максимум — 360.
        self.spy_lens.setFov(130)

        # 3. Устанавливаем эту линзу нашей основной камере
        self.cam.node().setLens(self.spy_lens)

    def disable_fisheye(self):
        # Возвращаем стандартную перспективную линзу обратно
        from panda3d.core import PerspectiveLens
        normal_lens = PerspectiveLens()
        normal_lens.setFov(base.camLens.getFov()) # возвращаем стандартный угол обзора
        self.cam.node().setLens(normal_lens)

    def shoot_sphere(self):
        print("-> Выстрел!")

        # 1. Базовая физика Bullet
        sphere_shape = BulletSphereShape(0.5)
        sphere_node = BulletRigidBodyNode("Sphere")
        sphere_node.setMass(2.0)
        sphere_node.addShape(sphere_shape)

        sphere_np = self.render.attachNewNode(sphere_node)

        # Позиция и направление (со сдвигом вперед на 3 единицы, чтобы не застревать)
        player_pos = self.char_np.getPos(self.render)
        forward_vector = self.cam.getQuat(self.render).getForward()
        sphere_np.setPos(player_pos + forward_vector * 3.0 + Vec3(0, 0, 2.0))

        # 2. Визуальная модель
        visual_model = self.loader.loadModel("smiley")
        visual_model.setScale(0.5)
        visual_model.reparentTo(sphere_np)

        # 3. Привязываем твой свет
        self.pointlig(0, 0, 0, sphere_np, 5.0)

        # Добавляем в физический мир
        self.world.attachRigidBody(sphere_node)

        # 4. Импульс полета
        shoot_force = 100.0
        impulse = forward_vector * shoot_force
        sphere_node.applyCentralImpulse(impulse)

        # 5. ТАЙМЕР НА 5 СЕКУНД
        # Через 5.0 секунд автоматически вызовется метод self.destroy_sphere_task
        # Мы передаем туда узел сферы (sphere_np) и физический узел (sphere_node)
        self.taskMgr.doMethodLater(
            5.0,
            self.destroy_sphere_task,
            f"DestroySphere_{sphere_np.get_key()}",
            extraArgs=[sphere_np, sphere_node],
            appendTask=True
        )

        # 6. ЗАПУСКАЕМ ТАСК ПРОВЕРКИ КОНТАКТА С ЗЕМЛЕЙ/СТЕНАМИ
        self.taskMgr.add(
            self.check_sphere_collision_task,
            f"CheckCol_{sphere_np.get_key()}",
            extraArgs=[sphere_np, sphere_node],
            appendTask=True
        )


    def destroy_sphere_task(self, sphere_np, sphere_node, task=None):
        if sphere_np and not sphere_np.isEmpty():
            explosion_pos = sphere_np.getPos(self.render)

            # Удаляем летящую сферу со сцены и из физики
            sphere_np.removeNode()
            self.world.removeRigidBody(sphere_node)

            # 1. Запускаем ослепительную вспышку света (гаснет за 0.3 сек)
            self.create_explosion_flash(explosion_pos)

            # 2. Запускаем фейерверк частиц (красиво разлетается и исчезает за 1.5 сек)
            self.create_fire(self.render, explosion_pos.x, explosion_pos.y, explosion_pos.z, scale=3.5)

            print(f"-> БУМ! Вспышка и фейерверк запущены в точке {explosion_pos}")

        # ИСПРАВЛЕНО: возвращаем статус для Panda3D только если метод вызван как таск движка
        if task:
            return task.done


    def create_explosion_flash(self, position):
        # Создаем пустой узел-пустышку в точке взрыва
        flash_np = self.render.attachNewNode("ExplosionFlash")
        flash_np.setPos(position)

        # Создаем супер-яркую вспышку с помощью ВАШЕГО метода pointlig.
        # Сила 300.0 сделает взрыв ослепительным в центре, а затухание настроим ниже
        light_np = self.pointlig(0, 0, 0, flash_np, 300.0)

        # Настраиваем быстрое затухание для взрыва (чтобы свет не заливал всю карту)
        light_np.node().setAttenuation((0, 0.1, 0.05))

        # Переменная для отслеживания текущей яркости взрыва
        flash_np.set_python_tag("current_force", 300.0)

        # Запускаем задачу плавного затухания этого конкретного взрыва
        self.taskMgr.add(self.fade_flash_task, f"FadeFlash_{flash_np.get_key()}", extraArgs=[flash_np, light_np], appendTask=True)

    def fade_flash_task(self, flash_np, light_np, task):
        dt = globalClock.getDt()

        # Достаем текущую силу света
        force = flash_np.get_python_tag("current_force")

        # Быстро уменьшаем силу света (каждый кадр отнимаем значение, умноженное на dt)
        # Коэффициент 1000.0 означает, что вспышка полностью угаснет примерно за 0.3 секунды
        force -= 1000.0 * dt

        if force <= 0:
            # Если свет полностью угас — удаляем источник света и сам узел вспышки
            self.render.clearLight(light_np)
            flash_np.removeNode()
            print("-> Вспышка взрыва полностью угасла.")
            return task.done # Останавливаем эту задачу

        # Если свет еще горит — обновляем его яркость через ваш формат цвета
        flash_np.set_python_tag("current_force", force)
        light_np.node().setColor((force, force, force / 2, 1))

        return task.cont


    # ---МЕТОД СОЗДАНИЯ ПЛАМЕНИ ---
    def create_fire(self, parent_np, x=0, y=0, z=0, scale=1.0):
        # Корневой узел для огня
        fire_np = parent_np.attachNewNode("AnimatedFireSource")
        fire_np.setPos(x, y, z)

        # Создаем плоскую карточку (полигон) для пламени
        cm = CardMaker("fire_card")
        cm.setFrame(-1.0, 1.0, -1.0, 1.0)
        card_geom = cm.generate()

        visual_np = fire_np.attachNewNode(card_geom)
        visual_np.setBillboardPointEye() # Всегда лицом к игроку
        visual_np.setScale(scale)

        # Настраиваем свечение и оранжевый цвет
        visual_np.setColor(Vec4(1, 0.4, 0, 1))
        visual_np.setTransparency(True)
        visual_np.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.M_add))

        # Устанавливаем первый кадр из закэшированного списка
        if self.fire_texture_sequence:
            visual_np.setTexture(self.fire_texture_sequence[0])

        # Добавляем ваш свет с таском мерцания
        fire_light = self.pointlig(0, 0, 0.5, fire_np, 5.0)
        # 5. ЗАПУСКАЕМ ТАСК ОБНОВЛЕНИЯ КАДРОВ И АВТОУДАЛЕНИЯ ---
        task_anim_name = f"AnimFire_{fire_np.get_key()}"

        # Передаем только статичные объекты, которые НЕ меняются
        fire_task = self.taskMgr.add(
            self.animate_fire_frames_task,
            task_anim_name,
            extraArgs=[fire_np, visual_np, self.fire_texture_sequence],
            appendTask=True
        )
        # Инициализируем счетчик кадров прямо в объекте таска
        fire_task.current_frame = 0.0

        return fire_np

    # --- 3. ТАСК ДЛЯ АНИМАЦИИ КАДРОВ ---
    def animate_fire_frames_task(self, fire_np, visual_np, texture_sequence, task):
        if fire_np.isEmpty() or not texture_sequence:
            return task.done

        dt = globalClock.getDt()

        # Берем текущий кадр из атрибута таска и обновляем его
        task.current_frame += 60.0 * dt
        frame_index = int(task.current_frame)

        # Если дошли до конца 250 кадров — удаляем взрыв
        if frame_index >= len(texture_sequence):
            self.extinguish_fire(fire_np)
            return task.done

        # Обновляем кадр пламени
        visual_np.setTexture(texture_sequence[frame_index])

        return task.cont

    def check_sphere_collision_task(self, sphere_np, sphere_node, task):
        # Если сфера уже была удалена по таймеру 5 секунд, завершаем этот таск
        if sphere_np.isEmpty():
            return task.done

        # Делаем проверку контактов в физическом мире Bullet
        result = self.world.contactTest(sphere_node)

        if result.getNumContacts() > 0:
            # Проверяем первый контакт
            contact = result.getContact(0)

            # ИСПРАВЛЕНО: Используем getNode1() для получения объекта, в который врезалась сфера
            node_b = contact.getNode1()

            # --- ДОБАВЛЯЕМ ПРОВЕРКУ ТУТ ---
            # Если объект, в который мы врезались, имеет имя "Base1" (или то, что вы передали в Name)
            if node_b.getName() == "Base1":
                if self.act ==1:
                    self.Deed1 = True
                    print("Переменная self.Deed1 установлена в True!")
                if self.act ==2:
                    self.Deed2 = True
                    print("Переменная self.Deed2 установлена в True!")


            # Получаем физический узел самого игрока для проверки
            player_node = self.char_np.node() if hasattr(self.char_np, 'node') else None

            # Игнорируем столкновения с самим игроком (чтобы сфера не взрывалась сразу в руках)
            if node_b == player_node or node_b.getName() in ["Player", "Character"]:
                return task.cont

            print(f"-> Касание с препятствием ({node_b.getName()})! Активируем взрыв.")

            # 1. Отменяем таймер автоматического удаления на 5 секунд, так как взрыв уже происходит
            self.taskMgr.remove(f"DestroySphere_{sphere_np.get_key()}")

            # 2. Принудительно вызываем ваш метод взрыва destroy_sphere_task
            self.destroy_sphere_task(sphere_np, sphere_node, task=None)

            # Завершаем текущий таск проверки коллизий
            return task.done

        return task.cont




    # --- 4. МЕТОД ОЧИСТКИ ПАМЯТИ ---
    def extinguish_fire(self, fire_np):
        if not fire_np.isEmpty():
            self.taskMgr.remove(f"Flicker_{fire_np.get_key()}")
            self.taskMgr.remove(f"AnimFire_{fire_np.get_key()}")
            fire_np.removeNode()


    def clean_explosion_effect_task(self, fire_np, p_sys, task):
        if fire_np and not fire_np.isEmpty():
            # Отключаем систему частиц от физического менеджера, чтобы освободить ресурсы
            base.physicsMgr.detachPhysical(p_sys)

            # Гасим свет
            light_node = fire_np.find("**/+PointLight")
            if not light_node.isEmpty():
                self.render.clearLight(light_node)

            fire_np.removeNode() # Полностью удаляем узел со сцены
            print("-> Эффект взрыва успешно очищен из памяти движка.")
        return task.done


    def auto_extinguish_task(self, fire_np, task):
        # Самоочистка эффекта по таймеру
        self.extinguish_fire(fire_np)
        return task.done


    def fire_flicker_task(self, fire_light, task):
        import random
        # Каждые несколько кадров слегка меняем яркость света, имитируя колебания пламени
        random_force = random.uniform(3.5, 5.0)
        fire_light.node().setColor((random_force, random_force * 0.5, random_force * 0.1, 1))
        return task.cont

    def extinguish_fire(self, fire_np, task=None):
        if fire_np and not fire_np.isEmpty():
            p_effect = fire_np.getPythonTag("particle_effect")
            if p_effect:
                p_effect.cleanup()

            light_node = fire_np.find("**/+PointLight")
            if not light_node.isEmpty():
                self.render.clearLight(light_node)

            fire_np.removeNode()
            print("-> Фейерверк полностью потушен, ресурсы очищены.")

        # 2. ОБЯЗАТЕЛЬНО возвращаем статус для Panda3D, если таск передан
        if task:
            return task.done




