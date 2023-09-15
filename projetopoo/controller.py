
from model import VideosEmAlta
import tkinter.messagebox as messagebox
from exceptions import ErroCidadeNaoEncontrada

class VideosEmAltaController:
    def __init__(self, capitais, api_key_youtube, api_key_places):
        self.videos_em_alta_model = VideosEmAlta(capitais, api_key_youtube, api_key_places)

    def buscar_videos_em_alta_por_capital(self, capital):
        try:
            return self.videos_em_alta_model._carregar_videos_por_capital(capital)
        except ErroCidadeNaoEncontrada as e:
            messagebox.showwarning("Vídeos em Alta", str(e))

    def get_capitais(self):
        return self.videos_em_alta_model._capitais

