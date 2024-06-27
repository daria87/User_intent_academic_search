import os
import fnmatch

def count_xml_files(directory):
    xml_count = 0
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, '*.xml'):
            if "volume" not in filename:
                xml_count += 1
    return xml_count

# Example usage:
directory_path = '../input/inex-1.4'
xml_file_count = count_xml_files(directory_path)
print(f"Number of XML files: {xml_file_count}")
