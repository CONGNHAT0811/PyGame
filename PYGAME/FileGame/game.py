import pygame,sys,random
# tạo hàm cho chò trơi
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))       
    screen.blit(floor,(floor_x_pos+432,650))       
def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midtop=(500,random_pipe_pos-650))   
    bottom_pipe = pipe_surface.get_rect(midtop=(500,random_pipe_pos))   
    return bottom_pipe,top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes  
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >=600:
           screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_sollision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False   
        if bird_rect.top <=10 or bird_rect.bottom >=620 :
            die_sound.play()
            return False
    return True            
def rotate_bird(bird1):
    new_bird=pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird     
def bird_animation():
    new_bird=bird_list[bird_index]
    new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird,new_bird_rect
def score_display(game_state):
    if game_state=='main_game':
        score_surface= game_font.render(str(int(score)),True,(255,255,255))
        score_rect=score_surface.get_rect(center=(216,100))
        screen.blit(score_surface,score_rect)
    if game_state=='game_over':
        score_surface= game_font.render(f'Score:{int(score)}',True,(0,0,0))
        score_rect=score_surface.get_rect(center=(216,390))
        screen.blit(score_surface,score_rect)
        
        high_score_surface= game_font.render(f'High Score:{int(high_score)}',True,(0,0,0))
        high_score_rect=high_score_surface.get_rect(center=(216,430))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score>high_score:
        high_score=score
    return high_score  
def draw_start_screen():
    # Hiển thị nút Start
    screen.blit(btn_start, btn_start_rect)
    # Hiển thị con chim
    rotated_bird = rotate_bird(bird)
    bird_rect.centery = 284 
    bird_rect.centerx = 316  
    screen.blit(rotated_bird, bird_rect)
    screen.blit(srting_word, string_word_rect)
pygame.mixer.pre_init(frequency=44100,size=16,channels=2,buffer=512)
pygame.init()
screen=pygame.display.set_mode((432,768))
clock=pygame.time.Clock()
game_font =pygame.font.Font('FileGame/04B_19.ttf',30)
pygame.display.set_caption("Flappy Bird")
# tạo các biến cho chò trơi
gravity=0.35
bird_movement=0
game_active=False
score=0
high_score=0
collision = False
game_over = False
game_over_timer = 0
# chèn nút chơi lại 
btn_reset = pygame.transform.scale(pygame.image.load('FileGame/assets/reset.png').convert_alpha(), (100, 50))
btn_reset_rect = btn_reset.get_rect(center=(216, 640))
# chèn chữ 
srting_word = pygame.transform.scale(pygame.image.load('FileGame/assets/flapp.png').convert_alpha(), (230, 80))
string_word_rect = srting_word.get_rect(center=(150, 284))
# chèn start
btn_start = pygame.transform.scale(pygame.image.load('FileGame/assets/start.png').convert_alpha(), (130, 50))
btn_start_rect = btn_start.get_rect(center=(216, 630))
# chèn backgroud
bg=pygame.image.load('FileGame/assets/background-night.png').convert()
bg=pygame.transform.scale2x(bg)
# chèn sàn
floor=pygame.image.load('FileGame/assets/floor.png').convert()
floor=pygame.transform.scale2x(floor) 
floor_x_pos=0
# tạo  chim
bird_down=pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-downflap.png')).convert_alpha() 
bird_mid=pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-midflap.png')).convert_alpha() 
bird_up=pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-upflap.png')).convert_alpha() 
bird_list=[bird_down,bird_mid,bird_up]
bird_index=0
bird=bird_list[bird_index]
bird_rect=bird.get_rect(center=(100,384))
# tạo ống 
pipe_surface=pygame.image.load('FileGame/assets/pipe-green.png').convert() 
pipe_surface=pygame.transform.scale2x(pipe_surface)
pipe_list = []
# tạo timer chi chim 
bird_flap=pygame.USEREVENT+1
pygame.time.set_timer(bird_flap,200)
# tạo timer
spawpipe=pygame.USEREVENT
pygame.time.set_timer(spawpipe,2000)
pipe_height=[200,300,400]
# tạo màn hình kết thúc 
game_over_surface=pygame.transform.scale2x(pygame.image.load('FileGame/assets/gameover.png')).convert_alpha() 
game_over_rect=game_over_surface.get_rect(center=(216,200))
# chèn hình get ready
get_ready_surface=pygame.transform.scale2x(pygame.image.load('FileGame/assets/message.png')).convert_alpha() 
get_ready_rect=get_ready_surface.get_rect(center=(216,200))
# chèn âm thanh 
flap_sound=pygame.mixer.Sound('FileGame/sound/sfx_wing.wav')
hit_sound=pygame.mixer.Sound('FileGame/sound/sfx_hit.wav')
score_sound=pygame.mixer.Sound('FileGame/sound/sfx_point.wav')
die_sound=pygame.mixer.Sound('FileGame/sound/sfx_die.wav')

score_sound_countdown=100

# vòng lặp của trò chơi
while True:
    # Xử lý các sự kiện
    for event in pygame.event.get():
        # Kiểm tra sự kiện thoát game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Xử lý sự kiện click chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_active:
                bird_movement = 0
                bird_movement = -11
                flap_sound.play()
            elif not game_active and btn_start_rect.collidepoint(event.pos):
                # Nếu game chưa bắt đầu và người chơi click vào nút bắt đầu, khởi tạo lại game
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        # Xử lý sự kiện tạo ống
        if event.type == spawpipe:
            pipe_list.extend(create_pipe())
        # Xử lý sự kiện chim nhảy
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    # Vẽ background
    screen.blit(bg, (0, 0))

    # Kiểm tra trạng thái game và vẽ màn hình tương ứng
    if not game_active and not game_over:
       draw_start_screen()
    if not game_active:
        if game_over_timer == 0:
            game_over_timer = pygame.time.get_ticks()  # Bắt đầu đếm thời gian khi trạng thái game over được kích hoạt
        if pygame.time.get_ticks() - game_over_timer > 2000:  # Điều chỉnh độ trễ (tính bằng mili giây) theo ý muốn
            game_over = True 
            high_score = update_score(score, high_score)
            reset_btn_rect = btn_reset.get_rect(center=(216, 600))
            screen.blit(game_over_surface, game_over_rect)
            screen.blit(btn_reset, reset_btn_rect)
            score_display('game_over')   
       
    elif game_active:
        # Xử lý chuyển động và vẽ chim                                
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        # Xử lý chuyển động và vẽ ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        game_active = check_sollision(pipe_list)

        # Tính điểm khi chim vượt qua ống
        for pipe in pipe_list:
            if pipe.right == bird_rect.left:
                score += 0.5
                score_sound.play()
            score_display('main_game')    
        
       
    # Vẽ sàn di chuyển
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    floor_x_pos -= 1
    pygame.display.update()
    clock.tick(60)
