SEO + Akademik Editör Pro / SEO + Academic Editor Pro
Türkçe | English

📘 Türkçe Dokümantasyon
Proje Hakkında
SEO + Akademik Editör Pro, yazarlar, akademisyenler, öğrenciler ve içerik üreticileri için geliştirilmiş çok yönlü bir metin düzenleme ve analiz uygulamasıdır. PyQt5 ile masaüstü uygulaması olarak geliştirilmiştir.

Ana özellikler:

Zengin metin editörü (HTML tabanlı)

Yapay zeka (Ollama / OpenAI) ile dil bilgisi, akademik ve SEO düzeltmeleri

Google Scholar entegrasyonu

YKS / DGS / KPSS / Üniversite ders notları sistemi (matematik, fizik, kimya vb.)

Sembolik matematik motoru (SymPy ile türev, integral, denklem çözme, birim dönüşümü)

Kişisel kütüphane (kitap ekleme, kapak görseli, notlar)

PDF işlemleri (birleştirme, bölme, metin çıkarma, oluşturma)

Kullanıcı yönetimi ve şifre koruması

Karanlık / açık tema desteği (varsayılan karanlık)

Otomatik yedekleme ve pencere geometrisi hafızası

Sözlük ve sabitler veritabanı

Kurulum
Python 3.9+ gereklidir.

Gerekli kütüphaneleri yükleyin:

bash
pip install PyQt5 PyQtWebEngine sympy numpy matplotlib language_tool_python ollama openai textstat keybert scholarly PyPDF2 python-docx markdown
Opsiyonel: html2docx (Word dışa aktarımı için)

bash
pip install html2docx
Ollama kurulumu (AI düzeltmeler için):

ollama.com adresinden indirin ve kurun.

Önerilen modeller: qwen2.5:3b, llama3.2:3b, bazobehram/turkish-gemma-9b-t1 (Türkçe için)

Modeli yüklemek için: ollama pull qwen2.5:3b

Uygulamayı başlatın:

bash
python main.py
Varsayılan kullanıcı adı ve şifre: admin / admin

Kullanım Kılavuzu
Ana Pencereler
Ana Editör: HTML metin düzenleme, şablonlar (SEO, Akademik, Blog, Ürün)

Ders Notlarım: YKS, AYT, DGS, KPSS, üniversite dersleri için not alma sistemi. Matematiksel ifadeleri görsel olarak ana editöre gönderebilirsiniz.

Akademik Editör: Tez, makale, kitap bölümleri oluşturma, APA/MLA/Chicago formatında kaynakça, dipnot, tablo, resim ekleme. HTML tabanlı profesyonel bir ara yüz.

Menüler ve Araçlar
Dosya: Yeni, Aç, Kaydet, Word şablonu yükleme.

Yazılar: Veritabanına kaydedilmiş yazıları listeleme, görüntüleme, düzenleme, silme.

Araçlar: Google Scholar arama, Matematik ifadesi ekleme, Kullanıcı sabitleri, Bul/Değiştir, Kütüphanem (kitap yönetimi), PDF işlemleri.

Sözlük: Kişisel sözlük oluşturma, kelime anlamları.

Rehber: SEO ve Akademik yazım kuralları.

Ayarlar: AI modellerini seçme, OpenAI API anahtarı girme, akademik format (APA/MLA/Chicago), AI düzeltmeyi açıp kapama, tema değiştirme, kullanıcı yönetimi (admin).

AI Düzeltme
Metni seçilen modda (Standart, SEO, Akademik) dil bilgisi ve anlatım bozukluklarına göre düzeltir.

Ollama (yerel) veya OpenAI (GPT-3.5) kullanılabilir.

Doğruluk raporu ve hata listesi gösterir.

Ders Notları – Matematik Sistemi
Ctrl+Shift+X, Ctrl+Shift+Y gibi kısayollarla sembol ekleyebilirsiniz.

Denklem çözme (Ctrl+E), türev (Ctrl+T), integral (Ctrl+I), limit (Ctrl+L), grafik çizme (Ctrl+G) gibi işlemler.

Birim dönüştürme (Ctrl+U) ile fiziksel büyüklükleri SI veya istenen birime çevirebilirsiniz.

Kullanıcı sabitleri ekleyip matematiksel ifadelerde kullanabilirsiniz.

Kütüphane (E-Kitap Yönetimi)
Kitap adı, yazar, yayınevi, yıl, ISBN, kapak resmi (base64) ve notlar ekleyebilirsiniz.

Listeleme, düzenleme, silme.

PDF İşlemleri
Birden fazla PDF’i birleştirme.

Sayfa aralığı belirterek PDF bölme.

Düz metinden PDF oluşturma.

PDF’den metin çıkarma.

Yapılandırma Dosyaları
ai_models.json – Görev bazlı AI model isimleri.

users.json – Kullanıcı adı/şifre (varsayılan: admin/admin).

openai_key.txt – İsteğe bağlı OpenAI API anahtarı.

window_geometry.json – Pencere boyutunu ve konumunu hatırlar.

autosave_backup.txt – Otomatik yedekleme (60 saniyede bir).

posts.db – SQLite veritabanı (yazılar, ders notları, sabitler, kitaplar, sözlük).

Katkıda Bulunma
Proje açık kaynaktır. Hata bildirimi veya özellik önerileri için iletişime geçebilirsiniz.

Lisans
Bu proje MIT Lisansı ile dağıtılmaktadır. Ticari veya özel kullanımda herhangi bir kısıtlama yoktur.

İletişim
Geliştirici: deliKadir
E-posta: astromoon.1990@gmail.com

📗 English Documentation
About the Project
SEO + Academic Editor Pro is a powerful text editing and analysis desktop application built with PyQt5. It targets writers, academics, students, and content creators who need advanced language correction, academic formatting, SEO optimization, and mathematical tools.

Key features:

Rich HTML editor

AI‑powered grammar, academic (APA/MLA/Chicago) and SEO corrections (Ollama / OpenAI)

Google Scholar integration

Study notes system for YKS (Turkish university entrance exam), DGS, KPSS, and university courses

Symbolic mathematics engine (SymPy): derivatives, integrals, equation solving, unit conversion

Personal library (book management with cover images)

PDF operations (merge, split, extract text, create from text)

User management and password protection

Dark / light theme (dark default)

Auto‑save and window geometry persistence

Dictionary and user constants database

Installation
Python 3.9+ required.

Install required libraries:

bash
pip install PyQt5 PyQtWebEngine sympy numpy matplotlib language_tool_python ollama openai textstat keybert scholarly PyPDF2 python-docx markdown
Optional for exporting to Word with formatting:

bash
pip install html2docx
Install Ollama (for local AI corrections):

Download from ollama.com

Recommended models: qwen2.5:3b, llama3.2:3b, bazobehram/turkish-gemma-9b-t1 (for Turkish)

Pull a model: ollama pull qwen2.5:3b

Run the application:

bash
python main.py
Default username / password: admin / admin

User Guide
Main Tabs
Main Editor: HTML editing with templates (SEO, Academic, Blog, Product)

My Study Notes: Note‑taking system for YKS, AYT, DGS, KPSS, and university subjects. You can send mathematical expressions as images to the main editor.

Academic Editor: Professional tool for theses, articles, and books. Supports chapters, APA/MLA/Chicago references, footnotes, tables, images, and PDF/Word export.

Menus and Tools
File: New, Open, Save, Load Word template.

Posts: List, view, edit, delete database entries.

Tools: Google Scholar search, Insert mathematical expression, User constants, Find/Replace, My Library (book management), PDF operations.

Dictionary: Personal word‑meaning dictionary.

Guide: SEO and academic writing guidelines.

Settings: Choose AI models per task, enter OpenAI API key, set academic format (APA/MLA/Chicago), enable/disable AI correction, change theme, user management (admin only).

AI Correction
Corrects grammar, style, and fluency in Standard, SEO, or Academic mode.

Uses local Ollama or OpenAI (GPT‑3.5).

Shows an accuracy report with a list of errors.

Mathematics / Study Notes
Keyboard shortcuts for symbols (e.g., Ctrl+Shift+X for x).

Solve equations (Ctrl+E), differentiate (Ctrl+T), integrate (Ctrl+I), compute limits (Ctrl+L), plot graphs (Ctrl+G).

Convert physical units (Ctrl+U) to SI or any defined unit.

Add custom constants (e.g., myG = 6.67430e-11 * m**3/(kg*s**2)) and use them in expressions.

My Library
Add/edit/delete books with title, author, publisher, year, ISBN, cover image (base64), and personal notes.

Search and filter.

PDF Operations
Merge multiple PDFs.

Split a PDF by page ranges (e.g., 1-3,5,7-9).

Create a PDF from plain text.

Extract all text from a PDF.

Configuration Files
ai_models.json – Task‑specific model names.

users.json – Username/password (default admin/admin).

openai_key.txt – Optional OpenAI API key.

window_geometry.json – Remembers window size and position.

autosave_backup.txt – Auto‑save backup every 60 seconds.

posts.db – SQLite database (posts, study notes, constants, books, dictionary).

Contributing
This project is open source. Feel free to report issues or suggest improvements.

License
This project is distributed under the MIT License. You may use it freely for commercial or private purposes.

Contact
Developer: deliKadir
Email: astromoon.1990@gmail.com

