
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt

class ScaledImageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = QPixmap()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(200, 200)

    def setPixmap(self, pixmap):
        if pixmap:
            self._pixmap = pixmap
        else:
            self._pixmap = QPixmap()
        self.update()

    def paintEvent(self, event):
        if self._pixmap.isNull():
            super().paintEvent(event)
            return
        
        scaled_pixmap = self._pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        x = (self.width() - scaled_pixmap.width()) // 2
        y = (self.height() - scaled_pixmap.height()) // 2
        
        painter = QPainter(self)
        painter.drawPixmap(x, y, scaled_pixmap)

class ImageSplitter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def split_image(self):
        if not hasattr(self, 'image_path'):
            self.lbl_status.setText('Please select an image first.')
            return

        try:
            rows = int(self.le_rows.text())
            cols = int(self.le_cols.text())
            pad_top = int(self.le_pad_top.text())
            pad_right = int(self.le_pad_right.text())
            pad_bottom = int(self.le_pad_bottom.text())
            pad_left = int(self.le_pad_left.text())
            space_hor = int(self.le_space_hor.text())
            space_ver = int(self.le_space_ver.text())

            if rows <= 0 or cols <= 0 or pad_top < 0 or pad_right < 0 or pad_bottom < 0 or pad_left < 0 or space_hor < 0 or space_ver < 0:
                raise ValueError()
        except ValueError:
            self.lbl_status.setText('Please enter valid positive numbers for all fields.')
            return

        original_image = QImage(self.image_path)
        if original_image.isNull():
            self.lbl_status.setText('Failed to load image.')
            return

        img_width = original_image.width()
        img_height = original_image.height()

        total_padding_width = pad_left + pad_right
        total_padding_height = pad_top + pad_bottom
        total_spacing_width = space_hor * (cols - 1)
        total_spacing_height = space_ver * (rows - 1)

        available_width = img_width - total_padding_width - total_spacing_width
        available_height = img_height - total_padding_height - total_spacing_height

        if available_width <= 0 or available_height <= 0:
            self.lbl_status.setText('Padding and spacing are too large for the image dimensions.')
            return

        tile_width = available_width // cols
        tile_height = available_height // rows

        rem_w = available_width % cols
        pad_left += rem_w // 2

        if tile_width <= 0 or tile_height <= 0:
            self.lbl_status.setText('Cannot create tiles with zero or negative size. Check parameters.')
            return

        import os
        path, ext = os.path.splitext(self.image_path)

        for i in range(rows):
            for j in range(cols):
                x = pad_left + j * (tile_width + space_hor)
                y = pad_top + i * (tile_height + space_ver)
                tile = original_image.copy(x, y, tile_width, tile_height)
                tile.save(f"{path}_{i}_{j}{ext}")

        self.lbl_status.setText(f'Successfully split image into {rows * cols} tiles.')


    def initUI(self):
        self.setWindowTitle('Image Splitter')
        self.layout = QVBoxLayout()

        # Image selection
        self.btn_select_image = QPushButton('Select Image')
        self.btn_select_image.clicked.connect(self.select_image)
        self.layout.addWidget(self.btn_select_image)

        self.lbl_image_path = QLabel('No image selected')
        self.layout.addWidget(self.lbl_image_path)

        # Image Preview
        self.lbl_preview = ScaledImageWidget()
        self.layout.addWidget(self.lbl_preview)

        # Rows and Columns input
        h_layout_rows_cols = QHBoxLayout()
        h_layout_rows_cols.addWidget(QLabel("Rows:"))
        self.le_rows = QLineEdit()
        self.le_rows.setPlaceholderText("Rows")
        self.le_rows.textChanged.connect(self.update_preview)
        h_layout_rows_cols.addWidget(self.le_rows)

        h_layout_rows_cols.addWidget(QLabel("Columns:"))
        self.le_cols = QLineEdit()
        self.le_cols.setPlaceholderText("Columns")
        self.le_cols.textChanged.connect(self.update_preview)
        h_layout_rows_cols.addWidget(self.le_cols)
        self.layout.addLayout(h_layout_rows_cols)

        # Padding input
        self.layout.addWidget(QLabel("Padding:"))
        h_layout_padding = QHBoxLayout()
        h_layout_padding.addWidget(QLabel("Top:"))
        self.le_pad_top = QLineEdit("0")
        self.le_pad_top.textChanged.connect(self.update_preview)
        h_layout_padding.addWidget(self.le_pad_top)
        h_layout_padding.addWidget(QLabel("Right:"))
        self.le_pad_right = QLineEdit("0")
        self.le_pad_right.textChanged.connect(self.update_preview)
        h_layout_padding.addWidget(self.le_pad_right)
        h_layout_padding.addWidget(QLabel("Bottom:"))
        self.le_pad_bottom = QLineEdit("0")
        self.le_pad_bottom.textChanged.connect(self.update_preview)
        h_layout_padding.addWidget(self.le_pad_bottom)
        h_layout_padding.addWidget(QLabel("Left:"))
        self.le_pad_left = QLineEdit("0")
        self.le_pad_left.textChanged.connect(self.update_preview)
        h_layout_padding.addWidget(self.le_pad_left)
        self.layout.addLayout(h_layout_padding)

        # Spacing input
        self.layout.addWidget(QLabel("Spacing:"))
        h_layout_spacing = QHBoxLayout()
        h_layout_spacing.addWidget(QLabel("Horizontal:"))
        self.le_space_hor = QLineEdit("0")
        self.le_space_hor.textChanged.connect(self.update_preview)
        h_layout_spacing.addWidget(self.le_space_hor)
        h_layout_spacing.addWidget(QLabel("Vertical:"))
        self.le_space_ver = QLineEdit("0")
        self.le_space_ver.textChanged.connect(self.update_preview)
        h_layout_spacing.addWidget(self.le_space_ver)
        self.layout.addLayout(h_layout_spacing)


        # Split button
        self.btn_split = QPushButton('Split Image')
        self.btn_split.clicked.connect(self.split_image)
        self.layout.addWidget(self.btn_split)

        # Status label
        self.lbl_status = QLabel('')
        self.layout.addWidget(self.lbl_status)

        self.setLayout(self.layout)

    def select_image(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if fileName:
            self.image_path = fileName
            self.lbl_image_path.setText(fileName)
            self.original_pixmap = QPixmap(self.image_path)
            self.update_preview()

    def update_preview(self):
        if not hasattr(self, 'original_pixmap'):
            return

        try:
            rows = int(self.le_rows.text()) if self.le_rows.text() else 0
            cols = int(self.le_cols.text()) if self.le_cols.text() else 0
            pad_top = int(self.le_pad_top.text()) if self.le_pad_top.text() else 0
            pad_right = int(self.le_pad_right.text()) if self.le_pad_right.text() else 0
            pad_bottom = int(self.le_pad_bottom.text()) if self.le_pad_bottom.text() else 0
            pad_left = int(self.le_pad_left.text()) if self.le_pad_left.text() else 0
            space_hor = int(self.le_space_hor.text()) if self.le_space_hor.text() else 0
            space_ver = int(self.le_space_ver.text()) if self.le_space_ver.text() else 0

            if rows <= 0 or cols <= 0:
                self.lbl_preview.setPixmap(self.original_pixmap)
                return
        except ValueError:
            self.lbl_preview.setPixmap(self.original_pixmap)
            return

        pixmap = self.original_pixmap.copy()
        painter = QPainter(pixmap)
        pen = QPen(QColor(255, 0, 0, 128), 2, Qt.SolidLine)
        painter.setPen(pen)

        img_width = pixmap.width()
        img_height = pixmap.height()

        total_padding_width = pad_left + pad_right
        total_padding_height = pad_top + pad_bottom
        total_spacing_width = space_hor * (cols - 1)
        total_spacing_height = space_ver * (rows - 1)

        available_width = img_width - total_padding_width - total_spacing_width
        available_height = img_height - total_padding_height - total_spacing_height
        
        if available_width <= 0 or available_height <= 0:
            self.lbl_preview.setPixmap(self.original_pixmap)
            return

        tile_width = available_width // cols
        tile_height = available_height // rows

        rem_w = available_width % cols
        pad_left += rem_w // 2
        
        if tile_width <= 0 or tile_height <= 0:
            self.lbl_preview.setPixmap(self.original_pixmap)
            return

        # Draw rectangles
        for i in range(rows):
            for j in range(cols):
                x = pad_left + j * (tile_width + space_hor)
                y = pad_top + i * (tile_height + space_ver)
                painter.drawRect(x, y, tile_width, tile_height)

        painter.end()
        self.lbl_preview.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageSplitter()
    ex.show()
    sys.exit(app.exec_())
