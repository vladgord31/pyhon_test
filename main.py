import pygame


clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((794, 446))
pygame.display.set_caption('Kvitkali')
Icon = pygame.image.load('image/icon.png').convert_alpha()
icon = pygame.image.load('image/icon.png').convert_alpha()
pygame.display.set_icon(icon)
bullet = pygame.image.load('image/bullet.png').convert_alpha()
bullets = []

bullets_left = 5

is_jump = False
jump_count = 8

#Player
bg = pygame.image.load('image/image1.png').convert_alpha()
walk_left = [
    pygame.image.load('image/player1.png').convert_alpha(),
    pygame.image.load('image/player2.png').convert_alpha(),
    pygame.image.load('image/player3.png').convert_alpha(),
    pygame.image.load('image/player4.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('image/player5.png').convert_alpha(),
    pygame.image.load('image/player6.png').convert_alpha(),
    pygame.image.load('image/player7.png').convert_alpha(),
    pygame.image.load('image/player8.png').convert_alpha(),
]

ghost = pygame.image.load('image/ghost.png').convert_alpha()
ghost_list_in_game = []
#bg_sound = pygame.mixer.Sound('sounds/sound.mp3')



player_anim_count = 0
bg_x = 0

player_speed = 5
player_y = 350
player_x = 150

is_jump = False
jump_count = 8

#bg_sound = pygame.mixer.Sound(image_path + 'sounds/sound.mp3')
#bg_sound.play(-1)

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

label = pygame.font.Font('fonts/Roboto-Black.ttf', 50)
lose_label = label.render('Ви програли!', False, (193, 196, 199))
restart_label = label.render('Грати знову', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(270, 200))

gameplay = True

running = True
while running:


    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 794, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))


        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))



        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 350:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -790:
            bg_x = 0


        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 790:
                    bullets.pop(i)
                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (260, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5


    pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(795, 350)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1
    clock.tick(10)