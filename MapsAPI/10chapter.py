from Samples.show_map import show_map_yandex
from Samples.geocoder import get_coordinates, get_ll_span, get_address, get_postal_code
from Samples.try_to_geocode import try_to
import argparse
import pygame
import os
import math

parser = argparse.ArgumentParser()
parser.add_argument('coord_x', type=float)
parser.add_argument('coord_y', type=float)
parser.add_argument('--zoom', type=float, default=5)
parser.add_argument('--type_map', type=str, default='map')
res = parser.parse_args()
pygame.init()
screen = pygame.display.set_mode((600, 450))
info_box = pygame.Rect(5, 70, 100, 200)


def main():
    global flag
    pygame.font.init()
    font = pygame.font.Font(None, 32)
    fond_for_err = pygame.font.Font(None, 16)
    input_box = pygame.Rect(5, 5, 140, 32)
    clear_button = pygame.Rect(5, 43, 110, 24)
    postal_button = pygame.Rect(125, 43, 110, 24)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('black')
    color = color_inactive
    active = False
    flag = False
    postal_flag = False
    text = ''
    end_text = font.render('', True, color)
    step = 0.006
    # Показываем карту с фиксированным масштабом.
    ll_spn = f"ll={res.coord_x},{res.coord_y}&z={res.zoom}&l={res.type_map}"
    x, y, zoom, type_map = res.coord_x, res.coord_y, res.zoom, res.type_map
    show_map_yandex(ll_spn, "map")
    map_file = "map.png"
    types = ['map', 'sat', 'sat,skl']
    info = ''
    postal = ''
    postal_message = 'Включить п.индекс'
    point_param = ''
    # Инициализируем pygame
    looping = True
    count = types.index(type_map)
    while looping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                if clear_button.collidepoint(event.pos):
                    point_param = ''
                    flag = False
                    show_map_yandex(ll_spn, "map")
                if postal_button.collidepoint(event.pos):
                    postal_variant = ['Включить п.индекс', 'Выключить п.индекс']
                    postal_message = postal_variant[(postal_variant.index(postal_message) + 1) % 2]
                    postal_flag = not postal_flag
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        toponym_to_find = text
                        ll = get_ll_span(toponym_to_find)
                        ll_spn = f"ll={ll}&z={zoom}&l={type_map}"
                        if try_to(ll_spn, "map"):
                            # Показываем карту с масштабом, подобранным по заданному объекту.
                            show_map_yandex(ll_spn, "map")
                            x, y = get_coordinates(text)
                            # Добавляем исходную точку на карту.
                            point_param = f"pt={ll}"
                            print(point_param)
                            show_map_yandex(ll_spn, "map", add_params=point_param)
                            end_text = fond_for_err.render('', True, (255, 0, 0))
                            info = get_address(text)
                            postal = get_postal_code(info)
                            flag = True
                        else:
                            end_text = fond_for_err.render('Введите корректное имя поиска', True, (255, 0, 0))
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            key = pygame.key.get_pressed()
            if key[pygame.K_PAGEUP]:
                zoom = zoom + 1 if zoom + 1 < 20 else zoom
                ll_spn = f"ll={x},{y}&z={zoom}&l={type_map}"
                show_map_yandex(ll_spn, "map", add_params=point_param)
            if key[pygame.K_PAGEDOWN]:
                zoom = zoom - 1 if zoom - 1 > 0 else zoom
                ll_spn = f"ll={x},{y}&z={zoom}&l={type_map}"
                show_map_yandex(ll_spn, "map", add_params=point_param)
            if key[pygame.K_UP]:
                y += step * math.pow(2, 15 - zoom)
                ll_spn = f"ll={x},{y}&z={zoom}&l={type_map}"
                show_map_yandex(ll_spn, "map", add_params=point_param)
            if key[pygame.K_DOWN]:
                y -= step * math.pow(2, 15 - zoom)
                ll_spn = f"ll={x},{y}&z={zoom}&l={type_map}"
                show_map_yandex(ll_spn, "map", add_params=point_param)
            if key[pygame.K_RIGHT]:
                x += step * math.pow(2, 15 - zoom)
                ll_spn = f"ll={x},{y}&z={zoom}&l={type_map}"
                show_map_yandex(ll_spn, "map", add_params=point_param)
            if key[pygame.K_LEFT]:
                x -= step * math.pow(2, 15 - zoom)
                ll_spn = f"ll={x},{y}&z={zoom}&l={type_map}"
                show_map_yandex(ll_spn, "map", add_params=point_param)
            if key[pygame.K_HOME]:
                count = (count + 1) % 3
                type_map = types[count]
                ll_spn = f"ll={x},{y}&z={zoom}&l={type_map}"
                show_map_yandex(ll_spn, "map", add_params=point_param)


        # Инициализируем pygame
        # Рисуем картинку, загружаемую из только что созданного файла.
        screen.blit(pygame.image.load(map_file), (0, 0))
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect
        pygame.draw.rect(screen, color, input_box, 1)
        pygame.draw.rect(screen, (200, 200, 200), clear_button)
        screen.blit(pygame.font.Font(None, 16).render('Сбросить метку', True, (0, 0, 0)), (clear_button.x + 5, clear_button.y + 5))
        pygame.draw.rect(screen, (200, 200, 200), postal_button)
        screen.blit(pygame.font.Font(None, 16).render(postal_message, True, (0, 0, 0)),
                    (postal_button.x + 5, postal_button.y + 5))
        screen.blit(end_text, [350, 430])
        if flag:
            pygame.draw.rect(screen, (240, 230, 240), info_box)
            screen.blit(pygame.font.Font(None, 16).render(info, True, (0, 0, 0)),
                        (info_box.x, info_box.y, 100, 200))
            if postal_flag:
                screen.blit(pygame.font.Font(None, 16).render('Почтовыый индекс: ' + postal, True, (0, 0, 0)),
                            (info_box.x, info_box.y + 30, 100, 200))
        # Переключаем экран и ждем закрытия окна.
        pygame.display.flip()
        pygame.display.update()
    pygame.quit()
    # Удаляем за собой файл с изображением.
    os.remove(map_file)


if __name__ == "__main__":
    main()