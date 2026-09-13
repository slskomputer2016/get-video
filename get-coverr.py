import requests,random

# ==========================================
# PENTING: Ganti dengan API Key valid Anda!
# Dapatkan gratis di https://coverr.co/developers
API_KEY = "5703397494fdf41a609b269253a58adf" 
# ==========================================



SEARCH = ["waterfall","beach","city", "stadion","wonder"]



URL_API = "https://api.coverr.co/videos"

# Menggunakan autentikasi Bearer Token sesuai dokumentasi Coverr
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# query_params = {
#     "query": SEARCH_QUERY,
#     "urls": "true"
# }

#print(f"Mencari video dengan kata kunci: '{SEARCH_QUERY}'...")


for i in range(5):

    try:
        SEARCH_QUERY = random.choice(SEARCH)

        query_params = {
            "query": SEARCH_QUERY,"urls": "true"
        }
        response = requests.get(URL_API, headers=headers, params=query_params)
        
        # 1. Validasi apakah HTTP statusnya 200 (OK)
        if response.status_code == 200:
            # 2. Ambil data JSON jika sukses
            data = response.json()
            videos = data.get("hits", [])
            
            if not videos:
                print("Video tidak ditemukan untuk kata kunci tersebut.")
            else:
                # Mengambil video pertama dari daftar
                first_video = videos[0] # Memperbaiki indeks array
                video_title = first_video.get("title", "downloaded_video")
                
                # Mengambil URL unduhan resmi
                download_url = first_video.get("urls", {}).get("mp4_download")
                
                if download_url:
                    # Membersihkan nama file agar aman di Windows
                    filename = "".join(c for c in video_title if c.isalnum() or c in (' ', '_', '-')).rstrip()
                    filename = f"{filename.replace(' ', '_')}_{i}.mp4"
                    
                    print(f"Video ditemukan: '{video_title}'")
                    print("Memulai proses unduhan...")
                    
                    # 3. Proses unduh file video
                    video_response = requests.get(download_url, stream=True)
                    if video_response.status_code == 200:
                        with open(filename, 'wb') as file:
                            for chunk in video_response.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    file.write(chunk)
                        print(f"Selesai! Video berhasil disimpan: {filename}")
                    else:
                        print("Gagal mengunduh file video dari server.")
                else:
                    print("URL unduhan video tidak ditemukan dalam respons API.")
                    
        elif response.status_code in [401, 403]:
            print("\n[EROR] API Key Anda tidak valid atau tidak dikenali oleh Coverr.")
            print("Silakan periksa kembali variabel API_KEY di bagian atas kode Anda.")
        else:
            print(f"\nGagal terhubung. Kode Status Server: {response.status_code}")
            print("Respons Server (Bukan JSON):")
            print(response.text[:200]) # Menampilkan 200 karakter pertama dari eror teks

    except requests.exceptions.JSONDecodeError:
        print("\n[EROR] Server memberikan respons teks biasa, bukan JSON.")
        print("Kemungkinan besar API Key kosong, salah ketik, atau kuota API habis.")
        print("Pesan asli dari server:")
        print(response.text[:200])
    except Exception as e:
        print(f"\nTercatat eror lain: {e}")
