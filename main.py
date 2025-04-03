# 셋업
import os,pygame,sys,random, time # type: ignore
from pygame.locals import * # type: ignore

# 현재 파일의 디렉토리로 작업 디렉토리 설정
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("참가자를 피해라!")
screen = pygame.display.set_mode((600, 700))

score = 0
shots =0
hits = 0
misses = 0
lives = 3  # 목숨 추가

font = pygame.font.Font(None, 20) # 기본 폰트, 크기:20
last_badguys_spawm_time = 0     # 악당이 마지막에 나온 시각을 기록

badguy_iamge = pygame.image.load("image/참가자(1).png").convert()
badguy_iamge.set_colorkey((0,0,0))

archer_image = pygame.image.load("image/참가자(2).png").convert()
archer_image.set_colorkey((0,0,0))

fighter_image = pygame.image.load("image/병장.png").convert()
fighter_image.set_colorkey((255,255,255))

missile_image = pygame.image.load("image\pngegg.png").convert()
missile_image.set_colorkey((255,255,255))

explosion_image = pygame.image.load("image/gameover2.png")

GAME_OVER = pygame.image.load("image\gameover.png").convert()


# 클래스 
class Badguy:
    def __init__(self):
        self.x = random.randint(0, 570)
        self.y = -100
        self.dy = random.randint(2, 4)
        self.dx = random.uniform(-2, 2)  # 더 부드러운 랜덤 움직임

    def move(self):
        # 일정 확률로 방향 변경    
        if random.random() < 0.02:
            self.dx = random.uniform(-2, 2)

        self.x += self.dx
        self.dy += 0.05  # 천천히 가속
        self.y += self.dy

    def draw(self):
        screen.blit(badguy_iamge, (self.x, self.y))

    def off_screen(self):
        return self.y > 640

    def touching(self, missile):
        return (self.x + 35 - missile.x) ** 2 + (self.y + 22 - missile.y) ** 2 < 1225

    def score(self):
        global score
        score += 100

class Fighter :
    def __init__(self) :
        self.x = 320
        self.lives = 3  # 목숨 추가
    def move(self) :
        if pressed_keys[K_LEFT] and self.x > 0 : # type: ignore
            self.x -= 7
        if pressed_keys[K_RIGHT] and self.x < 540 : # type: ignore
            self.x += 7
    def draw(self):
        screen.blit(fighter_image, (self.x, 591))
    def fire(self) :
        global shots
        shots += 1
        missiles.append(Missile(self.x+50))
    def hit_by(self, badguy):
        return(
            badguy.y > 585 and
            badguy.x > self.x - 55 and
            badguy.x < self.x + 85
        )
class Missile:
    def __init__(self, x):
        self.x = x
        self.y = 591

    def move(self):
        self.y -= 5

    def off_screen(self):
        return self.y < -8

    def draw(self):
        screen.blit(missile_image, (self.x - 4, self.y))

def reset_game() : # 게임을 다시 초기화
    global badguys, missiles, fighter, score, shots, hits, misses
    
    badguys = []
    missiles = []
    fighter = Fighter()
    score = 0
    hits = 0
    misses = 0
    shots = 0   
# 리스트
badguys = []
fighter = Fighter()
missiles = []

#초기 설정

missiles = []
ammo = 10  # 초기 총알 개수
font = pygame.font.Font(None, 20)

# 10초마다 총알 리셋 이벤트
AMMO_RESET = pygame.USEREVENT + 1
pygame.time.set_timer(AMMO_RESET, 10000)  # 10초마다 발생

game_over = False
game_over_reason = ""



# 게임루프
while 1 :
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT : # type: ignore
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE : # type: ignore
            fighter.fire()
    
    pressed_keys = pygame.key.get_pressed()

    if time.time() - last_badguys_spawm_time > 0.5 :
        badguys.append(Badguy())

        last_badguys_spawm_time = time.time()
    
    screen.fill((0,0,0))
    fighter.move()
    fighter.draw()

    i = 0
    while i < len(badguys):
        badguys[i].move()
        badguys[i].draw()
        if badguys[i].off_screen():
            del badguys[i]
            i -= 1
        i += 1

    i = 0
    while i < len(missiles): 
        missiles[i].move()
        missiles[i].draw()
        if missiles[i].off_screen():
            del missiles[i]
            misses += 1
            i -= 1
        i += 1

    i = 0
    while i < len(badguys):
        j = 0
        while j < len(missiles):
            if badguys[i].touching(missiles[j]):
                badguys[i].score()
                hits += 1
                del badguys[i]
                del missiles[j]
                i -= 1
                break 
            j += 1
        i += 1
    if game_over:
        if game_over_reason == "자폭":  
            # 자폭 이미지 출력 (플레이어 대신 폭발 이미지)
            screen.blit(explosion_image, (160,200))  
            pygame.display.flip()
            pygame.time.delay(2000)  # 2초 대기 후 종료
            
        pygame.time.delay(1000)  # 일반 게임 오버는 1초 대기
        break

    if game_over:
        game_over_text = font.render(game_over_reason, True, (255, 255, 255))
        pygame.display.flip()
        pygame.time.delay(3000)  # 3초 대기 후 종료
        break

    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if ammo > 0:
                missiles.append(Missile(400))  # 미사일 발사
                ammo -= 1  # ***발사 즉시 총알 감소***

        if event.type == AMMO_RESET:
            ammo = 5  # 총알 리셋

        # 총알이 0이 되면 자폭
    if ammo == 0:
        game_over = True
        game_over_reason = "자폭"
            
    # 미사일 이동 및 삭제
    for missile in missiles[:]:
        missile.move()
        missile.draw()
        if missile.off_screen():
            missiles.remove(missile)
            ammo -= 1  # 못 맞추면 총알 감소

    # 총알 개수 표시 (조금 아래로 이동)
    ammo_text = font.render(f"Ammo: {ammo}", True, (255, 255, 255))
    screen.blit(ammo_text, (4, 30))  # Y 좌표를 50으로 조정
    
        
    screen.blit(font.render("Score: "+ str(score), True, (255,255,255)), (5,5))
    

    for badguy in badguys:
        if fighter.hit_by(badguy):
            screen.blit(GAME_OVER, (160,200))

            screen.blit(font.render(str(shots), True, (255, 255, 255)), (286, 286))
            screen.blit(font.render(str(score), True, (255, 255, 255)), (246, 308))
            screen.blit(font.render(str(hits), True, (255, 255, 255)), (430, 285))
            screen.blit(font.render(str(misses), True, (255, 255, 255)), (410, 307))
            if shots == 0:
                screen.blit(font.render("--", True, (255, 255, 255)), (430, 327))
            else :
                screen.blit(font.render("{:.1f}%".format(100*hits/shots), True, (255, 255, 255)), (420, 327))

            while 1:
                for event in pygame.event.get():
                    if event.type == QUIT: # type: ignore
                        sys.exit()
                pygame.display.update()
    
    pygame.display.update()