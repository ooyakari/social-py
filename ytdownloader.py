from pytube import YouTube  # YouTube'dan video indirmek için pytube kütüphanesini kullanıyoruz
from Tiktok_uploader import uploadVideo
import ffmpeg  # Video işleme için ffmpeg kütüphanesini kullanıyoruz

# YouTube video URL
video_url = input("Video URL'ini yapıştırınız: ")  # Kullanıcıdan YouTube video URL'sini alıyoruz

# YouTube video nesnesini oluştur
yt = YouTube(video_url)  # YouTube video nesnesini oluşturuyoruz

# Video başlığını al
video_title = yt.title  # YouTube videosunun başlığını alıyoruz

# Videoyu indir
yt.streams.get_highest_resolution().download(filename="original.mp4")  # En yüksek çözünürlüklü videoyu indiriyoruz ve "original.mp4" olarak kaydediyoruz

# İndirilen videoyu TikTok formatına dönüştürme
def prepare_for_tiktok(input_file, output_file, title):
    # Giriş videosunu ve sesini yüksek çözünürlüklü formatında tanımla
    original_video = ffmpeg.input(input_file)
    audio_input = ffmpeg.input(input_file)

    # Ses akışını al ve ilk 60 saniyeyi kes
    audio_stream = audio_input.audio.filter('atrim', start=0, end=60)

    # Sesin girişine ve çıkışına fade in ve fade out efektleri ekle
    audio_stream = audio_stream.filter('afade', t='in', st=0, d=3).filter('afade', t='out', st=57, d=3)

    # İlk 60 saniyeyi kesme
    cut_video = original_video.trim(start_frame=0, end_frame=60*yt.streams.get_highest_resolution().fps)  # Videoyu ilk 60 saniyeye kesiyoruz

    # Videoyu 1:1 formatına dönüştürme
    square_video = cut_video.filter('scale', 1080, 1080).filter('pad', 1080, 1920, 0, '(1920 - ih) / 2', color='black')  # Videoyu 1:1 oranında kareye dönüştürüyoruz

    # Videoyu TikTok formatına dönüştürme ve sesi ekleyerek çıktıyı al
    ffmpeg.output(square_video, audio_stream, output_file, vcodec='libx264', acodec='aac', pix_fmt='yuv420p', aspect='9:16').run()

# Dönüşümü gerçekleştir ve video başlığını dosya adı olarak kullan
prepare_for_tiktok("original.mp4", f"{video_title}_tiktok_ready.mp4", video_title)  # prepare_for_tiktok fonksiyonunu çağırarak dönüşümü gerçekleştiriyoruz

#### Tiktok yükleme

session_id = "cookie_sessionid_"
file = "/Users/mac/Desktop/python/azerbulbul.mp4"
title = "Video Title"
tags = ["tag1", "tag2", "tag3"]

# Publish the video
uploadVideo(session_id, file, title, tags, verbose=True)
