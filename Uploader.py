from constants import *
from tiktok_uploader.upload import upload_video
from tiktok_uploader.auth import AuthBackend

class Uploader:
    def __init__(self):
        pass

    def upload(self, path_to_file : str, description : str):
        pass

class TikTokUploader(Uploader):
    def __init__(self):
        super().__init__()

    def upload(self, path_to_file : str, description : str):
        # single video
        upload_video(path_to_file,
                    description=description,
                    cookies=TIKTOK_COOKIES_FILEPATH)

if __name__ == "__main__":
    # vid = "completed_videos/_8730c0ed-8968-4e53-8e71-6aee486efb67.mp4"
    # t_upload = TikTokUploader()
    # t_upload.upload(vid)
    pass