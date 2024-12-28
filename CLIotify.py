import os
import pygame
from rich.console import Console
from rich.prompt import Prompt
import time
import random

console = Console()

class MusicPlayer:
    def __init__(self):
        """Initializes the music player with an empty playlist and a current song index."""
        self.songs = []
        self.current_song_index = 0
        pygame.mixer.init()
        self.stop_flag = None

    def read_songs_from_folder(self, folder_path):
        """Loads all MP3 songs from the specified folder into the playlist."""
        try:
            self.songs = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.mp3')]
            console.print("[magenta]Folder Initialized[/magenta]", justify="center")
        except FileNotFoundError:
            console.print("[bold red]Error: Folder not found.[/bold red]", justify="center")

    def validate_input(self, prompt_message, valid_choices=None, cast_type=None):
        """Validates user input based on given choices and optional type casting."""
        while True:
            user_input = Prompt.ask(prompt_message)
            if valid_choices and user_input not in valid_choices:
                console.print(f"[bold red]Invalid choice. Choose from {', '.join(valid_choices)}.[/bold red]", justify="center")
                continue
            if cast_type:
                try:
                    user_input = cast_type(user_input)
                except ValueError:
                    console.print("[bold red]Invalid input type. Please try again.[/bold red]", justify="center")
                    continue
            return user_input

    def play_song(self, song_index):
        """Plays the song at the given index in the playlist."""
        try:
            song_index = int(song_index) - 1
            if 0 <= song_index < len(self.songs):
                pygame.mixer.music.load(self.songs[song_index])
                pygame.mixer.music.play()
                self.current_song_index = song_index
                console.print(f"[cyan]Playing: {os.path.basename(self.songs[song_index])}[/cyan]", justify="center")
            else:
                console.print("[bold red]Invalid song number.[/bold red]", justify="center")
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a number.[/bold red]", justify="center")

    def is_playing(self):
        """Checks if any song is currently playing."""
        return pygame.mixer.music.get_busy()

    def pause_song(self):
        """Pauses the currently playing song."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            console.print("[cyan]Paused[/cyan]", justify="center")
        else:
            console.print("[bold red]No song is currently playing.[/bold red]", justify="center")

    def resume_song(self):
        """Resumes the song if it's paused."""
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
            console.print("[cyan]Resumed[/cyan]", justify="center")
        else:
            console.print("[bold red]No song is paused.[/bold red]", justify="center")

    def stop_song(self):
        """Stops the currently playing song."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            console.print("[magenta]Stopped[/magenta]", justify="center")
        else:
            console.print("[bold red]No song is currently playing.[/bold red]", justify="center")

    def next_song(self):
        """Plays the next song in the playlist."""
        self.current_song_index = (self.current_song_index + 1) % len(self.songs)
        self.play_song(str(self.current_song_index + 1))

    def previous_song(self):
        """Plays the previous song in the playlist."""
        self.current_song_index = (self.current_song_index - 1) % len(self.songs)
        self.play_song(str(self.current_song_index + 1))

    def seek_song(self, seconds):
        """Seeks the current song by the specified number of seconds."""
        try:
            seconds = int(seconds)
            if pygame.mixer.music.get_busy():
                current_position = pygame.mixer.music.get_pos() / 1000
                new_position = current_position + seconds
                pygame.mixer.music.set_pos(new_position)
                console.print(f"[cyan]Seeked to {seconds:.0f} seconds.[/cyan]", justify="center")
            else:
                console.print("[bold red]No song is currently playing.[/bold red]", justify="center")
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a number.[/bold red]", justify="center")

    def shuffle_songs(self):
        """Shuffles the playlist and plays the first song."""
        random.shuffle(self.songs)
        self.play_song("1")
        console.print("[magenta]Songs shuffled![/magenta]", justify="center")

    def list_songs(self):
        """Displays all the songs available in the playlist."""
        if not self.songs:
            console.print("[bold red]No songs available.[/bold red]", justify="center")
            return

        console.print("Available songs:", style="bold magenta", justify="center")

        for i in range(0, len(self.songs), 15):
            line_songs = self.songs[i:i + 15]
            line_display = [f"{index + 1 + i}. {os.path.basename(song)}" for index, song in enumerate(line_songs)]
            console.print(" | ".join(line_display), style="dim", justify="center")

    def search_songs(self, search_query):
        """Searches for songs in the playlist based on the given query."""
        matched_songs = [f"{index + 1}. {os.path.basename(song)}" for index, song in enumerate(self.songs) if search_query.lower() in os.path.basename(song).lower()]
        if matched_songs:
            console.print(f'[bold magenta]Search results for "{search_query}":[/bold magenta]', justify="center")
            console.print(" | ".join(matched_songs), style="cyan", justify="center")
        else:
            console.print(f"[bold red]No songs found matching '{search_query}'[/bold red]", justify="center")

    def display_ascii_art(self):
        """Displays ASCII art as a fun welcome message."""
        ascii_art = """
                                     ░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓██████▓▒░▒▓████████▓▒░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                                    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
                                    ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
                                    ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░▒▓██████▓▒░  ░▒▓██████▓▒░  
                                    ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░     
                                    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░     
                                     ░▒▓██████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓██████▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░     
                                                                                           
                                                                                           
"""
        console.print(ascii_art, style="bold magenta",justify="full")

    def add_song(self, song_path):
        """Adds a new song to the playlist from the specified file path."""
        if os.path.exists(song_path) and song_path.endswith(".mp3"):
            self.songs.append(song_path)
            console.print(f"[cyan]Added {os.path.basename(song_path)} to the playlist.[/cyan]", justify="center")
        else:
            console.print("[bold red]Invalid song path. Please ensure it's an mp3 file.[/bold red]", justify="center")

    def remove_song(self, song_index):
        """Removes a song from the playlist by its index."""
        try:
            song_index = int(song_index) - 1
            if 0 <= song_index < len(self.songs):
                removed_song = self.songs.pop(song_index)
                console.print(f"[cyan]Removed {os.path.basename(removed_song)} from the playlist.[/cyan]", justify="center")
            else:
                console.print("[bold red]Invalid song number.[/bold red]", justify="center")
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a valid number.[/bold red]", justify="center")

    def toggle_mute(self):
        """Toggles between mute and unmute for the music player."""
        current_volume = pygame.mixer.music.get_volume()
        if current_volume > 0:
            pygame.mixer.music.set_volume(0)
            console.print("[cyan]Muted[/cyan]", justify="center")
        else:
            pygame.mixer.music.set_volume(1)
            console.print("[cyan]Unmuted[/cyan]", justify="center")

    def run(self):
        """Runs the main loop for interacting with the user and controlling music playback."""
        self.display_ascii_art()
        folder_path = Prompt.ask("Enter the folder path to load songs")
        self.read_songs_from_folder(folder_path)
        commands = {
            "l": self.list_songs,
            "search": lambda: self.search_songs(Prompt.ask("Enter the song you want to search")),
            "p": lambda: self.play_song(self.validate_input("Enter the song number to play", cast_type=int)),
            "play": lambda: self.play_song(self.validate_input("Enter the song number to play", cast_type=int)),
            "pause": self.pause_song,
            "resume": self.resume_song,
            "s": self.stop_song,
            "stop": self.stop_song,
            "n": self.next_song,
            "next": self.next_song,
            "b": self.previous_song,
            "back": self.previous_song,
            "f": lambda: self.seek_song(self.validate_input("Enter seconds to forward", cast_type=int)),
            "forward": lambda: self.seek_song(self.validate_input("Enter seconds to forward", cast_type=int)),
            "r": lambda: self.seek_song(-self.validate_input("Enter seconds to reverse", cast_type=int)),
            "reverse": lambda: self.seek_song(-self.validate_input("Enter seconds to reverse", cast_type=int)),
            "shuffle": self.shuffle_songs,
            "m": self.toggle_mute,
            "mute": self.toggle_mute,
            "a": lambda: self.add_song(Prompt.ask("Enter the song path to add")),
            "add": lambda: self.add_song(Prompt.ask("Enter the song path to add")),
            "re": lambda: self.remove_song(self.validate_input("Enter the song number to remove", cast_type=int)),
            "remove": lambda: self.remove_song(self.validate_input("Enter the song number to remove", cast_type=int)),
            "q": lambda: console.print("[bold green]Exiting the player...[/bold green]", justify="center")
        }

        while True:
            choice = Prompt.ask("What do you want to do?").strip().lower()
            if choice in commands:
                if choice == "q":
                    commands[choice]()  
                    break
                else:
                    commands[choice]()
            else:
                console.print("[red]Invalid option! Try again.[/red]")


if __name__ == "__main__":
    player = MusicPlayer()
    player.run()
