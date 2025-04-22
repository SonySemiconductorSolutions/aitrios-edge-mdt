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
imx500_dev_def_version = "3.16.0" if is_dev else None
imx_500_converter_version = get_env('IMX500_CONVERTER_VERSION', imx500_dev_def_version)
mct_dev_def_version = "2.4.0" if is_dev else None
mct_version = get_env('MCT_VERSION', mct_dev_def_version)
tpc_dev_def_version = "1.1.0" if is_dev else None
tcp_version = get_env('TPC_VERSION', tpc_dev_def_version)
custom_layers_def_version = "0.3.0" if is_dev else None
custom_layers_version = get_env('CUSTOM_LAYERS_VERSION', custom_layers_def_version)
is_nightly = os.environ.get("IS_NIGHTLY", "true") == "true"
name = 'edge-mdt-nightly' if is_nightly else 'edge-mdt'

def get_log_description():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description


setup(
    name=name,
    long_description=get_log_description(),
    long_description_content_type="text/markdown",
    description='Edge AI Model Development Toolkit',
    version=version,
    packages=find_packages(),
    license="Apache-2.0",
    install_requires=[f"model-compression-toolkit~={mct_version}",
                      f"edge-mdt-tpc~={tcp_version}",
                      f'imx500-converter~={imx_500_converter_version}',
                      f'sony-custom-layers~={custom_layers_version}'
                      ],
    extras_require={
        'pt': [f'imx500-converter[pt]~={imx_500_converter_version}'],
        'tf': [f'imx500-converter[tf]~={imx_500_converter_version}']
    },
    classifiers=[
              "Programming Language :: Python :: 3",
              "Operating System :: OS Independent",
              "Topic :: Scientific/Engineering :: Artificial Intelligence"
          ],
    python_requires='>=3.9',
)
