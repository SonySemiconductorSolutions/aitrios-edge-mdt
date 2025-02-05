## 
<div align="center">
<figure>
<img src="docs/images/toolchain%20header%20image%20small.png" width="1000"
alt="Toolchain header" />
</figure>
</div>

# Edge AI Toolchain User Manual

## Introduction

The Edge AI Toolchain package installs all the packages that are
necessary for creating a model that can run on the IMX500 device.

<figure id="model-dev-flow">
<img src="docs/images/toolchain%20blocks.png"
alt="Flowchart showing the model development, conversion, and deployment flow from the framework environment to the AI Camera" />
<figcaption>Figure 1: Model development flow</figcaption>
</figure>

The Toolchain contains the following packages:

- [MCT](https://github.com/sony/model_optimization) (Model Compression
  Toolkit) - An open source python package for quantizing and
  compressing a neural network model, so that the model can be converted
  to run efficiently on the hardware device, while maintaining the
  accuracy of the model as close as possible to the original
  floating-point model.

- [IMX500
  Converter](https://developer.aitrios.sony-semicon.com/en/raspberrypi-ai-camera/documentation/imx500-converter)
  – A CLI application that converts (compiles) the neural network model
  that is the output of MCT (.onnx or .keras formats) into a binary file
  that can be loaded onto the device, and executed in real time.

- TPC (Target Platform Capabilities) - An open source package that
  contains descriptions for the various attributes (capabilities) of the
  target device’s hardware and software. MCT uses the relevant device
  description during its optimization process, such that the output
  model will be the best fit for the specific target device.

With the introduction of this AI Toolchain package, we are providing a
single installer that installs all the relevant packages for the user.
This simplifies the installation procedure for the user since the
installation can be done with single command. The installed packages are
still operated individually.

For regular usage, it is recommended to install only the AI Toolchain
package and avoid individual installation of the each dependent package.

In case of separate installation of individual dependent packages, it is
the user’s responsibility to make sure the relevant packages versions
are compatible with each other. Such installation may require manual
setup, and is not guaranteed to work without issues.

## How to use the Toolchain

Typical use of the Toolchain:

- Take an off-the-shelf or custom, pre-trained **floating point** model,
  in the **framework environment** (Tensorflow or PyTorch)

- Use **MCT** to quantize and compress the floating point model, and
  export it

- Use **Converter** to convert the output of MCT to a binary image that
  can be packaged and loaded onto the device

The figure [Model development flow](#model-dev-flow) shows the entire
development and deployment flow, and where MCT and the Converter fit as
part of the entire flow. After using the Converter, the user should use
the Converter’s output as input to the
[Packager](https://developer.aitrios.sony-semicon.com/en/raspberrypi-ai-camera/documentation/imx500-packager).
The Packager packs the converted model with additional information for
deployment on the target device.

For further information about MCT and Converter, please refer to the
relevant use manuals.

Note: The Packager component is not part of the Toolchain and is out of
scope of this manual

### Install parameters

The Toolchain package takes a parameter to select between installing the
Pytorch or Tensorflow version of it.  

If you are using Pytorch:

    $ pip install imx500_ai_toolchain[pt]

if you are using Tensorflow:

    $ pip install imx500_ai_toolchain[tf]

### Advanced installation cases

There could be few scenarios in which the user might want to perform a
special installation.

For example: if the user needs to install both pytorch and Tensorflow
versions on the same machine, or if the user needs to install a
combination of the Toolchain packages that is different from the
combination that comes with the Toolchain package.

In such cases of special installation we strongly recommend doing so in
separate Python virtual environments (for example, using
`python -m venv <virtual-environment-name>`). This avoids problems where
there are conflicts between packages or versions.

## System Requirements

The system running the neural network converter should at least meet the
requirements:

- RAM: 4 GB

- Python: {version-python}

- JVM 17

- OS: Tested and verified with Ubuntu 20.04 and 22.04.

<!-- -->

Raspberry Pi 4+

- RAM: 4 GB

- Python: {version-python}

- JVM 17

### Supported frameworks

| **Framework** | **Tested FW versions** | **Tested Python versions** | **Serialization** | **Opset** |
|----|----|----|----|----|
| PyTorch | 2.2-2.5 | 3.9-3.11 | .onnx | 15-20 |
| TensorFlow | 2.12-2.15 | 3.9-3.11 | .keras |  |

## Framework extensions

The AI Toolchain is making use of several framework extensions. The
extensions are installed as dependent libraries of the MCT and Converter
packages:

- [MCTQ](https://github.com/sony/mct_quantizers) – An open source python
  library of quantization layers and classes that is used by MCT for
  adding quantization to a network. The user does not need to directly
  make use of this library.

- [Custom layers](https://github.com/sony/custom_layers) – An open
  source python library containing several post processing layers. Users
  can choose to replace specific layers in existing model that cannot be
  converted otherwise with one of the available custom layers, in order
  to allow the model to convert onto the hardware device.
