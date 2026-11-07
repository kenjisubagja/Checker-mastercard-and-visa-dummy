# 🛠️ Mass BIN CC Generator & Live Checker

Script Python untuk melakukan *generate* massal kartu kredit (dummy) berdasarkan daftar BIN (Bank Identification Number), lalu mengecek validitasnya secara langsung ke API `chkr.cc`. 

Script ini didesain untuk mengekstrak BIN yang "Live" dan menyimpannya secara otomatis dalam format yang siap dipakai (siap import ke sistem lain).

##  Fitur Utama
- **Luhn Algorithm:** Menghasilkan nomor kartu yang valid secara matematis (lolos checksum).
- **Massal:** Bisa generate 5 kartu (atau lebih) untuk setiap 1 BIN.
- **Auto-Bypass Header:** Meniru request dari browser Chrome untuk menembus proteksi API `chkr.cc`.
- **Filter Otomatis:** Kartu yang mati (Dead) dibuang, yang hidup (Live) disimpan.
- **Format Bersih:** Hasil disimpan dalam format `Nomor|MM/YY|CVV`.
- **Auto-Overwrite:** File hasil (`live_cc.txt`) akan otomatis ditimpa setiap kali script dijalankan, biar gak numpuk file bekasan.

## 📋 Prasyarat
- Python 3.7 atau lebih baru.
- Library `requests`.
