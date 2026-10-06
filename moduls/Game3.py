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
import sys
from panda3d.bullet import *
from moduls.scene_base import Scene
from moduls.Game4 import App4



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
# смена ночи на день
DayNight = ((0, 0.05, 0.1),(0, 0.35, 0.6))


class App3(Scene, ShowBase):

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

        self.npc_speed = 20       # Скорость бега NPC (подберите под анимацию)
        self.stop_distance = 15.0   # Дистанция, ближе которой NPC перестанет бежать к игроку

        self.rot = self.cam.getH()

        self.FileRead()
        self.GameSave(2, "val 4")

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

        # 1. Инициализация физического мира Bullet
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

        # Добавляем задачу обновления физики в цикл рендеринга
        self.taskMgr.add(self.updatePhysics, "UpdatePhysics")


        house_shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        house_node = BulletRigidBodyNode("House")
        house_node.addShape(house_shape)
        house_np = self.render.attachNewNode(house_node)
        house_np.setPos(0, 0, -10)
        self.world.attachRigidBody(house_node)

        self.ground = self.loader.loadModel("model//GR.glb")
        self.ground.setPos(0, 0, -11)
        self.ground.setScale(1.5)
        self.ground.reparentTo(render)

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
        self.char_np.setPos(0, -150, 10)
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

        # дом
        self.house: NodePath = self.loader.loadModel("model//House_M.glb")
        self.house.setPos(0, 0, 10)
        self.house.setScale(2)
        self.house.reparentTo(render)
        self.house.flattenLight()
        # создание сложного коллайдера дома
        self.MeshCol(self.house)

        # дверь
        self.doorH: NodePath = self.loader.loadModel("model//House_Doors.glb")
        self.doorH.setPos(0, 0, 10)
        self.doorH.setScale(2)
        self.doorH.reparentTo(render)
        # входная_лестница
        self.STUhou: NodePath = self.loader.loadModel("model//STUHouse.glb")
        self.STUhou.setPos(0, 0, 10)
        self.STUhou.setScale(2)
        self.STUhou.reparentTo(render)
        self.STUhou.flattenLight()
        # создание сложного коллайдера лестницы
        self.MeshCol(self.STUhou)
        self.STUhou.hide()


        # лестница в доме
        self.Lest: NodePath = self.loader.loadModel("model//Lest.glb")
        self.Lest.setPos(0, 0, 10)
        self.Lest.setScale(2)
        self.Lest.reparentTo(render)

        # коллайдер лестницы
        self.LestCollis: NodePath = self.loader.loadModel("model//Lest_Collis.glb")
        self.LestCollis.setPos(0, 0, 10)
        self.LestCollis.setScale(2)
        self.LestCollis.reparentTo(render)
        self.LestCollis.flattenLight()
        # создание сложного коллайдера
        self.MeshCol(self.LestCollis)
        self.LestCollis.hide()


        # Загружаем вашу общую модель уровня
        self.level:NodePath = self.loader.loadModel("model//House_Triger.glb")
        self.level.setPos(0, 0, 10)
        self.level.setScale(2)
        self.level.reparentTo(render)

        # Словарь для хранения ссылок на триггеры (если понадобятся позже)
        self.triggers = {}

        # 2. Проходимся по всем 6 триггерам
        # Проходимся по всем 6 триггерам
        for i in range(1, 7):
            trig_name = f"Trig{i}"
            trig_np = self.level.find(f"**/{trig_name}")

            if not trig_np.isEmpty():
                # Скрываем визуальный меш триггера (пока не настроите, можно закомментировать, чтобы видеть разницу)
                trig_np.hide()

                # 1. Получаем локальные границы меша БЕЗ учета масштаба
                min_pt, max_pt = trig_np.getTightBounds()

                # 2. Получаем масштаб объекта, который пришел из Blender
                scale = trig_np.getScale(self.level)

                # 3. Вычисляем точные полу-размеры (half-extents), умножая их на масштаб
                half_x = ((max_pt.getX() - min_pt.getX()) / 2) * scale.getX()
                half_y = ((max_pt.getY() - min_pt.getY()) / 2) * scale.getY()
                half_z = ((max_pt.getZ() - min_pt.getZ()) / 2) * scale.getZ()

                # 4. Создаем форму правильного увеличенного размера
                shape = BulletBoxShape(Vec3(half_x+20, half_y+20, half_z))

                # 5. Создаем Ghost-ноду и добавляем форму
                ghost_node = BulletGhostNode(f"bullet-{trig_name}")
                ghost_node.addShape(shape)
                ghost_node.setIntoCollideMask(BitMask32.allOn())

                # 6. Привязываем к рендеру и копируем ПОЛНУЮ матрицу (включая позицию и поворот)
                ghost_np = self.render.attachNewNode(ghost_node)
                ghost_np.setPos(trig_np.getPos(self.render))
                ghost_np.setHpr(trig_np.getHpr(self.render))

                # Добавляем наш триггер в физический мир Bullet
                self.world.attachGhost(ghost_node)

                # Сохраняем NodePath триггера в словарь
                self.triggers[trig_name] = ghost_np


        # барьер перед кабинетом
        self.BlockH = self.BoxC(0,0,50, 30, 2, 20, 0, 0, 0 , Name = "House")

        # Загружаем дополнительные триггеры
        self.level1:NodePath = self.loader.loadModel("model//TriG_Dop.glb")
        self.level1.setPos(0, 0, -10)
        self.level1.setScale(1.5)
        self.level1.reparentTo(render)

        # Словарь для хранения ссылок на триггеры (если понадобятся позже)
        #self.triggers = {}

        # 2. Проходимся по всем 6 триггерам
        # Проходимся по всем 6 триггерам
        for i in range(8, 11):
            trig_name = f"Trig{i}"
            trig_np = self.level1.find(f"**/{trig_name}")

            if not trig_np.isEmpty():
                # Скрываем визуальный меш триггера (пока не настроите, можно закомментировать, чтобы видеть разницу)
                trig_np.hide()

                # 1. Получаем локальные границы меша БЕЗ учета масштаба
                min_pt, max_pt = trig_np.getTightBounds()

                # 2. Получаем масштаб объекта, который пришел из Blender
                scale = trig_np.getScale(self.level)

                # 3. Вычисляем точные полу-размеры (half-extents), умножая их на масштаб
                half_x = ((max_pt.getX() - min_pt.getX()) / 2) * scale.getX()
                half_y = ((max_pt.getY() - min_pt.getY()) / 2) * scale.getY()
                half_z = ((max_pt.getZ() - min_pt.getZ()) / 2) * scale.getZ()

                # 4. Создаем форму правильного увеличенного размера
                shape = BulletBoxShape(Vec3(half_x+20, half_y+20, half_z))

                # 5. Создаем Ghost-ноду и добавляем форму
                ghost_node1 = BulletGhostNode(f"bullet-{trig_name}")
                ghost_node1.addShape(shape)
                ghost_node1.setIntoCollideMask(BitMask32.allOn())

                # 6. Привязываем к рендеру и копируем ПОЛНУЮ матрицу (включая позицию и поворот)
                ghost_np1 = self.render.attachNewNode(ghost_node1)
                ghost_np1.setPos(trig_np.getPos(self.render))
                ghost_np1.setHpr(trig_np.getHpr(self.render))

                # Добавляем наш триггер в физический мир Bullet
                self.world.attachGhost(ghost_node1)

                # Сохраняем NodePath триггера в словарь
                self.triggers[trig_name] = ghost_np1

        # Загружаем палатки
        self.kemp:NodePath = self.loader.loadModel("model//Kemping_Dop.glb")
        self.kemp.setPos(0, 0, -10)
        self.kemp.setScale(1.5)
        self.kemp.reparentTo(render)

        # Загружаем скелет собаки
        self.base = Actor("model//Dog_scelet.glb")
        self.base.setPos(0, 0, -10)
        self.base.loop("ArmatureAction")
        self.base.setScale(1.5)
        self.base.reparentTo(render)

         # Загружаем палатки
        self.dog:NodePath = self.loader.loadModel("model//Dog.glb")
        self.dog.setPos(0, 0, -10)
        self.dog.setScale(1.5)
        self.dog.reparentTo(render)

        # NPC
         # Привязка 3D-модели (например, Actor'а)
        self.people = Actor("model/People3.glb")
        self.people.setScale(12)
        self.people.reparentTo(render)
        self.people.loop("menl_vrag1|mixamo.com")
        self.people.setPos(0, -150, -10)
        self.people.setH(180)
        self.people.setLightOff()

        self.people.hide()


        # NPC девушка
        self.people2 = Actor("model/Girl_NPC1.glb")
        self.people2.setScale(1.5)
        self.people2.setPos(1500, 0, -10)
        self.people2.reparentTo(render)

        # 1. Задаем ОДНО ТОЧНОЕ имя трека, который мы хотим запустить
        self.target_anim = "Armature.001|Armature.001Action.001"

        # 2. Запускаем анимацию в бесконечный цикл
        self.people2.loop(self.target_anim, fromFrame=0, toFrame=320)
        self.people2.getGeomNode().node().setFinal(True)
        self.people2.update()



        # корни/ветки
         # Привязка 3D-модели (например, Actor'а)
        self.base1 = Actor("model/BASe1.glb")
        #self.base1:NodePath = self.loader.loadModel("model/BASe1.glb")
        self.base1.setScale(10)
        self.base1.setPos(1400, 300, -10)
        self.base1.reparentTo(render)
        self.base1.loop("Armature|Armature|ArmatureAction")
        self.base1.setLightOff()
        self.branch_collider1=self.KinematicColl(self.base1)
        # 3. СРАЗУ СКРЫВАЕМ И ВЫКЛЮЧАЕМ (пока акт не равен 22)
        self.base1.hide()  # Прячем визуальную модель
        self.world.removeRigidBody(self.branch_collider1)  # Отключаем физику


        # Привязка 3D-модели (например, Actor'а)
        self.base2 = Actor("model/BASe1.glb")
        #self.base1:NodePath = self.loader.loadModel("model/BASe1.glb")
        self.base2.setScale(10)
        self.base2.setPos(1300, 300, -10)
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
        self.base2.hide()  # Прячем визуальную модель
        self.world.removeRigidBody(self.branch_collider2)  # Отключаем физику

        # Привязка 3D-модели (например, Actor'а)
        self.base3 = Actor("model/BASe1.glb")
        #self.base1:NodePath = self.loader.loadModel("model/BASe1.glb")
        self.base3.setScale(10)
        self.base3.setPos(1200, 300, -10)
        self.base3.reparentTo(render)
        self.base3.loop("Armature|Armature|ArmatureAction")
        self.base3.setLightOff()
        self.branch_collider3=self.KinematicColl(self.base3)
        self.base3.hide()  # Прячем визуальную модель
        self.world.removeRigidBody(self.branch_collider3)



        # корни/ветки
         # Привязка 3D-модели (например, Actor'а)
        self.base4 = Actor("model/BASe1.glb")
        #self.base1:NodePath = self.loader.loadModel("model/BASe1.glb")
        self.base4.setScale(10)
        self.base4.setPos(1400, 400, -10)
        self.base4.setH(90)
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

        self.base4.hide()  # Прячем визуальную модель
        self.world.removeRigidBody(self.branch_collider4)

        # Привязка 3D-модели (например, Actor'а)
        self.base5 = Actor("model/BASe1.glb")
        #self.base1:NodePath = self.loader.loadModel("model/BASe1.glb")
        self.base5.setScale(10)
        self.base5.setPos(1300, 400, -10)
        self.base5.setH(90)
        self.base5.reparentTo(render)
        self.base5.loop("Armature|Armature|ArmatureAction")
        self.base5.setLightOff()
        self.branch_collider5=self.KinematicColl(self.base5)
        self.base5.hide()  # Прячем визуальную модель
        self.world.removeRigidBody(self.branch_collider5)


        # Привязка 3D-модели (например, Actor'а)
        self.base6 = Actor("model/BASe1.glb")
        #self.base1:NodePath = self.loader.loadModel("model/BASe1.glb")
        self.base6.setScale(10)
        self.base6.setPos(1200, 400, -10)
        self.base6.setH(90)
        self.base6.reparentTo(render)
        self.base6.loop("Armature|Armature|ArmatureAction")
        self.base6.setLightOff()
        # создание сложного коллайдера дома
        self.branch_collider6=self.KinematicColl(self.base6)
        self.base6.hide()  # Прячем визуальную модель
        self.world.removeRigidBody(self.branch_collider6)


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
        self.spotlig(-200, -200, 50, 0, -35, 0, self.house)
        self.spotlig(-70, -260, 15, 0, 0, 0, self.ground)

        self.pointlig(0, 20, 25, self.house, 50)
        self.pointlig(0, -50, 30, self.house, 100)
        self.pointlig(90, -30, 65, self.house, 100)

        self.BoxC(-100,-600,0, 3000, 2,15, 0, 0, 0 , Name = "House")
        self.Barier2 = self.BoxC(1700,-300,0, 2, 2000,15, 0, 0, 0 , Name = "House")
        self.Barier1 = self.BoxC(300,-300,0, 2, 2000,15, 0, 0, 0 , Name = "House")
        self.BoxC(-800,-300,0, 2, 2000,15, 0, 0, 0 , Name = "House")
        self.BoxC(0, 1100,0, 5000, 2,15, 0, 0, 0 , Name = "House")

        # 1. Создаем ноду визуальной отладки
        debug_node = BulletDebugNode("Debug")
        debug_node.showWireframe(True)       # Показывать сетку столкновений
        debug_node.showConstraints(True)     # Показывать ограничения (если есть)
        #debug_node.showBoundingBoxes(False)  # Скрыть габаритные контейнеры (чтобы не спамить)

        # 2. Привязываем её к сцене
        debug_np = self.render.attachNewNode(debug_node)
        #debug_np.show()

        # 3. Передаем ноду отладки в физический мир Bullet
        #self.world.setDebugNode(debug_np.node())

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



    def updatePhysics(self, task):
        dt = globalClock.getDt()
        self.world.doPhysics(dt)

        # ==========================================================
        # ПРОВЕРКА ВАШИХ ТРИГГЕРОВ Trig1-Trig6 (Через Ghost Nodes)
        # ==========================================================
        for trig_name, ghost_node in self.triggers.items():
            #ghost_node = ghost_np.node()

            # Проверяем, находится ли наш игрок внутри этой ghost-ноды
            if self.char_node in ghost_node.node().getOverlappingNodes():

                # Логика конкретно для Trig5 (как в вашем примере)
                if trig_name == "Trig4" and self.act == 0:
                    self.act = 1
                    self.level =1
                    self.value_label['text'] = "Войди в дом"
                    self.dialog_label['text'] = "Войдите в дом"
                    print("Trig4 Войти в дом")
                    self.posCh = self.char_np.get_pos(self.render)


                    # 2. Запускаем анимацию в бесконечный цикл
                    self.people2.loop(self.target_anim, fromFrame=0, toFrame=320)
                    self.people2.getGeomNode().node().setFinal(True)
                    self.people2.update()

                # Здесь вы можете легко добавить логику для остальных триггеров:
                elif trig_name == "Trig5"and self.act == 1:
                    #self.act = 2
                    self.level =2
                    self.value_label['text'] = "Press key E"
                    self.dialog_label['text'] = "Принять ванную"
                    print("Trig5 Ванная")
                    self.posCh = self.char_np.get_pos(self.render)

                elif trig_name == "Trig3"and self.act == 2:
                    self.level =3
                    self.value_label['text'] = "Press key E"
                    self.dialog_label['text'] = "Лечь спать"
                    print("Trig3 Спать")
                    self.posCh = self.char_np.get_pos(self.render)

                elif trig_name == "Trig6"and self.act == 3:
                    self.act = 4
                    self.value_label['text'] = "Press key E"
                    self.dialog_label['text'] = "Приготовить завтрак"
                    print("Trig6 Завтрак")
                    self.posCh = self.char_np.get_pos(self.render)
                    self.level = 4

                elif trig_name == "Trig2"and self.act == 6:
                    self.level = 6
                    self.value_label['text'] = "Press key E"
                    self.dialog_label['text'] = "Прочитать дневник"
                    print("Trig2 Дневник")
                    self.posCh = self.char_np.get_pos(self.render)

                elif trig_name == "Trig1"and self.act == 8:
                    self.level = 9
                    self.value_label['text'] = "Press key E"
                    self.dialog_label['text'] = "Посмотреть в бинокль"
                    print("Trig1 Бинокль")
                    self.posCh = self.char_np.get_pos(self.render)

                elif trig_name == "Trig9"and self.act == 20:
                    self.level = 21
                    self.value_label['text'] = "Нажми E для продожения"
                    self.dialog_label['text'] = "Скелет собаки. Что-то убило животное"
                    print("Trig1 Бинокль")
                    #self.posCh = self.char_np.get_pos(self.render)
                    #self.Barier1.setZ(-100)

                elif trig_name == "Trig8"and self.act == 21:
                    self.level = 22
                    self.value_label['text'] = "Нажми E для продлжения"
                    self.dialog_label['text'] = "Пора поработать"
                    print("Trig8 Работа")
                    #self.posCh = self.char_np.get_pos(self.render)
                    self.Barier1.setZ(-100)

                elif trig_name == "Trig10"and self.act == 23:
                    self.level = 23
                    self.value_label['text'] = "Нажмите E для продожения"
                    self.dialog_label['text'] = "Какие-то туристы тут. Нужно их поискать"
                    print("Trig8 Работа")
                    #self.posCh = self.char_np.get_pos(self.render)

                elif trig_name == "Trig8" and self.act == 25:
                    self.act = 26
                    self.level = 26
                    self.value_label['text'] = "Вот мы и дома. Тебе нужно отдохнуть"
                    self.dialog_label['text'] = ""
                    print("Trig8 Войти в дом")

                elif trig_name == "Trig6"and self.act == 27:
                    self.act = 28
                    self.value_label['text'] = "Press key E"
                    self.dialog_label['text'] = "Выпить чего нибудь"
                    print("Trig6 Завтрак")
                    self.posCh = self.char_np.get_pos(self.render)
                    self.level = 28


        print(self.act, " act")
        print(self.level, " level")

        # 2. Проверяем контакты КОНКРЕТНО для нашего игрока
        result = self.world.contactTest(self.char_node)

        # ==========================================================
        # ДИНАМИЧЕСКАЯ АКТИВАЦИЯ ВЕТКИ НА АКТЕ 22
        # ==========================================================
        if self.act >= 24 and not self.branch_activated:
            self.base1.show()  # Показываем визуально
            self.base2.show()  # Показываем визуально
            self.base3.show()  # Показываем визуально
            self.base4.show()  # Показываем визуально
            self.base5.show()  # Показываем визуально
            self.base6.show()  # Показываем визуально
            self.world.attachRigidBody(self.branch_collider1)  # Включаем физику коллайдера
            self.world.attachRigidBody(self.branch_collider2)  # Включаем физику коллайдера
            self.world.attachRigidBody(self.branch_collider3)  # Включаем физику коллайдера
            self.world.attachRigidBody(self.branch_collider4)  # Включаем физику коллайдера
            self.world.attachRigidBody(self.branch_collider5)  # Включаем физику коллайдера
            self.world.attachRigidBody(self.branch_collider6)  # Включаем физику коллайдера

            # 2. Запускаем анимацию в бесконечный цикл
            self.people2.loop(self.target_anim, fromFrame=340, toFrame=400)
            self.people2.getGeomNode().node().setFinal(True)
            self.people2.update()

            self.branch_activated = True
            print("Ветка Base1 и её коллайдер успешно активированы!")

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
                self.dialog_label['text'] = "Ой, ветка ударила меня!"
                self.char_np.setPos(1500, 150, 10)
                break # Выходим из цикла, так как касание уже зафиксировано


        return task.cont

    def on_space_pressed(self):
        # Находим узел по имени (например, 'my_collider_name')
        collider_np = render.find("**/B")

        if self.act==1:
           self.act=2
           self.value_label['text'] = ""
           self.dialog_label['text'] = "Идите в спальню"

        elif self.act==2 and self.level ==3:
           self.act=3
           self.value_label['text'] = ""
           self.dialog_label['text'] = "Пора мне отдохнуть"
           # создание светлого неба и утро
           self.moon = 1
           base.setBackgroundColor(DayNight[1])

        elif self.act==3 :
           self.act=4
           self.value_label['text'] = "Нажать клавишу Е приготовить"
           self.dialog_label['text'] = "Приготовить завтрак"
           self.level =4


        elif self.act==4:
           self.act=5
           self.value_label['text'] = "Нажать клавишу Е чтобы поесть"
           self.dialog_label['text'] = ""
           self.level =5

        elif self.act==5 :
           self.act=6
           self.value_label['text'] = ""
           self.dialog_label['text'] = ""
           # --- ОТКЛЮЧИТЬ КОЛЛАЙДЕР (прячем над домом) ---
           self.BlockH.setZ(300)

        elif self.act==6 and self.level==6 :
           self.act=7
           self.value_label['text'] = ""
           self.dialog_label['text'] = ""
           self.interact_page.show()
           self.level = 7

        elif self.act==7:
           self.act=8
           self.level = 8
           self.value_label['text'] = ""
           self.dialog_label['text'] = ""
           self.interact_page.hide()

        elif self.act== 8 and self.level == 9:
           self.act=9
           self.level = 10
           self.value_label['text'] = "Нажми E чтобы посмотреть в бинокль"
           self.dialog_label['text'] = ""
           #self.enable_fisheye()

           self.CamPOS = self.cam.getPos()
           self.CamHpr = self.cam.getHpr()
           self.cam.setPos(self.CamPOS + Vec3(0, -500, 0))
           self.numb=1
           #self.cam.setH(180)

        elif self.act==9 and self.level == 10:
           self.act=11
           self.level = 11
           self.value_label['text'] = "Нажми E чтобы убрать бинокль"
           self.dialog_label['text'] = ""
           self.cam.setPos(self.CamPOS)
           self.numb=0
           self.people.show()


        # диалог
        elif self.act >= 12 and self.act<=19:
            self.dialog_label['text'] = LangC[self.vah][self.dialog]
            self.dialog +=1
            self.act +=1

        elif self.act == 20 and self.level < 21:
            self.people.hide()
            self.dialog_label['text'] = "Нужно сходить за водой. Родник справа по тропинке у реки."
            self.numb = 0
            self.dialog=0

        elif self.act == 20 and self.level == 21:
            self.dialog_label['text'] = "Пора возвращаться домой"
            self.act = 21

        elif self.act == 21 and self.level == 22:
            self.dialog_label['text'] = "Работа закончена. Уже вечер"
            self.act = 22

        elif self.act == 22 and self.level == 22:
            self.dialog_label['text'] = "Кто-то кричит недалеко. Нужно проверить"
            self.act = 23

        elif self.act == 23 and self.level == 23:
            #self.dialog_label['text'] = ""
            #self.value_label['text'] = ""
            self.act = 24

        elif self.act == 24 and self.level == 24:
            self.act = 25
            self.dialog_label['text'] = ""
            self.value_label['text'] = ""

        elif self.act == 26 and self.level == 26:
            self.act=27
            self.people2.setPos(-48,-50,5)
            self.people2.loop(self.target_anim, fromFrame=0, toFrame=1)
            self.people2.getGeomNode().node().setFinal(True)
            self.people2.update()
        # завершение этой сцены
        elif self.act == 28 and self.level == 28:
            self.newScene =True
            self.numb = 3

        # переход на новую сцену
        if self.newScene == True and self.numb ==3:
            for task in self.taskMgr.getTasks():
                self.taskMgr.remove(task)
            base.destroy()
            A = App4()
            A.load()

##        if self.newScene == True and self.numb == 3:
##            # 1. Корректно удаляем все таски (кроме системных)
##            self.taskMgr.removeAllTasks()
##
##            # 2. Очищаем все объекты старой сцены с экрана
##            # (если код пишется внутри App3, и App3 наследовал ShowBase,
##            # то render.clear() очистит всё видимое пространство)
##            render.clear()
##
##            # 3. Сбрасываем камеру в начальное положение (опционально)
##            base.camera.setPos(0, 0, 0)
##            base.camera.setHpr(0, 0, 0)
##
##            # 4. Запускаем новую сцену в этом же окне
##            self.A = App4()
##            self.A.load()

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

        if self.act==1:
            self.value_label['text'] = ""
            self.dialog_label['text'] = "Нужно принять душ после дороги"
        elif self.act==3:
            self.value_label['text'] = ""
            self.dialog_label['text'] = "Я проголодался, нужно пойти на кухню"
        elif self.act==6:
            self.value_label['text'] = ""
            self.dialog_label['text'] = "Пора зайти в кабинет дяди"
        elif self.act==7:
            self.value_label['text'] = "Нажмите E, чтобы положить дневник"
            self.dialog_label['text'] = ""
        elif self.act==8:
            self.value_label['text'] = ""
            self.dialog_label['text'] = "Нужно посмотреть, что там на чердаке"

        elif self.act==11:
            self.value_label['text'] = ""
            self.dialog_label['text'] = "Кто-то пришёл. Нужно спуститься. "
            distance = self.char_np.getDistance(self.people)

            # 2. Выводим в консоль для отладки (можно удалить потом)
            # print(f"Дистанция до NPC: {distance:.2f}")

            # 3. Логика взаимодействия (например, дистанция 10 юнитов)
            if distance < 2.0:
                print("Игрок подошел к NPC!")
                self.act=12
        elif self.act==12:
            self.value_label['text'] = ""
            self.dialog_label['text'] = "Здравствуйте Алексей, меня зовут Джон. Я местный шериф "

        elif self.act == 24 and self.level ==23:
            distance = self.char_np.getDistance(self.people2)

            # 2. Выводим в консоль для отладки (можно удалить потом)
            # print(f"Дистанция до NPC: {distance:.2f}")
            self.dialog_label['text'] = f"Дистанция до NPC: {distance:.2f}"

            # 3. Логика взаимодействия (например, дистанция 10 юнитов)
            if distance < 10.0:
                self.value_label['text'] = "Нажмите Е для продолжения"
                self.dialog_label['text'] = "Девушка что с вами случилось? Давайте я отведу вас домой. "
                print("Игрок подошел к NPC!")
                self.level =24

        # ==========================================================
        # ЛОГИКА ПРЕСЛЕДОВАНИЯ: NPC (people2) идет за игроком (char_np)
        # ==========================================================
        # Начинаем погоню/сопровождение, например, с 4-го акта (настройте под сюжет)
        if self.act == 25 and hasattr(self, 'people2') and hasattr(self, 'char_np'):

            self.people2.setPos(0,0,10)
            # 1. Получаем позиции игрока и NPC в глобальных координатах
            player_pos = self.char_np.getPos(render)
            npc_pos = self.people2.getPos(render)

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
                self.people2.lookAt(player_pos)
                # Корректируем наклон головы, чтобы NPC смотрел ровно перед собой
                self.people2.setP(0)
                self.people2.setR(0)
                self.people2.setH(self.people2.getH() + 180)

                # Вычисляем новую позицию шага
                new_pos = npc_pos + direction * self.npc_speed * dt
                self.people2.setPos(render, new_pos)

                # Здесь можно включить анимацию бега/ходьбы, если она еще не играет:
                # if self.npc_state != "walk":
                #     self.people2.loop("Armature|Walk")
                #     self.npc_state = "walk"

            elif distance >= self.stop_distance+200:
                self.value_label['text'] = "Подожди, ты ушёл от меня далеко. Я заблужусь."
            else:
                # Игрок близко — NPC останавливается и переходит в Idle-анимацию
                pass
                # if self.npc_state != "idle":
                #     self.people2.loop("Armature|Idle")
                #     self.npc_state = "idle"




##        if (self.act in (1, 2))  or (self.numb ==3):
##            target =  (self.posCh - global_pos).length()
##            #print("target = ", target)
##            if target >5:
##                self.numb=2
##                self.update_camera(task)
##
##                self.n = 1
##                self.numb=0
##                self.value_label['text'] = ""
##                self.dialog_label['text'] = ""


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

        # Делаем тело статическим (масса = 0)
        body_node.setMass(0)

        # Привязываем физический узел к дереву сцены
        body_np = render.attachNewNode(body_node)
        body_np.setPos(obj.getPos())
        body_np.setHpr(obj.getHpr())

        # Прикрепляем визуальную модель к физическому телу для симуляции
        #obj.reparentTo(body_np)

        self.world.attachRigidBody(body_node)


##    def update_camera(self, task):
##        # Если запущен диалог или управление заблокировано, ничего не делаем
##        if self.dialog != 0:
##            return Task.cont
##
##        # Получаем размеры окна
##        win_w = self.win.getXSize()
##        win_h = self.win.getYSize()
##
##        # Центр экрана в пикселях
##        center_x = win_w // 2
##        center_y = win_h // 2
##
##        # Получаем данные мыши напрямую
##        md = self.win.getPointer(0)
##        mouse_x = md.getX()
##        mouse_y = md.getY()
##
##        # Вычисляем смещение относительно центра
##        delta_x = mouse_x - center_x
##        delta_y = mouse_y - center_y
##
##        # Если мышь сдвинулась и активен нужный режим (numb == 0)
##        if self.numb == 0:
##            if delta_x != 0 or delta_y != 0:
##                # ВАЖНО: Считываем углы с того же объекта, который будем вращать!
##                # Обычно в Panda3D вращают либо self.camera, либо self.cam.
##                # Используем self.cam, раз вы его настраиваете.
##                h, p, r = self.cam.getHpr()
##
##                # Вычисляем новые углы поворота камеры
##                new_h = h - delta_x * self.camera_sens
##                new_p = p - delta_y * self.camera_sens
##
##                # Ограничиваем наклон вверх/вниз (Pitch), чтобы камера не делала сальто
##                new_p = max(-85.0, min(85.0, new_p))
##
##                # Применяем углы к камере
##                self.cam.setHpr(new_h, new_p, 0)
##
##                # Поворачиваем самого персонажа вслед за мышью по горизонтали (Heading)
##                # Используем дельту мыши напрямую для плавности
##                char_h = self.char_np.getH()
##                self.char_np.setH(char_h - delta_x) #* 0.5)
##
##            # Возвращаем курсор в центр экрана КАЖДЫЙ кадр, пока мы управляем камерой
##            self.win.movePointer(0, center_x, center_y)
##
##        return Task.cont

    def KinematicColl(self, obj, Name = "Base1"):
        # Предположим, из listJoints() мы узнали, что главная гнущаяся часть называется 'Bone.001'
        joint_name = 'Bone.006'

        # 1. Находим кость в модели
        joint_np = obj.exposeJoint(None, 'modelRoot', joint_name)

        # 2. Создаем для нее простую форму (например, коробку шириной 2, длиной 2, высотой 10)
        # Размеры подбирайте под визуальный размер части ветки
        box_shape = BulletBoxShape((0.5, 0.5, 3))

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




