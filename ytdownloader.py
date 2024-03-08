# YouTube'dan video indirmek için pytube kütüphanesini kullanıyoruz
from pytube import YouTube  

#Videoyu tiktok a upload etmek icin tiktok_uploader kullaniyoruz.
from Tiktok_uploader import uploadVideo  

# Video işleme için ffmpeg kütüphanesini kullanıyoruz
import ffmpeg  

# YouTube video URL - Kullanıcıdan YouTube video URL'sini alıyoruz
video_url = input("Video URL'ini yapıştırınız: ")  

# YouTube video nesnesini oluştur
yt = YouTube(video_url)  

# Video başlığını al
video_title = yt.title 

# En yüksek çözünürlüklü videoyu indiriyoruz ve "original.mp4" olarak kaydediyoruz
yt.streams.get_highest_resolution().download(filename="original.mp4")  

# İndirilen videoyu TikTok formatına dönüştürme
def prepare_for_tiktok(input_file, output_file, title):
    # Giriş videosunu ve sesini yüksek çözünürlüklü formatında tanımla
    original_video = ffmpeg.input(input_file)
    audio_input = ffmpeg.input(input_file)

    # Ses akışını al ve ilk 60 saniyeyi kes
    audio_stream = audio_input.audio.filter('atrim', start=0, end=60)

    # Sesin girişine ve çıkışına fade in ve fade out efektleri ekle
    audio_stream = audio_stream.filter('afade', t='in', st=0, d=3).filter('afade', t='out', st=57, d=3)

    # İlk 60 saniyeyi kesiyoruz. (Tiktok 60 saniye aliyordu sanirim)
    cut_video = original_video.trim(start_frame=0, end_frame=60*yt.streams.get_highest_resolution().fps) 

    # Videoyu 1:1 formatına dönüştürme
    square_video = cut_video.filter('scale', 1080, 1080).filter('pad', 1080, 1920, 0, '(1920 - ih) / 2', color='black')  

    # Videoyu TikTok formatına dönüştürme ve sesi ekleyerek çıktıyı al
    ffmpeg.output(square_video, audio_stream, output_file, vcodec='libx264', acodec='aac', pix_fmt='yuv420p', aspect='9:16').run()

# prepare_for_tiktok fonksiyonunu çağırarak dönüşümü gerçekleştiriyoruz
prepare_for_tiktok("original.mp4", f"{video_title}_tiktok_ready.mp4", video_title)  

#### Tiktok yükleme

session_id = "cookie_sessionid_"
file = "/Users/mac/Desktop/python/azerbulbul.mp4"
title = "Video Title"
tags = ["tag1", "tag2", "tag3"]

# Publish the video
uploadVideo(session_id, file, title, tags, verbose=True)
