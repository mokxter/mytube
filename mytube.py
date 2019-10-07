import getopt
from sys import argv, exit
from pytube import YouTube
from tqdm import tqdm

class Mytube:
    def __init__(self, url, progress=False, playlist=False):
        self.Progress = progress
        yt = YouTube(url)
        self.YouTube = yt
        self.PreviousSize = None
        self.Pbar = tqdm(total=self.YouTube.streams.first().filesize)

    def list_stream(self):
        print(self.YouTube.streams.all())
        self.Pbar.close()

    def download(self):
        self.YouTube.register_on_progress_callback(self.update_bar)
        self.YouTube.streams.first().download()
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

def main(argv):
    input_url_var = input("Enter url: ")

    try:
        opts, args = getopt.getopt(argv,'',['progress=','playlist='])
    except getop.GetoptError:
        print('Invalid argument')
        exit(2)

    if (len(input_url_var) == 0):
        # Exit immaturely
        exit(1)

    Mytube(url=input_url_var).download()

    # Exit properly
    exit(0)

if __name__ == "__main__":
    main(argv[1:])
