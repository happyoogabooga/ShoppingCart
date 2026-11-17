from db import get_db
from .usersRepository import usersRepository
class userService:
    def __init__(self):
        self.user_repository = usersRepository(get_db())

    def getUserById(self, id):
        return self.user_repository.findUserById(id)

    def authenticateUser(self, username, password):
        return self.user_repository.findUserByCredentials(username, password)

    def makeUser(self, username, password, location, name):
        return self.user_repository.makeUser(username, password, location, name)

    def getUsers(self):
        return self.user_repository.getUsers()

    def updateUser(self, user_id, username, password, location, name):
        return self.user_repository.updateUser(
            user_id, username, password, location, name
        )

    def deleteUser(self, user_id):
        return self.user_repository.deleteUser(user_id)