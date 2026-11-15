from db import get_db
from .usersRepository import usersRepository
class userService:
    def __init__(self):
        self.user_repository = usersRepository(get_db())

    def getUserById(self, id):
        return self.user_repository.findUserById(id)

    def makeUser(self, username, password, location):
        return self.user_repository.makeUser(username, password, location)

    def getUsers(self):
        return self.user_repository.getUsers()

    def updateUser(self, user_id, username, password, location):
        return self.updateUser(user_id, username, password, location)

    def deleteUser(self, user_id):
        return self.deleteUser(user_id)