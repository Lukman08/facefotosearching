import os
import sys
import shutil
import ctypes
from deepface import DeepFace

base_dir = os.path.dirname(os.path.abspath(__file__))

dir_sou = os.path.join(base_dir, "SOU")
dir_rev = os.path.join(base_dir, "REV")
dir_res = os.path.join(base_dir, "RES")

ekstensi_valid = ('.png', '.jpg', '.jpeg', '.webp')

os.makedirs(dir_sou, exist_ok=True)
os.makedirs(dir_rev, exist_ok=True)
os.makedirs(dir_res, exist_ok=True)

rev_images = [
    os.path.join(dir_rev, f)
    for f in os.listdir(dir_rev)
    if f.lower().endswith(ekstensi_valid)
]

if not rev_images:
    print(f"Tidak ada foto referensi ditemukan di folder: {dir_rev}")
    sys.exit()

sou_files = [
    f for f in os.listdir(dir_sou)
    if f.lower().endswith(ekstensi_valid)
]

if not sou_files:
    print(f"Tidak ada foto sumber ditemukan di folder: {dir_sou}")
    sys.exit()

total_sou = len(sou_files)
print(f"Direktori aktif  : {base_dir}")
print(f"Referensi dimuat : {len(rev_images)} foto dari REV")
print(f"Target pemindaian: {total_sou} foto di SOU\n")

jumlah_cocok = 0

for idx, filename in enumerate(sou_files, start=1):
    img_path = os.path.join(dir_sou, filename)
    persentase = (idx / total_sou) * 100

    # Tampilkan progres persentase secara real-time dalam 1 baris
    status_teks = f"\rProgres: {persentase:6.2f}% ({idx}/{total_sou}) | Cocok: {jumlah_cocok} | Cek: {filename[:25]:<25}"
    sys.stdout.write(status_teks)
    sys.stdout.flush()

    match_found = False
    for rev_img in rev_images:
        try:
            result = DeepFace.verify(
                img1_path=img_path,
                img2_path=rev_img,
                model_name="Facenet",
                enforce_detection=False,
                silent=True
            )
            if result.get("verified"):
                match_found = True
                break
        except Exception:
            continue

    if match_found:
        # Bersihkan baris progres sementara agar log [COCOK] tercetak rapi
        sys.stdout.write("\r" + " " * 90 + "\r")
        print(f"[COCOK] {filename} -> Disalin ke RES")
        shutil.copy2(img_path, os.path.join(dir_res, filename))
        jumlah_cocok += 1

# Bersihkan baris progres terakhir
sys.stdout.write("\r" + " " * 90 + "\r")
sys.stdout.flush()

ringkasan = (
    f"Pencarian selesai!\n"
    f"Total foto dipindai : {total_sou} foto\n"
    f"Foto yang sesuai    : {jumlah_cocok} foto\n"
    f"Lokasi hasil        : {dir_res}"
)

print("=" * 55)
print(ringkasan)
print("=" * 55)