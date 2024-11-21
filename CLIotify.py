import os
import pygame
from rich.console import Console
from rich.color import Color
from rich.text import Text
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

class MusicPlayer:
    def __init__(self):
        self.songs = []
        self.current_song_index = 0
        self.paused = False
        self.folder_path = ''
        pygame.init()
        pygame.mixer.init()

    def read_songs_from_folder(self, folder_path):
        self.folder_path = folder_path
        for filename in os.listdir(folder_path):
            if filename.endswith(".mp3"):
                self.songs.append(os.path.join(folder_path, filename))

    def list_songs(self):
        console.print("Available songs:", style="bold magenta")
        for i, song in enumerate(self.songs):
            console.print(f"{i + 1}. {song}", style="dim")

    def play_song(self, song_index):
        if song_index.isdigit() and 0 <= int(song_index) - 1 < len(self.songs):
            pygame.mixer.music.load(self.songs[int(song_index) - 1])
            pygame.mixer.music.play()
            self.current_song_index = int(song_index) - 1
            console.print(f"Now playing: {self.songs[self.current_song_index]}", style="dim")
        else:
            console.print("[red]Invalid song index.[/red]")

    def pause_song(self):
        if pygame.mixer.music.get_busy():
            if not self.paused:
                pygame.mixer.music.pause()
                self.paused = True
                console.print("[yellow]Song paused.[/yellow]")
            else:
                pygame.mixer.music.unpause()
                self.paused = False
                console.print("[yellow]Song resumed.[/yellow]")
        else:
            console.print("[red]No song is currently playing.[/red]")

    def stop_song(self):
        pygame.mixer.music.stop()
        console.print("[red]Song stopped.[/red]")

    def next_song(self):
        if len(self.songs) > 1:
            self.current_song_index += 1
            if self.current_song_index >= len(self.songs):
                self.current_song_index = 0
            self.play_song(str(self.current_song_index + 1))

    def previous_song(self):
        if len(self.songs) > 1:
            self.current_song_index -= 1
            if self.current_song_index < 0:
                self.current_song_index = len(self.songs) - 1
            self.play_song(str(self.current_song_index + 1))

    def seek_song(self, seconds):
        pygame.mixer.music.set_pos(seconds)
        console.print(f"[cyan]Seeked to {seconds} seconds.[/cyan]")

    def shuffle_songs(self):
        import random
        random.shuffle(self.songs)
        self.play_song("1")

    def run(self):
        centered_text = "CLIotify Music Player".center(85)
        console.print(Panel(centered_text, style="bold magenta",width=89))
        ascii_art = """                    ⠀⠀⠀⠀⠀⠀⠀⠀⣾⣛⡿⡿⢽⣶⣤⣀⣀⣀⣀⣀⣀⣠⣴⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⢠⣿⢬⡭⢭⣭⣽⣗⡋⠈⠉⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⡞⠁⣂⡠⠾⢛⣛⣀⣀⠀⠀⠙⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⣟⠛⠃⡀⣀⡉⠀⠄⠄⠈⠉⠑⠢⣄⡉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠈⠲⣍⣿⣿⣿⣿⣿⣿⣿⡉⠛⢿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⢿⣿⣖⠿⣯⢆⠀⠀⢁⠞⠉⠙⠻⠿⣿⣿⣿⣿⣦⣀⣩⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⣤⡄⠀⠀⠀⢀⡴⠛⢓⡜⢿⣿⣆⢀⢿⠀⠀⢻⣄⡀⠀⠀⠀⢒⣛⣫⣿⡟⠻⢿⠿⣾⡻⣿⡆⠀⠀⠀⠀⠀⠀⠀
                    ⢀⡀⢤⣤⢾⣿⣷⠄⢀⡠⠈⣄⠤⠀⠛⢾⣿⣿⣾⡎⠀⠀⠀⠈⠛⠒⠀⠀⠀⠀⠀⢈⣑⡒⠤⠄⣀⣈⣭⠗⠀⠀⠀⠀⠀⠀⠀
                    ⡏⠈⠉⠉⣿⣿⣿⠍⠹⣿⡄⠉⠻⢶⣌⠀⠻⣿⣿⣿⣷⣶⣴⣾⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣦⣄⣒⣊⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠹⡦⡁⠀⠸⡟⣿⣤⢬⢿⠀⠀⠀⠀⠉⡷⣄⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣶⣤⣤⣀⠀⠀
                    ⠀⠙⢾⡴⠄⡀⢸⣿⡏⠁⠀⠀⠀⠀⠀⠈⠪⡓⢤⡈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣿⣟⢵⣆⣈⣍⣿⣿⣿⣿⣷⡄
                    ⠀⠀⠀⢷⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠈⠂⢌⡓⠢⢤⣉⠉⠛⠻⢿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⠿⠛⠛⠛⠛⢛⣨⣿⡗
                    ⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠲⠤⠍⣒⡂⠀⢼⡉⠛⠁⠀⠀⠀⣠⠟⠻⠙⠉⠀⠁⣉⣁⡠⠔⠀
                    ⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠒⡇⠀⠀⠀⠀⠈⢀⡠⠔⠒⠀⠉⠉⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⢹⡘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⡿⣕⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⠤⠄⠰⠤⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⢳⡎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣺⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⢻⣿⣾⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⢀⡶⠏⠉⠻⢿⣿⣿⣿⣿⣿⡷⠆⠙⠿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠘⣄⠀⠀⠀⠈⣛⣿⡿⠟⢿⣷⣮⣸⡐⠛⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠙⠯⢒⣲⠄⠀⠀⠀⢄⣠⠀⠈⠿⣿⡀⠀⢻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠐⠲⢌⣓⠤⣀⠀⠀⠀⠈⢳⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠂⠭⠝⣒⠻⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    """
        console.print(Text(ascii_art, style="bold magenta"  ))

        folder_path = Prompt.ask("Enter the folder path")
        self.read_songs_from_folder(folder_path)
        console.print("[magenta]Folder Initialized[/magenta]")
        
        while True:
            console.print("[magenta]Options: list songs, play, pause/resume, stop, nextback shuffle, forward, reverse, quit[/magenta]")
            choice = Prompt.ask("Choose an option", choices=["l", "p", "pause", "resume", "s", "n", "b", "f", "r", "shuffle", "q"])

            if choice == 'l':
                self.list_songs()
            elif choice == 'p' or choice == 'play':
                song_index = Prompt.ask("Enter song number to play")
                self.play_song(song_index)
            elif choice == 'pause' or choice == 'resume':
                self.pause_song()
            elif choice == 's' or choice == 'stop':
                self.stop_song()
            elif choice == 'n' or choice == 'next':
                self.next_song()
            elif choice == 'b' or choice == 'back':
                self.previous_song()
            elif choice == 'f' or choice == 'forward':
                seconds = Prompt.ask("Enter the number of seconds to skip forward", type=int)
                self.seek_song(seconds)
            elif choice == 'r' or choice == 'reverse':
                seconds = Prompt.ask("Enter the number of seconds to skip backward", type=int)
                self.seek_song(-seconds)
            elif choice == 'shuffle':
                self.shuffle_songs()
            elif choice == 'q' or choice == 'quit':
                break
            else:
                console.print("[red]Invalid option. Please try again.[/red]")


if __name__ == "__main__":
    music_player = MusicPlayer()
    music_player.run()
