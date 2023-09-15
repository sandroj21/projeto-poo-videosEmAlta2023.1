import tkinter as tk
import tkinter.messagebox as messagebox
import tkintermapview as tkmv
import tkinter.ttk as ttk
from controller import VideosEmAltaController

class VideosEmAltaView:
    def __init__(self, controller):
        self.controller = controller
        self.current_marker = None

        self.window = tk.Tk()
        self.window.title("Buscador de vídeos em alta")

        self.map_frame = tk.Frame(self.window, width=600, height=400)
        self.map_frame.pack(fill=tk.BOTH, expand=True)

        self.interface_frame = tk.Frame(self.window)
        self.interface_frame.pack(side=tk.TOP)

        self.map_view = tkmv.TkinterMapView(self.map_frame, width=600, height=400, corner_radius=2)
        self.map_view.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=4)
        self.map_view.set_position(-12.0464, -51.8481) 
        self.map_view.pack(fill=tk.BOTH, expand=True) 

        titulo_label = tk.Label(self.interface_frame, text="Escolha a cidade", font=("Helvetica", 14))
        titulo_label.pack(pady=5)
        
        self.capitais_combobox = tk.ttk.Combobox(self.interface_frame, values=self.controller.get_capitais())
        self.capitais_combobox.set("Selecione uma capital")
        self.capitais_combobox.pack(pady=10)

        buscar_button = tk.Button(self.interface_frame, text="Buscar", command=self.realizar_busca)
        buscar_button.pack(pady=5)

    def run(self):
        self.window.mainloop()

    def realizar_busca(self):
        capital = self.capitais_combobox.get()
        if capital:
            videos_em_alta = self.controller.buscar_videos_em_alta_por_capital(capital)
            if videos_em_alta:
                mensagem = f"Vídeos em alta em {capital}:\n\n"
                for video in videos_em_alta:
                    mensagem += f"Título: {video.titulo}\nData: {video.data_publicacao}\n\n"
                    self.current_marker = self.map_view.set_marker(video.latitude, video.longitude, text=video.cidade)
                self.centralizar_mapa(videos_em_alta[0].latitude, videos_em_alta[0].longitude) 
                messagebox.showinfo("Vídeos em Alta", mensagem)
            else:
                messagebox.showinfo("Vídeos em Alta", f"Nenhum vídeo em alta encontrado para {capital}.")
        else:
            messagebox.showwarning("Vídeos em Alta", "Selecione uma capital antes de buscar vídeos em alta.")

    def centralizar_mapa(self, latitude, longitude):
        self.map_view.set_position(latitude, longitude) 
