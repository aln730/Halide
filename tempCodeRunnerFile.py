import os
import pygame
from rich.console import Console
from rich.color import Color
from rich.text import Text
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TimeRemainingColumn, TextColumn  # Fixed import
import time
import sys
import threading

console = Console()

# Helper function to convert seconds to MM:SS format
def seconds_to_mmss(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

# Updated time_duration_bar using rich.progress for an aesthetic progress bar
def time_duration_bar(total_time, bar_length=30, stop_flag=None):
    with Progress(
        TextColumn("[magenta]{task.description}"),
        BarColumn(style="dim"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Playing Song", total=total_time)
        
        while not progress.finished:
            if stop_flag and stop_flag():
                progress.stop()  # Stop the progress bar if the stop flag is set
                break

            # Update the progress bar every second
            progress.update(task, completed=progress.tasks[0].completed + 1)
            
            # Calculate elapsed time in MM:SS format
            elapsed_seconds = int(progress.tasks[0].completed)
            elapsed_time = seconds_to_mmss(elapsed_seconds)
            remaining_time = seconds_to_mmss(total_time - elapsed_seconds)
            
            # Update the task description to show elapsed/remaining time in MM:SS format
            progress.update(task, description=f"Elapsed: {elapsed_time}")
            
            time.sleep(1)  # Update every second

# The MusicPlayer class
class MusicPlayer:
    def __init__(self):
        self.songs = []
        self.current_song_index = 0
        self.paused = False
        self.folder_path = ''
        self.stop_flag = False  # Flag to stop the progress bar
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
            song_length = pygame.mixer.Sound(self.songs[self.current_song_index]).get_length()
            console.print(f"Now playing: {self.songs[self.current_song_index]}", style="dim")
            
            # Reset stop flag and start the progress bar in a separate thread
            self.stop_flag = False
            progress_thread = threading.Thread(target=time_duration_bar, args=(int(song_length),), kwargs={"stop_flag": self.is_song_stopped})
            progress_thread.daemon = True  # This allows the thread to close when the program ends
            progress_thread.start()
        else:
            console.print("[red]Invalid song index.[/red]")

    def is_song_stopped(self):
        return self.stop_flag  # Returns True if the song should be stopped

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
        self.stop_flag = True  # Set the stop flag to stop the progress bar
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
        centered_text = "CLIotify Music Player\n"
        console.print(centered_text, style="bold magenta", width=89)
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
        console.print(Text(ascii_art, style="bold magenta"))

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
