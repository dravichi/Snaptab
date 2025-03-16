from pdf2image import convert_from_path
from . import get_poppler_path, get_model_path
from PyPDF2 import PdfReader
from ultralytics import YOLO
import pkg_resources
import argparse
import sys
import re 
import os

POPPLER_PATH = get_poppler_path()
MODEL_PATH = get_model_path() 

_version_ = pkg_resources.get_distribution("snaptab").version
class_mapping = {0: 'table', 1: 'no_table'}
total_tables = total_pdfs = 0

def get_input_folder(input_folder):
    if not input_folder:
        raise ValueError("The input folder path cannot be empty. Please provide a valid folder path.")
    if not os.path.exists(input_folder):
        raise ValueError(f"The folder '{input_folder}' does not exist. Please provide a valid folder path.")
    if not any(fname.endswith('.pdf') for fname in os.listdir(input_folder)):
        raise ValueError(f"No PDF files found in the folder '{input_folder}'. Please provide a folder containing PDF files.")
    return input_folder

def get_output_folder(output_folder):
    if not output_folder:
        raise ValueError("The output folder path cannot be empty. Please provide a valid folder path.")
    output_folder = os.path.normpath(output_folder)
    if len(output_folder) > 260:
        raise ValueError("The output folder path is too long. It cannot exceed 260 characters.")
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except Exception as e:
            raise ValueError(f"Error occurred: {e}")
    return output_folder

def get_image_format(image_format_input):
    valid_formats = ['PNG', 'JPEG', 'JPG', 'TIFF', 'BMP']
    if image_format_input.upper() not in valid_formats:
        raise ValueError(f"Invalid format. Please choose from: {', '.join(valid_formats)}.")
    return image_format_input.upper()

def get_dpi(dpi_input):
    try:
        dpi = int(dpi_input)
        if 1 <= dpi <= 500:
            return dpi
        else:
            raise ValueError("DPI must be between 1 and 500.")
    except ValueError:
        raise ValueError("Invalid input. Please enter a valid integer for DPI.")

def get_conf_threshold(conf_threshold_input):
    try:
        conf_threshold = float(conf_threshold_input)
        if 0.0 <= conf_threshold <= 1.0:
            return round(conf_threshold, 2)
        else:
            raise ValueError("Confidence threshold must be between 0.0 and 1.0.")
    except ValueError:
        raise ValueError("Invalid input. Please enter a valid number for the confidence threshold.")

def get_crop(crop_input):
    if isinstance(crop_input, str):
        if crop_input.strip().lower() == 'true':
            return True
        elif crop_input.strip().lower() == 'false':
            return False
        else:
            raise ValueError("Invalid input. Please enter 'True' or 'False'.")

def get_base_name(base_name_input):
    if not re.match(r'^[\w\s]+$', base_name_input):
        raise ValueError("Invalid base_name. Please ensure it contains only alphanumeric characters, underscores, and spaces.")
    if len(base_name_input) > 255:
        raise ValueError("The base_name is too long. Please ensure it doesn't exceed 255 characters.")
    return base_name_input

def get_start_index(start_index_input):
    try:
        start_index = int(start_index_input)
        if start_index >= 1:
            return start_index
        else:
            raise ValueError("Starting index must be greater than or equal to 1.")
    except ValueError:
        raise ValueError("Invalid input. Please enter a valid integer for the starting index.")

def crop_image(image, bbox):
    x1, y1, x2, y2 = bbox
    width, height = image.size
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(width, x2), min(height, y2)
    if x1 >= x2 or y1 >= y2:
        print("Invalid crop coordinates: Skipping crop.")
        return image
    return image.crop((x1, y1, x2, y2))

def detect_table(image, model, conf_threshold):
    results = model(image, verbose=False)
    table_bboxes = []
    for result in results:
        for box in result.boxes:
            conf = box.conf[0].item()
            cls_id = int(box.cls[0].item())
            if class_mapping.get(cls_id) == 'table' and conf > conf_threshold:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                table_bboxes.append((x1, y1, x2, y2))
    return table_bboxes

def pdf_to_images(model, input_folder, output_folder, image_format, dpi, conf_threshold, crop_images, base_name, start_index, pages):
    global total_tables
    try:
        images = convert_from_path(input_folder, dpi=dpi, first_page=pages[0] if pages else 1, 
                                   last_page=pages[-1] if pages else None, poppler_path=POPPLER_PATH)
        for image in images:
            table_bboxes = detect_table(image, model, conf_threshold)
            if crop_images:
                for bbox in table_bboxes:
                    cropped_image = crop_image(image, bbox)
                    output_image_path = os.path.join(output_folder, f"{base_name}_{start_index}.{image_format.lower()}")
                    cropped_image.save(output_image_path, image_format)
                    print(f"Table detected! Saved: {output_image_path}")
                    total_tables, start_index = total_tables + 1, start_index + 1
            else:
                if table_bboxes:
                    output_image_path = os.path.join(output_folder, f"{base_name}_{start_index}.{image_format.lower()}")
                    image.save(output_image_path, image_format)
                    print(f"Table detected in the page. Saved: {output_image_path}")
                    total_tables, start_index = total_tables + 1, start_index + 1
        return start_index
    except Exception as e:
        print(f"Error occurred: {e}")
        return start_index

def convert(model, input_folder, output_folder, image_format, dpi, conf_threshold, crop_images, base_name, start_index, pages_per_chunk=25):
    global total_pdfs
    for filename in os.listdir(input_folder):
        _, ext = os.path.splitext(filename)
        if ext.lower() == '.pdf':
            total_pdfs += 1
            pdf_path = os.path.join(input_folder, filename)
            print(f"\nConverting: {pdf_path}")
            try:
                with open(pdf_path, 'rb') as f:
                    reader = PdfReader(f)
                    if reader.is_encrypted:
                        try:
                            reader.decrypt(" ")
                        except:
                            continue
                    total_pages = len(reader.pages)
                for i in range(0, total_pages, pages_per_chunk):
                    pages = list(range(i + 1, min(i + pages_per_chunk, total_pages) + 1))
                    start_index = pdf_to_images(model, pdf_path, output_folder, image_format, dpi, conf_threshold, crop_images, base_name, start_index, pages)
            except Exception as e:
                print(f"Error occurred: {e}")
        else:
            print(f"Skipping non-PDF file: {filename}")
    print(f"\nA total of {total_tables} table images were extracted from {total_pdfs} PDF files.")

def main():
    try:
        parser = argparse.ArgumentParser(description="Extract tables from PDFs using YOLO.")
        parser.add_argument('input_folder', type=str, help='Path to the input folder containing PDF files')
        parser.add_argument('output_folder', type=str, help='Path to the output folder where images will be saved')
        parser.add_argument('--image_format', type=str, default='PNG', choices=['PNG', 'JPEG', 'JPG', 'TIFF', 'BMP'], help='Image format for saved images (default: PNG)')
        parser.add_argument('--dpi', type=int, default=75, help='DPI for PDF conversion (default: 75)')
        parser.add_argument('--conf_threshold', type=float, default=0.1, help='Confidence threshold for table detection (default: 0.1)')
        parser.add_argument('--crop_images', type=str, default='False', help='Whether to crop detected tables from images (default: False)')
        parser.add_argument('--base_name', type=str, default='image', help='Basename for output images (default: "image")')
        parser.add_argument('--start_index', type=int, default=1, help='Starting index for image filenames (default: 1)')
        parser.add_argument('--version', action='version', version=f'%(prog)s {_version_}')
        args = parser.parse_args()
        input_folder = get_input_folder(args.input_folder)
        output_folder = get_output_folder(args.output_folder)
        image_format = get_image_format(args.image_format)
        dpi = get_dpi(args.dpi)
        conf_threshold = get_conf_threshold(args.conf_threshold)
        crop_images = get_crop(args.crop_images)
        base_name = get_base_name(args.base_name)
        start_index = get_start_index(args.start_index)
        model = YOLO(MODEL_PATH)
        convert(model=model, input_folder=input_folder, output_folder=output_folder, 
                image_format=image_format, dpi=dpi, 
                conf_threshold=conf_threshold, crop_images=crop_images, 
                base_name=base_name, start_index=start_index)
    except ValueError as e:
        print(f"ValueError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()