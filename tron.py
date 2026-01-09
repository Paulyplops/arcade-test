import arcade

SPEED = 10 # Pixels per second
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Tron"


# function to check if point q lies on line segment 'pr'
def on_segment(p, q, r):
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

# function to find orientation of ordered triplet (p, q, r)
# 0 --> p, q and r are collinear
# 1 --> Clockwise
# 2 --> Counterclockwise
def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - \
          (q[0] - p[0]) * (r[1] - q[1])

    # collinear
    if val == 0:
        return 0

    # clock or counterclock wise
    # 1 for clockwise, 2 for counterclockwise
    return 1 if val > 0 else 2


# function to check if two line segments intersect
def intersect(points):
    # find the four orientations needed
    # for general and special cases
    o1 = orientation(points[0][0], points[0][1], points[1][0])
    o2 = orientation(points[0][0], points[0][1], points[1][1])
    o3 = orientation(points[1][0], points[1][1], points[0][0])
    o4 = orientation(points[1][0], points[1][1], points[0][1])

    # general case
    if o1 != o2 and o3 != o4:
        return True

    # special cases
    # p1, q1 and p2 are collinear and p2 lies on segment p1q1
    if o1 == 0 and on_segment(points[0][0], points[1][0], points[0][1]):
        return True

    # p1, q1 and q2 are collinear and q2 lies on segment p1q1
    if o2 == 0 and on_segment(points[0][0], points[1][1], points[0][1]):
        return True

    # p2, q2 and p1 are collinear and p1 lies on segment p2q2
    if o3 == 0 and on_segment(points[1][0], points[0][0], points[1][1]):
        return True

    # p2, q2 and q1 are collinear and q1 lies on segment p2q2 
    if o4 == 0 and on_segment(points[1][0], points[0][1], points[1][1]):
        return True

    return False


def collision( seg, path ):
    for previous, current in zip( path, path[1:]):
        if intersect( ( seg, (previous, current) ) ):
            return True
    return False




class Player:
    def __init__(self, keys, start, vel, col ):
        self.keys = keys
        self.pos = start
        self.vel = vel
        self.col = col
        self.path = [ start, start ]


class TronGame(arcade.Window):

    """ Our custom Tron Window."""


    def __init__(self):

        """ Initializer """

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        
        self.players = []
        self.msg_text = arcade.Text("Message", 10, 10, arcade.color.WHITE, 14 )
 
        self.set_mouse_visible(False)        

        self.background_color = arcade.color.OXFORD_BLUE


    def setup(self):

        """ Set up the game and initialize the variables. """

        self.players = [ 
            Player( [arcade.key.A, arcade.key.D, arcade.key.W, arcade.key.S], (300, 50), (0,SPEED), arcade.color.BLUE ),
            Player( [arcade.key.LEFT,arcade.key.RIGHT, arcade.key.UP, arcade.key.DOWN], (300, 550), (0,-SPEED), arcade.color.YELLOW )
           ]
        
        self.msg_text.text = "Hello"


    def on_draw(self):

        """ Draw everything """

        self.clear()

        for player in self.players:
            arcade.draw_line_strip(player.path, player.col, 3)

        self.msg_text.draw()

    def on_update(self, delta_time):

        """ Update state """

        for player in self.players:
            player.pos = ( 
                player.pos[0] + player.vel[0] * delta_time, 
                player.pos[1] + player.vel[1] * delta_time )

            

            for opponent in self.players:
                for previous, current in zip( opponent.path, opponent.path[1:]):
                    if opponent != player and collision( (player.pos, player.path[-1]), opponent.path ):
                        self.msg_text.text = "CRASH"
                    elif collision( (player.pos, player.path[-1]), opponent.path[:-2] ):
                        self.msg_text.text = "SELF"

            player.path[-1] = player.pos

    def on_key_press(self, key, modifiers):
        for player in self.players:
            vel = None
            if player.keys[0] == key and player.vel[1] != 0:
                vel = (-SPEED,0)
            if player.keys[1] == key and player.vel[1] != 0:
                vel = (+SPEED,0)
            if player.keys[2] == key and player.vel[0] != 0:
                vel = (0,+SPEED)
            if player.keys[3] == key and player.vel[0] != 0:
                vel = (0,-SPEED)
            if vel:
                player.vel = vel
                player.path.append( player.pos )




def main():

    """ Main function """

    window = TronGame()

    window.setup()

    arcade.run()



if __name__ == "__main__":

    main()
