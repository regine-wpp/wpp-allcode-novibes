
import pygame
import pandas as pd
import random

pygame.init()

# THE LOST LABYRINTH OF MARS
# Okay, now that I can move my astronaut around,
# I want to give them things to actually discover!

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Lost Labyrinth of Mars")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
small_font = pygame.font.SysFont(None, 23)

# Colors
MARS_RED = (174, 96, 78)
WHITE = (235, 235, 225)
BLUE = (113, 190, 215)
DARK = (44, 45, 62)
CYAN = (105, 235, 220)
PURPLE = (190, 150, 225)
GOLD = (245, 205, 120)

# Load my fake Martian dataset
rooms = pd.read_csv("mars_labyrinth_rooms.csv")
print("Loaded", len(rooms), "Martian rooms!")

# Player stats
player = pygame.Rect(385, 285, 30, 40)
player_speed = 5

oxygen = 100
crystals = 0
backpack = []

# Objects the astronaut can discover
crystal = pygame.Rect(120, 190, 25, 35)
artifact = pygame.Rect(550, 390, 30, 30)
door = pygame.Rect(650, 130, 80, 110)

crystal_collected = False
artifact_collected = False

# Text displayed after an interaction
message = "Explore Mars! Press E near an object."
message_timer = 0


def show_message(text):
    global message, message_timer
    message = text
    message_timer = 240


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Press E to interact with nearby objects
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e:

                # inflate() creates a larger interaction area
                nearby = player.inflate(45, 45)

                if nearby.colliderect(crystal) and not crystal_collected:
                    crystal_collected = True
                    crystals += 25
                    show_message("You collected 25 energy crystals!")

                elif nearby.colliderect(artifact) and not artifact_collected:
                    artifact_collected = True
                    backpack.append("Ancient Martian Artifact")
                    show_message("An ancient artifact! Added to backpack.")

                elif nearby.colliderect(door):
                    # Randomly select a room from my dataset
                    new_room = rooms.sample(1).iloc[0]

                    print("\nNEW DISCOVERY!")
                    print("Room:", new_room["room_name"])
                    print("Type:", new_room["room_type"])
                    print("Description:", new_room["description"])

                    show_message("Discovered: " + str(new_room["room_name"]))

            # Press B to check the backpack
            elif event.key == pygame.K_b:
                print("\nYOUR BACKPACK:", backpack)
                show_message("Backpack: " + ", ".join(backpack) if backpack else "Your backpack is empty!")

    # Movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= player_speed

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += player_speed

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= player_speed

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += player_speed

    # Keep the player inside the window
    player.clamp_ip(screen.get_rect())

    # Draw the background
    screen.fill(MARS_RED)

    # Draw crystal, unless collected
    if not crystal_collected:
        pygame.draw.polygon(
            screen, CYAN,
            [
                (crystal.centerx, crystal.top),
                (crystal.right, crystal.centery),
                (crystal.centerx, crystal.bottom),
                (crystal.left, crystal.centery)
            ]
        )

    # Draw artifact, unless collected
    if not artifact_collected:
        pygame.draw.rect(screen, PURPLE, artifact, border_radius=5)
        pygame.draw.circle(screen, GOLD, artifact.center, 7)

    # Draw Martian doorway
    pygame.draw.rect(screen, DARK, door, border_radius=15)
    pygame.draw.rect(screen, PURPLE, door, 5, border_radius=15)

    # Draw astronaut
    pygame.draw.rect(
        screen, WHITE,
        (player.x + 5, player.y + 15, 20, 25),
        border_radius=5
    )

    pygame.draw.circle(
        screen, WHITE,
        (player.centerx, player.y + 12), 15
    )

    pygame.draw.ellipse(
        screen, BLUE,
        (player.x + 4, player.y + 5, 22, 12)
    )

    # HUD: display player information
    hud = font.render(
        f"Oxygen: {oxygen}   Crystals: {crystals}",
        True, WHITE
    )
    screen.blit(hud, (20, 20))

    # Instructions
    instructions = small_font.render(
        "WASD / Arrows: Move   E: Interact   B: Backpack",
        True, WHITE
    )
    screen.blit(instructions, (20, 55))

    # Message panel
    if message_timer > 0:
        message_timer -= 1

        pygame.draw.rect(
            screen, DARK,
            (20, 510, 760, 65),
            border_radius=10
        )

        message_text = small_font.render(message, True, WHITE)
        screen.blit(message_text, (35, 530))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
