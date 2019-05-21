# Use this script to convert Qt Creator UI and resource files to python
import os
import subprocess

input_path = os.path.join(os.path.dirname(__file__), 'resources', 'qt')
output_path = os.path.join(os.path.dirname(__file__), 'src', 'widgets')


def check_file(file):
    if 'All changes made in this file will be lost' in open(file).read():
        return True
    return False


for f in os.listdir(input_path):
    if not os.path.isfile(f):
        pass

    file_name, extension = os.path.splitext(f)

    if extension == '.ui':
        input_file = os.path.join(input_path, f)
        output_file = os.path.join(output_path, file_name + '.py')
        if os.path.isfile(output_file):
            if not check_file(output_file):
                print('Warning: tried to overwrite a file generated outside Qt Creator. {}'.format(output_file))
                continue
        subprocess.call('pyuic5 --import-from=widgets -x {} -o {}'.format(input_file, output_file), shell=True)
    elif extension == '.qrc':
        input_file = os.path.join(input_path, f)
        output_file = os.path.join(output_path, file_name + '_rc.py')
        if os.path.isfile(output_file):
            if not check_file(output_file):
                print('Warning: tried to overwrite a file generated outside Qt Creator. {}'.format(output_file))
                continue
        subprocess.call('pyrcc5 {} -o {}'.format(input_file, output_file), shell=True)

