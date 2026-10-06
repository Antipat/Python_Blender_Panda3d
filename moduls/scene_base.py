from direct.showbase.DirectObject import DirectObject

class Scene(DirectObject):
    def __init__(self, manager):
        self.manager = manager
        self.node = None # Контейнер для всех объектов сцены

    def load(self):
        """Загрузка объектов сцены"""
        self.node = render.attachNewNode(self.__class__.__name__)
        pass

    def unload(self):
        """Очистка ресурсов"""
        if self.node:
            self.node.removeNode()
        self.ignoreAll() # Отписываемся от всех событий