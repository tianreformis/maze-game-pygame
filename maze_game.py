import pygame
import random
import os
import json
from pathlib import Path
import sys

os.environ['SDL_VIDEODRIVER'] = 'windib'

pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 30
cols = WIDTH // CELL_SIZE
rows = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 48)

class GameState:
    def __init__(self):
        self.level = 1
        self.lives = 3
        self.failures = 0
        self.time_limit = 60
        self.current_time = 0
        self.game_over = False
        self.victory = False
        self.maze = []
        self.player_pos = [1, 1]
        self.exit_pos = [cols - 2, rows - 2]
        
    def save_game(self, filename="savegame.json"):
        data = {
            "level": self.level,
            "lives": self.lives,
            "failures": self.failures,
            "time_limit": self.time_limit
        }
        with open(filename, "w") as f:
            json.dump(data, f)
    
    def load_game(self, filename="savegame.json"):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                self.level = data.get("level", 1)
                self.lives = data.get("lives", 3)
                self.failures = data.get("failures", 0)
                self.time_limit = data.get("time_limit", 60)
            return True
        return False

def generate_maze(level):
    max_attempts = 100
    for attempt in range(max_attempts):
        maze = [[1 for _ in range(cols)] for _ in range(rows)]
        
        stack = [(1, 1)]
        maze[1][1] = 0
        
        while stack:
            x, y = stack[-1]
            neighbors = []
            
            for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
                nx, ny = x + dx, y + dy
                if 1 <= nx < cols - 1 and 1 <= ny < rows - 1 and maze[ny][nx] == 1:
                    neighbors.append((nx, ny, dx, dy))
            
            if neighbors:
                nx, ny, dx, dy = random.choice(neighbors)
                maze[y + dy // 2][x + dx // 2] = 0
                maze[ny][nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()
        
        maze[1][1] = 0
        
        exit_x, exit_y = cols - 2, rows - 2
        if maze[exit_y][exit_x] == 0:
            if is_path_valid(maze, (1, 1), (exit_x, exit_y)):
                add_walls(maze, level)
                return maze
        
        if maze[exit_y][exit_x] == 1:
            neighbors = []
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = exit_x + dx, exit_y + dy
                if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0:
                    neighbors.append((nx, ny))
            
            if neighbors:
                maze[exit_y][exit_x] = 0
                nx, ny = random.choice(neighbors)
                maze[ny][nx] = 0
                if is_path_valid(maze, (1, 1), (exit_x, exit_y)):
                    add_walls(maze, level)
                    return maze
    
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    for y in range(rows):
        for x in range(cols):
            if x == 0 or x == cols - 1 or y == 0 or y == rows - 1:
                maze[y][x] = 1
    add_walls(maze, level)
    return maze

def add_walls(maze, level):
    num_walls = level * 5
    max_attempts_add = num_walls * 3
    
    for _ in range(max_attempts_add):
        wx = random.randint(1, cols - 2)
        wy = random.randint(1, rows - 2)
        
        if maze[wy][wx] == 0:
            if (wx, wy) != (1, 1) and (wx, wy) != (cols - 2, rows - 2):
                maze[wy][wx] = 1
                
                if not is_path_valid(maze, (1, 1), (cols - 2, rows - 2)):
                    maze[wy][wx] = 0
                
                num_walls -= 1
                if num_walls <= 0:
                    break

def is_path_valid(maze, start, exit_pos):
    from collections import deque
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        x, y = queue.popleft()
        if (x, y) == exit_pos:
            return True
        
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    
    return False

def draw_maze(maze, player_pos, exit_pos):
    screen.fill(BLACK)
    
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, DARK_GRAY, rect, 1)
            else:
                pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.rect(screen, (30, 30, 30), rect, 1)
    
    exit_rect = pygame.Rect(exit_pos[0] * CELL_SIZE, exit_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, GREEN, exit_rect)
    
    player_rect = pygame.Rect(player_pos[0] * CELL_SIZE + 3, player_pos[1] * CELL_SIZE + 3, CELL_SIZE - 6, CELL_SIZE - 6)
    pygame.draw.rect(screen, BLUE, player_rect)

def draw_ui(state):
    level_text = font.render(f"Level: {state.level}/10", True, WHITE)
    lives_text = font.render(f"Lives: {state.lives}", True, WHITE)
    time_text = font.render(f"Time: {int(state.current_time)}s", True, YELLOW if state.current_time < 10 else WHITE)
    
    screen.blit(level_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))
    screen.blit(time_text, (WIDTH // 2 - 50, 10))

def show_menu():
    clock_menu = pygame.time.Clock()
    while True:
        clock_menu.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if buttons[0].collidepoint(mouse_pos):
                    return "new"
                elif buttons[1].collidepoint(mouse_pos):
                    return "load"
                elif buttons[2].collidepoint(mouse_pos):
                    return "exit"

        screen.fill(BLACK)
        title = title_font.render("MAZE RUNNER", True, GREEN)
        title_rect = title.get_rect(center=(WIDTH // 2, 150))
        screen.blit(title, title_rect)
        
        options = ["NEW GAME", "LOAD GAME", "EXIT"]
        buttons = []
        
        for i, option in enumerate(options):
            btn_rect = pygame.Rect(WIDTH // 2 - 100, 250 + i * 60, 200, 50)
            color = BLUE if i == 0 else (GRAY if i == 1 else RED)
            pygame.draw.rect(screen, color, btn_rect)
            pygame.draw.rect(screen, WHITE, btn_rect, 2)
            
            text = font.render(option, True, WHITE)
            text_rect = text.get_rect(center=btn_rect.center)
            screen.blit(text, text_rect)
            buttons.append(btn_rect)
        
        pygame.display.flip()

def show_game_over(victory, level):
    while True:
        screen.fill(BLACK)
        if victory:
            msg = "YOU WIN!"
            color = GREEN
        else:
            msg = "GAME OVER"
            color = RED
        
        title = title_font.render(msg, True, color)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(title, title_rect)
        
        level_text = font.render(f"Reached Level: {level}", True, WHITE)
        level_rect = level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        screen.blit(level_text, level_rect)
        
        continue_text = font.render("Press any key to continue...", True, GRAY)
        continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(continue_text, continue_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                return

def play_level(state):
    state.maze = generate_maze(state.level)
    state.player_pos = [1, 1]
    state.exit_pos = [cols - 2, rows - 2]
    state.current_time = state.time_limit - (state.level - 1) * 3
    state.current_time = max(state.current_time, 20)
    state.game_over = False
    
    start_ticks = pygame.time.get_ticks()
    
    while not state.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                new_pos = list(state.player_pos)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    new_pos[1] -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    new_pos[1] += 1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    new_pos[0] -= 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    new_pos[0] += 1
                
                if 0 <= new_pos[0] < cols and 0 <= new_pos[1] < rows:
                    if state.maze[new_pos[1]][new_pos[0]] == 0:
                        state.player_pos = new_pos
        
        elapsed = (pygame.time.get_ticks() - start_ticks) / 1000
        state.current_time = max(0, (state.time_limit - (state.level - 1) * 3) - elapsed)
        
        if state.player_pos == state.exit_pos:
            if state.level >= 10:
                state.victory = True
                state.game_over = True
                return "victory"
            else:
                state.level += 1
                state.game_over = True
                return "next_level"
        
        if state.current_time <= 0:
            state.failures += 1
            state.lives -= 1
            if state.lives <= 0:
                state.game_over = True
                return "game_over"
            else:
                state.game_over = True
                return "fail"
        
        draw_maze(state.maze, state.player_pos, state.exit_pos)
        draw_ui(state)
        pygame.display.flip()
        clock.tick(60)
    
    return "quit"

def main():
    state = GameState()
    
    while True:
        choice = show_menu()
        
        if choice == "exit":
            break
        elif choice == "load":
            if not state.load_game():
                continue
        elif choice == "new":
            state = GameState()
        
        while state.level <= 10:
            result = play_level(state)
            
            if result == "quit":
                break
            elif result == "victory":
                show_game_over(True, state.level)
                break
            elif result == "game_over":
                state.level = 1
                state.lives = 3
                state.failures = 0
                show_game_over(False, state.level)
                break
            elif result == "fail":
                if state.failures >= 3:
                    state.level = 1
                    state.lives = 3
                    state.failures = 0
                elif state.lives <= 0:
                    state.level = 1
                    state.lives = 3
                    state.failures = 0
            elif result == "next_level":
                state.save_game()
        
        if state.level > 10:
            show_game_over(True, 10)
    
    pygame.quit()

if __name__ == "__main__":
    main()
