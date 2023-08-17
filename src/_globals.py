"""
Collection of global variables.

Authors: Soesja Brunink & Gijs G. Hendrickx
"""
import typing

# configuration dictionaries
LABEL_CONFIG = dict()
MODEL_CONFIG = dict()

# complex type-settings
TypeXYKeys = typing.Collection[typing.Tuple[float, float]]
TypeXYBool = typing.Dict[typing.Tuple[float, float], bool]
TypeXYLabel = typing.Dict[typing.Tuple[float, float], str]
TypeXY = typing.Union[
    TypeXYKeys,
    TypeXYBool,
    TypeXYLabel
]
