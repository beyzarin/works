import random
import math

# --- Adım 1 & 2: Problem Tanımı ve Başlangıç Popülasyonu ---

# Şehirlerin koordinatlarını tanımlayalım
# (Gerçek koordinatlar yerine enlem/boylam benzeri değerler kullanıyoruz)
cities = {
    'Ankara': (39.93, 32.85),
    'İstanbul': (41.01, 28.97),
    'İzmir': (38.42, 27.14),
    'Antalya': (36.89, 30.71),
    'Bursa': (40.18, 29.06),
    'Adana': (37.00, 35.32),
    'Konya': (37.87, 32.49),
    'Trabzon': (41.00, 39.72),
    'Isparta': (37.77, 30.56),  # type: ignore
    'Malatya': (38.35, 38.31),
    'Aydin': (37.85, 27.85),
    'Erzurum': (39.90, 41.27),
    'Zonguldak': (41.45, 31.78),
    'Edirne': (41.68, 26.56),
    'Kirklareli': (41.73, 27.23),
    
    #şehirleri sözlük içinde tanımlayalım
}

city_names = list(cities.keys())
num_cities = len(city_names) #şehir sayısını değişkene atayalım

# Bir turdaki şehirler arasındaki mesafeyi hesaplayan fonksiyon
def calculate_distance(city1_name, city2_name):
    city1_coord = cities[city1_name] #iki şehrin kordinatlarını sözlükten çekelim
    city2_coord = cities[city2_name]
    # İki nokta arası Öklid mesafesi
    #Öklid mesafesi, iki nokta arasındaki en kısa mesafeyi, yani doğrusal (düz çizgi üzerindeki) uzaklığı gösterir.
    #d=(x2​−x1​)^2+(y2​−y1​)^2 formülü ile hesaplanır.
    return math.sqrt((city1_coord[0] - city2_coord[0])**2 + (city1_coord[1] - city2_coord[1])**2)

# Bir turun toplam mesafesini hesaplayan fonksiyon
def calculate_tour_distance(tour): #tour adında bir şehir listesi (yani bir rota) alır.
    total_distance = 0 #toplam mesafe sayacı
     #turdaki her şehir için
    for i in range(num_cities):#turdaki şehir sayısı kadar döngü
        from_city = tour[i] #başlangıç şehri
        # Son şehirden başa dönmek için modülo kullanılır
        to_city = tour[(i + 1) % num_cities] 
        #Hedef şehrimiz, listedeki bir sonraki şehir (i+1) olsun. Ama
        # Eğer son şehre (i=7) geldiysek, (7+1) % 8 işlemi 8 % 8 = 0 sonucunu verir. Yani hedef
        # şehir listenin başındaki ilk şehir olur." Bu hile, son şehirden eve (ilk şehre) dönmemizi sağlar.
        total_distance += calculate_distance(from_city, to_city)
    return total_distance

# --- Adım 3: Uygunluk Fonksiyonu ---
def calculate_fitness(tour):# Bu fonksiyon her bir tour listesine yani bir rotaya uygunluk değeri atar 
    # Mesafe ne kadar azsa, uygunluk o kadar yüksektir.
    return 1 / calculate_tour_distance(tour) #uygunluk, mesafenin tersidir (mesafe azaldıkça uygunluk artar)
    #uygunluk değeri ne kadar yüksekse, tur o kadar iyidir.

# Başlangıç popülasyonunu oluşturur
def create_initial_population(size): #size: popülasyon boyutu
    population = []
    for _ in range(size): # Popülasyon boyutu kadar döngü
        # Şehirleri rastgele sıralayarak bir tur (kromozom) oluştur
        tour = random.sample(city_names, num_cities)
        population.append(tour)
    return population

# --- Adım 4: Ebeveyn Seçimi (Turnuva Yöntemi) ---
def selection(population, fitnesses, k=3):
    # Popülasyondan rastgele 'k' adet birey seç (turnuva)
    selection_ix = random.sample(range(len(population)), k)
    # Tüm popülasyondan (örn: 100 tur) rastgele k tane (örn: 3 tane) tur seçer
    # Seçilenler arasından en uygun olanı bul
    best_ix = -1 #en iyi bireyin indeksini tutacak değişken
    best_fitness = -1.0 # Başlangıç değeri negatif olmalı
    #negatif bir sayı ile başlatıyoruz (-1.0) → fitness değerleri mutlaka daha büyük olur 
    # → ilk birey mutlaka seçilir
    for ix in selection_ix: #bu 3 turu tek tek incele
        if fitnesses[ix] > best_fitness: #eğer bu turun fitness değeri en iyiyse
            best_fitness = fitnesses[ix] #en iyi fitness değeri güncellenir
            best_ix = ix #en iyi bireyin indeksi güncellenir
            
    return population[best_ix]


# --- Adım 5: Çaprazlama (Sıralı Çaprazlama - Order 1 Crossover) ---
def crossover(parent1, parent2):
    child = [None] * num_cities #15 tane boş şehirden oluşan bir liste oluştur
    #yani listenin her bir elemanı başta None
    
    # Ebeveyn 1'den rastgele bir alt bölüm seç
    start, end = sorted(random.sample(range(num_cities), 2))
    
    # Bu bölümü doğrudan çocuğa kopyala
    child[start:end] = parent1[start:end]
    
    # Ebeveyn 2'den geri kalan şehirleri al
    remaining = (city for city in parent2 if city not in child) #parent2'de olup child'da olmayan şehirleri alır
    for i in range(num_cities):
        if child[i] is None:
            child[i] = next(remaining) #child'da None olan yerlere remaining'den şehir ekle

    return child
# --- Adım 6: Mutasyon (Takas Mutasyonu) ---
def mutate(tour, mutation_rate):
    if random.random() < mutation_rate: # 0 dahil 1 hariç arasında verilen rastgele sayının mutation_rate'den küçük olup olmadığını kontrol et
        #Tüm olasılıkların sadece %[mutation_rate]’i mutasyon geçirir → mutasyon nadiren gerçekleşir
        #belirtilen mutasyon oranından küçükse 
        # Turdaki iki şehri rastgele seç ve yerlerini değiştir
        idx1, idx2 = random.sample(range(num_cities), 2) #iki farklı indeks seçer
        #seçilen iki şehrin yerini değiştir
        tour[idx1], tour[idx2] = tour[idx2], tour[idx1]
    return tour #turu döndür(algoritmanın sıkışıp kalmasını önlemek için)

# --- Ana Genetik Algoritma Fonksiyonu ---
def genetic_algorithm(population_size, generations, mutation_rate, elitism_size):
    
    #Genetik algoritmanın 4 kuralını uygulayacağız:
    #Popülasyon kaç kişi olacak (population_size), 
    # kaç nesil sürecek (generations),
    # mutasyon ihtimali ne (mutation_rate) ve 
    # en iyilerden kaçı korunacak (elitism_size).
    # Bu parametreler, genetik algoritmanın nasıl çalışacağını belirler.
    
    # Başlangıç popülasyonunu oluştur
    population = create_initial_population(population_size)
    best_tour = None #en iyi turu tutacak değişken başlangıçta bilinmediği için boş bırakılır
    best_distance = float('inf') # En iyi mesafeyi sonsuzdan başlat
    #başlangıçta en iyi mesafe sonsuz olarak ayarlanır, böylece ilk bulunan tur mutlaka daha iyi olur

    print("Genetik algoritma başlıyor...")
    print(f"Popülasyon Büyüklüğü: {population_size}, Nesil Sayısı: {generations}, Mutasyon Oranı: {mutation_rate}\n")

    # Başlangıçtaki rastgele bir turun mesafesini gösterelim
    initial_tour = population[0] #başlangıç popülasyonundan ilk turu al
    initial_distance = calculate_tour_distance(initial_tour) #bu turun toplam mesafesini hesapla
    print(f"Başlangıçtaki rastgele tur mesafesi: {initial_distance:.2f}") #mesafeyi ekrana yazdır

    for gen in range(generations): #nesil sayısı kadar döngü
        # Popülasyondaki her bireyin uygunluğunu hesapla
        fitnesses = [calculate_fitness(tour) for tour in population]
        
        new_population = [] #yeni popülasyonu tutacak liste
        
        # Elitizm: En iyi bireyleri doğrudan yeni nesle aktar
        # zip kullanarak fitness ve popülasyonu birleştir,  ey yüksek fitness en başta olacak şekilde fitness'a göre sırala
        sorted_population = [x for _, x in sorted(zip(fitnesses, population), key=lambda pair: pair[0], reverse=True)]
        #bu  satır karışık olduğu için yaptıklarını açıklayalım:
        #1. zip(fitnesses, population) → fitness değerleri ile popülasyonu birleştirir
        #2. sorted(..., key=lambda pair: pair[0], reverse=True) → fitness değerine göre azalan sırada sıralar
        #3. [x for _, x in ...] → sadece popülasyonu alır
        
        new_population.extend(sorted_population[:elitism_size]) 
        #elitism_size kadar en iyi bireyi yeni popülasyona ekle
        #bu bireyler sonraki nesilde değişmeden kalacaklar 
        #bu bireyler seçim ve çaprazlama işlemlerinden etkilenmezler
        #selection sadece geri kalan bireyleri değiştirir


        # Yeni popülasyonun geri kalanını oluştur
        for _ in range(population_size - elitism_size):
            # Ebeveynleri seç
            parent1 = selection(population, fitnesses)
            parent2 = selection(population, fitnesses)
            
            # Çaprazlama yap
            child = crossover(parent1, parent2)
            
            # Mutasyon yap
            child = mutate(child, mutation_rate)
            
            new_population.append(child)
            
        population = new_population
        # eski popülasyon tamamen silir
        # yeni oluşan (elitler + yeni bireyler) popülasyon ile değiştirir
        #dolayısıyla eski popülasyondaki seçilmeyen bireyler tamamen kaybolur
        #Böylece popülasyonun ortalama kalitesi (fitness) her nesilde artar.
        #Nesil sayısı daha ne kadar çok oldukça popülasyonun kalitesi o kadar artar.
        #Fakat sadece yeterli çeşitlilik varsa işe yarar.
        #Problem çok karmaşık değilse popülasyon tek tipe dönebilir ve ilerleme durabilir.


        # Bu nesildeki en iyi turu bul
        current_best_tour = sorted_population[0] #sıralanmış popülasyondan en iyisini al
        current_best_distance = calculate_tour_distance(current_best_tour) #mesafesini hesapla

        # Eğer bu nesildeki en iyi tur, genel en iyi turdan daha iyiyse güncelle
        if current_best_distance < best_distance:
            best_distance = current_best_distance
            best_tour = current_best_tour #başta boş bıraktığımız en iyi turu güncelle
            # Her yeni en iyiyi bulduğunda ekrana yazdır
            print(f"Nesil {gen+1}: Yeni en iyi mesafe = {best_distance:.2f}")

    # Döngü bittiğinde en son bulunan en iyi turu ve mesafeyi döndür
    return best_tour, best_distance

# --- Algoritmayı Çalıştır  ---

# Parametreler
POPULATION_SIZE = 100 
GENERATIONS = 500     
MUTATION_RATE = 0.02  
ELITISM_SIZE = 5      

# Genetik algoritmayı çalıştır
# Not: genetic_algorithm fonksiyonunun bu kod bloğundan önce tanımlı olduğunu varsayıyoruz.
final_tour, final_distance = genetic_algorithm(
    population_size=POPULATION_SIZE,
    generations=GENERATIONS,
    mutation_rate=MUTATION_RATE,
    elitism_size=ELITISM_SIZE
)

print("\n--- Hesaplama Tamamlandı ---")
print(f"Bulunan en kısa mesafe: {final_distance:.2f}")
    
# En iyi turu (şehir sırasını) okunaklı bir şekilde yazdır
print("En iyi tur:")
print(" -> ".join(final_tour))