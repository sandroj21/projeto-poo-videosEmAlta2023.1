from googleapiclient.discovery import build
from datetime import datetime
import requests
from typing import List
from exceptions import ErroCidadeNaoEncontrada

class Video:
    def __init__(self, titulo, data_publicacao, pais, cidade, latitude, longitude):
        self._titulo = titulo
        self._data_publicacao = data_publicacao
        self._pais = pais
        self._cidade = cidade
        self._latitude = latitude
        self._longitude = longitude

    def __repr__(self):
        return f'Título: {self._titulo} | País: {self._pais} | Cidade: {self._cidade} | Data de Publicação: {self._data_publicacao} | Latitude: {self._latitude} | Longitude: {self._longitude}'

    @property
    def titulo(self):
        return self._titulo

    @property
    def data_publicacao(self):
        return self._data_publicacao

    @property
    def pais(self):
        return self._pais

    @property
    def cidade(self):
        return self._cidade

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

class VideosEmAlta():
    def __init__(self, capitais, api_key_youtube, api_key_places):
        self._capitais = capitais
        self._api_key_youtube = api_key_youtube
        self._api_key_places = api_key_places
        self._videos = self._carregar_videos_em_alta()

    def __iter__(self):
        return iter(self._videos)

    def _carregar_videos_em_alta(self):
        videos_em_alta = []

        for capital in self._capitais:
            videos = self._carregar_videos_por_capital(capital)
            videos_em_alta.extend(videos)

        videos_em_alta.sort(key=lambda video: video.data_publicacao)
        return videos_em_alta

    def _carregar_videos_por_capital(self, capital):
        youtube = build('youtube', 'v3', developerKey=self._api_key_youtube)

        parametros = {
            'part': 'snippet',
            'chart': 'mostPopular',
            'regionCode': '', 
            'maxResults': 10
        }

        
        if capital == 'Lima':
            parametros['regionCode'] = 'PE' 
        elif capital == 'La Paz':
            parametros['regionCode'] = 'BO'
        elif capital == 'Bogotá':
            parametros['regionCode'] = 'CO'
        elif capital == 'Caracas':
            parametros['regionCode'] = 'VE'
        elif capital == 'Buenos Aires':
            parametros['regionCode'] = 'AR'
        elif capital == 'Quito':
            parametros['regionCode'] = 'EC'
        elif capital == 'Montevidéu':
            parametros['regionCode'] = 'UY'
        elif capital == 'Santiago':
            parametros['regionCode'] = 'CL'
        elif capital == 'Washington D.C.':
            parametros['regionCode'] = 'US'
        elif capital == 'Cidade do México':
            parametros['regionCode'] = 'MX'
        elif capital == 'Ottawa':
            parametros['regionCode'] = 'CA'
        elif capital == 'Brasília':
            parametros['regionCode'] = 'BR'
        else:
            raise ErroCidadeNaoEncontrada(f"Cidade não encontrada: {capital}")

        resposta = youtube.videos().list(**parametros).execute()

        videos = []
        for item in resposta['items']:
            titulo = item['snippet']['title']
            data_publicacao_str = item['snippet']['publishedAt']
            data_publicacao = datetime.strptime(data_publicacao_str, '%Y-%m-%dT%H:%M:%SZ')
            latitude, longitude = self._obter_lat_lon_por_cidade(capital)
            video = Video(titulo, data_publicacao, parametros['regionCode'], capital, latitude, longitude)
            videos.append(video)

        return videos
    def _obter_lat_lon_por_cidade(self, cidade):
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        parametros = {
            "input": cidade,
            "inputtype": "textquery",
            "fields": "geometry/location",
            "key": self._api_key_places
        }

        response = requests.get(url, params=parametros)
        data = response.json()

        if data["status"] == "OK" and "candidates" in data:
            location = data["candidates"][0]["geometry"]["location"]
            latitude = location["lat"]
            longitude = location["lng"]
            return latitude, longitude

        return 0.0, 0.0

