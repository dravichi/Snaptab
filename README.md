# Snaptab: Automated Table Extraction from PDFs Using YOLOv8n  

**Snaptab** is a Python library designed to automate the extraction and conversion of tabular data from **PDFs into image formats**, making it easier to create **table image datasets** for AI research and document processing. It utilizes **YOLOv8n** (a lightweight deep learning model) for table detection, ensuring high accuracy and efficiency.  

## Key Features  
✅ **Automated Table Detection** – Uses YOLOv8n to identify and extract tables from PDFs.  
✅ **Batch Processing** – Processes a folder of PDFs in a single run..  
✅ **Flexible Image Output** – Supports **PNG, JPEG, JPG, TIFF, and BMP** formats.  
✅ **Adjustable DPI** – Customizable resolution for better image quality.  
✅ **Confidence Thresholding** – Set detection confidence to refine table extraction.  
✅ **Optional Table Cropping** – Extract only table regions or full-page images.  
✅ **Customizable Naming** – Define a base name and starting index for output files.  
✅ **Customizable Starting Index** – Set a specific starting index for numbered output image  

## Installation  
You can install Snaptab via **pip**:  
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ snaptab
```

## Usage  
Snaptab can be used as a command-line tool:  
```bash
snaptab input_folder output_folder --image_format=PNG --dpi=100 --conf_threshold=0.5 --crop_images=True --basename="Example" --start_index=1
```

## Requirements  
- **Python 3.6+**  
- **PyPDF2** (for reading PDFs)  
- **pdf2image** (for PDF-to-image conversion)  
- **Ultralytics YOLO** (for table detection)  

## Why Snaptab?  
📌 **Faster Dataset Creation** – Automates PDF-to-table-image conversion.  
📌 **Lightweight & Efficient** – Optimized for real-world applications.  
📌 **AI-Ready** – Generates structured table image datasets for **OCR, VQA, and document AI models**.  

## License  
Snaptab is open-source and licensed under **MIT**. Contributions are welcome!  