from helpfunctions import *

class InstructionHandler:


    def __init__(self, ai, multiguy):
        self.ai = ai
        self.multiguy = multiguy
        self.chatmessages = []
        self.instructionstack = []
        self.delayedinstructions = []


    def add_latest_messages(self):
        for i in range(10):
            if self.ai.scanGameMsg(i) not in self.chatmessages:
                self.chatmessages.append(self.ai.scanGameMsg(i))

        for message in self.chatmessages:
            if "mission" in message and "completed" not in message and message not in self.instructionstack:
                self.instructionstack.append(message)


    def add_delayed_instruction(self, message):
        self.delayedinstructions.append(message)


    def finish_latest_instruction(self):
        self.instructionstack.pop(0)


    def interpret_latest_message(self):
        latest_message = ""
        if self.delayedinstructions:
            latest_message = self.delayedinstructions[0]
        elif self.instructionstack:
            latest_message = self.instructionstack[0]

        if "attack" in latest_message:
            self.delegate_attack_instruction(latest_message)
        elif "move to" in latest_message:
            self.delegate_move_instruction(latest_message)


    def delegate_move_instruction(self, message):
        coordinates = helpfunctions.extract_coordinates_move_instruction(message)
        self.multiguy.findpath(coordinates)


    def delegate_attack_instruction(self, message):
        if "ship" in message:
            target_ship = helpfunctions.extract_target_ship_name(message)
            self.multiguy.attack(target_ship)
        else:
            self.multiguy.attack() # attacks nearest target
