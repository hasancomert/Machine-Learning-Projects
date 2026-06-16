# YZM212 Makine Öğrenmesi 4. Ödev

## Uzak Bir Galaksinin Parlaklık Analizi

Bu projede, gürültülü gözlem verileri kullanarak bir gök cisminin gerçek parlaklığını ve ölçüm hatasını Bayesyen çıkarım yöntemiyle tahmin ettim. Tahmin işlemi için MCMC yöntemini ve `emcee` kütüphanesini kullandım.

## Amaç

Bu ödevde amacım, sentetik olarak oluşturulan astronomik gözlem verilerinden iki parametreyi tahmin etmektir:

- `mu`: Gerçek parlaklık
- `sigma`: Gözlem hatası / standart sapma

Gerçek değerleri bildiğim için, modelin tahmin ettiği sonuçları gerçek değerlerle karşılaştırabildim.

## Veri

Verileri Python ile rastgele oluşturdum. Başlangıçta şu değerleri kullandım:

| Değişken | Değer |
|---|---:|
| Gerçek parlaklık (`true_mu`) | 150.0 |
| Gerçek hata (`true_sigma`) | 10.0 |
| Gözlem sayısı (`n_obs`) | 50 |

Ayrıca gözlem sayısının etkisini görmek için `n_obs = 5` olan ikinci bir deneme de yaptım.

## Yöntem

Bu çalışmada Bayesyen çıkarım kullandım. Modelde önce likelihood, prior ve posterior fonksiyonlarını tanımladım. Daha sonra `emcee` ile MCMC örneklemesi yaptım.

Ana deneyde geniş bir prior kullandım:

- `0 < mu < 300`
- `0 < sigma < 50`

Prior etkisini incelemek için ayrıca dar bir prior denemesi yaptım:

- `100 < mu < 110`
- `0 < sigma < 50`

Bu dar prior gerçek parlaklık değeri olan 150.0'ı içermediği için modelin sonucunu olumsuz etkiledi.

## Kullanılan Kütüphaneler

Projede şu kütüphaneleri kullandım:

- `numpy`
- `matplotlib`
- `emcee`
- `corner`
- `pandas`

Gerekli kütüphaneler şu komutla kurulabilir:

```bash
pip install numpy matplotlib emcee corner pandas
```

## Çalıştırma

Kod dosyasını çalıştırmak için:

```bash
python makine_ogrenmesi_odev4.py
```

Kod çalışınca grafikler ve sonuç tabloları `odev4_ciktilar` klasörüne kaydedilir.

## Sonuçlar

50 gözlem ve geniş prior ile model gerçek değerlere yakın sonuçlar verdi. Ortalama parlaklık için tahmin edilen değer gerçek değer olan 150.0'a yakın çıktı. Bu da modelin gürültülü veriye rağmen doğruya yakın tahmin yapabildiğini gösterdi.

Gözlem sayısını 5'e düşürdüğümde belirsizlik arttı. Posterior dağılımı daha genişledi ve tahminler daha az hassas hale geldi. Bu sonuç, veri sayısı arttıkça modelin daha güvenilir tahmin yaptığını gösterdi.

Dar prior denemesinde ise model yanlış sonuca yöneldi. Çünkü prior aralığı gerçek parlaklık değerini içermiyordu. Bu nedenle Bayesyen çıkarımda prior seçiminin önemli olduğunu gördüm.

## Grafiklerin Yorumu

Corner plot grafikleri, `mu` ve `sigma` parametrelerinin dağılımlarını gösterdi. 50 gözlemde dağılım daha dar ve düzenliyken, 5 gözlemde dağılım daha genişti.

Dar prior kullanılan deneyde `mu` değeri prior sınırına sıkıştı. Bu yüzden model gerçek parlaklığı bulamadı.

## Genel Yorum

Bu ödevde Bayesyen çıkarımın gürültülü verilerde nasıl çalıştığını uygulamalı olarak gördüm. MCMC yöntemi sayesinde sadece tek bir tahmin değil, tahminin belirsizlik aralığını da elde ettim.

Sonuç olarak, yeterli veri ve doğru prior seçimiyle Bayesyen yöntem gerçek değerlere yakın ve yorumlanabilir sonuçlar üretmektedir.
