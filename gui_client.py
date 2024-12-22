from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import requests

BASE_URL = "http://localhost:5000"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("URL Shortener")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs.addTab(self.tab1, "Shorten/Update/Delete")
        self.tabs.addTab(self.tab2, "View")
        self.tabs.addTab(self.tab3, "Stats")

        self.layout.addWidget(self.tabs)

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()

    def setup_tab1(self):
        self.shorten_url_input = QLineEdit()
        self.shorten_url_input.setPlaceholderText("Enter URL to shorten")
        self.shorten_url_button = QPushButton("Shorten")
        self.shorten_url_button.clicked.connect(self.handle_shorten_url)

        self.update_url_input = QLineEdit()
        self.update_url_input.setPlaceholderText("Enter short code to update")
        self.update_new_url_input = QLineEdit()
        self.update_new_url_input.setPlaceholderText("Enter new URL")
        self.update_url_button = QPushButton("Update")
        self.update_url_button.clicked.connect(self.handle_update_url)

        self.delete_url_input = QLineEdit()
        self.delete_url_input.setPlaceholderText("Enter short code to delete")
        self.delete_url_button = QPushButton("Delete")
        self.delete_url_button.clicked.connect(self.handle_delete_url)

        layout = QVBoxLayout()
        layout.addWidget(self.shorten_url_input)
        layout.addWidget(self.shorten_url_button)
        layout.addWidget(self.update_url_input)
        layout.addWidget(self.update_new_url_input)
        layout.addWidget(self.update_url_button)
        layout.addWidget(self.delete_url_input)
        layout.addWidget(self.delete_url_button)

        self.tab1.setLayout(layout)

    def setup_tab2(self):
        self.web_view = QWebEngineView()
        self.view_url_input = QLineEdit()
        self.view_url_input.setPlaceholderText("Enter short code to view")
        self.view_url_button = QPushButton("View")
        self.view_url_button.clicked.connect(self.handle_view_url)

        layout = QVBoxLayout()
        layout.addWidget(self.view_url_input)
        layout.addWidget(self.view_url_button)
        layout.addWidget(self.web_view)

        self.tab2.setLayout(layout)

    def setup_tab3(self):
        self.stats_url_input = QLineEdit()
        self.stats_url_input.setPlaceholderText("Enter short code to view stats")
        self.stats_url_button = QPushButton("View Stats")
        self.stats_url_button.clicked.connect(self.handle_view_stats)
        self.stats_display = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.stats_url_input)
        layout.addWidget(self.stats_url_button)
        layout.addWidget(self.stats_display)

        self.tab3.setLayout(layout)

    def handle_shorten_url(self):
        url = self.shorten_url_input.text()
        try:
            response = requests.post(f"{BASE_URL}/shorten", json={"url": url})
            response_data = response.json()
            self.shorten_url_input.setText(response_data.get("short_code", "Error"))
        except Exception as e:
            self.shorten_url_input.setText(f"Error: {e}")

    def handle_update_url(self):
        short_code = self.update_url_input.text()
        new_url = self.update_new_url_input.text()
        try:
            response = requests.put(f"{BASE_URL}/shorten/{short_code}", json={"url": new_url})
            response_data = response.json()
            self.update_url_input.setText(response_data.get("message", "Updated"))
        except Exception as e:
            self.update_url_input.setText(f"Error: {e}")

    def handle_delete_url(self):
        short_code = self.delete_url_input.text()
        try:
            response = requests.delete(f"{BASE_URL}/shorten/{short_code}")
            response_data = response.json()
            self.delete_url_input.setText(response_data.get("message", "Deleted"))
        except Exception as e:
            self.delete_url_input.setText(f"Error: {e}")

    def handle_view_url(self):
        short_code = self.view_url_input.text()
        try:
            response = requests.get(f"{BASE_URL}/shorten/{short_code}")
            response_data = response.json()
            url = response_data.get("url", "")
            if url:
                self.web_view.load(QUrl(url))
                self.web_view.settings().setAttribute(self.web_view.settings().WebAttribute.LocalContentCanAccessRemoteUrls, True)
            else:
                self.view_url_input.setText("Invalid short code")
        except Exception as e:
            self.view_url_input.setText(f"Error: {e}")
    
    def handle_view_stats(self):
        self.stats_display.clear()
        short_code = self.stats_url_input.text()
        try:
            response = requests.get(f"{BASE_URL}/shorten/{short_code}/stats")
            response_data = response.json()
            if response_data.get("error"):
                self.stats_url_input.setText("Not found")
            else:
                result_to_display = ""
                for key, value in response_data.items():
                    result_to_display += f"{key}: {value}\n"
                self.stats_display.setPlainText(result_to_display)
        except Exception as e:
            self.stats_url_input.setText(f"Error: {e}")

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
