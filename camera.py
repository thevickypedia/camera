import json
import subprocess
from typing import Dict, List
from xml.etree import ElementTree
import platform

import xmltodict

SYSTEM = platform.system()

Win32 = """wmic path CIM_LogicalDevice where "Description like 'USB Video%'" get /value"""
MacOS = "system_profiler -xml SPCameraDataType"


class Camera:
    """Initiates camera object to get information about the connected cameras.

    >>> Camera

    """

    def __init__(self):
        """Instantiates the camera object to run the OS specific builtin commands to get the camera information."""
        if SYSTEM == 'Darwin':
            cmd = MacOS
        else:
            cmd = Win32

        self.output, err = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).communicate()
        if error := err.decode(encoding='UTF-8'):
            raise SystemError(error)

    def get_camera_info_windows(self) -> List[Dict[str, str]]:
        """Get camera information for WindowsOS.

        Yields:
            List[Dict[str, str]]:
            Returns the information of all connected cameras as a list of dictionary.
        """
        output = list(
            filter(None, self.output.decode(encoding='UTF-8').splitlines()))  # Filter empty spaces in the list
        if not output:
            return

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

    def list_cameras_windows(self) -> List[str]:
        """Yields the camera name for WindowsOS.

        Yields:
            Names of the connected cameras.
        """
        info = self.get_camera_info_windows()
        for camera in info:
            yield camera.get('Name')

    def get_camera_info_darwin(self) -> Dict[str, Dict]:
        """Get camera information for macOS.

        Returns:
            Dict[str, Dict]:
            Returns the raw XML output as a dictionary.
        """
        ordered_dict = xmltodict.parse(self.output.decode())
        stringify = json.dumps(ordered_dict)
        return json.loads(stringify)

    def list_cameras_darwin(self) -> List[str]:
        """Yields the camera name for macOS.

        Yields:
            List[str]:
            Names of the connected cameras.
        """
        last_text = None
        try:
            parsed = ElementTree.fromstring(self.output).iterfind("./array/dict/array/dict/*")
        except ElementTree.ParseError:
            return
        for node in parsed:
            if last_text == "_name":
                yield node.text
            last_text = node.text

    def list_cameras(self) -> List[str]:
        """List of names of all cameras connected.

        Returns:
            List[str]:
            List of camera names.
        """
        if SYSTEM == 'Darwin':
            return list(self.list_cameras_darwin())
        return list(self.list_cameras_windows())


if __name__ == '__main__':
    print(Camera().list_cameras())
