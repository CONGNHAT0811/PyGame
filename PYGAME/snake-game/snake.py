# Import thư viện pygame và random
import pygame
import random

# Khởi tạo pygame
pygame.init()

# Thiết lập kích thước màn hình
screen_size = [768, 468]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Snake Game")


# Khởi tạo đồng hồ
clock = pygame.time.Clock()

# Trạng thái của trò chơi và biến kiểm soát vòng lặp
game_state = "start"
run = True

# Khởi tạo rắn và thức ăn
snake = [[50, 50, 20, 20]]
food_margin = 30
food_spacing = 40
num_food_x = (screen_size[0] - 2 * food_margin) // food_spacing
num_food_y = (screen_size[1] - 2 * food_margin) // food_spacing
food = [random.randint(food_margin, num_food_x * food_spacing + food_margin),
        random.randint(food_margin, num_food_y * food_spacing + food_margin)]

# Hướng di chuyển của rắn
direction = [2, 0]

# Điểm số và điểm số cao nhất
score = 0
high_score = 0
game_over = False
reset_requested = False
quit_requested = False


# Hàm xóa màn hình
def clearScreen():
    pygame.draw.rect(screen, (255, 255, 255), [0, 0, 768, 468])

# Hàm vẽ rắn
def drawSnake(snake):
    for segment in snake:
        pygame.draw.rect(screen, (255, 0, 0), segment)

# Hàm vẽ thức ănƯ
def drawFood(food):
    pygame.draw.circle(screen, (255, 255, 0), [food[0], food[1]], 10)

# Hàm vẽ điểm số
def draw_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {int(score)}', True, (0, 0, 0))
    screen.blit(score_text, [10, 10])

# Hàm vẽ điểm số cao nhất
def draw_high_score(high_score):
    
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'High Score: {int(high_score)}', True, (0, 0, 0))
    screen.blit(score_text, [580, 10])

# Hàm vẽ nút bắt đầu
def draw_start_button():
    pygame.draw.rect(screen, (0, 255, 0), [300, 200, 150, 50])
    font = pygame.font.Font(None, 36)
    start_text = font.render("Start", True, (0, 0, 0))
    screen.blit(start_text, [350, 210])
    
def draw_reset_button():
    pygame.draw.rect(screen, (0,0,255), [264,324 , 100, 40])
    font = pygame.font.Font(None, 36)
    start_text = font.render("Reset", True, (0, 0, 0))
    screen.blit(start_text, [280, 334]) 

def draw_Quit_button():
    pygame.draw.rect(screen, (255,0,0), [394,324 , 100, 40])
    font = pygame.font.Font(None, 36)
    start_text = font.render("Quit", True, (0, 0, 0))
    screen.blit(start_text, [410, 334])        

# Hàm vẽ nút thoát
def draw_quit_button():
    pygame.draw.rect(screen, (255, 0, 0), [300, 300, 150, 50])
    font = pygame.font.Font(None, 36)
    quit_text = font.render("Quit", True, (0, 0, 0))
    screen.blit(quit_text, [350, 310])

# Hàm cập nhật điểm số
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
# tạo game over 
def draw_game_over():
    # vẽ background cho game over 
    pygame.draw.rect(screen, (0, 255, 255), [0, 0, 768, 468])
    # vẽ game over 
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, [244,154])
    # vẽ điểm 
    pygame.draw.rect(screen, (255, 255, 0), [290, 230, 190, 30])
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {int(score)}', True, (0, 0, 0))
    screen.blit(score_text, [334,234])
    
    
    pygame.draw.rect(screen, (255, 255, 0), [290, 270, 190, 30])
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'High Score: {int(high_score)}', True, (0, 0, 0))
    screen.blit(score_text, [310, 274])
    # vẽ nút reset 
    draw_reset_button() 
    draw_Quit_button()
# Hàm bắt đầu trò chơi
def start_game():
    global game_state, direction
    game_state = "playing"
    direction = [2, 0]
# Hàm thoát trò chơi
def quit_game():
    global run
    run = False
    
# Vòng lặp chính của trò chơi
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if game_state == "start":
                if 300 < mouse_x < 450 and 200 < mouse_y < 250:
                    start_game()
                elif 300 < mouse_x < 450 and 300 < mouse_y < 350:
                    quit_game()
            elif game_state == "playing" and game_over:
                if 264 < mouse_x < 364 and 324 < mouse_y < 364:
                    reset_requested = True   
                elif 394 < mouse_x < 494 and 324 < mouse_y < 364:
                    quit_requested = True        
                    
    if game_state == "start":
        # Màn hình khởi đầu
        pygame.draw.rect(screen, (0, 255, 255), [0, 0, 768, 468])
        draw_start_button()
        draw_quit_button()
        
    elif game_state == "playing":
        # Điều khiển rắn bằng nút
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction[1] == 0:
            direction = [0, -2]
        elif keys[pygame.K_DOWN] and direction[1] == 0:
            direction = [0, 2]
        elif keys[pygame.K_RIGHT] and direction[0] == 0:
            direction = [2, 0]
        elif keys[pygame.K_LEFT] and direction[0] == 0:
            direction = [-2, 0]

        # Cập nhật vị trí của rắn liên tục
        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1], 20, 20]
        snake.insert(0, new_head)

        if snake[0][0] < food[0] < snake[0][0] + 20 and snake[0][1] < food[1] < snake[0][1] + 20:
            food = [random.randint(0, screen_size[0] - 20), random.randint(0, screen_size[1] - 20)]
            score += 5
        else:
            snake.pop()

        if (
                snake[0][0] < 0 or
                snake[0][1] < 0 or
                snake[0][0] + 20 > screen_size[0] or
                snake[0][1] + 20 > screen_size[1]
        ):
            game_over = True  # Đặt biến game_over thành True khi rắn va chạm

        for segment in snake[1:]:
            if snake[0][0] == segment[0] and snake[0][1] == segment[1]: 
                game_over = True  # Đặt biến game_over thành True khi rắn va chạm

        clearScreen()
        drawSnake(snake)
        drawFood(food)
        draw_score(score)
        draw_high_score(high_score)

        #khi rắn va chạm
        if game_over:
            high_score = update_score(score, high_score)  
            draw_game_over()
            
        if quit_requested:
            quit_game()
            quit_requested = True
            
        if reset_requested:
            # Reset trạng thái và dữ liệu cần thiết
            game_state = "playing"
            reset_requested = False
            game_over = False
            snake = [[50, 50, 20, 20]]
            direction = [2, 0]
            food = [random.randint(food_margin, num_food_x * food_spacing + food_margin),
                    random.randint(food_margin, num_food_y * food_spacing + food_margin)]
            score=0
    pygame.display.update()
    clock.tick(100)
