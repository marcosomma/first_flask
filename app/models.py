from app import UserMixin

class User(UserMixin):
    user_database = {"MarcoSomma": ("Marco", "Somma"),
                     "Test1Test": ("Test1", "11234"),
                     "Test2Test": ("Test2", "12234"),
                     "Test3Test": ("Test3", "12334")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)