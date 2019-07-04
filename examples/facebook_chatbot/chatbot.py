import random
import os
from flask import Flask, request
from pymessenger2.bot import Bot
from octorest import OctoRest

class ChatBot(Flask):

    def __init__(self, fb_access_tok='YourFBAccessToken', 
                fb_verify_tok="YourTokenVerification",
                octo_url="http://octopi.local",
                octo_apikey="YouShallNotPass"):
        """
        Initialisation of the ChatBot for OctoWatch
        Parameters:
            fb_access_tok - the Facebook messenger access token given
            fb_verify_tok - the Facebook messenger verification code set
            octo_url - the url of the desired OctoPrint server
            octo_apikey - the apikey found in the OctoPrint settings
        """
        Flask.__init__(self, __name__)

        self.access_token = fb_access_tok
        self.verify_token = fb_verify_tok
        self.url = octo_url
        self.apikey = octo_apikey

        self.bot = Bot(self.access_token)

        self.recipient = None

        self.client = self.make_client(url=self.url, apikey=self.apikey)
    
    def make_client(self, url=None, apikey=None):
        """
        Creates and returns an instance of the OctoRest client.
        Parameters:
            url - the url to the octoprint server
            apikey - the apikey from the octoprint server found in settings
        """
        if url is None:
            url = self.url
        if apikey is None:
            url = self.apikey
        try:
            client = OctoRest(url=url, apikey=apikey)
            return client
        except ConnectionError as ex:
            print(ex)

    def verify_fb_token(self, token_sent):
        """
        Take token sent by Facebook and verify it matches the verify token
        If they match, allow the request, else return an error
        Parameters:
            token_sent - the token received from Facebook
        """
        if token_sent == self.verify_token:
            return request.args.get("hub.challenge")
        return "Invalid verification token"

    def get_message(self):
        """
        Returns a random message from a list of strings
        """
        sample_responses = ["Your print is okay", "I have spotted an error", "1 hour to go"]
        return random.choice(sample_responses)

    def send_message(self, recipient_id, response):
        """
        Uses PyMessenger to send response to user
        Sends user the text message provided via input response parameter
        Parameters
            recipient_id - the id of the person receiving
            response - the text message to respond with
        """
        self.bot.send_text_message(recipient_id, response)
        return "success"

    def send_image(self, recipient_id, response):
        """
        Uses PyMessenger to send response to user
        Sends user an image provided via the image path in the input response parameter
        Parameters
            recipient_id - the id of the person receiving
            response - the image to respond with given as a path
        """
        self.bot.send_image(recipient_id, response)
        return "success"
    
    def get_printer_info(self):
        """
        Retrieves information about the printer
        and returns a chatbot message with its current state
        """
        message = str(self.client.version) + "\n"
        message += str(self.client.job_info()) + "\n"
        printing = self.client.printer()['state']['flags']['printing']
        if printing:
            message += "Currently printing!\n"
        else:
            message += "Not currently printing...\n"
        return message
    
    def get_version(self):
        """
        Retrieves the OctoPrint version and returns chatbot message
        """
        message = "You are using OctoPrint v" + str(self.client.version['server']) + "\n"
        return message
    
    def get_gcode_file_names(self):
        """
        Retrieves the GCODE file names from the
        OctoPrint server and returns chatbot message
        """
        message = "The GCODE files currently on the printer are:\n\n"
        for k in self.client.files()['files']:
            message += k['name'] + "\n"
        return message
    
    def home(self):
        """
        Homes the 3D printer and returns
        message to inform the user
        """
        message = "Homing your printer... :)"
        self.client.home()
        return message

    def toggle(self):
        """
        Toggles the current print from paused/printing
        states and returns message to inform the user
        """
        message = "Toggling your print!"
        self.client.pause()
        return message
    
    def receive_message(self):
        """
        Method for sending/receiving messages to/from users
        on Facebook. Checks if tokens are valid. Depending on
        the text received will select the appropriate reply.
        Receives JSON from OctoWatch containing information
        about the print if there has been an error.
        """
        if request.method == 'GET':
            """
            Before allowing people to message your bot, Facebook has
            implemented a verify token that confirms all requests 
            that your bot receives came from Facebook.
            """ 
            token_sent = request.args.get("hub.verify_token")
            return self.verify_fb_token(token_sent)
        # if the request was not get, it must be POST and we can just
        # proceed with sending a message back to user
        else:
            # get whatever message a user sent the bot
            output = request.get_json()
            # if it was from messenger
            if 'object' in output and 'entry' in output:
                for event in output['entry']:
                    messaging = event['messaging']
                    for message in messaging:
                        if message.get('message'):
                            # Facebook Messenger ID for user so we know where
                            # to send response back to
                            recipient_id = message['sender']['id']
                            self.recipient = recipient_id
                            text = message['message'].get('text')
                            if text == 'status':
                                self.send_message(recipient_id, self.get_printer_info())
                            elif text == 'version':
                                self.send_message(recipient_id, self.get_version())
                            elif text == 'files':
                                self.send_message(recipient_id, self.get_gcode_file_names())
                            elif text == 'home':
                                self.send_message(recipient_id, self.home())
                            elif text == 'toggle':
                                self.send_message(recipient_id, self.toggle())
                            elif message['message'].get('text'):
                                response_sent_text = self.get_message()
                                self.send_message(recipient_id, response_sent_text)
                            # if user sends us a GIF, photo,video, 
                            # or any other non-text item
                            if message['message'].get('attachments'):
                                response_sent_nontext = self.get_message()
                                self.send_message(recipient_id, response_sent_nontext)
                return "Message Processed"
            # if not recognised
            else:
                print("Don't recognise...")
                return "failed"
            
def main():
    """
    The main function of the program.
    Creates a ChatBot instance and runs.
    Defines a function for receiving messages
    using HTTP GET and POST.
    """
    app = ChatBot()

    @app.route("/", methods=['GET', 'POST'])
    def receive_message():
        return app.receive_message()
        
    app.run()

if __name__ == "__main__":
    main()