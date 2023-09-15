
from controller import VideosEmAltaController
from view import VideosEmAltaView

def main():
    api_key_youtube = 'AIzaSyB7FavJFSoi4fSsgb8d1pbdFgHccEdTjIg'
    api_key_places = 'AIzaSyDT47iJ95WhJ5mWLJGVLOKddsKihRU7too'
    capitais = ['Lima', 'Brasília', 'La Paz', 'Bogotá', 'Caracas', 'Buenos Aires', 'Quito', 'Montevidéu', 'Santiago', 'Washington D.C.', 'Cidade do México', 'Ottawa']

    controller = VideosEmAltaController(capitais, api_key_youtube, api_key_places)
    view = VideosEmAltaView(controller)
    view.run()

if __name__ == '__main__':
    main()
