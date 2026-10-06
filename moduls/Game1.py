from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import ActorInterval
from direct.task import Task
from panda3d.core import *
import sys
from panda3d.bullet import *
from moduls.scene_base import Scene
from moduls.Game2 import App2


RUSB = ["Для продолжения нажмите E", "Вы: Здравствуйте. Мне хот-дог и колу", "Бармен: Добрый вечер. Вот держите",
 "Бармен: С вас 2 доллара", "Вы: Я немного заблудился.", "Бармен: Вы не местный, проездом или к нам в наш городишко?",
  "Вы: - Да, я не местный, но мой дядя здесь жил, и я как раз еду к его дому. Меня зовут Алексей.", "Бармен: - И кто твой дядя? Я здесь всех знаю.",
   "Вы: Александр Шоц, его дом где-то недалеко, на окраине вашего города", "Бармен: - Тогда, добро пожаловать к нам, в городишко Горнолеск." ,
   "Бармен: Я Алексей Григорьевич, это моё кафе, а эта моя жена Наталья Андреевна",
   "Бармен: До дома твоего дяди недалеко, но как ты уже знаешь,он находится не в городе, а при въезде в него. ",
   "Бармен: Через три километра от сюда будет поворот налево на просёлочную дорогу, которая и приведёт тебя прямо нему." ]

ENGB = ["To continue, press E", "You: Hello. I'll have a hot dog and a Coke.", "Bartender: Good evening. Here you go.",
"Bartender: That'll be $2.", "You: I'm a little lost.", "Bartender: Not a local, just passing through or visiting our little town?",
"You: - Yes, I'm not a local, but my uncle used to live here, and I'm just on my way to his house. My name is Alexey.",
 "Bartender: - And who's your uncle? I know everyone here.",
"You: Alexander Shots, his house is somewhere nearby, on the outskirts of your town.",
 "Bartender: - Then welcome to our town of Gornolesk.", "Bartender: I'm Alexey Grigorievich, this is my café, and this is my wife, Natalya Andreyevna.",
"Bartender: It's not far to your uncle's house, but as you already know, it's not in the city, but at the entrance to it.",
"Bartender: Three kilometers from here, there's a left turn onto a dirt road, which will take you straight to him."]

RUSC = ["Для продолжения нажмите E", "Старик: Сдаётся мне это племянник старины Шоца, о котором он говорил. ", "Старик: Эх сынок, зря ты сюда приехал.",
 "Вы: я правда ничего не знаю об этом месте и с дядей я последний раз общался по телефону год назад.",
 "Вы: А две недели назад со мной связался его адвокат и сообщил мне, что он умер и я его наследник.",
 "Вы: Подробностей я не знаю, поэтому мне нужно добраться до его дома, а завтра у меня встреча с этим адвокатом и шерифом.",
  "Старик: Парень, ты должен знать куда приехал и что тебе нужно остерегаться.", "Вы: О чём я должен знать и что остерегаться?",
  "Старик: Молодой человек, я хорошо знал вашего дядю. Мы часто ходили с ним на рыбалку и охоту.",
  "Старик: И у него было прекрасное здоровье. Многие здесь думают, что я спятил, но я уверен в том, что говорю.",
  "Старик: На твоего дядю напал лесной монстр. Мы его называем Шепчущий", "Вы: Вы знаете как умер дядя? ",
  "Старик: Твоего дядю нашли у берега реки, рядом с крутым обрывом. Шериф сказал, что он упал с него и ударился головой о камень.",
  "Старик: Да, но упал он не случайно, а убегал от чудовища.",
  "Вы: От чудовища? Почему от него, а, например, не от какого-то хищника или человека? Там были какие –то следы?",
   "Старик: В том-то и дело, что следов никаких не нашли. Ни звериных, ни человеческих кроме твоего дяди.",
   "Старик: Но были странные порезы на коре дерева и в том месте много торчащих корней деревьев. Я раньше там их не видел",
   "Старик: Послушай меня сынок, то, что погубило твоего дядю ещё в лесу, поэтому будь осторожен.",
   "Старик: Он в последние дни жаловался мне, что ему докучают какие-то шумы по вечерам. И я считаю, что он стал жертвой Шепчущего.",
   "Старик: Храни тебя бог." ]

ENGC = ["To continue, press E", "Old Man: I think this is old Shotz's nephew he was talking about.", "Old Man: Oh, son, you shouldn't have come here.",
"You: I really don't know anything about this place, and I last spoke to my uncle on the phone a year ago.",
"You: And two weeks ago, his lawyer contacted me and told me he'd died and I was his heir.",
"You: I don't know the details, so I need to get to his house, and tomorrow I have a meeting with that lawyer and the sheriff.",
"Old Man: Boy, you should know where you've come and what you need to watch out for.", "You: What should I know and watch out for?",
"Old Man: Young man, I knew your uncle well. We often went fishing and hunting with him.",
"Old Man: And he was in excellent health. A lot of people here think I'm crazy, but I'm sure of what I'm saying.",
"Old Man: Your uncle was attacked by a forest monster. We call him the Whisperer.", "You: Do you know how your uncle died?",
"Old Man: Your uncle was found by the riverbank, next to a steep cliff. The sheriff said he fell off and hit his head on a rock.",
"Old Man: Yes, but he didn't fall by accident; he was running away from a monster.",
"You: From a monster? Why from it, and not, say, from some predator or a human? Were there any tracks?",
"Old Man: That's the point, they didn't find any tracks. Neither animal nor human, except your uncle's.",
"Old Man: But there were strange cuts on the tree bark, and there were a lot of tree roots sticking out in that place. I've never seen them there before.",
"Old Man: Listen to me, son, what killed your uncle back in the forest, so be careful." "Be careful.",
"Old Man: He's been complaining to me for the last few days that he's been bothered by some noises in the evenings. And I believe he's fallen victim to the Whisperer.",
"Old Man: God bless you."]

LangB =[RUSB, ENGB]
LangC =[RUSC, ENGC]

NextGame = ["Отправиться в дорогу", "Hit the road"]

print(len(RUSB))
print(len(ENGB))
print(len(RUSC))
print(len(ENGC))

class App1(Scene, ShowBase):

    def __init__(self):

        ShowBase.__init__(self)
        # шрифт
        self.font = loader.loadFont("Roboto/Roboto-Bold.ttf") #("cmr12.egg")

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

        # Отключаем камеру по умолчанию (свободный режим)
        #self.disableMouse()


        # туман и окружение
        base.setBackgroundColor(0, 0.05, 0.1)

        # Имя тумана используется для отладки
        fog = Fog("SceneFog")

        # 2. Настраиваем цвет тумана (RGBA)
        # Здесь: светло-серый туман
        fog.setColor(0.2, 0.2, 0.1)

        # 3. Настраиваем дальность тумана (у экспоненциального тумана свои параметры)
        fog.setExpDensity(0.001) # Для экспоненциального
        # Или линейный туман (начало, конец)
        #fog.setLinearRange(0.0, 1000.0)

        # 4. Применяем туман к сцене (render)
        render.setFog(fog)

        self.numb = 2
        self.act = 0
        # диалог
        self.dialog = 0
        self.vah = 0
        self.n = 1
        self.newScene = False
        self.Scene = False
        self.close = False

        self.rot = self.cam.getH()

        self.FileRead()
        self.GameSave(2, "val 3")

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


        self.ground = self.loader.loadModel("model//F1.glb")
        self.ground.setPos(0, 0, 11)
        self.ground.reparentTo(render)

        house_shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        house_node = BulletRigidBodyNode("House")
        house_node.addShape(house_shape)
        house_np = self.render.attachNewNode(house_node)
        house_np.setPos(0, 0, 0)
        self.world.attachRigidBody(house_node)


        # 2. Создание персонажа (модель + физика)
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
        self.char_np.setPos(0, 0, 1)
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
        self.cam.reparentTo(self.char_np)

        self.cam.setPos(0, 20, 10)
        self.cam.setH(180)

        # кафе
        self.cafe: NodePath = self.loader.loadModel("model//F6.glb")
        self.cafe.setPos(0, 0, 11)
        self.cafe.reparentTo(render)
        self.cafe.flattenLight()
        # создание сложного коллайдера кафе
        self.MeshCol(self.cafe)
        # фонарные столбы
        for i in range(1,7):
            self.flashlight = self.loader.loadModel(f"model//flashlight{i}.glb")
            self.flashlight.setPos(0, 0, 11)
            self.flashlight.reparentTo(render)
            self.flashlight.flattenLight()
            self.MeshCol(self.flashlight)

            #self.BoxC(world_pos.getX(),world_pos.getY(),world_pos.getZ(), 5,5,50, 0, 0, 0)

        # хоз. помещение
        self.barn = self.loader.loadModel("model//F3.glb")
        self.barn.setPos(0, 0, 11)
        self.barn.reparentTo(render)
        self.barn.flattenLight()
        self.MeshCol(self.barn)

        # крыша колонок
        self.roof = self.loader.loadModel("model//F4.glb")
        self.roof.setPos(0, 0, 11)
        self.roof.reparentTo(render)
        self.roof.flattenLight()
        self.MeshCol(self.roof)

        # колонки
        for i in range(1,7):
            self.refill = self.loader.loadModel(f"model//refill{i}.glb")
            self.refill.setPos(0, 0, 11)
            self.refill.reparentTo(render)
            self.refill.flattenLight()
            self.MeshCol(self.refill)

        # крыша колонок
        self.furniture = self.loader.loadModel("model//furniture.glb")
        self.furniture.setPos(0, 0, 11)
        self.furniture.reparentTo(render)
        self.furniture.flattenLight()
        self.MeshCol(self.furniture)

        # стены вокруг заправки
        self.BoxC(-90, 150, 0, 5, 500, 50, 0, 0, 0)
        self.BoxC(70, -170, 0, 50, 100, 50, 0, 0, 0)

        self.BoxC(0, -270, 0, 5, 100, 50, 90, 0, 0)
        self.BoxC(300, -70, 0, 5, 250, 50, 90, 0, 0)
        self.BoxC(250, 500, 0, 5, 500, 50, 90, 0, 0)
        self.BoxC(500, 150, 0, 5, 500, 50, 0, 0, 0)

        # Дверь.
        self.door = Actor("model/Door.glb")
        self.door.setPos(0,0,11)
        self.door.reparentTo(render)
##        self.door.flattenLight()
##        self.MeshCol(self.door, "D")##
##        #
        #self.door.loop('DoorAnim')
        self.BoxC(185,290,0, 10, 10, 30, 50, 0, 0 , "B")
        self.BoxTrigger(184,284,0, 20, 20, 30, 50, 0, 0 , "Door")

        # NPC
        # Привязка 3D-модели (например, Actor'а)
        self.people = Actor("model/People1.glb")
        self.people.setScale(1.2)
        self.people.reparentTo(render)
        self.people.loop("Game_engine|Game_engine|mixamo.com|Layer0.001")
        self.people.setPos(214, 380, 3)
        self.people.setLightOff()

        #  Привязка 3D-модели (например, Actor'а)
        self.people1 = Actor("model/People2.glb")
        self.people1.setScale(1.2)
        self.people1.reparentTo(render)
        self.people1.loop("Game_engine|Game_engine|mixamo.com|Layer0")
        self.people1.setPos(264, 335, 6)
        self.people1.setH(180)
         # Привязка 3D-модели (например, Actor'а)
        self.people2 = Actor("model/People3.glb")
        self.people2.setScale(12)
        self.people2.reparentTo(render)
        self.people2.loop("menl_vrag1|mixamo.com")
        self.people2.setPos(264, 365, 2)

         # Привязка 3D-модели (например, Actor'а)
        self.people3 = Actor("model/People4.glb")
        self.people3.setScale(12)
        self.people3.reparentTo(render)
        self.people3.loop("menl_vrag2|mixamo.com")
        self.people3.setPos(335, 300,2)
        self.people3.setH(-30)

        # триггер для взаимодействие с NPC
        self.BoxTrigger(250,345,0, 5, 5, 20, 20, 0, 0 , "NPC")
        # видимый указатель
        self.pointer = self.loader.loadModel("model//cylinder.glb")
        self.pointer.reparentTo(render)
        self.pointer.setPos(250,345,3)
        self.pointer.setScale(5)

        # Кнопки выбора бармена
        self.buttonB = self.loader.loadModel("model//GameB1.glb")
        self.buttonB.setPos(0, 0, -5)
        self.btn0 = DirectButton(
         geom=self.buttonB, scale=0.1, pos=(-0.8,0,0.45), frameColor=(0, 0, 0, 0), command = self.Dialog1)


        # Кнопка выбора посетителя
        self.buttonC = self.loader.loadModel("model//GameB2.glb")
        self.buttonC.setPos(0, 0, 0.5)
        self.btn1 = DirectButton(
        geom=self.buttonC,
        scale=0.1,pos=(-0.8,0,0.45), frameColor=(0, 0, 0, 0), command = self.Dialog2)
        # скрываем кнопки
        self.btn1.hide()
        self.btn0.hide()

        # кнопка закрытия игры
        self.btnClose = DirectButton( text = "Close Game", scale=0.1, pos=(-0.8,0,0.0), frameColor=(1, 0, 0, 1), command = self.PlayExit)
        self.btnClose.hide()

        # окружающий лес
        self.trees = self.loader.loadModel("model//Trees.glb")
        self.trees.reparentTo(render)
        #self.pointer.setPos(250,345,3)
        #self.pointer.setScale(1)

        # рассеянное освещение
        ambLight = AmbientLight("ambient")
        ambLight.setColor(Vec4(0.4, 0.4, 0.45, 0.7))
        # установка нового узла света
        ambNode = render.attachNewNode(ambLight)
        render.setLight(ambNode)

        # освещение кафе
        self.pointlig(214, 340, 15, self.roof, 20)
        self.pointlig(335, 300, 15, self.roof, 20)

        # освещение заправки
        self.spotlig(57, -47, 15, 150, 0, 0, self.ground)
        self.spotlig(-70, -260, 15, 0, 0, 0, self.ground)

        self.pointlig(126, 193, 15, self.furniture, 200)
        self.pointlig(-35, 113, 15, self.furniture, 200)
        self.pointlig(374, 65, 15, self.furniture, 200)

        self.spotlig(374, 65, 65, 0, -90, 0, self.ground)


        # 1. Создаем ноду визуальной отладки
        debug_node = BulletDebugNode("Debug")
        debug_node.showWireframe(True)       # Показывать сетку столкновений
        debug_node.showConstraints(True)     # Показывать ограничения (если есть)
        debug_node.showBoundingBoxes(False)  # Скрыть габаритные контейнеры (чтобы не спамить)

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
                if other_node.getName() == "Door" and (self.act ==0):
                    self.act = 1
                    self.value_label['text'] = "Press key E"
                    self.posCh = self.char_np.get_pos(self.render)

                if other_node.getName() == "NPC":
                    if self.dialog ==0:
                        self.btn1.show()
                        self.btn0.show()
                        self.value_label['text'] = ""
                        self.posCh = self.char_np.get_pos(self.render)
                        self.n=1
                        self.dialog = 1

                if other_node.getName() == "Scene":
                    self.value_label['text'] = "Continue your journey. Press E."
                    self.posCh = self.char_np.get_pos(self.render)

                    self.numb = 3




        return task.cont

    def on_space_pressed(self):
        # Находим узел по имени (например, 'my_collider_name')
        collider_np = render.find("**/B")

        if self.act ==1:
            print("E нажат!")
            self.door.play("DoorAnim", fromFrame=0, toFrame=30)
            if not collider_np.is_empty():
                body = collider_np.node()
                # Для удаления из симуляции
                self.world.remove(body)
            self.act=2
            self.value_label['text'] = ""

            # логика включение триггера
            self.newScene = True
            if self.Scene != self.newScene:
                self.Scene = True
                # триггер для перехода
                self.BoxTrigger(0,-50,0, 50, 5, 20, 0, 0, 0 , "Scene")
                # видимый указатель
                self.pointer = self.loader.loadModel("model//cylinder.glb")
                self.pointer.reparentTo(render)
                self.pointer.setPos(0,-50,0)
                self.pointer.setScale(10)



        elif self.act==2:
           close_door = ActorInterval(self.door, "DoorAnim", startFrame=30, endFrame=0)
           close_door.start()
           self.act=1
           self.value_label['text'] = ""
           if not collider_np.is_empty():
               body = collider_np.node()
               # Для удаления из симуляции
               self.world.attach(body)

        # логика диалога для кнопки
        if self.dialog >= 1:
            self.n+=1
            print(self.dialog)

            self.value_label['text'] = LangB[self.vah][0]
            if self.dialog ==2:
                if self.n>= len(LangB[self.vah])-1:
                    self.n = 1
                self.dialog_label['text'] = LangB[self.vah][self.n]
                if "Вы:" in LangB[self.vah][self.n] or "You:" in LangB[self.vah][self.n]:
                    self.speekG.play()
                    self.speekNPC2.stop()
                else:
                    self.speekNPC2.play()
                    self.speekG.stop()

            elif self.dialog ==3:
                if self.n>= len(LangC[self.vah])-1:
                    self.n = 1
                self.dialog_label['text'] = LangC[self.vah][self.n]

                if "Вы:" in LangC[self.vah][self.n] or "You:" in LangC[self.vah][self.n]:
                    self.speekG.play()
                    self.speekNPC2.stop()
                else:
                    self.speekNPC2.play()
                    self.speekG.stop()

        # переход на новую сцену
        if self.newScene == True and self.numb ==3:
            for task in self.taskMgr.getTasks():
                self.taskMgr.remove(task)
                base.destroy()
                A = App2()
                A.load()

    def close_game(self):
        self.close = not self.close
        if self.close ==True:
            self.btnClose.show()
        else:
            self.btnClose.hide()


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

        if (self.act in (1, 2)) or (self.dialog in (2,3)) or (self.numb ==3):
            target =  (self.posCh - global_pos).length()
            #print("target = ", target)
            if target >5:
                self.numb=2
                self.update_camera(task)
                self.act = 0
                self.dialog = 0
                self.btn1.hide()
                self.btn0.hide()
                self.n = 1
                self.numb=0
                self.value_label['text'] = ""
                self.dialog_label['text'] = ""


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

        print(global_pos)
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
        body_np.setPos(self.cafe.getPos())
        body_np.setHpr(self.cafe.getHpr())

        # Прикрепляем визуальную модель к физическому телу для симуляции
        obj.reparentTo(body_np)

        self.world.attachRigidBody(body_node)
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

            if self.numb==0 and self.dialog == 0:
                # Изменяем углы (инверсия по Y для классического управления)
                self.cam.setH(180+h - delta_x * self.camera_sens)
                self.cam.setP(p - delta_y* self.camera_sens)
                self.yy = p - delta_y* self.camera_sens

                # если не задействован диалог
                self.char_np.setH(self.char_np.getH() + int(h - delta_x * 0.05)) #self.camera_sens))

                #print(10+h - delta_x , " / ", -110+p - delta_y)
        #self.win.movePointer(0, center_x, center_y) #int(self.yy)


            # Возвращаем курсор строго в центр экрана

        if self.numb==2:
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
        # СВЕТ ПРИВЯЗАН К ПАНДЕ:
        self.slnp.reparentTo(obj)

        # Позиционируем свет относительно панды (например, над головой)
        self.slnp.setPos(x, y, z)# В локальных координатах модели
        #self.slnp.lookAt(self.scene) # Свет смотрит на модель
        self.slnp.setHpr(h, p, r)
        # 4. Включаем отображение контура (пирамиды) источника света
##        sptLight.showFrustum()

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

##        # 3. Создаем визуальный контур (сферу)
##        # Загружаем базовую модель сферы из встроенных ассетов Panda3D
##        light_sphere = loader.loadModel("models/misc/sphere")
##        light_sphere.reparentTo(self.plnp)
##
##        # Масштабируем сферу под радиус действия вашего света
##        light_sphere.setScale(10)
##
##        # Делаем сферу полупрозрачной сеткой (wireframe), чтобы она не перекрывала сцену
##        light_sphere.setRenderModeWireframe()
##        light_sphere.setTextureOff(1)
##        light_sphere.setLightOff(1) #





