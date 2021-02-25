import pygame
import requests
import sys
import os


def show_map(ll_spn=None, map_type="map", add_params=None):
    looping = True
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    map_file = "map.png"

    def mapping():
        if ll_spn:
            map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}"
            print(ll_spn)
        else:
            map_request = f"http://static-maps.yandex.ru/1.x/?l={map_type}"

        if add_params:
            map_request += "&" + add_params
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        try:
            with open(map_file, "wb") as file:
                file.write(response.content)
        except IOError as ex:
            print("Ошибка записи временного файла:", ex)
            sys.exit(2)

    while looping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]:
                a = str(ll_spn).split('&')
                b = a[1].split('=')
                print(b)
                ll_spn = '&'.join((a[0], '='.join((b[0],
                                                   ','.join((str(round(float(b[1].split(',')[0]) - 1, 5) if float(b[1].split(',')[0]) - 1 > 0 else float(b[1].split(',')[0])),
                                                             str(round(float(b[1].split(',')[1]) - 1, 5) if float(b[1].split(',')[1]) - 1 > 0 else float(b[1].split(',')[1]))))))))
                mapping()
            if key[pygame.K_DOWN]:
                a = str(ll_spn).split('&')
                b = a[1].split('=')
                print(b)
                ll_spn = '&'.join((a[0], '='.join((b[0],
                                                   ','.join((str(round(float(b[1].split(',')[0]) + 1, 5) if float(b[1].split(',')[0]) + 1 > 0 else float(b[1].split(',')[0])),
                                                             str(round(float(b[1].split(',')[1]) + 1, 5) if float(b[1].split(',')[1]) + 1 > 0 else float(b[1].split(',')[1]))))))))
                mapping()
        # Инициализируем pygame
        # Рисуем картинку, загружаемую из только что созданного файла.
        screen.blit(pygame.image.load(map_file), (0, 0))
        # Переключаем экран и ждем закрытия окна.
        pygame.display.flip()
        pygame.display.update()
    pygame.quit()
    # Удаляем за собой файл с изображением.
    os.remove(map_file)
