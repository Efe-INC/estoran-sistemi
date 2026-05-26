import streamlit as st

# Web sayfasının başlığı ve açıklaması
st.title("🍔 Dijital Restoran Sipariş Sistemi")
st.write("Lütfen aşağıdaki bilgileri doldurarak siparişinizi veriniz.")

# Web arayüzündeki girdi alanları
isim = st.text_input("Adınız nedir?")
yemek = st.text_input("Ne yiyeceksiniz? (tantuni, kebap, makarna)")
icecek = st.text_input("Ne içeceksiniz? (kola, ayran, su)")
masa = st.text_input("Kaç numaralı masaya oturacaksınız?")

# Cinsiyet seçimi
cinsiyetiniz = st.radio("Cinsiyetiniz nedir?", ["erkek", "kadın"])

# Kullanıcı bu butona bastığında işlemler başlayacak
if st.button("Siparişi Onayla"):

    isimsınırı = len(isim)
    toplam_hesap = 0

    # 1. HATA KONTROLÜ: İsim sınırı
    if isimsınırı > 10:
        st.error("Hata! İsminiz 10 karakterden büyük olamaz.")

    # 2. HATA KONTROLÜ: Yemek menüde var mı?
    elif yemek not in ["tantuni", "kebap", "makarna"]:
        st.error("Hata! Maalesef sadece tantuni, kebap veya makarna servisimiz vardır.")

    # HER ŞEY YOLUNDAYSA
    else:
        # --- YEMEK FİYATLANDIRMASI ---
        if yemek == "tantuni":
            toplam_hesap += 150
        elif yemek == "kebap":
            toplam_hesap += 250
        elif yemek == "makarna":
            toplam_hesap += 120

        # --- İÇECEK FİYATLANDIRMASI ---
        if icecek == "kola":
            toplam_hesap += 40
        elif icecek == "ayran":
            toplam_hesap += 25
        elif icecek == "su":
            toplam_hesap += 10
        else:
            toplam_hesap += 30

            # --- SİPARİŞİ VE HESABI EKRANA YAZDIRMA ---
        hitap = "Bey" if cinsiyetiniz == "erkek" else "Hanım"

        st.success(f"🎉 Siparişiniz Başarıyla Alındı!")
        st.info(
            f"📋 **Sipariş Detayı:** {isim.title()} {hitap}, {yemek} ve {icecek} masanıza geliyor. (Masa No: {masa})")

        # Düzeltilen kısım burası:
        st.metric(label="Ödenecek Toplam Tutar", value=f"{toplam_hesap} TL")