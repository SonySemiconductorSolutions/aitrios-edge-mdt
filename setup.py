# -------------------------------------------------------------------------------
# (c) Copyright 2025 Sony Semiconductor Israel, Ltd. All rights reserved.
#
#      This software, in source or object form (the "Software"), is the
#      property of Sony Semiconductor Israel Ltd. (the "Company") and/or its
#      licensors, which have all right, title and interest therein, You
#      may use the Software only in accordance with the terms of written
#      license agreement between you and the Company (the "License").
#      Except as expressly stated in the License, the Company grants no
#      licenses by implication, estoppel, or otherwise. If you are not
#      aware of or do not agree to the License terms, you may not use,
#      copy or modify the Software. You may use the source code of the
#      Software only for your internal purposes and may not distribute the
#      source code of the Software, any part thereof, or any derivative work
#      thereof, to any third party, except pursuant to the Company's prior
#      written consent.
#      The Software is the confidential information of the Company.
# -------------------------------------------------------------------------------
from setuptools import setup, find_packages
import os


def get_env(name, default=None):
    value = os.environ.get(name, default)
    if not value:
        print(f'{name} environment variable is not set')
        exit(1)
    return value

dev_version = "0.0.0.dev0"
version = get_env('EDGE_MDT_VERSION', dev_version)
is_dev = version == dev_version or "dev" in version
imx500_dev_def_version = "3.14.3" if is_dev else None
imx_500_converter_version = get_env('IMX500_CONVERTER_VERSION', imx500_dev_def_version)
mct_dev_def_version = "2.1.1" if is_dev else None
mct_version = get_env('MCT_VERSION', mct_dev_def_version)


setup(
    name='edge-mdt',
    version=version,
    packages=find_packages(),
    install_requires=[f"model-compression-toolkit=={mct_version}",
                      f'imx500-converter=={imx_500_converter_version}'],
    extras_require={
        'pt': [f'imx500-converter[pt]=={imx_500_converter_version}'],
        'tf': [f'imx500-converter[tf]=={imx_500_converter_version}']
    },
)