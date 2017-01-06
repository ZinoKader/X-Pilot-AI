class InstructionHandler:


    def __init__(self, ai, multiguy):
        self.ai = ai
        self.multiguy = multiguy
        self.chatmessages = []
        self.instructionstack = []


    def add_latest_messages(self):
        for i in range(10):
            if self.ai.scanGameMsg(i) not in self.chatmessages:
                self.chatmessages.append(self.ai.scanGameMsg(i))

        for message in self.chatmessages:
            if "move" in message and "completed" not in message and message not in self.instructionstack:
                self.instructionstack.append(message)


    def interpret_latest_message(self):
        latest_message = self.instructionstack[-1]

        if "move-to-pass" in latest_message.lower() or "move-to-stop" in latest_message.lower():
            self.delegate_move_instruction(latest_message)


    def delegate_move_instruction(self, message):
        moveinstruction = message[:12]
        message = message.replace(moveinstruction, "")
        message = message.strip()

        xcoords = ""
        for char in message:
            if char == " ":
                break
            if char in "0123456789":
                xcoords += char

        message = message.replace(xcoords, "", 1) # ta bort en gång (ifall x och y-koordinaterna är samma)
        message = message.strip()

        ycoords = ""
        for char in message:
            if char == " ":
                break
            if char in "0123456789":
                ycoords += char


        self.multiguy.findpath(xcoords, ycoords)
