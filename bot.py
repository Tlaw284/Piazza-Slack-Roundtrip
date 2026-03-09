from piazza_api import Piazza
from piazza_api.rpc import PiazzaRPC

from config import PIAZZA_EMAIL, PIAZZA_PASSWORD, PIAZZA_ID



class PiazzaBot():

    # Initialize the bot
    def __init__(self):
        self.piazza = Piazza()
        self.piazza.user_login(email=PIAZZA_EMAIL, password=PIAZZA_PASSWORD)
        self.network = self.piazza.network(PIAZZA_ID)

    # Read a post from post number
    def ReadPost(self, postNum:int)->str:
        post = self.network.get_post(postNum)
        subject = post['history'][0]['subject']
        content = post['history'][0]['content']

        print(f"{subject}\n-------------------\n{content}\n-------------------")

    # Respond as an instructor
    def InstructorRespond(self, postNum:int, message:str, tag:str)->None:
        post = self.network.get_post(postNum)
        currResponse = ""
        revisionNum = 0
        for child in post['children']:
            if child['type'] == "i_answer":
                revisionNum = child['history_size']
                currResponse += child['history'][0]["content"]
                currResponse += "\n"
                currResponse += "\n"
        currResponse += message
        currResponse += "\n"
        currResponse += tag
        self.network.create_instructor_answer(post, currResponse, revision=revisionNum)


def main():
    bot = PiazzaBot()
    
    choice = input("Input choice:")

    while choice:
        if choice == "1":
            post = int(input("Post Num:"))
            bot.ReadPost(post)
        elif choice == "2":
            post = int(input("Post Num:"))
            message = input("Input message:")
            bot.InstructorRespond(post, message, tag = "-- Thomas")
        
        choice = input("Input choice:")



main()