import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols # En küçük kareler yöntemi yapan fonksiyon
from statsmodels.stats.anova import anova_lm # ANOVA tablosu oluşturan fonksiyon

# ==========================================
# 1. ADIM: VERİYİ OLUŞTURMA
# ==========================================
data = {
    'Kagit_Cinsi': [
        'KR', 'FL', 'FL', 'KR', 'KM', 'FL', 'KR', 'KM', 'KR', 'KM', 
        'KR', 'KR', 'KR', 'FL', 'ANSY', 'FL', 'FL', 'FL', 'FL', 'ANSY',
        'KM', 'FL', 'KM', 'ANSY', 'KR', 'FL', 'FL', 'FL', 'KM', 'KM',
        'KR', 'KR', 'ANSY', 'KM', 'KM', 'KM', 'FL', 'KR', 'KR', 'KR',
        'ANSY', 'ANSY', 'ANSY', 'KR', 'KR', 'ANSY', 'KR', 'ANSY', 'ANSY', 'ANSY',
        'KR', 'KM', 'FL', 'KR', 'ANSY', 'KR', 'KR', 'ANSY', 'ANSY', 'KM',
        'KR', 'KM', 'KM', 'KR', 'KM', 'ANSY', 'FL', 'ANSY', 'KR', 'FL',
        'FL', 'ANSY', 'ANSY', 'ANSY', 'ANSY', 'ANSY', 'ANSY', 'KR', 'FL', 'FL',
        'KR', 'ANSY', 'FL'
    ],
    'Durus_Suresi': [
        9, 7, 14, 10, 14, 6, 7, 8, 6, 5, 
        6, 9, 10, 8, 6, 6, 8, 7, 9, 9, 
        4, 8, 6, 7, 3, 7, 6, 16, 8, 8, 
        3, 3, 19, 7, 6, 7, 9, 16, 21, 9, 
        7, 17, 10, 11, 18, 8, 12, 20, 16, 17, 
        12, 8, 6, 17, 9, 24, 7, 39, 17, 29, 
        6, 6, 10, 4, 8, 7, 6, 10, 9, 6, 
        15, 12, 16, 7, 12, 21, 21, 9, 13, 21, 
        4, 17, 9
    ],
    'Durus_Nedeni': [
        'Yırtık', 'Yırtık', 'Yırtık', 'Yapışık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık',
        'Yapışık', 'Yapışık', 'Yapışık', 'Yapışık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık',
        'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yapışık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık',
        'Yırtık', 'Yırtık', 'Yapışık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık',
        'Yırtık', 'Yırtık', 'Yapışık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yapışık', 'Yırtık', 'Yırtık', 'Yapışık',
        'Yırtık', 'Yapışık', 'Delik', 'Yapışık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yapışık', 'Yırtık', 'Yırtık',
        'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık',
        'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yırtık', 'Yapışık', 'Yapışık', 'Yırtık',
        'Yırtık', 'Yırtık', 'Yırtık'
    ]
}

df = pd.DataFrame(data)

# --- 2. ADIM: İKİ YÖNLÜ ANOVA MODELİ ---
# Sadece 'Yırtık' veya 'Yapışık' olan satırları al (Filtreleme)
# Boş verilerden kurtulmak ve orijinal veriyi bozmamak için copy() kullanıyoruz.
df_analiz = df[df['Durus_Nedeni'].isin(['Yırtık', 'Yapışık'])].copy() 

# Veriyi ekrana yazdırma kısmı 
#print("\n" + "="*40)
#print("ANALİZDE KULLANILAN FİLTRELENMİŞ VERİ")
#print("="*40)
#pd.set_option('display.max_rows', None) # Tüm satırları göster
#print(df_analiz) # Veriyi bas

# ANOVA İşlemi
formula = 'Durus_Suresi ~ C(Kagit_Cinsi) * C(Durus_Nedeni)'

# OLS modeli oluşturma: Formüle en uygun matematiksel denklemi bulmak için 
# .fit() fonksiyonu kullanılır. Bu fonksiyon, kareler toplamını minimize etmeye çalışır (Varyansları hesaplar, ortalamaları alır, hataları ölçer).
model = ols(formula, data=df_analiz).fit() 

anova_table = anova_lm(model, typ=3)

# --- 3. ADIM: SONUÇLARI YAZDIRMA ---
print("\n" + "="*70)
print("İKİ YÖNLÜ ANOVA SONUÇ RAPORU (Kağıt Cinsi x Duruş Nedeni)")
print("="*70)
print(anova_table)

print("\n" + "-"*70)
print("MÜHENDİSLİK KARARLARI (α = 0.05):")
print("-" * 70)

# YORUM KURALI::
# Eğer p-değeri 0.05'ten büyükse, H0 hipotezi kabul edilir; yani, faktörün etkisi yoktur.
# Eğer p-değeri 0.05'ten küçükse, H1 hipotezi kabul edilir; yani, faktörün duruş sürelerinin ortalaması üzerinde anlamlı bir etkisi vardır.

# P-Değerlerini Çekelim
p_kagit = anova_table.loc['C(Kagit_Cinsi)', 'PR(>F)']
p_neden = anova_table.loc['C(Durus_Nedeni)', 'PR(>F)']
p_etkilesim = anova_table.loc['C(Kagit_Cinsi):C(Durus_Nedeni)', 'PR(>F)']

# 1. Kağıt Etkisi
if p_kagit < 0.05:
    print(f"[H1 KABUL] Kağıt Cinsinin süreye etkisi vardır (p={p_kagit:.4f}).")

else:
    print(f"[H0 KABUL] Kağıt Cinsinin etkisi yoktur (p={p_kagit:.4f}).")

# 2. Duruş Nedeni Etkisi
if p_neden < 0.05:
    print(f"[H1 KABUL] Duruş Nedeninin süreye etkisi vardır (p={p_neden:.4f}).")

else:
    print(f"[H0 KABUL] Duruş Nedeninin tek başına anlamlı bir etkisi yoktur (p={p_neden:.4f}).")


# 3. Etkileşim Etkisi 
if p_etkilesim < 0.05:
    print(f"[H1 KABUL - KRİTİK] ETKİLEŞİM VARDIR! (p={p_etkilesim:.4f}).")
    print("   -> Kağıt Cinsi ve Duruş Nedeni birlikte süreyi anlamlı şekilde etkiliyor.")

else:
    print(f"[H0 KABUL] Etkileşim yoktur (p={p_etkilesim:.4f}).")
    



print("\nANALİZ SONLANDI.")