import sys
import re as regex
try:
    import random
except ImportError:
    random = None
try:
    import json
except ImportError:
    json = None
    print("Kütüphane Kurulu değil")
import os
try:
    import sqlite3
except ImportError:
    sqlite3 = None
try:
    from datetime import datetime
except ImportError:
    datetime = None
try:
    import textstat
except ImportError:
    textstat = None
    print("Kütüphane Kurulu değil")
import webbrowser
import time
try:
    import language_tool_python
except ImportError:
    language_tool_python = None
try:
    import ollama
except ImportError:
    ollama = None
import numpy as np
try:
    import matplotlib.pyplot as plt
except ImportError:
    matplotlib = None
    print("Kütüphane Kurulu değil")
import base64
from io import BytesIO

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QFileDialog, QCheckBox, QComboBox,
    QMessageBox, QAction, QToolBar, QLabel, QProgressBar, QGroupBox,
    QDialog, QDialogButtonBox, QLineEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QInputDialog, QFontComboBox, QColorDialog,
    QListWidget, QListWidgetItem, QProgressDialog, QMenu, QMenuBar, QTabWidget,
    QShortcut, QFormLayout, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl, QTimer
from PyQt5.QtGui import QFont, QColor, QTextCharFormat, QTextCursor, QKeySequence, QPixmap, QTextDocument
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog

from sympy import *
from sympy.physics.units import (
    m, kg, s, A, K, mol, cd,
    N, J, W, Pa, V, ohm, Hz, C, F, tesla,
    km, cm, mm, minute, hour, day,
    g, tonne,
    convert_to, Quantity,
    speed_of_light, gravitational_constant, planck, elementary_charge,
    boltzmann, avogadro_number
)

try:
    from sympy.physics.units import gas_constant
except ImportError:
    try:
        from sympy.physics.units import R as gas_constant
    except ImportError:
        try:
            from sympy.constants import R as gas_constant
        except ImportError:
            gas_constant = 8.314462618 * J / (mol * K)

try:
    from sympy.physics.units import electron_rest_mass, proton_rest_mass
except ImportError:
    try:
        from sympy.constants import m_e as electron_rest_mass, m_p as proton_rest_mass
    except ImportError:
        electron_rest_mass = 9.1093837015e-31 * kg
        proton_rest_mass = 1.67262192369e-27 * kg

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    from keybert import KeyBERT
except ImportError:
    KeyBERT = None
    print("Kütüphane Kurulu değil")
try:
    import docx
except ImportError:
    docx = None
    print("Kütüphane Kurulu değil")

try:
    from scholarly import scholarly
except ImportError:
    scholarly = None

# ----------------------------------------------------------------------
# Yapay Zeka Model Yapılandırması
# ----------------------------------------------------------------------
CONFIG_FILE = "ai_models.json"
DEFAULT_MODELS = {
    "academic": "bazobehram/turkish-gemma-9b-t1",
    "seo": "alicankiraz0/Kizagan-E4B:latest",
    "standard": "qwen2.5:3b"
}

def load_model_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        save_model_config(DEFAULT_MODELS)
        return DEFAULT_MODELS.copy()

def save_model_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# ----------------------------------------------------------------------
# Karanlık Tema Siyah Tema Windows 11 tema modeli
# ----------------------------------------------------------------------
DARK_STYLE = """
QMainWindow { background-color: #1e1e1e; }
QWidget { background-color: #2d2d2d; color: #f0f0f0; font-family: 'Segoe UI', 'Consolas', monospace; font-size: 10pt; }
QTextEdit { background-color: #1e1e1e; color: #dcdcdc; border: 1px solid #3c3c3c; border-radius: 6px; padding: 8px; }
QPushButton { background-color: #3c3c3c; border: 1px solid #5a5a5a; border-radius: 4px; padding: 6px 12px; font-weight: bold; }
QPushButton:hover { background-color: #505050; }
QPushButton:pressed { background-color: #2a2a2a; }
QCheckBox, QComboBox, QLabel { background-color: transparent; }
QComboBox { background-color: #3c3c3c; border: 1px solid #5a5a5a; border-radius: 4px; padding: 4px; }
QMenuBar { background-color: #2d2d2d; color: #f0f0f0; }
QMenuBar::item:selected { background-color: #3c3c3c; }
QMenu { background-color: #2d2d2d; color: #f0f0f0; }
QMenu::item:selected { background-color: #3c3c3c; }
QGroupBox { border: 1px solid #5a5a5a; border-radius: 6px; margin-top: 10px; padding-top: 10px; }
QToolBar { background-color: #252525; border: none; spacing: 4px; }
QProgressBar { border: 1px solid #5a5a5a; border-radius: 4px; text-align: center; background-color: #1e1e1e; }
QProgressBar::chunk { background-color: #0e639c; border-radius: 4px; }
QLineEdit { background-color: #1e1e1e; border: 1px solid #3c3c3c; border-radius: 4px; padding: 4px; }
QTableWidget { background-color: #1e1e1e; border: 1px solid #3c3c3c; alternate-background-color: #2a2a2a; }
QHeaderView::section { background-color: #3c3c3c; padding: 4px; }
QDialog { background-color: #2d2d2d; }
QListWidget { background-color: #1e1e1e; border: 1px solid #3c3c3c; border-radius: 4px; }
QTabWidget::pane { border: 1px solid #3c3c3c; background-color: #2d2d2d; }
QTabBar::tab { background-color: #3c3c3c; padding: 8px 16px; margin-right: 2px; }
QTabBar::tab:selected { background-color: #0e639c; }
"""

#Açık tema yeni eklediğim tema ama kullanılmayacak kaldırılacak.
LIGHT_STYLE = """
QMainWindow { background-color: #f0f0f0; }
QWidget { background-color: #ffffff; color: #000000; font-family: 'Segoe UI', 'Consolas', monospace; font-size: 10pt; }
QTextEdit { background-color: #fafafa; color: #000000; border: 1px solid #cccccc; border-radius: 6px; padding: 8px; }
QPushButton { background-color: #e0e0e0; border: 1px solid #aaaaaa; border-radius: 4px; padding: 6px 12px; font-weight: bold; }
QPushButton:hover { background-color: #d0d0d0; }
QPushButton:pressed { background-color: #c0c0c0; }
QCheckBox, QComboBox, QLabel { background-color: transparent; }
QComboBox { background-color: #ffffff; border: 1px solid #aaaaaa; border-radius: 4px; padding: 4px; }
QMenuBar { background-color: #f0f0f0; color: #000000; }
QMenuBar::item:selected { background-color: #d0d0d0; }
QMenu { background-color: #ffffff; color: #000000; }
QMenu::item:selected { background-color: #d0d0d0; }
QGroupBox { border: 1px solid #aaaaaa; border-radius: 6px; margin-top: 10px; padding-top: 10px; }
QToolBar { background-color: #e8e8e8; border: none; spacing: 4px; }
QProgressBar { border: 1px solid #aaaaaa; border-radius: 4px; text-align: center; background-color: #ffffff; }
QProgressBar::chunk { background-color: #0e639c; border-radius: 4px; }
QLineEdit { background-color: #ffffff; border: 1px solid #cccccc; border-radius: 4px; padding: 4px; }
QTableWidget { background-color: #ffffff; border: 1px solid #cccccc; alternate-background-color: #f0f0f0; }
QHeaderView::section { background-color: #e0e0e0; padding: 4px; }
QDialog { background-color: #ffffff; }
QListWidget { background-color: #ffffff; border: 1px solid #cccccc; border-radius: 4px; }
QTabWidget::pane { border: 1px solid #cccccc; background-color: #ffffff; }
QTabBar::tab { background-color: #e0e0e0; padding: 8px 16px; margin-right: 2px; }
QTabBar::tab:selected { background-color: #0e639c; color: white; }
"""

# ----------------------------------------------------------------------
# Akademik Editör (HTML dosyasından yüklenecek)
# ----------------------------------------------------------------------
def create_tez_editor_html():
    html_content = """..."""  # (değişmedi, aynen kaldı)
    file_path = os.path.join(os.path.dirname(__file__), "tez_editor.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return file_path

class AcademicEditorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🎓 Akademik Tez Editörü Pro")
        self.setGeometry(150, 150, 1300, 850)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.web_view = QWebEngineView()
        html_file = create_tez_editor_html()
        self.web_view.setUrl(QUrl.fromLocalFile(html_file))
        layout.addWidget(self.web_view)
        close_btn = QPushButton("✖ Kapat")
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

# ----------------------------------------------------------------------
# AI Modelleri Yapılandırma Diyaloğu
# ----------------------------------------------------------------------
class AIModelsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yapay Zeka Modelleri Seçimi")
        self.setMinimumSize(500, 500)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        self.config = load_model_config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        group = QGroupBox("Görev Bazlı Modeller")
        form_layout = QVBoxLayout()
        h1 = QHBoxLayout()
        h1.addWidget(QLabel("Akademik Makale Modeli:"))
        self.academic_combo = QComboBox()
        self.academic_combo.setEditable(True)
        self.academic_combo.addItems(self.get_installed_models())
        self.academic_combo.setCurrentText(self.config.get("academic", DEFAULT_MODELS["academic"]))
        h1.addWidget(self.academic_combo)
        form_layout.addLayout(h1)
        h2 = QHBoxLayout()
        h2.addWidget(QLabel("SEO Düzeltme Modeli:"))
        self.seo_combo = QComboBox()
        self.seo_combo.setEditable(True)
        self.seo_combo.addItems(self.get_installed_models())
        self.seo_combo.setCurrentText(self.config.get("seo", DEFAULT_MODELS["seo"]))
        h2.addWidget(self.seo_combo)
        form_layout.addLayout(h2)
        h3 = QHBoxLayout()
        h3.addWidget(QLabel("Standart Düzeltme Modeli:"))
        self.standard_combo = QComboBox()
        self.standard_combo.setEditable(True)
        self.standard_combo.addItems(self.get_installed_models())
        self.standard_combo.setCurrentText(self.config.get("standard", DEFAULT_MODELS["standard"]))
        h3.addWidget(self.standard_combo)
        form_layout.addLayout(h3)
        group.setLayout(form_layout)
        layout.addWidget(group)

        api_group = QGroupBox("OpenAI API (İsteğe bağlı)")
        api_layout = QVBoxLayout()
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setPlaceholderText("sk-...")
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        api_layout.addWidget(QLabel("OpenAI API Anahtarı:"))
        api_layout.addWidget(self.api_key_edit)
        self.use_openai = QCheckBox("Ollama yerine OpenAI kullan")
        api_layout.addWidget(self.use_openai)
        if os.path.exists("openai_key.txt"):
            with open("openai_key.txt", "r") as f:
                self.api_key_edit.setText(f.read().strip())
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)

        info = QLabel("Not: Yeni bir model adı yazıp kaydedebilirsiniz.\nModelin sistemde kurulu olması gerekir.\nOpenAI kullanmak için API anahtarı girin ve kutucuğu işaretleyin.")
        info.setWordWrap(True)
        info.setStyleSheet("color: #9cdcfe; font-size: 9pt;")
        layout.addWidget(info)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Kaydet ve Kapat")
        save_btn.clicked.connect(self.save_and_close)
        cancel_btn = QPushButton("İptal")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def get_installed_models(self):
        try:
            result = ollama.list()
            models = [model['name'] for model in result['models']]
            if not models:
                models = ["qwen2.5:3b", "llama3.2:3b", "gemma3:4b", "bazobehram/turkish-gemma-9b-t1"]
            return models
        except:
            return ["qwen2.5:3b", "llama3.2:3b", "gemma3:4b", "bazobehram/turkish-gemma-9b-t1"]

    def save_and_close(self):
        new_config = {
            "academic": self.academic_combo.currentText().strip(),
            "seo": self.seo_combo.currentText().strip(),
            "standard": self.standard_combo.currentText().strip()
        }
        save_model_config(new_config)
        api_key = self.api_key_edit.text().strip()
        with open("openai_key.txt", "w") as f:
            f.write(api_key)
        QMessageBox.information(self, "Başarılı", "Model ayarları ve API anahtarı kaydedildi.\nDeğişiklikler için uygulamayı yeniden başlatın.")
        self.accept()

# ----------------------------------------------------------------------
# Hibrit Doğrulama Thread (OpenAI desteği ile)
# ----------------------------------------------------------------------
class HybridCheckThread(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, text, language='tr-TR', use_ai=True, mode='standart', academic_format='APA', model_name=None, use_openai=False, openai_api_key=""):
        super().__init__()
        self.text = text
        self.language = language
        self.use_ai = use_ai
        self.mode = mode
        self.academic_format = academic_format
        self.model_name = model_name
        self.use_openai = use_openai
        self.openai_api_key = openai_api_key

    def run(self):
        try:
            self.progress.emit(10)
            try:
                lt = language_tool_python.LanguageTool(self.language)
            except:
                lt = language_tool_python.LanguageTool('en-US')
            matches = lt.check(self.text)
            corrected = language_tool_python.utils.correct(self.text, matches)
            lt.close()
            self.progress.emit(40)
            if self.use_ai:
                if self.use_openai and OPENAI_AVAILABLE and self.openai_api_key:
                    openai.api_key = self.openai_api_key
                    if self.mode == 'seo':
                        prompt = f"Aşağıdaki metni SEO kurallarına göre düzenle. Sadece düz metin çıktısı ver.\n\nMetin:\n{corrected}\n\nDüzenlenmiş SEO metni:"
                    elif self.mode == 'academic':
                        fmt = "APA 7" if self.academic_format=='APA' else ("MLA 9" if self.academic_format=='MLA' else "Chicago 17")
                        prompt = f"Aşağıdaki metni akademik makale formatında düzenle. {fmt} kurallarına uy. Metnin dilini resmi, bilimsel yap.\n\nMetin:\n{corrected}\n\nDüzenlenmiş akademik metin:"
                    else:
                        prompt = f"Aşağıdaki metni dil bilgisi, yazım ve anlatım bozukluklarına göre düzelt.\nSadece düzeltilmiş metni ver.\n\nYanlış metin: {corrected}\nDoğru metin:"
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3
                    )
                    corrected = response.choices[0].message.content.strip()
                else:
                    if not self.model_name:
                        raise Exception("AI model adı belirtilmedi.")
                    try:
                        ollama.list()
                    except Exception as e:
                        self.error.emit(f"Ollama çalışmıyor: {str(e)}")
                        return
                    if self.mode == 'seo':
                        prompt = f"Aşağıdaki metni SEO kurallarına göre düzenle. Sadece düz metin çıktısı ver.\n\nMetin:\n{corrected}\n\nDüzenlenmiş SEO metni:"
                    elif self.mode == 'academic':
                        fmt = "APA 7" if self.academic_format=='APA' else ("MLA 9" if self.academic_format=='MLA' else "Chicago 17")
                        prompt = f"Aşağıdaki metni akademik makale formatında düzenle. {fmt} kurallarına uy. Metnin dilini resmi, bilimsel yap.\n\nMetin:\n{corrected}\n\nDüzenlenmiş akademik metin:"
                    else:
                        prompt = f"Aşağıdaki metni dil bilgisi, yazım ve anlatım bozukluklarına göre düzelt.\nSadece düzeltilmiş metni ver.\n\nYanlış metin: {corrected}\nDoğru metin:"
                    response = ollama.generate(model=self.model_name, prompt=prompt)
                    corrected = response['response'].strip()
                self.progress.emit(80)
            score = self.calculate_accuracy(corrected, matches)
            self.progress.emit(95)
            result = {
                'corrected_text': corrected,
                'errors': matches,
                'accuracy_score': score,
                'original_length': len(self.text.split()),
                'corrected_length': len(corrected.split())
            }
            self.progress.emit(100)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

    def calculate_accuracy(self, text, errors):
        word_count = len(text.split())
        if word_count == 0:
            return 0
        score = 100 - min(len(errors)*2, 100)
        try:
            readability = textstat.flesch_reading_ease(text)
            if readability > 60:
                score = min(100, score+5)
            elif readability < 30:
                score = max(0, score-5)
        except:
            pass
        return max(0, min(100, score))

# ----------------------------------------------------------------------
# AccuracyReportDialog
# ----------------------------------------------------------------------
class AccuracyReportDialog(QDialog):
    def __init__(self, errors, score, corrected_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Doğruluk Raporu")
        self.setMinimumSize(700, 500)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        layout = QVBoxLayout(self)
        score_label = QLabel(f"<h1>📊 DOĞRULUK SKORU: {score}/100</h1>")
        if score >= 80:
            score_label.setStyleSheet("color: #4ec9b0;")
        elif score >= 50:
            score_label.setStyleSheet("color: #dcdcaa;")
        else:
            score_label.setStyleSheet("color: #f48771;")
        layout.addWidget(score_label)
        layout.addWidget(QLabel("<b>🔧 Tespit Edilen Hatalar:</b>"))
        self.error_list = QListWidget()
        if errors:
            for err in errors[:20]:
                msg = err.message
                if err.replacements:
                    msg += f" → Öneri: {', '.join(err.replacements[:2])}"
                self.error_list.addItem(QListWidgetItem(f"⚠️ {msg}"))
        else:
            self.error_list.addItem("✅ Hiç hata yok!")
        layout.addWidget(self.error_list)
        layout.addWidget(QLabel("<b>📝 Düzeltilmiş Metin (ilk 500 karakter):</b>"))
        preview = QTextEdit()
        preview.setPlainText(corrected_text[:500] + ("..." if len(corrected_text)>500 else ""))
        preview.setReadOnly(True)
        preview.setMaximumHeight(200)
        layout.addWidget(preview)
        btn = QPushButton("Kapat")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

# ----------------------------------------------------------------------
# Google Scholar
# ----------------------------------------------------------------------
class ScholarSearchThread(QThread):
    result_ready = pyqtSignal(dict)
    progress_update = pyqtSignal(int)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    def __init__(self, query): super().__init__(); self.query = query
    def run(self):
        try:
            search = scholarly.search_pubs(self.query)
            count=0
            for r in search:
                if count>=20: break
                bib=r.get('bib',{})
                info={'title':bib.get('title',''),'authors':bib.get('author',''),'year':bib.get('pub_year',''),'raw_data':r}
                if isinstance(info['authors'],list): info['authors']=', '.join(info['authors'])
                self.result_ready.emit(info)
                count+=1
                self.progress_update.emit(count*5)
                time.sleep(0.1)
            self.progress_update.emit(100)
            self.finished.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))
            self.finished.emit()

class GoogleScholarDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Google Scholar Arama")
        self.setMinimumSize(700,500)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        self.search_thread=None
        self.init_ui()
    def init_ui(self):
        layout=QVBoxLayout(self)
        top=QHBoxLayout()
        self.search_input=QLineEdit()
        self.search_input.setPlaceholderText("Arama cümlesi...")
        self.search_btn=QPushButton("🔍 Ara")
        self.search_btn.clicked.connect(self.start_search)
        top.addWidget(self.search_input)
        top.addWidget(self.search_btn)
        layout.addLayout(top)
        self.progress=QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        self.result_list=QListWidget()
        self.result_list.itemClicked.connect(self.open_link)
        layout.addWidget(self.result_list)
        self.status=QLabel("Arama yapın.")
        layout.addWidget(self.status)
        close=QPushButton("Kapat")
        close.clicked.connect(self.accept)
        layout.addWidget(close)
    def start_search(self):
        q=self.search_input.text().strip()
        if not q: QMessageBox.warning(self,"Uyarı","Arama metni girin."); return
        if self.search_thread and self.search_thread.isRunning(): self.search_thread.terminate()
        self.result_list.clear()
        self.progress.setValue(0)
        self.progress.setVisible(True)
        self.search_btn.setEnabled(False)
        self.status.setText("Aranıyor...")
        self.search_thread=ScholarSearchThread(q)
        self.search_thread.result_ready.connect(self.add_result)
        self.search_thread.progress_update.connect(self.progress.setValue)
        self.search_thread.finished.connect(self.search_finished)
        self.search_thread.error_occurred.connect(self.search_error)
        self.search_thread.start()
    def add_result(self,data):
        item=QListWidgetItem(f"{data['title']} | {data['authors']} ({data['year']})")
        item.setData(Qt.UserRole,data['raw_data'])
        self.result_list.addItem(item)
    def search_finished(self):
        self.search_btn.setEnabled(True)
        self.progress.setVisible(False)
        self.status.setText(f"Tamamlandı. {self.result_list.count()} sonuç.")
    def search_error(self,msg):
        self.search_btn.setEnabled(True)
        self.progress.setVisible(False)
        self.status.setText("Hata oluştu.")
        QMessageBox.critical(self,"Hata",msg)
    def open_link(self,item):
        raw=item.data(Qt.UserRole)
        if not raw: return
        url=raw.get('pub_url') or raw.get('url_scholar')
        if url: webbrowser.open(url)
        else:
            title=raw.get('bib',{}).get('title','')
            if title: webbrowser.open(f"https://scholar.google.com/scholar?q={title.replace(' ','+')}")

# ----------------------------------------------------------------------
# Sözlük ve Veritabanı Kodları ve Kontrolleri
# ----------------------------------------------------------------------
class DictionaryDB:
    def __init__(self, db_name="posts.db"):
        self.db_name=db_name
        self.init_db()
    def init_db(self):
        conn=sqlite3.connect(self.db_name)
        c=conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS dictionary (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT UNIQUE, meaning TEXT)''')
        conn.commit(); conn.close()
    def add_word(self,word,meaning):
        try:
            conn=sqlite3.connect(self.db_name)
            c=conn.cursor()
            c.execute("INSERT INTO dictionary (word,meaning) VALUES (?,?)",(word.strip(),meaning.strip()))
            conn.commit(); conn.close(); return True
        except: return False
    def get_all_words(self):
        conn=sqlite3.connect(self.db_name)
        c=conn.cursor()
        c.execute("SELECT word,meaning FROM dictionary ORDER BY word")
        rows=c.fetchall(); conn.close(); return rows

class AddWordDialog(QDialog):
    def __init__(self,db,parent=None):
        super().__init__(parent)
        self.db=db
        self.setWindowTitle("Kelime Ekle")
        self.setMinimumWidth(400)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        layout=QVBoxLayout(self)
        wl=QHBoxLayout(); wl.addWidget(QLabel("Kelime:")); self.word_edit=QLineEdit(); wl.addWidget(self.word_edit); layout.addLayout(wl)
        ml=QHBoxLayout(); ml.addWidget(QLabel("Anlam:")); self.meaning_edit=QTextEdit(); self.meaning_edit.setMaximumHeight(150); ml.addWidget(self.meaning_edit); layout.addLayout(ml)
        btnl=QHBoxLayout(); save=QPushButton("Kaydet"); save.clicked.connect(self.save); cancel=QPushButton("İptal"); cancel.clicked.connect(self.reject); btnl.addWidget(save); btnl.addWidget(cancel); layout.addLayout(btnl)
    def save(self):
        w=self.word_edit.text().strip(); m=self.meaning_edit.toPlainText().strip()
        if not w or not m: QMessageBox.warning(self,"Uyarı","Boş bırakmayın"); return
        if self.db.add_word(w,m): QMessageBox.information(self,"Başarılı","Eklendi"); self.accept()
        else: QMessageBox.warning(self,"Hata","Zaten var")

class DictionaryDialog(QDialog):
    def __init__(self,db,parent=None):
        super().__init__(parent)
        self.db=db
        self.setWindowTitle("Sözlük Uygulaması")
        self.setMinimumSize(500,400)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        self.all_words=[]
        self.init_ui()
        self.load_all()
    def init_ui(self):
        layout=QVBoxLayout(self)
        top=QHBoxLayout()
        self.filter=QLineEdit()
        self.filter.setPlaceholderText("Ara...")
        self.filter.textChanged.connect(self.filter_words)
        addbtn=QPushButton("➕ Ekle")
        addbtn.clicked.connect(self.add_new)
        top.addWidget(self.filter); top.addWidget(addbtn)
        layout.addLayout(top)
        self.list=QListWidget()
        self.list.itemDoubleClicked.connect(self.show_meaning)
        layout.addWidget(self.list)
        close=QPushButton("Kapat")
        close.clicked.connect(self.accept)
        layout.addWidget(close)
    def load_all(self):
        self.all_words=self.db.get_all_words()
        self.filter_words()
    def filter_words(self):
        kw=self.filter.text().strip().lower()
        self.list.clear()
        for w,m in self.all_words:
            if kw in w.lower(): self.list.addItem(w)
    def add_new(self):
        dlg=AddWordDialog(self.db,self)
        if dlg.exec_(): self.load_all()
    def show_meaning(self,item):
        word=item.text()
        for w,m in self.all_words:
            if w==word: QMessageBox.information(self,f"Anlamı: {word}",m); return

class DatabaseManager:
    def __init__(self, db_name="posts.db"):
        self.db_name=db_name
        self.init_db()
    def init_db(self):
        conn=sqlite3.connect(self.db_name)
        c=conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, type TEXT, date TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS study_notes (id INTEGER PRIMARY KEY AUTOINCREMENT, ders TEXT, konu TEXT, content TEXT, date TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS user_constants (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, value_expr TEXT, unit TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            cover_base64 TEXT,
            publisher TEXT,
            year TEXT,
            isbn TEXT,
            notes TEXT,
            date_added TEXT
        )''')
        conn.commit(); conn.close()
    def save_post(self,title,content,ptype):
        conn=sqlite3.connect(self.db_name)
        c=conn.cursor()
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO posts (title,content,type,date) VALUES (?,?,?,?)",(title,content,ptype,date))
        conn.commit(); conn.close(); return True
    def update_post(self,pid,title,content,ptype):
        conn=sqlite3.connect(self.db_name)
        c=conn.cursor()
        c.execute("UPDATE posts SET title=?, content=?, type=? WHERE id=?",(title,content,ptype,pid))
        conn.commit(); conn.close(); return True
    def delete_post(self,pid):
        conn=sqlite3.connect(self.db_name); c=conn.cursor()
        c.execute("DELETE FROM posts WHERE id=?",(pid,))
        conn.commit(); conn.close(); return True
    def get_all_posts(self):
        conn=sqlite3.connect(self.db_name); c=conn.cursor()
        c.execute("SELECT id, title, type, date FROM posts ORDER BY date DESC")
        rows=c.fetchall(); conn.close(); return rows
    def get_post_content(self,pid):
        conn=sqlite3.connect(self.db_name); c=conn.cursor()
        c.execute("SELECT content, title, type, date FROM posts WHERE id=?",(pid,))
        row=c.fetchone(); conn.close(); return row
    def save_study_note(self, ders, konu, content):
        conn=sqlite3.connect(self.db_name)
        c=conn.cursor()
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("SELECT id FROM study_notes WHERE ders=? AND konu=?", (ders, konu))
        existing = c.fetchone()
        if existing:
            c.execute("UPDATE study_notes SET content=?, date=? WHERE ders=? AND konu=?",(content, date, ders, konu))
        else:
            c.execute("INSERT INTO study_notes (ders,konu,content,date) VALUES (?,?,?,?)",(ders, konu, content, date))
        conn.commit(); conn.close(); return True
    def get_study_note(self, ders, konu):
        conn=sqlite3.connect(self.db_name)
        c=conn.cursor()
        c.execute("SELECT content FROM study_notes WHERE ders=? AND konu=?", (ders, konu))
        row=c.fetchone()
        conn.close()
        return row[0] if row else None
    def get_all_study_notes(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT DISTINCT ders, konu FROM study_notes ORDER BY ders, konu")
        rows = c.fetchall()
        conn.close()
        return rows
    def add_user_constant(self, name, value_expr, unit=""):
        conn=sqlite3.connect(self.db_name)
        c=conn.cursor()
        try:
            c.execute("INSERT INTO user_constants (name, value_expr, unit) VALUES (?,?,?)", (name, value_expr, unit))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    def get_all_user_constants(self):
        conn=sqlite3.connect(self.db_name)
        c=conn.cursor()
        c.execute("SELECT name, value_expr, unit FROM user_constants")
        rows=c.fetchall()
        conn.close()
        return rows
    def delete_user_constant(self, name):
        conn=sqlite3.connect(self.db_name)
        c=conn.cursor()
        c.execute("DELETE FROM user_constants WHERE name=?", (name,))
        conn.commit()
        conn.close()
    def add_book(self, title, author, cover_base64, publisher, year, isbn, notes):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO books (title, author, cover_base64, publisher, year, isbn, notes, date_added) VALUES (?,?,?,?,?,?,?,?)",
                  (title, author, cover_base64, publisher, year, isbn, notes, date_added))
        conn.commit()
        conn.close()
    def update_book(self, book_id, title, author, cover_base64, publisher, year, isbn, notes):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("UPDATE books SET title=?, author=?, cover_base64=?, publisher=?, year=?, isbn=?, notes=? WHERE id=?",
                  (title, author, cover_base64, publisher, year, isbn, notes, book_id))
        conn.commit()
        conn.close()
    def delete_book(self, book_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        conn.close()
    def get_all_books(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT id, title, author, cover_base64, publisher, year, isbn, notes, date_added FROM books ORDER BY title")
        rows = c.fetchall()
        conn.close()
        return rows
    def get_book(self, book_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT id, title, author, cover_base64, publisher, year, isbn, notes FROM books WHERE id=?", (book_id,))
        row = c.fetchone()
        conn.close()
        return row

class UserConstantsDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Kullanıcı Sabitleri")
        self.setMinimumSize(500, 400)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Sembol", "Birim İfadesi", "Birim"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Yeni Sabit")
        add_btn.clicked.connect(self.add_constant)
        del_btn = QPushButton("🗑️ Seçili Sabiti Sil")
        del_btn.clicked.connect(self.delete_constant)
        refresh_btn = QPushButton("🔄 Yenile")
        refresh_btn.clicked.connect(self.load_constants)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        btn_layout.addWidget(refresh_btn)
        layout.addLayout(btn_layout)
        self.load_constants()

    def load_constants(self):
        rows = self.db.get_all_user_constants()
        self.table.setRowCount(len(rows))
        for i, (name, expr, unit) in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(expr))
            self.table.setItem(i, 2, QTableWidgetItem(unit))
        self.table.resizeColumnsToContents()

    def add_constant(self):
        name, ok = QInputDialog.getText(self, "Yeni Sabit", "Sembol (ör: myG):")
        if not ok or not name.strip():
            return
        expr, ok = QInputDialog.getText(self, "Sabit İfadesi", "Sympy ifadesi (ör: 6.67430e-11):")
        if not ok or not expr.strip():
            return
        unit, ok = QInputDialog.getText(self, "Birim (isteğe bağlı)", "Birim (m, kg, m/s, ...):")
        if not ok:
            unit = ""
        if self.db.add_user_constant(name.strip(), expr.strip(), unit):
            QMessageBox.information(self, "Başarılı", "Sabit eklendi.")
            self.load_constants()
        else:
            QMessageBox.warning(self, "Hata", "Bu sembol zaten var.")

    def delete_constant(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir sabit seçin.")
            return
        name = self.table.item(row, 0).text()
        if QMessageBox.question(self, "Onay", f"{name} silinsin mi?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            self.db.delete_user_constant(name)
            self.load_constants()

class PostsListDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db=db
        self.parent_app=parent
        self.setWindowTitle("Kayıtlı Yazılar")
        self.setMinimumSize(700,500)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        layout=QVBoxLayout(self)
        self.table=QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID","Başlık","Tür","Tarih"])
        self.table.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.table)
        btnl=QHBoxLayout()
        view=QPushButton("Görüntüle"); view.clicked.connect(self.view)
        edit=QPushButton("✏️ Düzenle"); edit.clicked.connect(self.edit)
        delete=QPushButton("🗑️ Sil"); delete.clicked.connect(self.delete)
        refresh=QPushButton("Yenile"); refresh.clicked.connect(self.load)
        close=QPushButton("Kapat"); close.clicked.connect(self.accept)
        for b in (view,edit,delete,refresh,close): btnl.addWidget(b)
        layout.addLayout(btnl)
        self.load()
    def load(self):
        posts=self.db.get_all_posts()
        self.table.setRowCount(len(posts))
        for r,(pid,title,ptype,date) in enumerate(posts):
            self.table.setItem(r,0,QTableWidgetItem(str(pid)))
            self.table.setItem(r,1,QTableWidgetItem(title))
            self.table.setItem(r,2,QTableWidgetItem(ptype))
            self.table.setItem(r,3,QTableWidgetItem(date))
        self.table.resizeColumnsToContents()
    def get_selected_id(self):
        row=self.table.currentRow()
        if row<0: QMessageBox.warning(self,"Uyarı","Seçim yapın"); return None
        return int(self.table.item(row,0).text())
    def view(self):
        pid=self.get_selected_id()
        if not pid: return
        content,title,ptype,date=self.db.get_post_content(pid)
        dlg=QDialog(self); dlg.setWindowTitle(title); dlg.setMinimumSize(700,500); # dlg.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        lay=QVBoxLayout(dlg)
        lay.addWidget(QLabel(f"<b>{title}</b> | {ptype} | {date}"))
        te=QTextEdit(); te.setHtml(content); te.setReadOnly(True); lay.addWidget(te)
        btn=QDialogButtonBox(QDialogButtonBox.Ok); btn.accepted.connect(dlg.accept); lay.addWidget(btn)
        dlg.exec_()
    def edit(self):
        pid=self.get_selected_id()
        if not pid: return
        content,title,ptype,date=self.db.get_post_content(pid)
        self.parent_app.load_post_for_edit(pid,title,ptype,content)
        self.accept()
    def delete(self):
        pid=self.get_selected_id()
        if not pid: return
        if QMessageBox.question(self,"Silmeyi Onayla","Emin misiniz?",QMessageBox.Yes|QMessageBox.No)==QMessageBox.Yes:
            self.db.delete_post(pid); QMessageBox.information(self,"Silindi","Silindi"); self.load()

# ----------------------------------------------------------------------
# Kütüphane Diyaloğu (E-Kitap Yönetimi)
# ----------------------------------------------------------------------
class LibraryDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("📚 Kütüphanem - Kitap Yönetimi")
        self.setMinimumSize(900, 600)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        self.current_book_id = None
        self.current_cover_base64 = None
        self.init_ui()
        self.load_books()

    def init_ui(self):
        layout = QVBoxLayout(self)
        main_layout = QHBoxLayout()
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.addWidget(QLabel("📖 Kitaplarım"))
        self.book_list = QListWidget()
        self.book_list.itemClicked.connect(self.on_book_selected)
        left_layout.addWidget(self.book_list)
        main_layout.addWidget(left_widget, 1)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        self.title_edit = QLineEdit()
        self.author_edit = QLineEdit()
        self.publisher_edit = QLineEdit()
        self.year_edit = QLineEdit()
        self.isbn_edit = QLineEdit()
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(100)
        form_layout.addRow("Kitap Adı:", self.title_edit)
        form_layout.addRow("Yazar:", self.author_edit)
        form_layout.addRow("Yayınevi:", self.publisher_edit)
        form_layout.addRow("Yıl:", self.year_edit)
        form_layout.addRow("ISBN:", self.isbn_edit)
        form_layout.addRow("Notlar:", self.notes_edit)
        cover_layout = QHBoxLayout()
        self.cover_label = QLabel()
        self.cover_label.setFixedSize(150, 200)
        self.cover_label.setStyleSheet("border: 1px solid #555; background-color: #1e1e1e;")
        self.cover_label.setAlignment(Qt.AlignCenter)
        self.cover_label.setText("Kapak Yok")
        cover_layout.addWidget(self.cover_label)
        cover_btn_layout = QVBoxLayout()
        load_cover_btn = QPushButton("📷 Kapak Yükle")
        load_cover_btn.clicked.connect(self.load_cover_image)
        clear_cover_btn = QPushButton("🗑️ Kapağı Kaldır")
        clear_cover_btn.clicked.connect(self.clear_cover)
        cover_btn_layout.addWidget(load_cover_btn)
        cover_btn_layout.addWidget(clear_cover_btn)
        cover_layout.addLayout(cover_btn_layout)
        right_layout.addWidget(form_widget)
        right_layout.addLayout(cover_layout)
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("➕ Kitap Ekle / Güncelle")
        self.save_btn.clicked.connect(self.save_book)
        self.delete_btn = QPushButton("🗑️ Seçili Kitabı Sil")
        self.delete_btn.clicked.connect(self.delete_book)
        self.clear_btn = QPushButton("🔄 Temizle")
        self.clear_btn.clicked.connect(self.clear_form)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.clear_btn)
        right_layout.addLayout(btn_layout)
        main_layout.addWidget(right_widget, 2)
        layout.addLayout(main_layout)
        self.status_label = QLabel("Kütüphane yüklendi.")
        layout.addWidget(self.status_label)
        close_btn = QPushButton("Kapat")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def load_books(self):
        self.book_list.clear()
        books = self.db.get_all_books()
        for book in books:
            book_id, title, author, _, _, _, _, _, _ = book
            display = f"{title} - {author}" if author else title
            item = QListWidgetItem(display)
            item.setData(Qt.UserRole, book_id)
            self.book_list.addItem(item)
        self.status_label.setText(f"{len(books)} kitap yüklendi.")

    def on_book_selected(self, item):
        book_id = item.data(Qt.UserRole)
        book = self.db.get_book(book_id)
        if book:
            self.current_book_id = book[0]
            self.title_edit.setText(book[1])
            self.author_edit.setText(book[2])
            self.current_cover_base64 = book[3]
            self.publisher_edit.setText(book[4])
            self.year_edit.setText(book[5])
            self.isbn_edit.setText(book[6])
            self.notes_edit.setPlainText(book[7])
            self.display_cover(self.current_cover_base64)

    def display_cover(self, base64_str):
        if base64_str and base64_str.strip():
            try:
                pixmap = QPixmap()
                pixmap.loadFromData(base64.b64decode(base64_str))
                pixmap = pixmap.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.cover_label.setPixmap(pixmap)
            except:
                self.cover_label.setText("Hata")
                self.cover_label.setPixmap(QPixmap())
        else:
            self.cover_label.setText("Kapak Yok")
            self.cover_label.setPixmap(QPixmap())

    def load_cover_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Kitap Kapağı Seç", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            with open(file_path, "rb") as f:
                self.current_cover_base64 = base64.b64encode(f.read()).decode()
                self.display_cover(self.current_cover_base64)

    def clear_cover(self):
        self.current_cover_base64 = None
        self.cover_label.setText("Kapak Yok")
        self.cover_label.setPixmap(QPixmap())

    def save_book(self):
        title = self.title_edit.text().strip()
        if not title:
            QMessageBox.warning(self, "Uyarı", "Kitap adı boş olamaz.")
            return
        author = self.author_edit.text().strip()
        publisher = self.publisher_edit.text().strip()
        year = self.year_edit.text().strip()
        isbn = self.isbn_edit.text().strip()
        notes = self.notes_edit.toPlainText().strip()
        cover = self.current_cover_base64 if self.current_cover_base64 else ""
        if self.current_book_id is None:
            self.db.add_book(title, author, cover, publisher, year, isbn, notes)
            QMessageBox.information(self, "Başarılı", "Kitap eklendi.")
        else:
            self.db.update_book(self.current_book_id, title, author, cover, publisher, year, isbn, notes)
            QMessageBox.information(self, "Başarılı", "Kitap güncellendi.")
        self.load_books()
        self.clear_form()

    def delete_book(self):
        if self.current_book_id is None:
            QMessageBox.warning(self, "Uyarı", "Lütfen listeden bir kitap seçin.")
            return
        if QMessageBox.question(self, "Onay", "Bu kitabı silmek istediğinize emin misiniz?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.db.delete_book(self.current_book_id)
            QMessageBox.information(self, "Başarılı", "Kitap silindi.")
            self.load_books()
            self.clear_form()

    def clear_form(self):
        self.current_book_id = None
        self.title_edit.clear()
        self.author_edit.clear()
        self.publisher_edit.clear()
        self.year_edit.clear()
        self.isbn_edit.clear()
        self.notes_edit.clear()
        self.clear_cover()
        self.status_label.setText("Yeni kitap eklemek için formu doldurun.")

# ----------------------------------------------------------------------
# PDF İşlemleri Diyaloğu (Birleştir, Böl, Oluştur, Metin Çıkar)
# ----------------------------------------------------------------------
class PDFOperationsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📄 PDF İşlemleri")
        self.setMinimumSize(700, 500)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        # Sekmeler aynen kaldı...
        merge_tab = QWidget()
        merge_layout = QVBoxLayout(merge_tab)
        merge_layout.addWidget(QLabel("Birleştirilecek PDF dosyalarını seçin:"))
        self.merge_list = QListWidget()
        merge_layout.addWidget(self.merge_list)
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Dosya Ekle")
        add_btn.clicked.connect(self.add_merge_files)
        remove_btn = QPushButton("🗑️ Seçiliyi Kaldır")
        remove_btn.clicked.connect(lambda: self.remove_selected(self.merge_list))
        clear_btn = QPushButton("🔄 Tümünü Temizle")
        clear_btn.clicked.connect(lambda: self.merge_list.clear())
        merge_btn = QPushButton("🔗 Birleştir ve Kaydet")
        merge_btn.clicked.connect(self.merge_pdfs)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(remove_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(merge_btn)
        merge_layout.addLayout(btn_layout)
        self.tabs.addTab(merge_tab, "🔗 Birleştir")
        split_tab = QWidget()
        split_layout = QVBoxLayout(split_tab)
        split_layout.addWidget(QLabel("Kaynak PDF dosyası:"))
        self.split_file_edit = QLineEdit()
        self.split_file_edit.setReadOnly(True)
        split_file_btn = QPushButton("📂 Seç")
        split_file_btn.clicked.connect(self.select_split_file)
        split_layout.addWidget(self.split_file_edit)
        split_layout.addWidget(split_file_btn)
        split_layout.addWidget(QLabel("Sayfa aralığı (örn: 1-3,5,7-9):"))
        self.split_range_edit = QLineEdit()
        self.split_range_edit.setPlaceholderText("Örnek: 1-5,8,10-15")
        split_layout.addWidget(self.split_range_edit)
        split_btn = QPushButton("✂️ Böl ve Kaydet")
        split_btn.clicked.connect(self.split_pdf)
        split_layout.addWidget(split_btn)
        self.tabs.addTab(split_tab, "✂️ Böl")
        create_tab = QWidget()
        create_layout = QVBoxLayout(create_tab)
        create_layout.addWidget(QLabel("Kaynak metin:"))
        self.create_text_edit = QTextEdit()
        create_layout.addWidget(self.create_text_edit)
        create_layout.addWidget(QLabel("Çıktı PDF dosyası:"))
        self.create_output_edit = QLineEdit()
        self.create_output_edit.setReadOnly(True)
        create_output_btn = QPushButton("💾 Çıktı Yolu Seç")
        create_output_btn.clicked.connect(lambda: self.save_pdf_dialog(self.create_output_edit))
        create_layout.addWidget(self.create_output_edit)
        create_layout.addWidget(create_output_btn)
        create_pdf_btn = QPushButton("📄 PDF Oluştur")
        create_pdf_btn.clicked.connect(self.create_pdf_from_text)
        create_layout.addWidget(create_pdf_btn)
        self.tabs.addTab(create_tab, "📄 Oluştur")
        extract_tab = QWidget()
        extract_layout = QVBoxLayout(extract_tab)
        extract_layout.addWidget(QLabel("PDF dosyası:"))
        self.extract_file_edit = QLineEdit()
        self.extract_file_edit.setReadOnly(True)
        extract_file_btn = QPushButton("📂 Seç")
        extract_file_btn.clicked.connect(self.select_extract_file)
        extract_layout.addWidget(self.extract_file_edit)
        extract_layout.addWidget(extract_file_btn)
        extract_btn = QPushButton("📝 Metni Çıkar")
        extract_btn.clicked.connect(self.extract_text_from_pdf)
        extract_layout.addWidget(extract_btn)
        self.extract_result = QTextEdit()
        self.extract_result.setReadOnly(True)
        extract_layout.addWidget(self.extract_result)
        self.tabs.addTab(extract_tab, "📝 Metin Çıkar")
        close_btn = QPushButton("Kapat")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    # ... diğer metodlar aynı ...
    def add_merge_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "PDF Dosyaları Seç", "", "PDF Dosyaları (*.pdf)")
        for f in files:
            self.merge_list.addItem(f)
    def remove_selected(self, list_widget):
        for item in list_widget.selectedItems():
            list_widget.takeItem(list_widget.row(item))
    def merge_pdfs(self):
        if self.merge_list.count() == 0:
            QMessageBox.warning(self, "Uyarı", "Birleştirilecek dosya seçmediniz.")
            return
        output_path, _ = QFileDialog.getSaveFileName(self, "Birleştirilmiş PDF Kaydet", "", "PDF Dosyası (*.pdf)")
        if not output_path:
            return
        try:
            from PyPDF2 import PdfMerger
            merger = PdfMerger()
            for i in range(self.merge_list.count()):
                merger.append(self.merge_list.item(i).text())
            merger.write(output_path)
            merger.close()
            QMessageBox.information(self, "Başarılı", f"PDF'ler birleştirildi:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Birleştirme hatası: {str(e)}")
    def select_split_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Bölünecek PDF Seç", "", "PDF Dosyaları (*.pdf)")
        if path:
            self.split_file_edit.setText(path)
    def split_pdf(self):
        source = self.split_file_edit.text().strip()
        if not source or not os.path.exists(source):
            QMessageBox.warning(self, "Uyarı", "Geçerli bir kaynak PDF seçin.")
            return
        range_text = self.split_range_edit.text().strip()
        if not range_text:
            QMessageBox.warning(self, "Uyarı", "Sayfa aralığı girin (örn: 1-3,5,7-9).")
            return
        try:
            from PyPDF2 import PdfReader, PdfWriter
            reader = PdfReader(source)
            total_pages = len(reader.pages)
            pages_to_extract = set()
            parts = range_text.split(',')
            for part in parts:
                part = part.strip()
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    if start < 1 or end > total_pages or start > end:
                        raise ValueError(f"Geçersiz aralık: {part}")
                    pages_to_extract.update(range(start-1, end))
                else:
                    p = int(part)
                    if p < 1 or p > total_pages:
                        raise ValueError(f"Sayfa numarası geçersiz: {p}")
                    pages_to_extract.add(p-1)
            if not pages_to_extract:
                raise ValueError("Hiçbir sayfa seçilmedi.")
            output_path, _ = QFileDialog.getSaveFileName(self, "Bölünmüş PDF Kaydet", "", "PDF Dosyası (*.pdf)")
            if not output_path:
                return
            writer = PdfWriter()
            for page_num in sorted(pages_to_extract):
                writer.add_page(reader.pages[page_num])
            with open(output_path, 'wb') as f:
                writer.write(f)
            QMessageBox.information(self, "Başarılı", f"PDF bölündü ve kaydedildi:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))
    def save_pdf_dialog(self, line_edit):
        path, _ = QFileDialog.getSaveFileName(self, "PDF Kaydet", "", "PDF Dosyası (*.pdf)")
        if path:
            line_edit.setText(path)
    def create_pdf_from_text(self):
        text = self.create_text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Uyarı", "Metin girin.")
            return
        output_path = self.create_output_edit.text().strip()
        if not output_path:
            QMessageBox.warning(self, "Uyarı", "Çıktı dosyası yolunu seçin.")
            return
        try:
            doc = QTextDocument()
            doc.setPlainText(text)
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(output_path)
            doc.print_(printer)
            QMessageBox.information(self, "Başarılı", f"PDF oluşturuldu:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"PDF oluşturma hatası: {str(e)}")
    def select_extract_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "PDF Seç", "", "PDF Dosyaları (*.pdf)")
        if path:
            self.extract_file_edit.setText(path)
    def extract_text_from_pdf(self):
        path = self.extract_file_edit.text().strip()
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "Uyarı", "Geçerli bir PDF dosyası seçin.")
            return
        try:
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            self.extract_result.setPlainText(text if text.strip() else "Metin bulunamadı.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Metin çıkarma hatası: {str(e)}")

# ----------------------------------------------------------------------
# Kullanıcı Yönetimi (Admin)
# ----------------------------------------------------------------------
class UserManager:
    def __init__(self,filename="users.json"):
        self.filename=filename
        self.load()
    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename,"r",encoding="utf-8") as f: self.users=json.load(f)
        else:
            self.users={"admin":"admin"}
            self.save()
    def save(self):
        with open(self.filename,"w",encoding="utf-8") as f: json.dump(self.users,f,indent=2,ensure_ascii=False)
    def validate(self,user,pwd): return self.users.get(user)==pwd
    def change_password(self,user,old,new):
        if self.validate(user,old): self.users[user]=new; self.save(); return True
        return False
    def get_password(self,user): return self.users.get(user)
    def adduser(self,username,password):
        if username in self.users:
            return False
        self.users[username]=password
        self.save()
        return True
    def remove_user(self,username):
        if username == "admin" or username not in self.users:
            return False
        del self.users[username]
        self.save()
        return True
    def list_users(self):
        return list(self.users.keys())

class LoginDialog(QDialog):
    def __init__(self,um,parent=None):
        super().__init__(parent)
        self.um=um
        self.setWindowTitle("Giriş")
        self.setMinimumWidth(350)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        layout=QVBoxLayout(self)
        layout.addWidget(QLabel("Kullanıcı:"))
        self.user=QLineEdit(); self.user.setPlaceholderText("admin"); layout.addWidget(self.user)
        layout.addWidget(QLabel("Şifre:"))
        self.pwd=QLineEdit(); self.pwd.setEchoMode(QLineEdit.Password); layout.addWidget(self.pwd)
        btnl=QHBoxLayout()
        login=QPushButton("Giriş"); login.clicked.connect(self.check)
        change=QPushButton("Şifre Değiştir"); change.clicked.connect(self.open_change)
        forgot=QPushButton("Şifremi Unuttum"); forgot.clicked.connect(self.open_forgot)
        btnl.addWidget(login); btnl.addWidget(change); btnl.addWidget(forgot)
        layout.addLayout(btnl)
        self.msg=QLabel(""); self.msg.setStyleSheet("color:#f48771"); layout.addWidget(self.msg)
    def check(self):
        if self.um.validate(self.user.text().strip(), self.pwd.text().strip()): self.accept()
        else: self.msg.setText("❌ Hatalı giriş")
    def open_change(self): ChangePasswordDialog(self.um,self).exec_()
    def open_forgot(self): ForgotPasswordDialog(self.um,self).exec_()

class ChangePasswordDialog(QDialog):
    def __init__(self,um,parent=None):
        super().__init__(parent)
        self.um=um
        self.setWindowTitle("Şifre Değiştir")
        self.setMinimumWidth(300)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        layout=QVBoxLayout(self)
        layout.addWidget(QLabel("Kullanıcı:"))
        self.user=QLineEdit(); layout.addWidget(self.user)
        layout.addWidget(QLabel("Eski Şifre:")); self.old=QLineEdit(); self.old.setEchoMode(QLineEdit.Password); layout.addWidget(self.old)
        layout.addWidget(QLabel("Yeni Şifre:")); self.new1=QLineEdit(); self.new1.setEchoMode(QLineEdit.Password); layout.addWidget(self.new1)
        layout.addWidget(QLabel("Tekrar:")); self.new2=QLineEdit(); self.new2.setEchoMode(QLineEdit.Password); layout.addWidget(self.new2)
        btn=QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        btn.accepted.connect(self.save); btn.rejected.connect(self.reject)
        layout.addWidget(btn)
        self.status=QLabel(""); self.status.setStyleSheet("color:#f48771"); layout.addWidget(self.status)
    def save(self):
        u=self.user.text().strip(); o=self.old.text().strip(); n=self.new1.text().strip(); c=self.new2.text().strip()
        if not u or not o or not n: self.status.setText("Tüm alanları doldurun"); return
        if n!=c: self.status.setText("Şifreler uyuşmuyor"); return
        if self.um.change_password(u,o,n): QMessageBox.information(self,"Başarılı","Değişti"); self.accept()
        else: self.status.setText("Kullanıcı/şifre hatalı")

class ForgotPasswordDialog(QDialog):
    def __init__(self,um,parent=None):
        super().__init__(parent)
        self.um=um
        self.setWindowTitle("Şifremi Unuttum")
        self.setMinimumWidth(300)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        layout=QVBoxLayout(self)
        layout.addWidget(QLabel("Kullanıcı adı:"))
        self.user=QLineEdit(); layout.addWidget(self.user)
        show=QPushButton("Göster"); show.clicked.connect(self.show_pwd)
        layout.addWidget(show)
        self.res=QLabel(""); self.res.setWordWrap(True); layout.addWidget(self.res)
        close=QDialogButtonBox(QDialogButtonBox.Close); close.rejected.connect(self.reject); layout.addWidget(close)
    def show_pwd(self):
        p=self.um.get_password(self.user.text().strip())
        if p: self.res.setText(f"Şifreniz: {p}")
        else: self.res.setText("Kullanıcı bulunamadı")

class UserManagementDialog(QDialog):
    def __init__(self, user_manager, parent=None):
        super().__init__(parent)
        self.um = user_manager
        self.setWindowTitle("Kullanıcı Yönetimi (Admin)")
        self.setMinimumSize(400, 300)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        layout = QVBoxLayout(self)
        self.user_list = QListWidget()
        self.refresh_list()
        layout.addWidget(self.user_list)
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Yeni Kullanıcı")
        add_btn.clicked.connect(self.add_user)
        del_btn = QPushButton("🗑️ Seçili Kullanıcıyı Sil")
        del_btn.clicked.connect(self.delete_user)
        close_btn = QPushButton("Kapat")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
    def refresh_list(self):
        self.user_list.clear()
        for u in self.um.list_users():
            self.user_list.addItem(u)
    def add_user(self):
        username, ok = QInputDialog.getText(self, "Yeni Kullanıcı", "Kullanıcı adı:")
        if not ok or not username.strip():
            return
        if username.strip() in self.um.list_users():
            QMessageBox.warning(self, "Hata", "Bu kullanıcı zaten var.")
            return
        password, ok = QInputDialog.getText(self, "Şifre", "Şifre:", QLineEdit.Password)
        if not ok or not password:
            return
        if self.um.adduser(username.strip(), password):
            QMessageBox.information(self, "Başarılı", "Kullanıcı eklendi.")
            self.refresh_list()
        else:
            QMessageBox.warning(self, "Hata", "Eklenemedi.")
    def delete_user(self):
        current = self.user_list.currentItem()
        if not current:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir kullanıcı seçin.")
            return
        username = current.text()
        if username == "admin":
            QMessageBox.warning(self, "Hata", "Admin kullanıcısı silinemez.")
            return
        if QMessageBox.question(self, "Onay", f"{username} silinsin mi?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            if self.um.remove_user(username):
                QMessageBox.information(self, "Başarılı", "Silindi.")
                self.refresh_list()
            else:
                QMessageBox.warning(self, "Hata", "Silinemedi.")

# ----------------------------------------------------------------------
# Şablon ve Yardımcı
# ----------------------------------------------------------------------
def seo_template(): return "<h1>SEO Makalesi Örneği</h1><p>İçerik buraya.</p>"
def academic_template(): return "<h1>Akademik Makale Örneği</h1><p>Tez rehberi...</p>"
def blog_template(): return "<h1>Blog Yazısı Örneği</h1><p>Blog içeriği...</p>"
def product_template(): return "<h1>Ürün Tanıtımı</h1><p>Ürün bilgileri...</p>"

def clean_html(raw):
    cleaner=regex.compile('<.*?>')
    text=regex.sub(cleaner,'',raw)
    return text.replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>')

def text_correction_engine(text):
    text=regex.sub(r'\s+',' ',text)
    words=text.split()
    fixed=[]
    for i,w in enumerate(words):
        if i==0 or w.lower()!=words[i-1].lower(): fixed.append(w)
    text=' '.join(fixed)
    text=regex.sub(r'\s+([.,!?])',r'\1',text)
    text=regex.sub(r'([.,!?])([^\s])',r'\1 \2',text)
    return text.strip()

def seo_rewrite(text,keywords):
    sentences=text.split('.')
    out=[]
    for i,s in enumerate(sentences):
        s=s.strip()
        if not s: continue
        if i==0 and keywords: s=keywords[0]+' '+s
        out.append(s)
    result='. '.join(out)
    if keywords: result=f"# {keywords[0].title()}\n\n"+result
    return result

def academic_rewrite(text,format_type):
    connectors=["Bununla birlikte","Öte yandan","Dolayısıyla","Ayrıca","Bu bağlamda","Nitekim","Buna karşın"]
    sentences=text.split('.')
    out=["Bu çalışma kapsamında konu sistematik olarak incelenmektedir"]
    for i,s in enumerate(sentences):
        s=s.strip()
        if not s: continue
        if len(s.split())<6: s+=" Bu durum literatürde desteklenmektedir"
        if i!=0: s=random.choice(connectors)+", "+s.lower()
        out.append(s)
    text='. '.join(out)+'.'
    text=regex.sub(r'(\w+) yapıldı',r'Yapıldı \1 tarafından',text)
    if format_type=="APA": text+=" (Yazar, 2020)"
    elif format_type=="MLA": text+=" (Yazar 20)"
    else: text+=" (Yazar, 2020, s.10)"
    return text

kw_model=None
def get_keybert_model():
    global kw_model
    if kw_model is None:
        try: kw_model=KeyBERT()
        except: kw_model=None
    return kw_model

def extract_keywords(text):
    model=get_keybert_model()
    if model is None: return ["model yüklenemedi"]
    try:
        kws=model.extract_keywords(text,top_n=5)
        return [k[0] for k in kws]
    except: return ["hata"]

def keyword_density(text,keywords):
    total=len(text.split())
    if total==0: return {}
    return {k: round(text.lower().count(k.lower())/total*100,2) for k in keywords}

def seo_score_details(text,density,readability):
    wc=len(text.split())
    avg_density=sum(density.values())/len(density) if density else 0
    details={}
    score=0
    if wc>800: details["Kelime Sayısı (>800)"]=35; score+=35
    elif wc>300: details["Kelime Sayısı (300-800)"]=20; score+=20
    else: details["Kelime Sayısı (<300)"]=0
    if 0.8<=avg_density<=2.5: details["Yoğunluk (0.8-2.5%)"]=35; score+=35
    elif 0.5<=avg_density<0.8 or 2.5<avg_density<=3.5: details["Yoğunluk (0.5-0.8 veya 2.5-3.5%)"]=15; score+=15
    else: details["Yoğunluk"]=0
    if readability>60: details["Okunabilirlik (>60)"]=25; score+=25
    elif readability>40: details["Okunabilirlik (40-60)"]=12; score+=12
    else: details["Okunabilirlik (<40)"]=0
    if regex.search(r'^#',text) or regex.search(r'^Başlık|^H1',text,regex.M): details["Başlık etiketi"]=5; score+=5
    else: details["Başlık etiketi"]=0
    return min(score,100), details

def serp_prediction(score):
    if score>80: return "🟢 1. Sayfa (Top 1-3)"
    elif score>60: return "🟡 1-2. Sayfa"
    else: return "🔴 3+ Sayfa"

def text_stats(text):
    words=text.split()
    wc=len(words)
    cc=len(text)
    sentences=regex.split(r'[.!?]+',text)
    sc=len([s for s in sentences if s.strip()])
    rt=round(wc/200,1)
    return {"Kelime":wc,"Karakter":cc,"Cümle":sc,"Okuma Süresi (dk)":rt}

def get_seo_guide_html(): return "<h1>SEO Rehberi</h1><p>Detaylı rehber...</p>"
def get_academic_guide_html(): return "<h1>Akademik Rehber</h1><p>Makale yazım kuralları...</p>"

def show_guide_dialog(title, html, parent=None):
    dlg = QDialog(parent)
    dlg.setWindowTitle(title)
    dlg.setMinimumSize(600, 400)
    # dlg.setStyleSheet(DARK_STYLE)  # KALDIRILDI
    layout = QVBoxLayout(dlg)
    label = QLabel(f"<b>{title}</b>")
    layout.addWidget(label)
    editor = QTextEdit()
    editor.setHtml(html)
    layout.addWidget(editor)
    btn_layout = QHBoxLayout()
    word_btn = QPushButton("📄 Word'den Şablon Ekle")
    word_btn.clicked.connect(lambda: load_word_into_editor(editor))
    btn_layout.addWidget(word_btn)
    btn_layout.addStretch()
    save_btn = QPushButton("💾 Kaydet")
    save_btn.clicked.connect(lambda: save_guide_content(editor, title))
    btn_layout.addWidget(save_btn)
    close_btn = QPushButton("Kapat")
    close_btn.clicked.connect(dlg.accept)
    btn_layout.addWidget(close_btn)
    layout.addLayout(btn_layout)
    dlg.exec_()

def load_word_into_editor(editor):
    file_path, _ = QFileDialog.getOpenFileName(None, "Word Şablonu Seç", "", "Word Belgeleri (*.docx)")
    if not file_path:
        return
    try:
        doc = docx.Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        if not paragraphs:
            QMessageBox.warning(None, "Uyarı", "Seçilen dosyada okunabilir metin bulunamadı.")
            return
        full_text = "\n".join(paragraphs)
        reply = QMessageBox.question(None, "İçerik Ekle",
                                     "Mevcut içeriği değiştirmek istiyor musunuz?\n(Evet: mevcut içerik silinir, Hayır: sona eklenir)",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            editor.setPlainText(full_text)
        elif reply == QMessageBox.No:
            editor.append(full_text)
    except Exception as e:
        QMessageBox.critical(None, "Hata", f"Dosya okunamadı:\n{str(e)}")

def save_guide_content(editor, title):
    content = editor.toHtml()
    file_path, _ = QFileDialog.getSaveFileName(None, "Rehberi Kaydet", "", "HTML Dosyası (*.html)")
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            QMessageBox.information(None, "Başarılı", "Rehber kaydedildi.")
        except Exception as e:
            QMessageBox.critical(None, "Hata", f"Kaydedilemedi: {str(e)}")

# ----------------------------------------------------------------------
# YKS Matematik Sistemi (Birim ve sabit desteği ile)
# ----------------------------------------------------------------------

GREEK_TO_SYMPY = {
    'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta', 'ε': 'epsilon',
    'ζ': 'zeta', 'η': 'eta', 'θ': 'theta', 'ι': 'iota', 'κ': 'kappa',
    'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi', 'ο': 'omicron',
    'π': 'pi', 'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon',
    'φ': 'phi', 'χ': 'chi', 'ψ': 'psi', 'ω': 'omega',
    'Α': 'Alpha', 'Β': 'Beta', 'Γ': 'Gamma', 'Δ': 'Delta', 'Ε': 'Epsilon',
    'Ζ': 'Zeta', 'Η': 'Eta', 'Θ': 'Theta', 'Ι': 'Iota', 'Κ': 'Kappa',
    'Λ': 'Lambda', 'Μ': 'Mu', 'Ν': 'Nu', 'Ξ': 'Xi', 'Ο': 'Omicron',
    'Π': 'Pi', 'Ρ': 'Rho', 'Σ': 'Sigma', 'Τ': 'Tau', 'Υ': 'Upsilon',
    'Φ': 'Phi', 'Χ': 'Chi', 'Ψ': 'Psi', 'Ω': 'Omega'
}

UNIT_SYMBOLS = {
    'm': m, 'kg': kg, 's': s, 'A': A, 'K': K, 'mol': mol, 'cd': cd,
    'km': km, 'cm': cm, 'mm': mm, 'μm': 1e-6*m, 'nm': 1e-9*m,
    'mile': 1609.34*m, 'inch': 0.0254*m, 'ft': 0.3048*m,
    'min': minute, 'hour': hour, 'day': day,
    'g': g, 'tonne': tonne, 'mg': 0.001*g,
    'N': N, 'J': J, 'W': W, 'Pa': Pa, 'V': V, 'Ohm': ohm, 'Hz': Hz, 'C': C, 'F': F, 'T': tesla,
}

PHYSICAL_CONSTANTS_UNITS = {
    'c':   ('c', speed_of_light),
    'G':   ('G', gravitational_constant),
    'h':   ('h', planck),
    'hbar':('ħ', planck/(2*pi)),
    'e_charge':('e', elementary_charge),
    'k':   ('k', boltzmann),
    'R':   ('R', gas_constant),
    'N_A': ('N_A', avogadro_number),
    'm_e': ('m_e', electron_rest_mass),
    'm_p': ('m_p', proton_rest_mass),
    'g':   ('g', 9.80665 * m/s**2),
    'mu0': ('μ₀', 4e-7 * pi * N/A**2),
    'epsilon0':('ε₀', 8.8541878128e-12 * F/m),
}

def convert_expr(expr):
    import re as regex_inner
    for gr, sym in GREEK_TO_SYMPY.items():
        expr = expr.replace(gr, sym)
    expr = expr.replace('ħ', 'hbar')
    expr = expr.replace('ℏ', 'hbar')
    expr = expr.replace('μ₀', 'mu0')
    expr = expr.replace('ε₀', 'epsilon0')
    expr = expr.replace("^", "**")
    expr = expr.replace("×", "*")
    expr = expr.replace("÷", "/")
    expr = expr.replace("√", "sqrt")
    expr = expr.replace("π", "pi")
    expr = regex_inner.sub(r'(\d)([a-zA-Zα-ωΑ-Ω])', r'\1*\2', expr)
    return expr

def expression_to_latex(expr_str):
    replacements = {
        'λ': '\\lambda', 'Λ': '\\Lambda',
        'α': '\\alpha', 'β': '\\beta', 'γ': '\\gamma', 'δ': '\\delta',
        'ε': '\\epsilon', 'ζ': '\\zeta', 'η': '\\eta', 'θ': '\\theta',
        'ι': '\\iota', 'κ': '\\kappa', 'μ': '\\mu', 'ν': '\\nu',
        'ξ': '\\xi', 'ο': '\\omicron', 'π': '\\pi', 'ρ': '\\rho',
        'σ': '\\sigma', 'τ': '\\tau', 'υ': '\\upsilon', 'φ': '\\phi',
        'χ': '\\chi', 'ψ': '\\psi', 'ω': '\\omega',
        'Φ': '\\Phi', 'Ψ': '\\Psi', 'Ω': '\\Omega', 'Δ': '\\Delta',
        'Γ': '\\Gamma', 'Θ': '\\Theta', 'Σ': '\\Sigma',
        '∫': '\\int', '∂': '\\partial', '∞': '\\infty',
        '≈': '\\approx', '≤': '\\le', '≥': '\\ge', '≠': '\\ne',
        '√': '\\sqrt', '×': '\\times', '⋅': '\\cdot',
        '∑': '\\sum', '∏': '\\prod',
        'μ₀': '\\mu_0', 'ε₀': '\\varepsilon_0',
        'ħ': '\\hbar', 'ℏ': '\\hbar'
    }
    for old, new in replacements.items():
        expr_str = expr_str.replace(old, new)
    expr_str = regex.sub(r'\^(\d+)', r'^{\1}', expr_str)
    expr_str = regex.sub(r'\^\{([^}]+)\}', r'^{\1}', expr_str)
    expr_str = regex.sub(r'\^([a-zA-Zα-ωΑ-Ω])', r'^{\1}', expr_str)
    expr_str = regex.sub(r'_(\d+)', r'_{\1}', expr_str)
    expr_str = regex.sub(r'_\{([^}]+)\}', r'_{\1}', expr_str)
    expr_str = regex.sub(r'_([a-zA-Zα-ωΑΩ])', r'_{\1}', expr_str)
    expr_str = regex.sub(r'√\{([^}]+)\}', r'\\sqrt{\1}', expr_str)
    expr_str = regex.sub(r'√([a-zA-Z0-9α-ωΑ-Ω])', r'\\sqrt{\1}', expr_str)
    expr_str = expr_str.replace('*', '')
    return expr_str

def render_math_as_image(expr_str):
    latex_expr = expression_to_latex(expr_str)
    full_latex = f"${latex_expr}$"
    try:
        fig = plt.figure(figsize=(6, 1.5))
        fig.patch.set_facecolor('none')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        ax.text(0.5, 0.5, full_latex, size=20, ha='center', va='center',
                transform=ax.transAxes, usetex=False)
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', pad_inches=0.1, transparent=True)
        plt.close(fig)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        return img_base64
    except Exception as e:
        print(f"Render hatası: {e}")
        return None

class NoteDialog(QDialog):
    def __init__(self, db: DatabaseManager, ders: str, konu: str, parent=None):
        super().__init__(parent)
        self.db = db
        self.ders = ders
        self.konu = konu
        self.setWindowTitle(f"📖 {ders} - {konu}")
        self.setMinimumSize(900, 700)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        layout = QVBoxLayout(self)
        toolbar = QHBoxLayout()
        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(self.change_font)
        toolbar.addWidget(QLabel("Yazı Tipi:"))
        toolbar.addWidget(self.font_combo)
        self.font_size = QComboBox()
        self.font_size.addItems([str(i) for i in range(8, 73, 2)])
        self.font_size.setCurrentText("10")
        self.font_size.currentTextChanged.connect(self.change_font_size)
        toolbar.addWidget(QLabel("Boyut:"))
        toolbar.addWidget(self.font_size)
        bold_btn = QPushButton("B")
        bold_btn.clicked.connect(lambda: self.editor.setFontWeight(QFont.Bold if self.editor.fontWeight() != QFont.Bold else QFont.Normal))
        toolbar.addWidget(bold_btn)
        italic_btn = QPushButton("I")
        italic_btn.clicked.connect(lambda: self.editor.setFontItalic(not self.editor.fontItalic()))
        toolbar.addWidget(italic_btn)
        underline_btn = QPushButton("U")
        underline_btn.clicked.connect(lambda: self.editor.setFontUnderline(not self.editor.fontUnderline()))
        toolbar.addWidget(underline_btn)
        color_btn = QPushButton("🎨 Renk")
        color_btn.clicked.connect(self.change_text_color)
        toolbar.addWidget(color_btn)
        img_btn = QPushButton("🖼️ Resim Ekle")
        img_btn.clicked.connect(self.insert_image)
        toolbar.addWidget(img_btn)
        img_effect_btn = QPushButton("🌈 Resim Efekti")
        img_effect_btn.clicked.connect(self.apply_image_effect)
        toolbar.addWidget(img_effect_btn)
        print_btn = QPushButton("🖨️ Yazdır")
        print_btn.clicked.connect(self.print_note)
        toolbar.addWidget(print_btn)
        pdf_btn = QPushButton("📄 PDF Olarak Kaydet")
        pdf_btn.clicked.connect(self.export_pdf)
        toolbar.addWidget(pdf_btn)
        word_btn = QPushButton("📝 Word Olarak Kaydet")
        word_btn.clicked.connect(self.export_word)
        toolbar.addWidget(word_btn)
        layout.addLayout(toolbar)
        self.editor = QTextEdit()
        layout.addWidget(self.editor)
        saved = db.get_study_note(ders, konu)
        if saved:
            self.editor.setHtml(saved)
        bottom_layout = QHBoxLayout()
        word_load_btn = QPushButton("📄 Word'den Yükle")
        word_load_btn.clicked.connect(self.load_word)
        bottom_layout.addWidget(word_load_btn)
        save_btn = QPushButton("💾 Kaydet")
        save_btn.clicked.connect(self.save_note)
        bottom_layout.addWidget(save_btn)
        close_btn = QPushButton("Kapat")
        close_btn.clicked.connect(self.accept)
        bottom_layout.addWidget(close_btn)
        layout.addLayout(bottom_layout)

    # ... diğer metodlar aynı ...
    def change_font(self, font):
        self.editor.setCurrentFont(font)
    def change_font_size(self, size):
        font = self.editor.currentFont()
        font.setPointSize(int(size))
        self.editor.setCurrentFont(font)
    def change_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.editor.setTextColor(color)
    def insert_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            with open(file_path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            ext = os.path.splitext(file_path)[1][1:].lower()
            if ext == 'jpg':
                ext = 'jpeg'
            html = f'<img src="data:image/{ext};base64,{data}" style="max-width: 100%; margin: 10px 0;" />'
            self.editor.textCursor().insertHtml(html)
    def apply_image_effect(self):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            QMessageBox.warning(self, "Uyarı", "Lütfen bir resim seçin (üzerine tıklayarak imleci resmin içine getirin).")
            return
        selected_html = cursor.selectedHtml()
        if '<img' not in selected_html:
            QMessageBox.warning(self, "Uyarı", "Seçili alan resim içermiyor.")
            return
        effects = ["Sepia", "Gri Ton", "Parlaklık +20%", "Kontrast +20%", "Renk Döndür (180°)"]
        effect, ok = QInputDialog.getItem(self, "Resim Efekti", "Efekt seçin:", effects, 0, False)
        if not ok:
            return
        filter_str = ""
        if effect == "Sepia":
            filter_str = "sepia(100%)"
        elif effect == "Gri Ton":
            filter_str = "grayscale(100%)"
        elif effect == "Parlaklık +20%":
            filter_str = "brightness(1.2)"
        elif effect == "Kontrast +20%":
            filter_str = "contrast(1.2)"
        elif effect == "Renk Döndür (180°)":
            filter_str = "hue-rotate(180deg)"
        new_html = selected_html.replace('<img', f'<img style="filter: {filter_str};"')
        cursor.insertHtml(new_html)
    def print_note(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.editor.document().print_(printer)
    def export_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "PDF Olarak Kaydet", "", "PDF Dosyası (*.pdf)")
        if file_path:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(file_path)
            self.editor.document().print_(printer)
            QMessageBox.information(self, "Başarılı", "PDF kaydedildi.")
    def export_word(self):
        import traceback
        try:
            base_dir = os.path.join(os.path.dirname(__file__), "ders_notları")
            os.makedirs(base_dir, exist_ok=True)
            ders_dir = os.path.join(base_dir, self.ders)
            os.makedirs(ders_dir, exist_ok=True)
            safe_konu = "".join(c for c in self.konu if c not in r'\/:*?"<>|')
            docx_path = os.path.join(ders_dir, f"{safe_konu}.docx")
            html_content = self.editor.toHtml()
            try:
                from html2docx import html2docx
                html2docx(html_content, docx_path)
                QMessageBox.information(self, "Başarılı", f"Word belgesi (biçimli) kaydedildi:\n{docx_path}")
            except ImportError:
                QMessageBox.warning(self, "Uyarı", 
                    "HTML'den Word'e dönüşüm için 'html2docx' kütüphanesi gerekli.\n"
                    "Kurmak için: pip install html2docx\n"
                    "Şimdilik düz metin olarak kaydediliyor.")
                doc = docx.Document()
                plain_text = self.editor.toPlainText()
                for line in plain_text.split('\n'):
                    doc.add_paragraph(line)
                doc.save(docx_path)
                QMessageBox.information(self, "Başarılı", f"Düz metin Word belgesi kaydedildi.\n{docx_path}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Kaydedilemedi: {str(e)}")
                try:
                    doc = docx.Document()
                    plain_text = self.editor.toPlainText()
                    for line in plain_text.split('\n'):
                        doc.add_paragraph(line)
                    doc.save(docx_path)
                    QMessageBox.information(self, "Başarılı", f"Düz metin Word belgesi kaydedildi (alternatif).\n{docx_path}")
                except Exception as e2:
                    QMessageBox.critical(self, "Hata", f"Alternatif kayıt da başarısız: {str(e2)}")
        except Exception as global_e:
            QMessageBox.critical(self, "Hata", f"Beklenmeyen hata: {str(global_e)}")
    def load_word(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Word Dosyası Seç", "", "Word Belgeleri (*.docx)")
        if not file_path:
            return
        try:
            doc = docx.Document(file_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            if not paragraphs:
                QMessageBox.warning(self, "Uyarı", "Okunabilir metin bulunamadı.")
                return
            content = "\n".join(paragraphs)
            reply = QMessageBox.question(self, "İçerik", "Mevcut içeriği değiştiriyim mi?\n(Evet: sil ve yükle, Hayır: sona ekle)",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.editor.setPlainText(content)
            elif reply == QMessageBox.No:
                self.editor.append(content)
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))
    def save_note(self):
        content = self.editor.toHtml()
        self.db.save_study_note(self.ders, self.konu, content)
        QMessageBox.information(self, "Başarılı", "Not kaydedildi.")
        if hasattr(self.parent(), 'refresh_notes_menu'):
            self.parent().refresh_notes_menu()

class YKSMath(QMainWindow):
    def __init__(self, main_app=None):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("YKS Matematik Sistemi")
        self.setGeometry(150, 150, 1100, 800)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        self.db = main_app.db if main_app else DatabaseManager()
        self.create_menus()
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        self.text = QTextEdit()
        self.text.setPlaceholderText("Örnek: λ = A^2 + ∫ -V * 1/2 + φ^-2 ≈")
        layout.addWidget(self.text)
        self.web = QWebEngineView()
        layout.addWidget(self.web)
        self.result = QLabel("Sonuç:")
        self.result.setStyleSheet("color:lime; font-size:18px;")
        layout.addWidget(self.result)
        if self.main_app is not None:
            send_btn = QPushButton("📤 Ana Editöre Gönder (Matematiksel Görsel Olarak)")
            send_btn.clicked.connect(self.send_to_main_editor)
            layout.addWidget(send_btn)
        self.text.textChanged.connect(self.render)
        self.render()

    def create_menus(self):
        menubar = self.menuBar()
        self.dersler = {
            "TYT Türkçe": ["Sözcükte Anlam","Söz Yorumu","Deyim ve Atasözü","Cümlede Anlam","Paragraf","Paragrafta Anlatım Teknikleri",
            "Paragrafta Düşünceyi Geliştirme Yolları","Paragrafta Yapı","Paragrafta Konu-Ana Düşünce","Paragrafta Yardımcı Düşünce",
            "Ses Bilgisi","Yazım Kuralları","Noktalama İşaretleri","Sözcükte Yapı/Ekler","Sözcük Türleri","İsimler","Zamirler",
            "Sıfatlar","Zarflar","Edat – Bağlaç – Ünlem","Fiiller","Fiilde Anlam (Kip-Kişi-Yapı)","Ek Fiil","Fiilimsi","Fiilde Çatı",
            "Sözcük Grupları","Cümlenin Ögeleri","Cümle Türleri","Anlatım Bozukluğu",
            ],
            "TYT Tarih": ["Tarih Bilimine Giriş","Uygarlığın Doğuşu ve İlk Uygarlıklar","İlk ve Orta Çağlarda Türk Dünyası",
            "İslam Medeniyetinin Doğuşu","Türk-İslam Devletleri (10-13. yüzyıllar)","Türkiye Tarihi (11-13. yüzyıllar)",
            "Beylikten Devlete (1300-1453)","Dünya Gücü Osmanlı Devleti (1453-1600)","Yeniçağ Avrupası (1453-1789)",
            "Osmanlı Kültür ve Medeniyeti","Arayış Yılları (17. yüzyıl)","18. Yüzyılda Değişim ve Diplomasi","Yakınçağ Avrupası (1789….)",
            "En Uzun Yüzyıl (1800-1922)","20. Yüzyıl Başlarında Osmanlı Devleti","1. Dünya Savaşı","Milli Mücadeleye Hazırlık Dönemi",
            "Kurtuluş Savaşında Cepheler","Türk İnkılabı","Atatürkçülük ve Atatürk İlkeleri","Türk Dış Politikası",
            ],
            "TYT Coğrafya":["Doğa ve İnsan","Dünya’nın Şekli ve Hareketleri","Coğrafi Konum","Harita Bilgisi","Atmosfer ve Sıcaklık",
            "İklimler","Basınç ve Rüzgarlar","Nem, Yağış ve Buharlaşma","İç Kuvvetler / Dış Kuvvetler","Su – Toprak ve Bitkiler",
            "Nüfus","Göç","Yerleşme","Türkiye’nin Yer Şekilleri","Ekonomik Faaliyetler","Bölgeler","Uluslararası Ulaşım Hatları",
            "Çevre ve Toplum","Doğal Afetler",
            ],
            "TYT Felsefe": ["Felsefenin Konusu","Bilgi Felsefesi","Varlık Felsefesi","Din, Kültür ve Medniyet","Ahlak Felsefesi",
            "Sanat Felsefesi","Din Felsefesi","Siyaset Felsefesi","Bilim Felsefesi",
            ],
            "TYT Din Kültürü":["İnanç","İbadet","Ahlak ve Değerler","Din, Kültür ve Medniyet","Hz. Mhammed (S.A.V.)","Vahiy ve Akıl",
            "Dünya ve Ahiret","Kur’an'a göre Hz. Muhammed (S.A.V.)","İnançla İlgili Meseleler","Yahudilik ve Hristiyanlık",
            "İslam ve Bilim","Anadolu da İslam","İslam Düşüncesinde Tasavvufi Yorumlar","Güncel Dini Meseler","Hint ve Çin Dinleri",
            ],
            "TYT Matematik": ["Sayılar","Sayı Basamakları","Bölme ve Bölünebilme","OBEB-OKEK","Rasyonel Sayılar",
            "Basit Eşitsizlikler","Mutlak Değer","Üslü Sayılar","Köklü Sayılar","Çarpanlara Ayırma","Oran Orantı",
            "Denklem Çözme","Problemler","Kümeler","Fonksiyonlar","Permütasyon","Kombinasyon","Binom","Olasılık",
            "İstatistik","2.Derece Denklemler",
            ],
            "TYT Geometri": ["Doğruda ve Üçgende Açılar","Dik Kenarda Trigonometrik Bağlantılar","İkizkenar ve Eşkenar Üçgen",
            "Üçgende Açıortay Bağlantıları","Kenarortay Bağıntıları","Eşlik ve Benzerlik","Açı-Kenar Bağıntıları",
            "Çokgenler","Dörtgenler","Yamuk","Paralelkenar","Eşkenar Dörtgen - Deltoid","Dikdörtgen","Çemberde Açı","Çemberde Uzunluk",
            ],
            "TYT Fizik": ["Fiziğin Tanımı ve Özellikleri", "Fiziğin Alt Dalları", "İş-Güç-Enerji","Mekanik Enerji","Enerjinin Korunumu ve Enerji Dönüşümleri",
            "Fiziğin Diğer Disiplinler ile İlişkisi", "Verim","Enerji Kaynakları","Isı ve Sıcaklık", "Hal Değişimi",
            "Fiziğin Bilim ve Araştırma Merkezleri", "Isıl Denge", "Enerji İletim Yolları ve Hızı","Genleşme",
            "Madde ve Özkütle", "Dayanıklılık", "Elektrik Yükü","Elektrikle Yüklenme Çeşitleri","Elektroskop",
            "Adezyon ve Kohezyon", "İletken ve Yalıtkanlarda Yük Dağılımı", "Topraklama", "Coulomb Kuvveti",
            "Hareket", "Düzlem Ayna","Kırılma","Mercekler","Prizmalar","Kuvvet","Newton'un Hareket Yasaları",
            "Sürtünme Kuvveti",
            ],
            "TYT Kimya": ["Kimyadan Simyaya,","Atom ve Yapısı","Periyodik Sistem","Kimyasal Türler Arası Etkileşim",
            "Asitler-Bazlar-Tuzlar","Bileşikler","Kimyasal Tepkimeler","Kimyanın Temel Yasaları","Maddenin Halleri",
            "Karışımlar","Endüstride ve Canlılarda Enerji","Kimya Her Yerde",
            ],
            "TYT Biyoloji": ["Biyoloji Bilimi","İnorganik Bileşikler","Organik Bileşikler","Hücre","Madde Geçişleri","DNA - RNA","Protein Sentezi",
            "Enzimler","Canlıların Sınıflandırılması","Ekoloji","Hücre Bölünmeleri","Eşeyli - Eşeysiz Üreme",
            ],
            "AYT Matematik": ["Karmaşık Sayılar","Parabol","Polinomlar","Temel Kavramlar","Sayı Basamakları",
            "Rasyonel Sayılar","Ondalıklı Sayılar","Basit Eşitsizlikler","Mutlak Değer","Üslü Sayılar","Köklü Sayılar",
            "Çarpanlara Ayırma","Denklem Çözme","Oran-Orantı","Problemler","Fonksiyonlar","Kümeler","Permütasyon",
            "Kombinasyon","Binom","Olasılık","İstatistik","2.Derece Denklemler","Karmaşık Sayılar","Mantık","Modüler Aritmatik",
            "Eşitsizlikler","Logaritma","Diziler","Seriler","Limit ve Süreklilik","Türev","İntegral",
            ],
            "AYT Geometri": ["Daire","Prizmalar","Piramitler","Küre","Koordinat ve Nokta Analitiği","Vektör-1","Doğru Analitiği",
            "Tekrar - Dönen - Yansıyan Şekiller","Uzay Geometri","Dönüşümlerle Geometri","Trigonometri","Genel Konik Tanımı",
            "Parabol","Elips","Hiperbol",
            ],
            "AYT Türk Dili ve Edebiyatı": ["Edebiyat Türleri", "Şiir Bilgisi", "Roman", "Hikaye", "Edebî Dönemler ve Akımlar", "Anlam Bilgisi", "Dil Bilgisi"],
            "AYT Biyoloji": ["AA"],
            "AYT Fizik": ["Kuvvet ve Hareket","Vektörler","Bağıl Hareket","Newton'un Hareket Yasaları",
            "Bir Boyutta Sabit İvmeli Hareket","İki Boyutta Sabit İvmeli Hareket","Enerji ve Hareket",
            "İtme ve Çizgisel Momentum","Tork","Denge","Basit Makineler","Elektrik Kuvvet ve Elektrik Alan",
            "Düzgün Elektrik Alanı ve Sığa","Manyetizma ve Elektromanyetik İndükleme","Alternatif Akım",
            "Transformatörler","Düzgün Çembersel Hareket","Dönerek Öteleme Hareketi","Açısal Momentum",
            "Kütle Çekim ve Kepler Kanunu","Basit Harmonik Hareket","Dalgalarda Kırınım,Girişim ve Doppler Olayı",
            "Elektromanyetik Dalgalar","Atom Kavramının Tarihsel Gelişimi","Büyük Patlama ve Evrenin Oluşumu",
            "Elektrik Alanı","Elektrik Akımı, Potansiyel Farkı ve Direnci","Elektrik Devreleri","Mıknatıs ve Manyetik Alan",
            "Akım ve Manyetik Alan","Basınç","Kaldırma Kuvveti","Dalgalar","Aydınlanma","Modern Fizik",
            ],
            "AYT Kimya": ["Modern Atom Teorisi","Kimyasal Hesaplamalar","Gazlar","Sıvı Çözeltiler",
            "Kimya ve Enerji","Tepkimelerde Hız","Kimyasal Denge","Sıvı Çözeltilerde Denge","Kimya ve Elektrik",
            "Karbon Kimyasına Giriş","Organik Kimya","Hayatımız Kimya",
            ],
            "AYT Tarih": [],
            "AYT Felsefe Grubu": [],
            "AYT Coğrafya": [],
            "DGS Türkçe": [],
            "DGS Sözel Mantık": [],
            "DGS Matematik": [],
            "DGS Sayısal Mantık": [],
            "KPSS Türkçe": [],
            "KPSS Tarih":[],
            "KPSS Coğrafya":[],
            "KPSS Vatandaşlık":[],
            "KPSS Matematik":[],
            "KPSS Geometri ve Analitik Geometri": [],
            "LVS - Laborant ve Veteriner Sağlık":["Atatürk İlkeleri ve İnkılap Tarihi I  (ATATÜRK'S PRINCIPLES AND THE HISTORY OF HIS REFORMS I)",
            "Türk Dili I  (TURKISH LANGUAGE I )","Temel Yabancı Dil I (İngilizce) (BASIC FOREIGN LANGUAGE I) ((English)",
            "Fizyoloji PHYSIOLOGY ","Biyokimya BIOCHEMISTRY ","Histoloji ve Embriyoloji HISTOLOGY AND EMBRYOLOGY ",
            "Anatomi ANATOMY","Tıbbi Laboratuvar Tekniği MEDICAL LABORATORY TECHNIQUE","Genel Mikrobiyoloji GENERAL MICROBIOLOGY",
            "Bilgi Ve İletişim Teknolojileri I (INFORMATION AND COMMUNICATION TECHNOLOGIES I)",
            ],
            "ANAAOF - Engelli Bakımı ve Rehabilitasyon":[],
            "Almanca": [],
            "İspanyolca": [],
            "İngilizce": [],
            "Rusça": []
        }

        tyt_menu = menubar.addMenu("TYT Dersleri")
        ayt_menu = menubar.addMenu("AYT Dersleri")
        dgs_menu = menubar.addMenu("DGS Dersleri")
        kpss_menu = menubar.addMenu("KPSS Dersleri")
        universities_menu = menubar.addMenu("Okuduğum Üniversitelerin Dersleri")
        other_menu = menubar.addMenu("Dil Dersleri")

        for ders, konular in self.dersler.items():
            if ders.startswith("TYT"):
                parent = tyt_menu
            elif ders.startswith("AYT"):
                parent = ayt_menu
            elif ders.startswith("DGS"):
                parent = dgs_menu
            elif ders.startswith("KPSS"):
                parent = kpss_menu
            elif ders.startswith("LVS"):
                parent = universities_menu
            elif ders.startswith("ANAAOF"):
                parent = universities_menu
            else:
                parent = other_menu
            ders_menu = parent.addMenu(ders)
            for konu in konular:
                action = QAction(konu, self)
                action.triggered.connect(lambda checked, d=ders, k=konu: self.open_note(d, k))
                ders_menu.addAction(action)

        self.notes_menu = menubar.addMenu("Popüler Ders Notlarım")
        self.notes_menu.aboutToShow.connect(self.populate_notes_menu)

        klavye_menu = menubar.addMenu("Matematik Klavyesi")
        sembol_menu = klavye_menu.addMenu("🔣 Semboller")
        semboller = ["x","y","z","a","b","c","d","+","-","*","/","=","(",")","^","√","∞","≤","≥","≠","≈","∫","∂","Σ","Π","Δ","Ω"]
        kisayollar = {
            "x": "Ctrl+Shift+X", "y": "Ctrl+Shift+Y", "z": "Ctrl+Shift+Z",
            "a": "Ctrl+Shift+A", "b": "Ctrl+Shift+B", "c": "Ctrl+Shift+C",
            "d": "Ctrl+Shift+D", "+": "Ctrl+Shift+Plus", "-": "Ctrl+Shift+Minus",
            "*": "Ctrl+Shift+8", "/": "Ctrl+Shift+Slash", "=": "Ctrl+Shift+Equal"
        }
        for sym in semboller:
            act = QAction(sym, self)
            if sym in kisayollar:
                act.setShortcut(QKeySequence(kisayollar[sym]))
            act.triggered.connect(lambda checked, val=sym: self.insert_text(val))
            sembol_menu.addAction(act)

        yunan_menu = klavye_menu.addMenu("🇬🇷 Yunan Harfleri")
        yunanlar = ["α","β","γ","δ","ε","θ","λ","μ","π","ρ","σ","τ","φ","ω"]
        for sym in yunanlar:
            act = QAction(sym, self)
            if sym == "π":
                act.setShortcut(QKeySequence("Ctrl+Shift+P"))
            act.triggered.connect(lambda checked, val=sym: self.insert_text(val))
            yunan_menu.addAction(act)

        sabit_menu = klavye_menu.addMenu("⚛️ Sabitler")
        sabitler = ["π","e","i","c","G","h","ħ","g","k","R","N_A","μ₀","ε₀"]
        sabit_kisayollar = {
            "π": "Ctrl+Shift+P", "e": "Ctrl+Shift+E", "i": "Ctrl+Shift+I",
            "c": "Ctrl+Alt+C", "G": "Ctrl+Alt+G", "h": "Ctrl+Alt+H"
        }
        for sym in sabitler:
            act = QAction(sym, self)
            if sym in sabit_kisayollar:
                act.setShortcut(QKeySequence(sabit_kisayollar[sym]))
            act.triggered.connect(lambda checked, val=sym: self.insert_text(val))
            sabit_menu.addAction(act)

        birim_menu = klavye_menu.addMenu("📏 Birimler")
        birimler = ["m","kg","s","N","J","W","Pa","V","Ohm","Hz","C","F","T"]
        birim_kisayollar = {"m":"Ctrl+Alt+M", "kg":"Ctrl+Alt+K", "s":"Ctrl+Alt+S"}
        for sym in birimler:
            act = QAction(sym, self)
            if sym in birim_kisayollar:
                act.setShortcut(QKeySequence(birim_kisayollar[sym]))
            act.triggered.connect(lambda checked, val=sym: self.insert_text(val))
            birim_menu.addAction(act)

        islemler_menu = menubar.addMenu("Matematik İşlemleri")

        cebir_menu = islemler_menu.addMenu("📐 Cebir")
        solve_action = QAction("Denklem Çöz\tCtrl+E", self)
        solve_action.setShortcut(QKeySequence("Ctrl+E"))
        solve_action.triggered.connect(self.solve)
        cebir_menu.addAction(solve_action)

        simplify_action = QAction("Sadeleştir\tCtrl+Shift+S", self)
        simplify_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        simplify_action.triggered.connect(self.simplify_expr)
        cebir_menu.addAction(simplify_action)

        factor_action = QAction("Çarpanlara Ayır\tCtrl+Shift+F", self)
        factor_action.setShortcut(QKeySequence("Ctrl+Shift+F"))
        factor_action.triggered.connect(self.factor_expr)
        cebir_menu.addAction(factor_action)

        evaluate_action = QAction("Sayısal Değerlendir\tCtrl+Shift+D", self)
        evaluate_action.setShortcut(QKeySequence("Ctrl+Shift+D"))
        evaluate_action.triggered.connect(self.evaluate_numeric)
        cebir_menu.addAction(evaluate_action)

        analiz_menu = islemler_menu.addMenu("📈 Analiz")
        derivative_action = QAction("Türev Al\tCtrl+T", self)
        derivative_action.setShortcut(QKeySequence("Ctrl+T"))
        derivative_action.triggered.connect(self.derivative)
        analiz_menu.addAction(derivative_action)

        integral_action = QAction("İntegral Al\tCtrl+I", self)
        integral_action.setShortcut(QKeySequence("Ctrl+I"))
        integral_action.triggered.connect(self.integral)
        analiz_menu.addAction(integral_action)

        limit_action = QAction("Limit Hesapla\tCtrl+L", self)
        limit_action.setShortcut(QKeySequence("Ctrl+L"))
        limit_action.triggered.connect(self.limit_calc)
        analiz_menu.addAction(limit_action)

        plot_action = QAction("Grafik Çiz\tCtrl+G", self)
        plot_action.setShortcut(QKeySequence("Ctrl+G"))
        plot_action.triggered.connect(self.plot_graph)
        analiz_menu.addAction(plot_action)

        lineer_menu = islemler_menu.addMenu("🔢 Lineer Cebir")
        det_action = QAction("Determinant\tCtrl+Alt+D", self)
        det_action.setShortcut(QKeySequence("Ctrl+Alt+D"))
        det_action.triggered.connect(self.matrix_det)
        lineer_menu.addAction(det_action)

        inv_action = QAction("Ters Matris\tCtrl+Alt+M", self)
        inv_action.setShortcut(QKeySequence("Ctrl+Alt+M"))
        inv_action.triggered.connect(self.matrix_inv)
        lineer_menu.addAction(inv_action)

        komb_menu = islemler_menu.addMenu("🎲 Kombinatorik")
        perm_action = QAction("Permütasyon\tCtrl+P", self)
        perm_action.setShortcut(QKeySequence("Ctrl+P"))
        perm_action.triggered.connect(self.permutation)
        komb_menu.addAction(perm_action)

        comb_action = QAction("Kombinasyon\tCtrl+K", self)
        comb_action.setShortcut(QKeySequence("Ctrl+K"))
        comb_action.triggered.connect(self.combination)
        komb_menu.addAction(comb_action)

        unit_action = QAction("📏 Birim Dönüştür\tCtrl+U", self)
        unit_action.setShortcut(QKeySequence("Ctrl+U"))
        unit_action.triggered.connect(self.convert_unit)
        islemler_menu.addAction(unit_action)

    def open_note(self, ders, konu):
        dlg = NoteDialog(self.db, ders, konu, self)
        dlg.exec_()
    def insert_text(self, t):
        self.text.textCursor().insertText(t)
    def get_expr(self):
        expr_str = self.text.toPlainText()
        expr_str = convert_expr(expr_str)
        local_dict = {}
        for gr, sym in GREEK_TO_SYMPY.items():
            local_dict[sym] = symbols(sym)
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            if letter not in local_dict:
                local_dict[letter] = symbols(letter)
        for unit_name, unit_obj in UNIT_SYMBOLS.items():
            local_dict[unit_name] = unit_obj
        for name, (_, unit_obj) in PHYSICAL_CONSTANTS_UNITS.items():
            local_dict[name] = unit_obj
        user_consts = self.db.get_all_user_constants()
        for name, expr_val, unit in user_consts:
            try:
                val = sympify(expr_val)
                if unit:
                    unit_obj = UNIT_SYMBOLS.get(unit, None)
                    if unit_obj:
                        val = val * unit_obj
                local_dict[name] = val
            except:
                pass
        local_dict['pi'] = pi
        local_dict['e'] = E
        local_dict['i'] = I
        try:
            return parse_expr(expr_str, local_dict=local_dict)
        except:
            return sympify(expr_str, locals=local_dict)
    def render(self):
        content = self.text.toPlainText()
        latex = expression_to_latex(content)
        html = f"""
        <html>
        <head>
        <script src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'></script>
        </head>
        <body style='background:#111;color:white;font-size:26px;'>
        $$ {latex} $$
        </body>
        </html>
        """
        self.web.setHtml(html)
    def solve(self):
        try:
            expr = self.text.toPlainText()
            if "=" in expr:
                l, r = expr.split("=", 1)
                lhs = sympify(convert_expr(l))
                rhs = sympify(convert_expr(r))
                eq = Eq(lhs, rhs)
                syms = list(eq.free_symbols)
                if not syms:
                    self.result.setText("Denklemde değişken yok.")
                    return
                var = syms[0]
                sol = solve(eq, var)
                numeric_sol = []
                for s in sol:
                    try:
                        numeric_sol.append(N(s))
                    except:
                        numeric_sol.append(s)
                self.result.setText(f"Çözüm ({var}): {numeric_sol}")
            else:
                val = N(self.get_expr())
                self.result.setText(f"Sayısal değer ≈ {val}")
        except Exception as e:
            self.result.setText(f"Hata: {str(e)}")
    def simplify_expr(self):
        try:
            expr = self.get_expr()
            self.result.setText(f"Sade: {simplify(expr)}")
        except Exception as e:
            self.result.setText(str(e))
    def factor_expr(self):
        try:
            expr = self.get_expr()
            self.result.setText(f"Çarpan: {factor(expr)}")
        except Exception as e:
            self.result.setText(str(e))
    def derivative(self):
        try:
            x = symbols('x')
            expr = self.get_expr()
            self.result.setText(f"Türev: {diff(expr, x)}")
        except Exception as e:
            self.result.setText(str(e))
    def integral(self):
        try:
            x = symbols('x')
            expr = self.get_expr()
            self.result.setText(f"İntegral: {integrate(expr, x)}")
        except Exception as e:
            self.result.setText(str(e))
    def limit_calc(self):
        try:
            x = symbols('x')
            expr = self.get_expr()
            lim = limit(expr, x, 0)
            self.result.setText(f"Limit (x→0): {lim}")
        except Exception as e:
            self.result.setText(str(e))
    def plot_graph(self):
        try:
            x = symbols('x')
            expr = self.get_expr()
            f = lambdify(x, expr, 'numpy')
            xs = np.linspace(-10, 10, 200)
            ys = f(xs)
            plt.figure()
            plt.plot(xs, ys)
            plt.title("Grafik")
            plt.show()
        except Exception as e:
            self.result.setText(str(e))
    def evaluate_numeric(self):
        try:
            expr = self.get_expr()
            val = N(expr)
            self.result.setText(f"≈ {val}")
        except Exception as e:
            self.result.setText(str(e))
    def convert_unit(self):
        try:
            expr = self.get_expr()
            target, ok = QInputDialog.getItem(self, "Birim Dönüşümü", "Hedef birim:", list(UNIT_SYMBOLS.keys()), 0, False)
            if ok and target in UNIT_SYMBOLS:
                converted = convert_to(expr, UNIT_SYMBOLS[target])
                self.result.setText(f"{expr} = {converted}")
            else:
                si_units = (m, kg, s, A, K, mol, cd)
                converted = convert_to(expr, si_units)
                self.result.setText(f"SI biriminde: {converted}")
        except Exception as e:
            self.result.setText(str(e))
    def permutation(self):
        try:
            text = self.text.toPlainText()
            n_val, r_val = map(int, text.split(","))
            result = factorial(n_val) / factorial(n_val - r_val)
            self.result.setText(f"P({n_val},{r_val}) = {result}")
        except:
            self.result.setText("Format: n,r")
    def combination(self):
        try:
            text = self.text.toPlainText()
            n_val, r_val = map(int, text.split(","))
            result = factorial(n_val) / (factorial(r_val) * factorial(n_val - r_val))
            self.result.setText(f"C({n_val},{r_val}) = {result}")
        except:
            self.result.setText("Format: n,r")
    def matrix_det(self):
        try:
            expr = self.get_expr()
            if isinstance(expr, MatrixBase):
                self.result.setText(f"Determinant: {expr.det()}")
            else:
                self.result.setText("Lütfen matris girin (ör: [[1,2],[3,4]])")
        except Exception as e:
            self.result.setText(str(e))
    def matrix_inv(self):
        try:
            expr = self.get_expr()
            if isinstance(expr, MatrixBase):
                if expr.det() == 0:
                    self.result.setText("Matrisin tersi yok (determinant=0)")
                else:
                    self.result.setText(f"Ters matris: {expr.inv()}")
            else:
                self.result.setText("Lütfen matris girin (ör: [[1,2],[3,4]])")
        except Exception as e:
            self.result.setText(str(e))
    def send_to_main_editor(self):
        expr = self.text.toPlainText().strip()
        if not expr:
            QMessageBox.warning(self, "Uyarı", "Gönderilecek matematik ifadesi yok.")
            return
        img_base64 = render_math_as_image(expr)
        if img_base64 is None:
            QMessageBox.warning(self, "Hata", "Matematik ifadesi görsel olarak oluşturulamadı.\nDüz metin olarak gönderiliyor.")
            self.main_app.editor.insertPlainText(expr)
        else:
            html_img = f'<img src="data:image/png;base64,{img_base64}" alt="{expr}" style="max-width:100%; margin:10px 0;">'
            self.main_app.editor.insertHtml(html_img)
            QMessageBox.information(self, "Gönderildi", "Matematik ifadesi görsel olarak ana editöre eklendi.")
    def populate_notes_menu(self):
        self.notes_menu.clear()
        notes = self.db.get_all_study_notes()
        if not notes:
            empty_action = QAction("Henüz kayıtlı not yok", self)
            empty_action.setEnabled(False)
            self.notes_menu.addAction(empty_action)
            return
        ders_dict = {}
        for ders, konu in notes:
            ders_dict.setdefault(ders, []).append(konu)
        for ders, konular in sorted(ders_dict.items()):
            ders_menu = self.notes_menu.addMenu(ders)
            for konu in sorted(konular):
                action = QAction(konu, self)
                action.triggered.connect(lambda checked, d=ders, k=konu: self.open_saved_note(d, k))
                ders_menu.addAction(action)
    def open_saved_note(self, ders, konu):
        dlg = NoteDialog(self.db, ders, konu, self)
        dlg.finished.connect(self.refresh_notes_menu)
        dlg.exec_()
    def refresh_notes_menu(self):
        if hasattr(self, 'notes_menu'):
            self.populate_notes_menu()

# ----------------------------------------------------------------------
# Bul ve Değiştir Diyaloğu
# ----------------------------------------------------------------------
class FindReplaceDialog(QDialog):
    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setWindowTitle("Bul ve Değiştir")
        self.setMinimumWidth(400)
        # self.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Bul:"))
        self.find_edit = QLineEdit()
        layout.addWidget(self.find_edit)
        layout.addWidget(QLabel("Değiştir:"))
        self.replace_edit = QLineEdit()
        layout.addWidget(self.replace_edit)
        btn_layout = QHBoxLayout()
        find_btn = QPushButton("🔍 Bul")
        find_btn.clicked.connect(self.find)
        replace_btn = QPushButton("📝 Değiştir")
        replace_btn.clicked.connect(self.replace)
        replace_all_btn = QPushButton("⚡ Tümünü Değiştir")
        replace_all_btn.clicked.connect(self.replace_all)
        btn_layout.addWidget(find_btn)
        btn_layout.addWidget(replace_btn)
        btn_layout.addWidget(replace_all_btn)
        layout.addLayout(btn_layout)
        close_btn = QPushButton("Kapat")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def find(self):
        from PyQt5.QtGui import QTextDocument
        text = self.find_edit.text()
        if text:
            flags = QTextDocument.FindFlags()
            cursor = self.editor.textCursor()
            if not cursor.selectedText() or cursor.selectedText() != text:
                cursor = self.editor.document().find(text, 0, flags)
            else:
                cursor = self.editor.document().find(text, cursor, flags)
            if not cursor.isNull():
                self.editor.setTextCursor(cursor)
            else:
                QMessageBox.information(self, "Bilgi", "Metin bulunamadı")
    def replace(self):
        if self.editor.textCursor().hasSelection():
            self.editor.textCursor().insertText(self.replace_edit.text())
    def replace_all(self):
        search_text = self.find_edit.text()
        replace_text = self.replace_edit.text()
        if not search_text:
            return
        from PyQt5.QtGui import QTextCursor
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        self.editor.moveCursor(QTextCursor.Start)
        count = 0
        while self.editor.find(search_text):
            self.editor.textCursor().insertText(replace_text)
            count += 1
        cursor.endEditBlock()
        QMessageBox.information(self, "Tamam", f"{count} değişiklik yapıldı")

# ----------------------------------------------------------------------
# Ana Uygulama
# ----------------------------------------------------------------------
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SEO + Akademik Editör Pro")
        self.setGeometry(200,200,1300,800)
        # self.setStyleSheet(DARK_STYLE)  # Başlangıçta tema uygulanacak, bu satırı kaldır
        self.db = DatabaseManager()
        self.dict_db = DictionaryDB()
        self.user_manager = UserManager()
        self.edit_mode = False
        self.editing_post_id = None
        self.word_template_type = None
        self.current_theme = "dark"
        self.academic_format = "APA"
        self.use_ollama = True
        self.create_menu()
        self.setup_ui()
        self.create_toolbar()
        self.create_format_toolbar()
        self.model_config = load_model_config()
        QMessageBox.information(self, "Bilgi", f"KeyBERT hazırlanıyor.\nAkademik: {self.model_config.get('academic')}\nSEO: {self.model_config.get('seo')}\nStandart: {self.model_config.get('standard')}")
        self.check_ollama()
        self.setup_shortcuts()
        self.start_autosave()
        self.restore_geometry()

        self.statusBar().showMessage("Hazır")
        self.word_count_label = QLabel("0 kelime")
        self.char_count_label = QLabel("0 karakter")
        self.statusBar().addPermanentWidget(self.word_count_label)
        self.statusBar().addPermanentWidget(self.char_count_label)
        self.editor.textChanged.connect(self.update_word_count)
        self.update_word_count()

        if os.path.exists("theme_config.json"):
            with open("theme_config.json", "r") as f:
                cfg = json.load(f)
                self.set_theme(cfg.get("theme", "dark"))
        else:
            self.set_theme("dark")

    def update_word_count(self):
        text = self.editor.toPlainText()
        words = len(text.split())
        chars = len(text)
        self.word_count_label.setText(f"{words} kelime")
        self.char_count_label.setText(f"{chars} karakter")
        return words

    def restore_geometry(self):
        if os.path.exists("window_geometry.json"):
            try:
                with open("window_geometry.json", "r") as f:
                    geo = json.load(f)
                    geom = base64.b64decode(geo.get("geometry", ""))
                    state = base64.b64decode(geo.get("state", ""))
                    self.restoreGeometry(geom)
                    self.restoreState(state)
            except:
                pass

    def save_geometry(self):
        geom_bytes = self.saveGeometry()
        state_bytes = self.saveState()
        with open("window_geometry.json", "w") as f:
            json.dump({
                "geometry": base64.b64encode(geom_bytes).decode('ascii'),
                "state": base64.b64encode(state_bytes).decode('ascii')
            }, f)

    def closeEvent(self, event):
        self.save_geometry()
        event.accept()

    def set_theme(self, theme_name):
        if theme_name == "dark":
            style = DARK_STYLE
            self.current_theme = "dark"
        elif theme_name == "light":
            style = LIGHT_STYLE
            self.current_theme = "light"
        else:
            return
        QApplication.instance().setStyleSheet(style)
        with open("theme_config.json", "w") as f:
            json.dump({"theme": theme_name}, f)
        self.statusBar().showMessage(f"{theme_name} tema aktif", 2000)

    def setup_shortcuts(self):
        new_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        new_shortcut.activated.connect(self.new_file)
        open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        open_shortcut.activated.connect(self.open_file)
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save_file)
        saveas_shortcut = QShortcut(QKeySequence("Ctrl+Shift+S"), self)
        saveas_shortcut.activated.connect(lambda: self.save_file(force_dialog=True))
        f5_shortcut = QShortcut(QKeySequence("F5"), self)
        f5_shortcut.activated.connect(self.analyze)
        find_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        find_shortcut.activated.connect(lambda: FindReplaceDialog(self.editor, self).exec_())
        zoom_in = QShortcut(QKeySequence("Ctrl+="), self)
        zoom_in.activated.connect(self.zoom_in)
        zoom_out = QShortcut(QKeySequence("Ctrl+-"), self)
        zoom_out.activated.connect(self.zoom_out)

    def zoom_in(self):
        font = self.editor.font()
        font.setPointSize(font.pointSize() + 1)
        self.editor.setFont(font)
        self.statusBar().showMessage(f"Yazı boyutu: {font.pointSize()}", 1500)

    def zoom_out(self):
        font = self.editor.font()
        if font.pointSize() > 6:
            font.setPointSize(font.pointSize() - 1)
            self.editor.setFont(font)
            self.statusBar().showMessage(f"Yazı boyutu: {font.pointSize()}", 1500)

    def start_autosave(self):
        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(60000)  # 60 saniye

    def autosave(self):
        content = self.editor.toPlainText()
        if content.strip():
            with open("autosave_backup.txt", "w", encoding="utf-8") as f:
                f.write(content)
            self.statusBar().showMessage("Otomatik yedeklendi", 2000)

    def check_ollama(self):
        try:
            ollama.list()
            self.ollama_available = True
        except:
            self.ollama_available = False
            QMessageBox.warning(self, "Uyarı", "Ollama çalışmıyor.")

    def setup_ui(self):
        container = QWidget()
        self.setCentralWidget(container)
        main_layout = QVBoxLayout(container)
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.main_tab = QWidget()
        main_tab_layout = QHBoxLayout(self.main_tab)
        left = QWidget()
        self.left_layout = QVBoxLayout(left)
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Metin girin...")
        self.left_layout.addWidget(QLabel("📝 Metin Düzenleyici"))
        self.left_layout.addWidget(self.editor)

        template_group = QGroupBox("Şablonlar")
        t_layout = QHBoxLayout()
        self.cb_seo = QCheckBox("SEO Makalesi")
        self.cb_academic = QCheckBox("Akademik Makale")
        self.cb_blog = QCheckBox("Blog Yazısı")
        self.cb_product = QCheckBox("Ürün Tanıtımı")
        for cb in (self.cb_seo, self.cb_academic, self.cb_blog, self.cb_product):
            t_layout.addWidget(cb)
        template_group.setLayout(t_layout)
        self.left_layout.addWidget(template_group)

        self.right_tabs = QTabWidget()
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)
        self.right_tabs.addTab(self.result_edit, "📊 Analiz")
        self.html_preview = QWebEngineView()
        self.right_tabs.addTab(self.html_preview, "📄 Önizleme")
        stats = QGroupBox("Metin İstatistikleri")
        s_layout = QVBoxLayout()
        self.stats_label = QLabel("Henüz analiz yok.")
        self.stats_label.setWordWrap(True)
        s_layout.addWidget(self.stats_label)
        stats.setLayout(s_layout)
        self.right_tabs.addTab(stats, "📈 İstatistik")
        seo = QGroupBox("SEO Skor Detayı")
        sd_layout = QVBoxLayout()
        self.seo_details_label = QLabel("-")
        self.seo_details_label.setWordWrap(True)
        sd_layout.addWidget(self.seo_details_label)
        self.seo_progress = QProgressBar()
        self.seo_progress.setRange(0, 100)
        sd_layout.addWidget(QLabel("SEO Skoru"))
        sd_layout.addWidget(self.seo_progress)
        seo.setLayout(sd_layout)
        self.right_tabs.addTab(seo, "🔎 SEO")
        ai = QGroupBox("🤖 Yapay Zeka Derin Düzeltme")
        ai_layout = QVBoxLayout()
        self.deep_btn = QPushButton("🎯 AI ile Düzelt")
        self.deep_btn.clicked.connect(self.start_deep_correction)
        ai_layout.addWidget(self.deep_btn)
        ai.setLayout(ai_layout)
        self.right_tabs.addTab(ai, "🤖 AI Düzeltme")
        main_tab_layout.addWidget(left, 2)
        main_tab_layout.addWidget(self.right_tabs, 1)
        self.tabs.addTab(self.main_tab, "📝 Ana Editör")
        self.math_widget = YKSMath(main_app=self)
        self.tabs.addTab(self.math_widget, "📐 Ders Notlarım")
        self.academic_dialog = AcademicEditorDialog(self)
        self.academic_dialog.setParent(self)
        self.academic_dialog.setWindowFlags(Qt.Widget)
        self.academic_dialog.setVisible(True)
        self.tabs.addTab(self.academic_dialog, "🎓 Akademik Editör")
        self.editor.textChanged.connect(self.update_html_preview)

    def update_html_preview(self):
        html_content = self.editor.toHtml()
        styled_html = f"""
        <html>
        <head>
        <style>
            body {{
                background-color: #1e1e1e;
                color: #dcdcdc;
                font-family: 'Segoe UI', 'Consolas', monospace;
                padding: 20px;
            }}
            img {{ max-width: 100%; }}
        </style>
        </head>
        <body>
        {html_content}
        </body>
        </html>
        """
        self.html_preview.setHtml(styled_html)

    def create_format_toolbar(self):
        tb = QToolBar("Biçimlendirme")
        self.addToolBar(tb)
        bold = QPushButton("B")
        bold.clicked.connect(lambda: self.editor.setFontWeight(QFont.Bold if self.editor.fontWeight() != QFont.Bold else QFont.Normal))
        tb.addWidget(bold)
        italic = QPushButton("I")
        italic.clicked.connect(lambda: self.editor.setFontItalic(not self.editor.fontItalic()))
        tb.addWidget(italic)
        under = QPushButton("U")
        under.clicked.connect(lambda: self.editor.setFontUnderline(not self.editor.fontUnderline()))
        tb.addWidget(under)
        sup_btn = QPushButton("X²")
        sup_btn.clicked.connect(self.insert_superscript)
        tb.addWidget(sup_btn)
        sub_btn = QPushButton("X₂")
        sub_btn.clicked.connect(self.insert_subscript)
        tb.addWidget(sub_btn)
        math_btn = QPushButton("∑")
        math_btn.clicked.connect(self.insert_math_expression)
        tb.addWidget(math_btn)
        color = QPushButton("🎨 Renk")
        color.clicked.connect(self.change_text_color)
        tb.addWidget(color)
        img = QPushButton("🖼️ Resim")
        img.clicked.connect(self.insert_image_base64)
        tb.addWidget(img)
        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(lambda f: self.editor.setCurrentFont(f))
        tb.addWidget(QLabel("Font:"))
        tb.addWidget(self.font_combo)
        self.font_size = QComboBox()
        self.font_size.addItems([str(i) for i in range(8, 73, 2)])
        self.font_size.setCurrentText("10")
        self.font_size.currentTextChanged.connect(self.change_font_size)
        tb.addWidget(QLabel("Boyut:"))
        tb.addWidget(self.font_size)
        inc = QPushButton("A+")
        inc.clicked.connect(self.increase_font_size)
        dec = QPushButton("A-")
        dec.clicked.connect(self.decrease_font_size)
        tb.addWidget(inc)
        tb.addWidget(dec)

    def insert_superscript(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            cursor.insertHtml(f"<sup>{selected_text}</sup>")
        else:
            text, ok = QInputDialog.getText(self, "Üst Simge", "Üst simge olarak eklenecek metni girin:")
            if ok and text:
                self.editor.textCursor().insertHtml(f"<sup>{text}</sup>")

    def insert_subscript(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            cursor.insertHtml(f"<sub>{selected_text}</sub>")
        else:
            text, ok = QInputDialog.getText(self, "Alt Simge", "Alt simge olarak eklenecek metni girin:")
            if ok and text:
                self.editor.textCursor().insertHtml(f"<sub>{text}</sub>")

    def insert_math_expression(self):
        cursor = self.editor.textCursor()
        base_char = ""
        if cursor.hasSelection():
            base_char = cursor.selectedText()
        else:
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)
            base_char = cursor.selectedText()
            if not base_char:
                QMessageBox.warning(self, "Uyarı", "Lütfen bir karakter seçin veya imleci karakterin hemen yanına getirin.")
                return
        dialog = QDialog(self)
        dialog.setWindowTitle("Matematiksel Dört Köşe İfadesi")
        # dialog.setStyleSheet(DARK_STYLE)  # KALDIRILDI
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel(f"Taban karakter: <b>{base_char}</b>"))
        layout.addWidget(QLabel("Dört köşeye eklenecek sayıları girin:"))
        grid = QVBoxLayout()
        row1 = QHBoxLayout()
        self.left_upper = QLineEdit()
        self.left_upper.setPlaceholderText("Sol Üst")
        self.right_upper = QLineEdit()
        self.right_upper.setPlaceholderText("Sağ Üst")
        row1.addWidget(QLabel("Sol Üst:"))
        row1.addWidget(self.left_upper)
        row1.addWidget(QLabel("Sağ Üst:"))
        row1.addWidget(self.right_upper)
        grid.addLayout(row1)
        row2 = QHBoxLayout()
        self.left_lower = QLineEdit()
        self.left_lower.setPlaceholderText("Sol Alt")
        self.right_lower = QLineEdit()
        self.right_lower.setPlaceholderText("Sağ Alt")
        row2.addWidget(QLabel("Sol Alt:"))
        row2.addWidget(self.left_lower)
        row2.addWidget(QLabel("Sağ Alt:"))
        row2.addWidget(self.right_lower)
        grid.addLayout(row2)
        layout.addLayout(grid)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        if dialog.exec_() != QDialog.Accepted:
            return
        lu = self.left_upper.text().strip()
        ru = self.right_upper.text().strip()
        ll = self.left_lower.text().strip()
        rl = self.right_lower.text().strip()
        if not any([lu, ru, ll, rl]):
            QMessageBox.warning(self, "Uyarı", "En az bir köşeye değer girin.")
            return
        html = (
            '<table border="0" cellpadding="0" cellspacing="0" '
            'style="display:inline-table; vertical-align:middle; '
            'font-size:1em; line-height:1; margin:0;">'
            '<tr>'
            f'<td style="text-align:left; font-size:0.7em; vertical-align:top; padding:0 2px;">{lu}</td>'
            f'<td style="text-align:center; vertical-align:middle; padding:0 2px;"></td>'
            f'<td style="text-align:right; font-size:0.7em; vertical-align:top; padding:0 2px;">{ru}</td>'
            '</tr>'
            '<tr>'
            f'<td style="text-align:center; vertical-align:middle; padding:0 2px;"></td>'
            f'<td style="text-align:center; font-weight:normal; vertical-align:middle; padding:0 2px;">{base_char}</td>'
            f'<td style="text-align:center; vertical-align:middle; padding:0 2px;"></td>'
            '</tr>'
            '<tr>'
            f'<td style="text-align:left; font-size:0.7em; vertical-align:bottom; padding:0 2px;">{ll}</td>'
            f'<td style="text-align:center; vertical-align:middle; padding:0 2px;"></td>'
            f'<td style="text-align:right; font-size:0.7em; vertical-align:bottom; padding:0 2px;">{rl}</td>'
            '</tr>'
            '</table>'
        )
        if cursor.hasSelection():
            cursor.removeSelectedText()
        cursor.insertHtml(html)
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor)
        cursor.insertText("\u200B")
        self.editor.setTextCursor(cursor)

    def change_text_color(self):
        c = QColorDialog.getColor()
        if c.isValid():
            self.editor.setTextColor(c)

    def insert_image_base64(self):
        path, _ = QFileDialog.getOpenFileName(self, "Resim", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            with open(path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            ext = os.path.splitext(path)[1][1:].lower()
            if ext == 'jpg':
                ext = 'jpeg'
            self.editor.insertHtml(f'<img src="data:image/{ext};base64,{data}" width="300">')

    def change_font_size(self, size):
        f = self.editor.currentFont()
        f.setPointSize(int(size))
        self.editor.setCurrentFont(f)

    def increase_font_size(self):
        cur = self.editor.currentFont().pointSize()
        self.font_size.setCurrentText(str(cur + 2))

    def decrease_font_size(self):
        cur = self.editor.currentFont().pointSize()
        if cur > 8:
            self.font_size.setCurrentText(str(cur - 2))

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Dosya")
        new = QAction("Yeni", self); new.triggered.connect(self.new_file); file_menu.addAction(new)
        open_action = QAction("Aç...", self); open_action.triggered.connect(self.open_file); file_menu.addAction(open_action)
        save = QAction("Kaydet", self); save.triggered.connect(self.save_file); file_menu.addAction(save)
        saveas = QAction("Farklı Kaydet...", self); saveas.triggered.connect(lambda: self.save_file(force_dialog=True))
        file_menu.addAction(saveas)
        file_menu.addSeparator()
        word_template_action = QAction("📄 Word Şablonu Yükle", self)
        word_template_action.triggered.connect(self.load_word_template)
        file_menu.addAction(word_template_action)
        file_menu.addSeparator()
        exit = QAction("Çıkış", self); exit.triggered.connect(self.close); file_menu.addAction(exit)

        posts_menu = menubar.addMenu("Yazılar")
        listp = QAction("Kayıtlı Yazılar", self); listp.triggered.connect(self.show_posts_list); posts_menu.addAction(listp)

        tools_menu = menubar.addMenu("Araçlar")
        scholar = QAction("🔎 Google Scholar", self); scholar.triggered.connect(self.open_google_scholar); tools_menu.addAction(scholar)
        math_action = QAction("∑ Matematik İfadesi Ekle", self)
        math_action.triggered.connect(self.insert_math_expression)
        tools_menu.addAction(math_action)
        yks_action = QAction("📐 Ders Notlarım", self)
        yks_action.triggered.connect(self.open_yks_math)
        tools_menu.addAction(yks_action)
        const_action = QAction("🔢 Kullanıcı Sabitleri", self)
        const_action.triggered.connect(self.open_user_constants)
        tools_menu.addAction(const_action)
        find_action = QAction("🔍 Bul/Değiştir (Ctrl+F)", self)
        find_action.triggered.connect(lambda: FindReplaceDialog(self.editor, self).exec_())
        tools_menu.addAction(find_action)
        library_action = QAction("📚 Kütüphanem", self)
        library_action.triggered.connect(self.open_library)
        tools_menu.addAction(library_action)
        pdf_action = QAction("📄 PDF İşlemleri", self)
        pdf_action.triggered.connect(self.open_pdf_operations)
        tools_menu.addAction(pdf_action)

        dict_menu = menubar.addMenu("Sözlük")
        open_dict = QAction("📖 Sözlüğü Aç", self); open_dict.triggered.connect(self.open_dictionary); dict_menu.addAction(open_dict)

        guide_menu = menubar.addMenu("Rehber")
        seo_g = QAction("SEO Rehberi", self)
        seo_g.triggered.connect(lambda: show_guide_dialog("SEO Rehberi", get_seo_guide_html(), self))
        academic_g = QAction("Akademik Rehber", self)
        academic_g.triggered.connect(lambda: show_guide_dialog("Akademik Rehber", get_academic_guide_html(), self))
        guide_menu.addAction(seo_g)
        guide_menu.addAction(academic_g)

        settings_menu = menubar.addMenu("Ayarlar")
        ai_config = QAction("🤖 AI Modellerini Yapılandır", self)
        ai_config.triggered.connect(self.open_ai_settings)
        settings_menu.addAction(ai_config)

        user_mgmt = QAction("👥 Kullanıcı Yönetimi (Admin)", self)
        user_mgmt.triggered.connect(self.open_user_management)
        settings_menu.addAction(user_mgmt)

        format_menu = settings_menu.addMenu("📘 Akademik Format")
        apa_action = QAction("APA", self, checkable=True)
        apa_action.triggered.connect(lambda: self.set_academic_format("APA"))
        mla_action = QAction("MLA", self, checkable=True)
        mla_action.triggered.connect(lambda: self.set_academic_format("MLA"))
        chicago_action = QAction("Chicago", self, checkable=True)
        chicago_action.triggered.connect(lambda: self.set_academic_format("Chicago"))
        format_menu.addAction(apa_action)
        format_menu.addAction(mla_action)
        format_menu.addAction(chicago_action)
        apa_action.setChecked(True)

        self.ai_use_action = QAction("🎯 AI Düzeltmeyi Kullan", self, checkable=True)
        self.ai_use_action.setChecked(self.use_ollama)
        self.ai_use_action.triggered.connect(lambda checked: self.set_use_ai(checked))
        settings_menu.addAction(self.ai_use_action)

        analyze_action = QAction("🔍 Analiz Et", self)
        analyze_action.triggered.connect(self.analyze)
        settings_menu.addAction(analyze_action)

        deep_corr_action = QAction("🎯 AI ile Düzelt", self)
        deep_corr_action.triggered.connect(self.start_deep_correction)
        settings_menu.addAction(deep_corr_action)

        theme_menu = menubar.addMenu("Tema")
        dark_theme = QAction("Koyu Tema", self)
        dark_theme.triggered.connect(lambda: self.set_theme("dark"))
        light_theme = QAction("Açık Tema", self)
        light_theme.triggered.connect(lambda: self.set_theme("light"))
        theme_menu.addAction(dark_theme)
        theme_menu.addAction(light_theme)

        help_menu = menubar.addMenu("Yardım")
        about = QAction("Hakkında", self); about.triggered.connect(lambda: QMessageBox.about(self, "Hakkında", "Coder: deliKadir\nemail: astromoon.1990@gmail.com")); help_menu.addAction(about)

    def open_library(self):
        dlg = LibraryDialog(self.db, self)
        dlg.exec_()

    def open_pdf_operations(self):
        dlg = PDFOperationsDialog(self)
        dlg.exec_()

    def set_academic_format(self, fmt):
        self.academic_format = fmt
        self.statusBar().showMessage(f"Akademik format: {fmt}", 2000)

    def set_use_ai(self, checked):
        self.use_ollama = checked
        self.statusBar().showMessage(f"AI düzeltme {'aktif' if checked else 'pasif'}", 2000)

    def open_yks_math(self):
        self.tabs.setCurrentWidget(self.math_widget)

    def open_user_constants(self):
        dlg = UserConstantsDialog(self.db, self)
        dlg.exec_()

    def load_word_template(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Word Şablonu Seç", "", "Word Belgeleri (*.docx)")
        if not file_path:
            return
        try:
            doc = docx.Document(file_path)
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            if not paragraphs:
                QMessageBox.warning(self, "Uyarı", "Seçilen dosyada okunabilir metin bulunamadı.")
                return
            full_text = "\n".join(paragraphs)
            self.editor.setPlainText(full_text)
            for cb in (self.cb_seo, self.cb_academic, self.cb_blog, self.cb_product):
                cb.blockSignals(True)
                cb.setChecked(False)
                cb.blockSignals(False)
            types = ["SEO Makalesi", "Akademik Makale", "Blog Yazısı", "Ürün Tanıtımı", "Word Şablonu"]
            selected_type, ok = QInputDialog.getItem(self, "Şablon Tipi", "Bu şablonun türünü seçin:", types, 4, False)
            if ok and selected_type:
                self.word_template_type = selected_type
            else:
                self.word_template_type = "Word Şablonu"
            QMessageBox.information(self, "Başarılı", f"Word şablonu yüklendi. Tür: {self.word_template_type}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya okunamadı:\n{str(e)}")

    def create_toolbar(self):
        tb = QToolBar("Araçlar")
        self.addToolBar(tb)
        new_btn = QPushButton("Yeni"); new_btn.clicked.connect(self.new_file); tb.addWidget(new_btn)
        open_btn = QPushButton("Aç"); open_btn.clicked.connect(self.open_file); tb.addWidget(open_btn)
        save_btn = QPushButton("Kaydet"); save_btn.clicked.connect(self.save_file); tb.addWidget(save_btn)
        dbsave = QPushButton("💾 Veritabanına Kaydet"); dbsave.clicked.connect(self.save_to_database); tb.addWidget(dbsave)
        tb.addSeparator()
        tb.addWidget(self.deep_btn)

    def open_ai_settings(self):
        dlg = AIModelsDialog(self)
        if dlg.exec_():
            if QMessageBox.question(self, "Yeniden Başlat", "Ayarlar değişti. Yeniden başlatılsın mı?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
                os.execl(sys.executable, sys.executable, *sys.argv)

    def open_user_management(self):
        pwd, ok = QInputDialog.getText(self, "Admin Doğrulama", "Admin şifresini girin:", QLineEdit.Password)
        if ok and pwd == "admin":
            dlg = UserManagementDialog(self.user_manager, self)
            dlg.exec_()
        else:
            QMessageBox.warning(self, "Yetkisiz Giriş Denemesi", "Sadece admin kullanıcı yönetebilir.")

    def open_google_scholar(self):
        GoogleScholarDialog(self).exec_()

    def open_dictionary(self):
        DictionaryDialog(self.dict_db, self).exec_()

    def show_posts_list(self):
        PostsListDialog(self.db, self).exec_()

    def open_academic_editor(self):
        self.tabs.setCurrentWidget(self.academic_dialog)

    def load_post_for_edit(self, pid, title, ptype, content):
        self.edit_mode = True
        self.editing_post_id = pid
        self.editor.setHtml(content)
        self.edit_title = title
        self.edit_type = ptype
        if not hasattr(self, 'update_btn'):
            self.update_btn = QPushButton("💾 Düzenleme Modu")
            self.update_btn.clicked.connect(self.update_post)
            self.update_btn.setStyleSheet("background:#0e639c")
            self.left_layout.insertWidget(0, self.update_btn)
        else:
            self.update_btn.show()
        QMessageBox.information(self, "Düzenleme Modu", f"Yazı düzenleniyor: {title}")

    def update_post(self):
        if not self.edit_mode:
            return
        new_content = self.editor.toHtml()
        new_title, ok = QInputDialog.getText(self, "Başlık Güncelle", "Yeni başlık:", text=self.edit_title)
        if not ok or not new_title.strip():
            return
        new_type, ok = QInputDialog.getItem(self, "Tür Güncelle", "Yeni tür:", ["SEO Makalesi", "Akademik Makale", "Blog Yazısı", "Ürün Tanıtımı", "Standart Not"], 0, False)
        if not ok:
            return
        self.db.update_post(self.editing_post_id, new_title.strip(), new_content, new_type)
        QMessageBox.information(self, "Başarılı", "Güncellendi.")
        self.edit_mode = False
        self.editing_post_id = None
        self.update_btn.hide()
        self.editor.clear()
        for cb in (self.cb_seo, self.cb_academic, self.cb_blog, self.cb_product):
            cb.setChecked(False)

    def load_template(self, name):
        for cb in (self.cb_seo, self.cb_academic, self.cb_blog, self.cb_product):
            cb.blockSignals(True)
            cb.setChecked(False)
        if name == "seo":
            self.cb_seo.setChecked(True)
            self.editor.setHtml(seo_template())
        elif name == "academic":
            self.cb_academic.setChecked(True)
            self.open_academic_editor()
        elif name == "blog":
            self.cb_blog.setChecked(True)
            self.editor.setHtml(blog_template())
        elif name == "product":
            self.cb_product.setChecked(True)
            self.editor.setHtml(product_template())
        for cb in (self.cb_seo, self.cb_academic, self.cb_blog, self.cb_product):
            cb.blockSignals(False)

    def new_file(self):
        self.editor.clear()
        self.result_edit.clear()
        self.stats_label.setText("Henüz analiz yok.")
        self.seo_details_label.setText("-")
        self.seo_progress.setValue(0)
        self.word_template_type = None
        if self.edit_mode:
            self.edit_mode = False
            if hasattr(self, 'update_btn'):
                self.update_btn.hide()
        self.update_word_count()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", "", "All Files (*);;HTML (*.html);;Text (*.txt);;Word (*.docx);;PDF (*.pdf)")
        if path:
            try:
                if path.endswith(".docx"):
                    doc = docx.Document(path)
                    text = "\n".join([p.text for p in doc.paragraphs])
                    self.editor.setPlainText(text)
                elif path.endswith(".pdf") and PDF_SUPPORT:
                    text = self.extract_pdf_text(path)
                    self.editor.setPlainText(text)
                elif path.endswith(".html"):
                    with open(path, "r", encoding="utf-8") as f:
                        self.editor.setHtml(f.read())
                else:
                    with open(path, "r", encoding="utf-8") as f:
                        self.editor.setPlainText(f.read())
                self.current_file = path
                self.statusBar().showMessage(f"Dosya açıldı: {os.path.basename(path)}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Hata", str(e))

    def extract_pdf_text(self, path):
        text = ""
        if PDF_SUPPORT:
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        else:
            QMessageBox.warning(self, "Uyarı", "PDF desteği için 'pip install PyPDF2' kurun.")
        return text

    def save_file(self, force_dialog=False):
        content = self.editor.toHtml()
        if not content.strip():
            QMessageBox.warning(self, "Uyarı", "Boş metin")
            return
        if not force_dialog and hasattr(self, 'current_file') and self.current_file and not self.current_file.endswith(".pdf"):
            with open(self.current_file, "w", encoding="utf-8") as f:
                if self.current_file.endswith(".html"):
                    f.write(content)
                else:
                    f.write(self.editor.toPlainText())
            QMessageBox.information(self, "Başarılı", "Kaydedildi.")
            self.statusBar().showMessage(f"Kaydedildi: {os.path.basename(self.current_file)}", 2000)
        else:
            path, _ = QFileDialog.getSaveFileName(self, "Kaydet", "", "HTML (*.html);;Text (*.txt)")
            if path:
                self.current_file = path
                with open(path, "w", encoding="utf-8") as f:
                    if path.endswith(".html"):
                        f.write(content)
                    else:
                        f.write(self.editor.toPlainText())
                QMessageBox.information(self, "Başarılı", "Kaydedildi.")
                self.statusBar().showMessage(f"Kaydedildi: {os.path.basename(path)}", 2000)

    def save_to_database(self):
        content = self.editor.toHtml()
        if not content.strip():
            QMessageBox.warning(self, "Uyarı", "Boş metin")
            return
        title, ok = QInputDialog.getText(self, "Başlık", "Yazı başlığı:")
        if not ok or not title.strip():
            return
        if self.cb_seo.isChecked():
            ptype = "SEO Makalesi"
        elif self.cb_academic.isChecked():
            ptype = "Akademik Makale"
        elif self.cb_blog.isChecked():
            ptype = "Blog Yazısı"
        elif self.cb_product.isChecked():
            ptype = "Ürün Tanıtımı"
        elif self.word_template_type:
            ptype = self.word_template_type
        else:
            ptype = "Standart Not"
        self.db.save_post(title.strip(), content, ptype)
        QMessageBox.information(self, "Başarılı", "Veritabanına kaydettim.")
        self.statusBar().showMessage("Veritabanına kaydedildi", 2000)

    def start_deep_correction(self):
        text = clean_html(self.editor.toHtml())
        if not text.strip():
            QMessageBox.warning(self, "Uyarı", "Metin girin")
            return
        use_openai = False
        openai_key = ""
        if os.path.exists("openai_key.txt"):
            with open("openai_key.txt", "r") as f:
                openai_key = f.read().strip()
            if openai_key and OPENAI_AVAILABLE:
                use_openai = True
        if not self.ollama_available and not use_openai:
            QMessageBox.warning(self, "Uyarı", "Ollama çalışmıyor ve OpenAI anahtarı yok.")
            return
        mode = 'standart'
        if self.cb_seo.isChecked():
            mode = 'seo'
        elif self.cb_academic.isChecked():
            mode = 'academic'
        config = load_model_config()
        if mode == 'seo':
            model = config.get('seo', DEFAULT_MODELS['seo'])
        elif mode == 'academic':
            model = config.get('academic', DEFAULT_MODELS['academic'])
        else:
            model = config.get('standard', DEFAULT_MODELS['standard'])
        lang = 'tr-TR' if any(c in 'çğıöşüÇĞİÖŞÜ' for c in text) else 'en-US'
        self.progress = QProgressDialog("Düzeltiyorum...", "İptal", 0, 100, self)
        self.progress.setWindowModality(Qt.WindowModal)
        self.thread = HybridCheckThread(text, lang, self.use_ollama, mode, self.academic_format, model, use_openai, openai_key)
        self.thread.progress.connect(self.progress.setValue)
        self.thread.finished.connect(self.on_correction_finished)
        self.thread.error.connect(self.on_correction_error)
        self.thread.start()
        self.statusBar().showMessage("AI düzeltme başlatıldı...", 2000)

    def on_correction_finished(self, res):
        self.progress.close()
        dlg = AccuracyReportDialog(res['errors'], res['accuracy_score'], res['corrected_text'], self)
        if dlg.exec_():
            if QMessageBox.question(self, "Metni Güncelle", f"Doğruluk: {res['accuracy_score']}/100\nDüzeltilmiş metni kopyala?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
                self.editor.setPlainText(res['corrected_text'])
                self.result_edit.setPlainText(f"✅ Düzeltme tamam. Skor: {res['accuracy_score']}/100")
                self.statusBar().showMessage(f"Düzeltme tamamlandı. Skor: {res['accuracy_score']}/100", 5000)

    def on_correction_error(self, msg):
        self.progress.close()
        QMessageBox.critical(self, "Hata", msg)
        self.statusBar().showMessage(f"Hata: {msg}", 5000)

    def analyze(self):
        text = clean_html(self.editor.toHtml())
        if not text.strip():
            QMessageBox.warning(self, "Uyarı", "Metin gir.")
            return
        fixed = text_correction_engine(text)
        keywords = extract_keywords(text)
        density = keyword_density(text, keywords)
        readability = textstat.flesch_reading_ease(text)
        mode = "Standart"
        if self.cb_seo.isChecked():
            fixed = seo_rewrite(fixed, keywords)
            mode = "SEO"
        elif self.cb_academic.isChecked():
            fixed = academic_rewrite(fixed, self.academic_format)
            mode = f"Akademik ({self.academic_format})"
        elif self.word_template_type:
            mode = self.word_template_type
        score, details = seo_score_details(text, density, readability)
        serp = serp_prediction(score)
        stats = text_stats(text)
        result = f"ANALİZ RAPORU\nMod: {mode}\nSEO Skor: {score}/100 {serp}\n"
        for k, v in details.items():
            result += f"{k}: {v}\n"
        result += f"Kelime: {stats['Kelime']} | Okuma: {stats['Okuma Süresi (dk)']} dk\nAnahtar Kelimeler: {', '.join(keywords)}\nYoğunluk: {density}\nOkunabilirlik: {readability:.1f}\nDüzeltilmiş (ilk 500): {fixed[:500]}"
        self.result_edit.setPlainText(result)
        self.stats_label.setText(f"{stats['Kelime']} kelime | {stats['Cümle']} cümle | {stats['Okuma Süresi (dk)']} dk")
        self.seo_details_label.setText("\n".join([f"{k}: {v}" for k, v in details.items()]))
        self.seo_progress.setValue(score)
        if QMessageBox.question(self, "Metni Güncelle", "Düzeltilmiş metni editöre kopyala?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            self.editor.setPlainText(fixed)
        self.statusBar().showMessage("Analiz tamamlandı", 2000)

# ----------------------------------------------------------------------
# Başlangıç
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Başlangıçta koyu temayı uygula
    app.setStyleSheet(DARK_STYLE)
    um = UserManager()
    login = LoginDialog(um)
    if login.exec_():
        window = App()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()