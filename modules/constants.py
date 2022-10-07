# noinspection PyUnresolvedReferences
"""Generates constants for use in camera.py.

>>> Constants

"""

Windows = """wmic path CIM_LogicalDevice where "Description like 'USB Video%'" get /value"""
Darwin = "system_profiler SPCameraDataType"
