## This is Simple GUI programme -  PDF to CSV Converter in Python using the PyQt5
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QFileDialog, QProgressBar
import tabula

class PDFtoCSVConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()

        self.grid.addWidget(QLabel("PDF File:"), 0, 0)
        self.pdf_file_label = QLabel("")
        self.grid.addWidget(self.pdf_file_label, 0, 1)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.select_pdf_file)
        self.grid.addWidget(self.browse_button, 0, 2)

        self.grid.addWidget(QLabel("Save CSV file as:"), 1, 0)
        self.csv_file_label = QLabel("")
        self.grid.addWidget(self.csv_file_label, 1, 1)

        self.save_button = QPushButton("Save As", self)
        self.save_button.clicked.connect(self.select_csv_file)
        self.grid.addWidget(self.save_button, 1, 2)

        self.convert_button = QPushButton("Convert to CSV", self)
        self.convert_button.clicked.connect(self.convert_pdf_to_csv)
        self.grid.addWidget(self.convert_button, 2, 1)

        self.result_label = QLabel("")
        self.grid.addWidget(self.result_label, 3, 1)

        self.progress_bar = QProgressBar(self)
        self.grid.addWidget(self.progress_bar, 4, 1)

        self.setLayout(self.grid)

        self.setWindowTitle("PDF to CSV Converter")

    def select_pdf_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select PDF file", "",
                                                  "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_name:
            self.pdf_file_label.setText(file_name)

    def select_csv_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV file", "",
                                                  "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            self.csv_file_label.setText(file_name)

    def convert_pdf_to_csv(self):
        pdf_file = self.pdf_file_label.text()
        if not pdf_file.endswith(".pdf"):
            self.result_label.setText("Invalid PDF file")
            return
        csv_file = self.csv_file_label.text()
        if not csv_file.endswith(".csv"):
            self.result_label.setText("Invalid CSV file")
            return
        try:
            tabula.convert_into(pdf_file, output_path=csv_file, output_format='csv', pages='all', java_options=['-Xmx2048m'])
            self.result_label.setText("Conversion successful!")
        except:
            self.result_label.setText("Error during conversion")

        self.progress_bar.setValue(0)

    def update_progress_bar(self, current, total):
        progress = int(current / total * 100)
        self.progress_bar.setValue(progress)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = PDFtoCSVConverter()
    converter.show()
    sys.exit(app.exec_())
