from piazza_api import Piazza
from piazza_api.rpc import PiazzaRPC
import json

from config import PIAZZA_EMAIL, PIAZZA_PASSWORD, PIAZZA_ID



class PiazzaBot():

    # Initialize the bot
    def __init__(self):
        """Create Bot
        """
        # Piazza libraries requirements
        self.piazza = Piazza()
        self.piazza.user_login(email=PIAZZA_EMAIL, password=PIAZZA_PASSWORD)
        self.network = self.piazza.network(PIAZZA_ID)
        self.__ReadTags__()

    def __ReadTags__(self):
        """Read tags on init
        """
        with open("./tags.json") as tagJSON:
            tags = json.load(tagJSON)
        self.instructorTags = tags.get("instructorTags", None)
        if not self.instructorTags:
            self.instructorTags = {"default" : "Instructor"}
    
    def __WriteTags__(self):
        """Write tags when new one is added
        """
        with open("./tags.json", "w") as tagJSON:
            json.dump(self.instructorTags, tagJSON)
        


    def ReadPost(self, postNum:int)->str:
        """Read a post from post number

        Args:
            postNum (int): Post to Read

        Returns:
            str: Post contents
        """
        # Get a post and scrape content
        post = self.network.get_post(postNum)
        subject = post['history'][0]['subject']
        content = post['history'][0]['content']

        retStr = f"{subject}\n-------------------\n{content}\n-------------------"
        print(retStr)
        return retStr

    def InstructorRespond(self, postNum:int, message:str, instructor:str)->None:
        """Respond to the instructor

        Args:
            postNum (int): Number of post to read
            message (str): Message to respond
            Instructor (str): Instructor name
        """
        if not self.instructorTags.get(instructor, False):
            tag = self.instructorTags.get("default")
        tag = self.instructorTags[instructor]
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
        currResponse += "-- "
        currResponse += tag
        self.network.create_instructor_answer(post, currResponse, revision=revisionNum)

    def AddInstructorTag(self, instructor:str, tag:str) -> None:
        """Create an instructor tag and save it
        Args:
            tag (str): Instructor tag
        """
        self.instructorTags[instructor] = tag
        self.__WriteTags__()



# Test main()
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
            bot.InstructorRespond(post, message, instructor = "Thomas")
        elif choice == "3":
            name = input("Instructor name:")
            tag = input("Instructor tag:")
            bot.AddInstructorTag(name, tag)

        
        choice = input("Input choice:")



main()