import subprocess
from xml.etree import ElementTree


def list_cameras_darwin():
    flout, _ = subprocess.Popen(
        "system_profiler -xml SPCameraDataType",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()

    last_text = None

    for node in ElementTree.fromstring(flout).iterfind("./array/dict/array/dict/*"):
        if last_text == "_name":
            yield node.text
        last_text = node.text


def get_camera_info_windows() -> list:
    output, err = subprocess.Popen(
        """wmic path CIM_LogicalDevice where "Description like 'USB Video%'" get /value""",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()
    output = list(filter(None, output.decode(encoding='UTF-8').splitlines()))  # Filter empty spaces in the list

    # Split indices at the required value where the list as to be split and rebuilt as a new one
    split_indices = [index + 1 for index, val in enumerate(output) if val.startswith('SystemName')]

    # Rebuild the new list split at the given index value
    split_list = [output[i: j] for i, j in
                  zip([0] + split_indices,
                      split_indices + ([len(output)] if split_indices[-1] != len(output) else []))]

    for list_ in split_list:
        values = {}
        for sub_list in list_:
            values[sub_list.split('=')[0]] = sub_list.split('=')[1]
        yield values


if __name__ == '__main__':
    print(list(list_cameras_darwin()))
