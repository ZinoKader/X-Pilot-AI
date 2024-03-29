import helpfunctions

class InstructionHandler:


    def __init__(self, ai, multiguy):
        self.ai = ai
        self.multiguy = multiguy
        self.chatmessages = []
        self.instructionstack = []
        self.delayedinstructions = []
        self.finishedinstructions = []
        self.idleticks = 0

    def should_roam(self):
        return (len(self.instructionstack) + len(self.delayedinstructions) == 0) and self.idleticks > 2000


    def update_instructions(self):
        # check for idleness
        if not self.instructionstack and not self.delayedinstructions:
            self.idleticks += 1
        else:
            self.idleticks = 0

        if self.should_roam():
            self.delegate_roam_instruction()

        # update instructionstack with latest instruction
        for i in range(10):
            if self.ai.scanGameMsg(i) not in self.chatmessages: # don't allow same message to be added multiple times
                self.chatmessages.append(self.ai.scanGameMsg(i))

        for message in self.chatmessages:
            if "mission" in message and "completed" not in message and message not in self.instructionstack and message not in self.finishedinstructions:
                self.instructionstack.append(message)


    def add_delayed_instruction(self, message):
        self.delayedinstructions.append(message)


    def finish_latest_instruction(self):
        self.finishedinstructions.append(self.instructionstack[0])
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

    def delegate_roam_instruction(self):
        self.multiguy.roam()
