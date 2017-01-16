import helpfunctions
import math

class Attacker:

    def __init__(self, ai):
        self.ai = ai
        self.ai.setTurnSpeed(64)

    def target_alive(self, target):
        pass

    def attack_player(self, target = None, target_id = None):

        # if server id and ship id have not been matched yet
        if not target_id:
            for i in range(self.ai.playerCountServer()):
                for y in range(self.ai.shipCountScreen()):
                    player_id = self.ai.playerId(i)
                    ship_id = self.ai.shipId(y)
                    print(self.ai.playerName(i))
                    if player_id == ship_id and self.ai.playerName(i) == target:
                        target_id = y
                        px, py = helpfunctions.get_wrapped_coordinates(self.ai, target_id)
                        break

        print("****")
        print(target_id)
        print("****")
        px, py = helpfunctions.get_wrapped_coordinates(self.ai, target_id)
        vx, vy = (self.ai.shipVelX(target_id) - self.ai.selfVelX(), self.ai.shipVelY(target_id) - self.ai.selfVelY())

        bulletspeedx = (30 * math.cos(self.ai.selfHeadingRad())) + self.ai.selfSpeed()
        bulletspeedy = (30 * math.sin(self.ai.selfHeadingRad())) + self.ai.selfSpeed()
        bulletspeed = ( (bulletspeedx ** 2) + (bulletspeedy ** 2) ) ** (1 / 2)

        time_of_impact = helpfunctions.time_of_impact(px, py, vx, vy, bulletspeed)

        targetX = px + (vx * time_of_impact)
        targetY = py + (vy * time_of_impact)

        aim_direction = math.atan2(targetY, targetX)

        if self.ai.shipCountScreen() > 0:
            self.ai.turnToRad(aim_direction)
            self.ai.fireShot()


    def attack_nearest(self): # returns True if ships were nearby, False if not

        selfX = ( self.ai.selfRadarX() / self.ai.radarWidth() ) * self.ai.mapWidthPixels()
        selfY = ( self.ai.selfRadarY() / self.ai.radarHeight() ) * self.ai.mapHeightPixels()

        # match server id with ship id and put closest targets in a dictionary
        ship_distances = {}
        for i in range(self.ai.playerCountServer()):
            for y in range(self.ai.shipCountScreen()):
                player_id = self.ai.playerId(i)
                ship_id = self.ai.shipId(y)
                if player_id == ship_id and player_id != self.ai.selfId():
                    px, py = helpfunctions.get_wrapped_coordinates(self.ai, y)
                    rel_distance = ( ( px ** 2) + ( py ** 2) ) ** ( 1/2 )
                    ship_distances[rel_distance] = y
                    break

        if ship_distances:
            # pick out the closest target from the dictionary
            closest_target_id = ship_distances.get(min(ship_distances))
            self.attack_player(None, closest_target_id)
            return True
        else:
            return False
