import cv2
import csv
import xml.etree.ElementTree as ET
import glob
import os
from fire import Fire


def write_kitti_label(filename, bboxes):
    with open(filename, 'wb') as f:
        writer = csv.writer(f, delimiter=' ')

        for bbox in bboxes:
            row = [bbox[0], 0.0, 0, 0] + bbox[1:] + [0] * 7
            writer.writerow(row)


# label_dir = '/data/barcodes/train_1/kitti_labels/'
# annotation_dir = '/data/barcodes/train_1/Annotations/'

def pascalvoc_to_kitti(annotation_dir, label_dir):
    """
    Converts pascal voc annotation files to kitti annotation format.
    Args:
        annotation_dir: Directory containing pascal voc annotations.
        label_dir: Directory where kitti annotations to be written.

    """
    annotation_files = glob.glob(annotation_dir + '*.xml')
    for ann_file in annotation_files:
        with open(ann_file) as f:
            tree = ET.parse(f)
            root = tree.getroot()
            all_objects = []
            for obj in root.iter('object'):
                current = list()
                name = obj.find('name').text
                xmlbox = obj.find('bndbox')
                xn = int(float(xmlbox.find('xmin').text))
                xx = int(float(xmlbox.find('xmax').text))
                yn = int(float(xmlbox.find('ymin').text))
                yx = int(float(xmlbox.find('ymax').text))
                current = [name, xn, yn, xx, yx]
                all_objects += [current]
            label_filename = os.path.basename(ann_file)
            label_filename = os.path.join(label_dir, label_filename[:label_filename.rfind('.')] + '.txt')
            write_kitti_label(label_filename, all_objects)


if __name__ == '__main__':
    Fire(pascalvoc_to_kitti)
