# Lojistik Regresyon ve Özdeğer Analizi Projesi

Bu proje, Yapay Zeka ve Veri Mühendisliği laboratuvar çalışması kapsamında, Lojistik Regresyon algoritmasının incelenmesi ve matris işlemleri üzerine hazırlanmıştır.

##  Klasör İçeriği ve Dosyalar

* **`LogisticRegressionScikitLearn.ipynb`**: Lojistik Regresyon algoritmasının Scikit-Learn kütüphanesi ile temel uygulaması. Ayrıca bu dosya içerisinde Numpy kütüphanesinin `linalg.eig` fonksiyonunun kaynak kod analizi, özdeğer (eigenvalue) ve özvektör (eigenvector) hesaplamaları bulunmaktadır.
* **`logisticRegressionBayes.ipynb`**: Lojistik Regresyon modellerine ait ek analizler ve denemeler (ödevin bu kısmında ekstra karşılaştırmalar yapıldıysa bu dosyada yer almaktadır).
* **Veri Dosyaları**: Proje içinde dışarıdan bir veri seti (`.csv` vb.) kullanıldıysa bu dizinde yer alır (Çalışmada Scikit-Learn içerisindeki hazır veri setleri kullanılmıştır).

##  Kullanılan Teknolojiler ve Kurulum

Çalışmadaki kodları kendi bilgisayarında yürütebilmek için aşağıdaki Python kütüphanelerine ihtiyacın olacaktır:

- `numpy` (Matris ve doğrusal cebir işlemleri için)
- `scikit-learn` (Makine öğrenmesi modeli ve veri setleri için)

Kütüphaneleri kurmak için terminale şu komutu yazabilirsin:
`pip install numpy scikit-learn`

##  Çalışma Mantığı
Bu laboratuvar çalışmasında, verilerin sınıflandırılması için Sigmoid fonksiyonu temelli Lojistik Regresyon kullanılmış ve boyut indirgeme/veri analizi için temel bir adım olan karesel matrislerin özdeğer analizleri LAPACK tabanlı Numpy rutinleri incelenerek gerçekleştirilmiştir.