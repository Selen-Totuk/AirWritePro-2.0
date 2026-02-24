# AirStudio Pro - Virtual Engineering Studio

## English Version

**AirStudio Pro** is a virtual engineering drawing and calculation tool using hand tracking. Users can draw shapes and interact with an engineering calculator in real-time using hand gestures captured by a webcam.


### Features
- **Hand Gesture Drawing**: Draw rectangles, prisms, triangles, circles, and cylinders using only hand gestures.
- **Interactive Sidebar**: Select drawing shapes, open engineering calculator, or clear the canvas.
- **Engineering Calculator**: A built-in calculator for quick computations.
- **Zooming Shapes**: Increase or decrease shape sizes using open hand or fist gestures.
- **Real-time Interaction**: Full webcam-based interaction without any mouse or keyboard.

### Controls
- **Select Shape**: Hover over sidebar buttons with index + middle finger together.
- **Draw Shape**: Use index finger on the drawing area.
- **Calculator Interaction**: Open with sidebar button, click using only the index finger.
- **Clear Canvas**: Press the "Clear" button on sidebar (index + middle finger together).
- **Zoom Shapes**:
  - Fist → shrink all shapes.
  - Open hand → enlarge all shapes.
- **Quit Application**: Press `q` key.

### Requirements
- Python 3.10+
- OpenCV (`cv2`)
- Numpy (`numpy`)
- Custom modules: `hand_tracker.py`, `shape_manager.py`, `calc_manager.py`

### Installation
```bash
git clone https://github.com/YourUsername/AirWritePro-2.0.git
cd AirWritePro-2.0
pip install opencv-python numpy
python main.py


# AirStudio Pro - Sanal Mühendislik Stüdyosu


## Tanıtım

**AirStudio Pro**, el hareketleri ile şekil çizebileceğiniz ve mühendislik hesaplamaları yapabileceğiniz sanal bir stüdyo uygulamasıdır. Web kamerası aracılığıyla el hareketlerini takip ederek gerçek zamanlı etkileşim sağlar.

### Özellikler
- **El Hareketi ile Çizim**: Sadece el hareketleriyle kare, prizma, üçgen, daire ve silindir çizin.
- **Etkileşimli Yan Menü**: Çizim türlerini seçin, hesap makinesini açın veya tuvali temizleyin.
- **Mühendislik Hesap Makinesi**: Hızlı hesaplamalar için entegre bir hesap makinesi.
- **Şekil Büyütme/Küçültme**: Açık el veya yumruk hareketleriyle şekillerin boyutunu değiştirin.
- **Gerçek Zamanlı Etkileşim**: Fare veya klavye olmadan tamamen web kamerası ile kontrol.

### Kontroller
- **Şekil Seçimi**: Yan menü butonlarına işaret + orta parmak birleşik olarak dokunun.
- **Şekil Çizimi**: Çizim alanında sadece işaret parmağı kullanın.
- **Hesap Makinesi Kullanımı**: Yan menüden açın, sadece işaret parmağıyla tıklayın.
- **Tuvali Temizle**: Yan menüdeki "TEMİZLE" butonuna işaret + orta parmak ile dokunun.
- **Şekil Büyütme/Küçültme**:
  - Yumruk → tüm şekilleri küçült.
  - Açık el → tüm şekilleri büyüt.
- **Uygulamayı Kapat**: `q` tuşuna basın.

### Gereksinimler
- Python 3.10+
- OpenCV (`cv2`)
- Numpy (`numpy`)
- Özel modüller: `hand_tracker.py`, `shape_manager.py`, `calc_manager.py`

### Kurulum
```bash
git clone https://github.com/YourUsername/AirWritePro-2.0.git
cd AirWritePro-2.0
pip install opencv-python numpy
python main.py
