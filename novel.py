import pygame
import sys
import json
import os

# --- 1. 定数と初期設定 ---
SCREEN_SIZE = (800, 600)
CONFIG_FILE = "config.json"
SCENARIO_FILE = "scenario.json" # シナリオファイル名

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Python Novel Game Engine (JSON Load)")
clock = pygame.time.Clock()

# フォント設定
font_msg = pygame.font.SysFont("notosanscjp", 28)
font_ui = pygame.font.SysFont("notosanscjp", 24)
font_title = pygame.font.SysFont("notosanscjp", 60)

# --- 2. システム関数 ---
def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {path}: {e}")
            return default
    return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

config = load_json(CONFIG_FILE, {"bgm_volume": 0.5})

# --- 3. クラス定義 ---
class Character:
    def __init__(self, name, x_pos):
        self.name = name
        self.alpha = 0
        self.target_alpha = 0
        self.rect = pygame.Rect(x_pos, 100, 300, 500)
    
    def update(self):
        if self.alpha < self.target_alpha: self.alpha = min(self.alpha + 10, self.target_alpha)
        elif self.alpha > self.target_alpha: self.alpha = max(self.alpha - 10, self.target_alpha)

    def draw(self, surface):
        if self.alpha > 0:
            char_surf = pygame.Surface((300, 500), pygame.SRCALPHA)
            pygame.draw.ellipse(char_surf, (255, 200, 200, self.alpha), (0, 0, 300, 500))
            surface.blit(char_surf, (self.rect.x, self.rect.y))

class Engine:
    def __init__(self):
        # 起動時に一度だけシナリオを読み込む
        self.scenario_data = load_json(SCENARIO_FILE, [
            {"text": "Error: scenario.json not found.", "show": False}
        ])
        self.reset_game()
        
    def reset_game(self):
        self.state = "TITLE"
        self.current_idx = 0
        self.char_count = 0
        self.love_points = {"ヒロイン": 0}
        self.heroine = Character("ヒロイン", 250)
        self.scenario = self.scenario_data # 読み込んだデータを使用

    def update(self):
        if self.state == "PLAYING":
            self.heroine.update()
            scene = self.scenario[self.current_idx]
            self.heroine.target_alpha = 255 if scene.get("show") else 0
            if self.char_count < len(scene["text"]):
                self.char_count += 0.5

    def draw(self):
        if self.state == "TITLE":
            screen.fill((30, 30, 40))
            title_text = font_title.render("僕らのPythonノベル", True, (255, 255, 255))
            screen.blit(title_text, (SCREEN_SIZE[0]//2 - title_text.get_width()//2, 150))
            
            start_btn = pygame.Rect(300, 350, 200, 50)
            pygame.draw.rect(screen, (100, 100, 150), start_btn)
            screen.blit(font_ui.render("START (Space)", True, (255, 255, 255)), (330, 360))

        elif self.state == "PLAYING":
            scene = self.scenario[self.current_idx]
            screen.fill(scene.get("bg", (40, 40, 40)))
            self.heroine.draw(screen)
            
            pygame.draw.rect(screen, (0, 0, 0), (50, 450, 700, 120))
            txt = scene["text"][:int(self.char_count)]
            screen.blit(font_msg.render(txt, True, (255, 255, 255)), (70, 470))
            
            if "options" in scene and self.char_count >= len(scene["text"]):
                for i, opt in enumerate(scene["options"]):
                    rect = pygame.Rect(200, 150 + i*70, 400, 50)
                    pygame.draw.rect(screen, (50, 50, 150), rect)
                    screen.blit(font_ui.render(opt["text"], True, (255, 255, 255)), (220, 160 + i*70))

        elif self.state == "CLEAR":
            screen.fill((200, 255, 200))
            msg = font_title.render("HAPPY END", True, (0, 100, 0))
            screen.blit(msg, (SCREEN_SIZE[0]//2 - msg.get_width()//2, 200))
            screen.blit(font_ui.render(f"Score: {self.love_points['ヒロイン']}", True, (0, 0, 0)), (350, 300))
            screen.blit(font_ui.render("Space to Title", True, (50, 50, 50)), (330, 450))

        elif self.state == "GAMEOVER":
            screen.fill((50, 0, 0))
            msg = font_title.render("GAME OVER", True, (255, 0, 0))
            screen.blit(msg, (SCREEN_SIZE[0]//2 - msg.get_width()//2, 200))
            screen.blit(font_ui.render("Space to Title", True, (200, 200, 200)), (330, 450))

        elif self.state == "CONFIG":
            screen.fill((20, 20, 20))
            screen.blit(font_msg.render("CONFIG (Esc to Return)", True, (255, 255, 255)), (280, 50))
            pygame.draw.rect(screen, (100, 100, 100), (200, 300, 400, 20))
            knob_x = 200 + (config["bgm_volume"] * 400)
            pygame.draw.circle(screen, (255, 100, 100), (int(knob_x), 310), 15)

# --- 4. メインループ ---
engine = Engine()

while True:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_json(CONFIG_FILE, config)
            pygame.quit(); sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if engine.state in ["PLAYING", "CONFIG"]:
                    engine.state = "CONFIG" if engine.state == "PLAYING" else "PLAYING"
            
            if event.key == pygame.K_SPACE:
                if engine.state == "TITLE":
                    engine.state = "PLAYING"
                elif engine.state in ["CLEAR", "GAMEOVER"]:
                    engine.reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if engine.state == "PLAYING":
                scene = engine.scenario[engine.current_idx]
                
                if "options" in scene and engine.char_count >= len(scene["text"]):
                    for i, opt in enumerate(scene["options"]):
                        if pygame.Rect(200, 150 + i*70, 400, 50).collidepoint(mx, my):
                            engine.love_points["ヒロイン"] += opt.get("love", 0)
                            engine.current_idx = opt["next"]
                            engine.char_count = 0
                
                elif engine.char_count >= len(scene["text"]):
                    if "result" in scene:
                        engine.state = scene["result"]
                    elif engine.current_idx < len(engine.scenario) - 1:
                        engine.current_idx += 1
                        engine.char_count = 0
                else:
                    engine.char_count = len(scene["text"])
            
            elif engine.state == "CONFIG":
                if pygame.Rect(200, 300, 400, 20).collidepoint(mx, my):
                    config["bgm_volume"] = max(0.0, min(1.0, (mx - 200) / 400))

    engine.update()
    engine.draw()
    pygame.display.update()
    clock.tick(60)
