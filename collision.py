# collision.py
"""Xử lý va chạm và phản ứng va chạm trong game."""

import pygame


def handle_bullet_collisions(bullets: list, tanks: list) -> set:
    """
    Kiểm tra từng đạn có trúng tank nào không.

    Quy tắc:
    - Đạn không thể trúng chính tank đã bắn ra nó (owner).
    - Đạn địch không giết địch khác.
    - Khi trúng: đạn bị hủy (alive = False), tank bị đánh dấu destroyed.
    - Hai đạn đi ngược chiều có thể triệt tiêu nhau.
    """
    from tank import EnemyTank

    destroyed = set()

    for bullet in bullets:
        if not bullet.alive:
            continue

        for tank in tanks:
            if tank is bullet.owner:
                continue

            if isinstance(bullet.owner, EnemyTank) and isinstance(tank, EnemyTank):
                continue

            bx = bullet.x - 3
            by = bullet.y - 3
            bw = bh = 6

            tx = tank.x
            ty = tank.y
            ts = tank.size

            if bx < tx + ts and bx + bw > tx and by < ty + ts and by + bh > ty:
                bullet.alive = False
                destroyed.add(tank)

    for i in range(len(bullets)):
        for j in range(i + 1, len(bullets)):
            b1, b2 = bullets[i], bullets[j]
            if not b1.alive or not b2.alive:
                continue
            if abs(b1.x - b2.x) < 8 and abs(b1.y - b2.y) < 8:
                b1.alive = False
                b2.alive = False

    return destroyed


def check_base_destroyed(bullets: list) -> bool:
    """Trả về True nếu có viên đạn nào bắn trúng Base."""
    return any(getattr(b, "hit_base", False) for b in bullets)


def try_move_tank(tank, direction: str, game_map, other_tanks=None) -> bool:
    """Di chuyển tank nếu không bị chặn bởi bản đồ hoặc tank khác."""
    from constants import COLS, ROWS, TILE_SIZE

    tank.direction = direction

    new_x = tank.x
    new_y = tank.y

    if direction == "UP":
        new_y -= tank.speed
    elif direction == "DOWN":
        new_y += tank.speed
    elif direction == "LEFT":
        new_x -= tank.speed
    elif direction == "RIGHT":
        new_x += tank.speed

    new_x = max(0, min(new_x, (COLS - 1) * TILE_SIZE))
    new_y = max(0, min(new_y, (ROWS - 1) * TILE_SIZE))

    if not tank._is_passable(new_x, new_y, game_map):
        return False

    if other_tanks:
        target_rect = pygame.Rect(new_x, new_y, tank.size, tank.size)
        for other in other_tanks:
            if other is tank:
                continue
            if target_rect.colliderect(other.rect):
                if not other._try_push(direction, game_map, other_tanks):
                    return False
                break

    tank.x = new_x
    tank.y = new_y
    tank.rect.topleft = (tank.x, tank.y)
    return True


def resolve_tank_tank_collision(player, enemies: list) -> None:
    """Đẩy player ra khỏi enemy khi xảy ra va chạm trực diện."""
    player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)
        if player_rect.colliderect(enemy_rect):
            if player.direction == "UP":
                player.y += player.speed
            elif player.direction == "DOWN":
                player.y -= player.speed
            elif player.direction == "LEFT":
                player.x += player.speed
            elif player.direction == "RIGHT":
                player.x -= player.speed
            player.rect.topleft = (player.x, player.y)
            break
