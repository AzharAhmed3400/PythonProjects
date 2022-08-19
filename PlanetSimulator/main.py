import pygame
import math

#initialize
pygame.init()

#Set width and height, ideally square
WIDTH, HEIGHT = 900, 900

#Takes width and height to create window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#colors:
WHITE =(255, 255, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (169, 169, 169)
BLUE = (100, 139, 247)
RED = (188, 39, 50)
FONT = pygame.font.SysFont("comicsans", 16)
#sets caption of window
pygame.display.set_caption('Planet simulator')

class Planet:
    #distance from earth to sun (AU --> meters)
    AU = 149.6e9
    #gravitational constant
    G =  6.67428e-11
    SCALE = 250 / AU #1AU = 100 pixels
    TIMESTEP = 3600*24#1 day
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.distance_to_sun = 0
        #orbits of planets to get circular orbit
        self.orbit = []

        #X & Y velocities
        self.x_vel = 0
        self.y_vel = 0

        self.sun = False
    def draw(self, win):
        #x and y need to be offset since planets are in relation to Sun at center. Screen is always top left (0,0)
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        #present orbits
        if len(self.orbit) > 2:
            scaled_orbits = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                scaled_orbits.append((x,y))
            pygame.draw.lines(WIN, self.color, False, scaled_orbits, 2)

        pygame.draw.circle(win, self.color, (x,y), self.radius)
        
        #draw distance to sun for each planet
        if not self.sun:
            distance_text = FONT.render(f'{round(self.distance_to_sun, 1)}-m', 1, WHITE)
            WIN.blit(distance_text, (x-distance_text.get_width()/2, y - distance_text.get_height()/2))
    
    def attraction(self, other):
        #Find distance from other planet obejct using pythagorean thm
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y**2)

        #if other object is sun, store distace in the object value
        if other.sun:
            self.distance_to_sun = distance
        
        #calc force using Newton's law of gravitation
        force = self.G * self.mass * other.mass / distance**2
        #find angle between y force and x force of attraction
        theta = math.atan2(distance_y, distance_x)
        #calc x and y forces of attraction
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_pos(self, planets):
        #find total x and y forces from all the planets
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        #calculate the velocties the self planet in relation to the total forces
        #Use the timestep to go over a period of time, as f/m = a, and a*t=v
        #adding because velocty can become negative due to change in direction, as with an elliptical orbit
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        #assign positions based on veloctiy and make sure we move in accurate amount of time
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        #update orbit positions based on velocity
        self.orbit.append((self.x, self.y))




#This is an event loop. We want the simulator to keep running until the person exits out
def main():
    run = True
    # Makes sure frame rate of our game does not go past a certain value
    clock = pygame.time.Clock()
    sun = Planet(0,0,35,YELLOW, 1.98892 * 10**30)
    sun.sun=True

    #.y_vel in m/s
    mercury = Planet(0, 0.387 * Planet.AU, 8, DARKGRAY, 3.3 * 10**23)
    mercury.x_vel = 47.4 * 1000

    venus= Planet(0.723 * Planet.AU, 0, 9, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(0, -1.52 * Planet.AU, 12, RED, 6.39 * 10**23)
    mars.x_vel = -24.077 * 1000


    planets=[sun, mercury, venus, earth, mars]
    while run:
        #put in max num of times you want clock to update per sec
        clock.tick(60)
        WIN.fill((0, 0, 0))
        
        #gets events that happen, like mouseclicks and mouse movements
        for event in pygame.event.get():
            #we are only worried about exiting the game
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.update_pos(planets)
            planet.draw(WIN)
        
        pygame.display.update()
    #quit running the pygame
    pygame.quit()

main()