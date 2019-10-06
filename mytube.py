import sys
from pytube import YouTube
from tqdm import tqdm

class Mytube:
    def __init__(self, url, progress=False, playlist=False):
        self.Progress = progress
        yt = YouTube(url)
        self.YouTube = yt
        self.PreviousSize = None
        self.Pbar = tqdm(total=self.YouTube.streams.get_by_itag(18).filesize)

    def list_stream(self):
        print(self.YouTube.streams.all())
        self.Pbar.close()

    def download(self):
        self.YouTube.register_on_progress_callback(self.update_bar)
        self.YouTube.streams.get_by_itag(18).download()
        self.Pbar.close()

    def update_bar(self, stream, chunk, file_handle, bytes_remaining):
        update_bytes = 0
        if self.PreviousSize is None:
            update_bytes = stream.filesize  - bytes_remaining
            self.PreviousSize = stream.filesize - update_bytes
        else:
            update_bytes = self.PreviousSize - bytes_remaining
            self.PreviousSize = self.PreviousSize - update_bytes
            
        self.Pbar.update(update_bytes)

if __name__ == "__main__":
    Mytube(url="https://www.youtube.com/watch?v=BriBDiBxaMY").download()
