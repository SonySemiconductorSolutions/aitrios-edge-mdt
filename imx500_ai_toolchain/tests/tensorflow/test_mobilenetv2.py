import os
import tensorflow as tf
import keras
import model_compression_toolkit as mct
from keras.applications.mobilenet_v2 import MobileNetV2
from typing import Generator
import time
import tempfile

from imx500_ai_toolchain.tests.download_dataset import get_ds_path
from imx500_ai_toolchain.tests.convert import convert_model



def imagenet_preprocess_input(images, labels):
    return tf.keras.applications.mobilenet_v2.preprocess_input(images), labels

def get_representative_dataset(representative_dataset_folder: str, batch_size: int, n_iter: int) -> Generator:
    print('Loading dataset, this may take a few minutes...')
    dataset = tf.keras.utils.image_dataset_from_directory(
        directory=representative_dataset_folder,
        batch_size=batch_size,
        image_size=[224, 224],
        shuffle=False,
        crop_to_aspect_ratio=True,
        interpolation='bilinear'
    )

    dataset = dataset.map(lambda x, y: (imagenet_preprocess_input(x, y)))

    def representative_dataset() -> Generator:
        for _ in range(n_iter):
            yield dataset.take(1).get_single_element()[0].numpy()

    return representative_dataset

def run_quantization(output_folder: str, batch_size: int = 50, n_iter: int = 10) -> str:
    representative_dataset_gen = get_representative_dataset(
        representative_dataset_folder=get_ds_path(),
        batch_size=batch_size,
        n_iter=n_iter
    )

    float_model = MobileNetV2()

    tpc = mct.get_target_platform_capabilities("tensorflow", 'imx500', target_platform_version='v1')

    q_config = mct.core.QuantizationConfig(
        activation_error_method=mct.core.QuantizationErrorMethod.MSE,
        weights_error_method=mct.core.QuantizationErrorMethod.MSE,
        weights_bias_correction=True,
        shift_negative_activation_correction=True,
        z_threshold=16
    )

    ptq_config = mct.core.CoreConfig(quantization_config=q_config)

    quantized_model, quantization_info = mct.ptq.keras_post_training_quantization(
        in_model=float_model,
        representative_data_gen=representative_dataset_gen,
        core_config=ptq_config,
        target_platform_capabilities=tpc
    )

    float_model.compile(loss=keras.losses.SparseCategoricalCrossentropy(), metrics=["accuracy"])
    quantized_model.compile(loss=keras.losses.SparseCategoricalCrossentropy(), metrics=["accuracy"])

    output_path = os.path.join(output_folder, './mobilenetv2.keras')
    mct.exporter.keras_export_model(model=quantized_model, save_model_path=output_path)

    return os.path.abspath(output_path)


def test_mobilenet_v2():
    start_time = time.time()
    with tempfile.TemporaryDirectory() as tempdir:
        quantized_model_path = run_quantization(tempdir)
        convert_model(quantized_model_path)
    end_time = time.time()
    print(f"Quantized and converted MobileNetV2 in {end_time - start_time:.2f} seconds.")