Proje Adı: HMM ile Basit Kelime Sınıflandırma

Problem Tanımı: Bu projede amaç, dışarıdan gelen ses özelliklerini kullanarak sınırlı bir kelime dağarcığı ("EV" ve "OKUL") üzerinden basit bir Kelime Tanıyıcı (Speech Classifier) simülasyonu geliştirmektir.

Kullanılan Veri: Model, doğrudan sürekli ses dalgaları yerine, seslerin işlenmesiyle elde edildiği varsayılan ayrık (kategorik) gözlem dizilerini işlemektedir. Başlangıç, geçiş ve emisyon olasılık matrisleri temsili olarak tanımlanmış olup; [0, 1, 1] ve [2, 2, 2] gibi yapay gözlem dizileri test verisi olarak sisteme sunulmuştur.

Yöntem: Python ve hmmlearn kütüphanesi kullanılarak her iki kelime için ayrı bir Kategorik Saklı Markov Modeli (CategoricalHMM) oluşturulmuştur. Yeni bir gözlem dizisi geldiğinde, her iki model üzerinden score() fonksiyonu ile Log-Likelihood (log-olasılık) hesaplanmış ve en yüksek skoru veren (sıfıra en yakın olan) model doğru tahmin kabul edilerek sınıflandırma yapılmıştır.

Sonuçlar:

[0, 1, 1] gözlem dizisi (1. Test Verisi) EV modelinde daha yüksek Log-Likelihood skoru ürettiği için kelime doğru bir şekilde "EV" olarak tahmin edilmiştir.

[2, 2, 2] gözlem dizisi (2. Test Verisi) OKUL modelinde daha yüksek Log-Likelihood skoru ürettiği için kelime doğru bir şekilde "OKUL" olarak tahmin edilmiştir.

Yorum ve Tartışma: Çıkan skorların negatif (eksi) olması, 0 ile 1 arasındaki olasılık değerlerinin logaritmasının hesaplanmasından kaynaklanmaktadır; bu nedenle eksi olsa da sıfıra en yakın olan değer, daha yüksek bir olasılığa işaret eder. Öte yandan, kütüphanenin güncel versiyonu gereği ayrık gözlemler içeren bu yapıda MultinomialHMM sınıfı yerine CategoricalHMM kullanılması hata alınmasının önüne geçmiş ve matematiksel olarak modelin doğasına daha uygun bir çözüm sağlamıştır.