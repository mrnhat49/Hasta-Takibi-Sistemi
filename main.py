import serial
import time
import csv
import tkinter as tk
from tkinter import font
from datetime import datetime
import os

# --- AYARLAR ---
COM_PORT = 'COM12'
# EĞER ESP32 KULLANIYORSANIZ BURAYI 115200 YAPMAYI DENEYİN!
BAUD_RATE = 9600 
DOSYA_ADI = "sicaklik_nem_kayitlari.csv"
SINIR_SICAKLIK = 37.5

# --- EXCEL (CSV) BAŞLATMA ---
if not os.path.exists(DOSYA_ADI):
    with open(DOSYA_ADI, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Tarih", "Saat", "Sicaklik (C)", "Nem (%)", "Durum"])

# --- SERİ HABERLEŞME BAŞLATMA ---
ser = None
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"{COM_PORT} üzerinden bağlantı başarılı.")
except Exception as e:
    print(f"HATA: {COM_PORT} portuna bağlanılamadı! Hata detayı: {e}")

# --- ANA FONKSİYONLAR ---
son_kayit_zamani = 0

def veri_oku_ve_guncelle():
    global son_kayit_zamani, ser
    
    if ser is None:
        lbl_durum.config(text="Arduino Bağlı Değil!", fg="red")
        pencere.after(1000, veri_oku_ve_guncelle)
        return

    try:
        if ser.in_waiting > 0:
            # Gelen veriyi ham haliyle alıyoruz
            veri = ser.readline().decode('utf-8', errors='replace').strip()
            
            # --- HATA AYIKLAMA İÇİN YAZDIRMA (DEBUG) ---
            # Terminalde bu satırın ne yazdığına dikkat edin!
            if veri:
                print(f"GELEN HAM VERİ: >{veri}<") 
            
            if veri and "," in veri:
                parcalar = veri.split(',')
                if len(parcalar) >= 2:
                    try:
                        # Gelen parçaları temizleyip sayıya çevirmeyi dene
                        ham_sicaklik = parcalar[0].strip()
                        ham_nem = parcalar[1].strip()
                        
                        sicaklik = float(ham_sicaklik)
                        nem = float(ham_nem)

                        # Arayüzü Güncelle
                        lbl_sicaklik.config(text=f"{sicaklik} °C")
                        lbl_nem.config(text=f"% {nem}")
                        
                        # --- KURAL 1: RENK DEĞİŞİMİ ---
                        if sicaklik > SINIR_SICAKLIK:
                            pencere.config(bg="red")
                            lbl_durum.config(text="⚠️ KRİTİK SICAKLIK!LÜTFEN HASTANIN DURUMUNU KONTROL EDİN", bg="red", fg="white")
                            lbl_sicaklik.config(bg="red", fg="white")
                            lbl_nem.config(bg="red", fg="white")
                            lbl_baslik.config(bg="red", fg="white")
                            lbl_kayit.config(bg="red", fg="white")
                            durum_metni = "KRITIK"
                        else:
                            pencere.config(bg="#f0f0f0") 
                            lbl_durum.config(text="Sistem Normal", bg="#f0f0f0", fg="green")
                            lbl_sicaklik.config(bg="#f0f0f0", fg="black")
                            lbl_nem.config(bg="#f0f0f0", fg="black")
                            lbl_baslik.config(bg="#f0f0f0", fg="black")
                            lbl_kayit.config(bg="#f0f0f0", fg="black")
                            durum_metni = "NORMAL"

                        # --- KURAL 2: KAYIT ---
                        simdiki_zaman = time.time()
                        if simdiki_zaman - son_kayit_zamani >= 60:
                            tarih = datetime.now().strftime("%d.%m.%Y")
                            saat = datetime.now().strftime("%H:%M:%S")
                            
                            with open(DOSYA_ADI, mode='a', newline='') as file:
                                writer = csv.writer(file, delimiter=';')
                                writer.writerow([tarih, saat, sicaklik, nem, durum_metni])
                            
                            lbl_kayit.config(text=f"Son Kayıt: {saat}")
                            son_kayit_zamani = simdiki_zaman

                    except ValueError:
                        print(f"SAYIYA ÇEVRİLEMEDİ: Parçalar: {parcalar}")
                        pass 

    except Exception as e:
        print(f"Hata oluştu: {e}")

    pencere.after(100, veri_oku_ve_guncelle)

# --- ARAYÜZ TASARIMI ---
pencere = tk.Tk()
pencere.title("Hasta Ortamı İzleme")
pencere.geometry("450x450")

buyuk_font = font.Font(family="Helvetica", size=30, weight="bold")
orta_font = font.Font(family="Helvetica", size=15)

lbl_baslik = tk.Label(pencere, text="Sıcaklık ve Nem Takibi", font=orta_font)
lbl_baslik.pack(pady=10)

lbl_sicaklik = tk.Label(pencere, text="-- °C", font=buyuk_font)
lbl_sicaklik.pack(pady=10)

lbl_nem = tk.Label(pencere, text="% --", font=buyuk_font)
lbl_nem.pack(pady=10)

lbl_durum = tk.Label(pencere, text="Bekleniyor...", font=orta_font, fg="blue")
lbl_durum.pack(pady=20)

lbl_kayit = tk.Label(pencere, text="Henüz kayıt yapılmadı", font=("Arial", 10))
lbl_kayit.pack(side="bottom", pady=20)

pencere.after(100, veri_oku_ve_guncelle)
pencere.mainloop()