import requests

# 1. Konfigurasi API Key dan Kata Kunci
API_KEY = '57580538-5673bdcdc030707fdcbc4e250'
SEARCH_QUERY = 'music concert'
MAX_VIDEOS = 20

BASE_URL = 'https://pixabay.com/api/videos/'
payload = {
    'key': API_KEY,
    'q': SEARCH_QUERY,
    'per_page': MAX_VIDEOS
}

# SOLUSI 403: Menyamar sebagai browser populer agar tidak diblokir sistem Cloudflare/WAF
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

print(f"Menghubungi Pixabay API untuk mencari '{SEARCH_QUERY}'...")

# Mengirim request lengkap dengan parameter dan headers
response = requests.get(BASE_URL, params=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
    video_list = data.get('hits', [])
    
    if len(video_list) > 0:
        print(f"Menemukan {len(video_list)} video. Memulai proses download...\n")
        
        for index, video_item in enumerate(video_list, start=1):
            try:
                video_url = video_item['videos']['medium']['url']
                video_id = video_item['id']
                filename = f"pixabay_{SEARCH_QUERY}_{index}_{video_id}.mp4"
                
                print(f"[{index}/{len(video_list)}] Mendownload: {filename}...")
                
                # Gunakan headers yang sama saat mendownload file videonya
                video_response = requests.get(video_url, stream=True, headers=headers)
                
                if video_response.status_code == 200:
                    with open(filename, 'wb') as f:
                        for chunk in video_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"-> Sukses disimpan!\n")
                else:
                    print(f"-> Gagal unduh file. Status: {video_response.status_code}\n")
                
            except KeyError:
                print(f"-> Gagal mengambil URL untuk video indeks ke-{index}\n")
            except Exception as e:
                print(f"-> Gagal mendownload karena error: {e}\n")
                
        print("Semua proses download selesai!")
    else:
        print('Pencarian selesai, tetapi video tidak ditemukan.')
else:
    print(f'Gagal terhubung ke API. Status code: {response.status_code}')
    print('Solusi Tambahan: Buka link API di browser Anda untuk memastikan API Key Anda aktif.')
