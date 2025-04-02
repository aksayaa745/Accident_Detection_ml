import os
import xml.etree.ElementTree as ET

# Define paths
xml_folder = "xml_folder"  # Change this to your XML folder name
output_folder = "yolo_labels"  # The folder where YOLO txt files will be saved
image_folder = "images"  # The folder where your images are stored

# Make output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# Define class names (must match your dataset labels)
class_names = ["accident", "helmet", "vehicle"]  # Add your classes here

# Convert XML to YOLO format
def convert_xml_to_yolo(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    img_name = root.find("filename").text
    img_path = os.path.join(image_folder, img_name)
    
    # Get image width & height
    size = root.find("size")
    img_w, img_h = int(size.find("width").text), int(size.find("height").text)

    yolo_lines = []
    
    for obj in root.findall("object"):
        class_name = obj.find("name").text
        if class_name not in class_names:
            continue
        
        class_id = class_names.index(class_name)
        bbox = obj.find("bndbox")
        
        x_min, y_min = int(bbox.find("xmin").text), int(bbox.find("ymin").text)
        x_max, y_max = int(bbox.find("xmax").text), int(bbox.find("ymax").text)

        # Normalize for YOLO format (center_x, center_y, width, height)
        x_center = (x_min + x_max) / (2 * img_w)
        y_center = (y_min + y_max) / (2 * img_h)
        bbox_w = (x_max - x_min) / img_w
        bbox_h = (y_max - y_min) / img_h

        yolo_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_w:.6f} {bbox_h:.6f}")

    # Save as YOLO txt
    txt_filename = os.path.join(output_folder, os.path.splitext(img_name)[0] + ".txt")
    with open(txt_filename, "w") as f:
        f.write("\n".join(yolo_lines))

# Process all XML files
for xml_file in os.listdir(xml_folder):
    if xml_file.endswith(".xml"):
        convert_xml_to_yolo(os.path.join(xml_folder, xml_file))

print("✅ XML to YOLO conversion complete! Check the 'yolo_labels' folder.")
 