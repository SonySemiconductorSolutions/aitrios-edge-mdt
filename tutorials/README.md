# EdgeMDT Tutorials
The notebooks in this tutorial demonstrate how to use EdgeMDT tools,
to quantize models with MCT and to convert them for IMX500 using the SDSP Converter.

#### Python Version Downgrade for Google Colab (as of December 2025)

The default Python version in Google Colab (3.12 or later) does not support TensorFlow 2.15 or earlier and Custom layers 0.3.0.
If you want to run tutorials that use them, please downgrade to Python 3.11 by following these steps:

1. In your Colab notebook, select **Runtime** → **Change runtime type** from the menu

2. In the "Change runtime type" dialog, set **Runtime version** to `2025.07`

## Tutorials

### Keras Tutorials

  | Model                                                                      |
  |----------------------------------------------------------------------------|
  | [MobileNetV2](keras_mobilenetv2.ipynb)                                     |

### Pytorch Tutorials

  | Model                                                                      |
  |----------------------------------------------------------------------------|
  | [MobileNetV2](pytorch_mobilenetv2.ipynb)                                   |
  | [ShuffleNetV2](pytorch_shufflenetv2.ipynb)                                 |
