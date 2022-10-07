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
    return list(filter(None, output.decode(encoding='UTF-8').splitlines()))  # Filter empty spaces in the list


if __name__ == '__main__':
    print(list(list_cameras_darwin()))
