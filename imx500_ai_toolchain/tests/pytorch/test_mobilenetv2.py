import os
import tempfile
import time
from torch.utils.data import DataLoader
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
from torchvision.datasets import ImageNet

from imx500_ai_toolchain.tests.convert import convert_model
from imx500_ai_toolchain.tests.download_dataset import get_ds_path
import model_compression_toolkit as mct


def get_representative_dataset(dataset_folder: str, batch_size: int, n_iter: int):
    dataset = ImageNet(root=dataset_folder, split='val', transform=MobileNet_V2_Weights.IMAGENET1K_V2.transforms())
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    def representative_dataset_gen():
        dataloader_iter = iter(dataloader)
        for _ in range(n_iter):
            yield [next(dataloader_iter)[0]]

    return representative_dataset_gen


def run_quantization(output_folder: str, batch_size: int = 16, n_iter: int = 10) -> str:
    representative_dataset_gen = get_representative_dataset(
        dataset_folder=get_ds_path(),
        batch_size=batch_size,
        n_iter=n_iter
    )

    float_model = mobilenet_v2(weights=MobileNet_V2_Weights.IMAGENET1K_V2)

    target_platform_cap = mct.get_target_platform_capabilities('pytorch', 'default')

    quantized_model, quantization_info = mct.ptq.pytorch_post_training_quantization(
        in_module=float_model,
        representative_data_gen=representative_dataset_gen,
        target_platform_capabilities=target_platform_cap
    )

    output_path = os.path.join(output_folder, 'mobilenetv2_quantized.onnx')
    mct.exporter.pytorch_export_model(quantized_model, save_model_path=output_path, repr_dataset=representative_dataset_gen)

    return os.path.abspath(output_path)


def test_mobilenet_v2():
    start_time = time.time()
    with tempfile.TemporaryDirectory() as tempdir:
        quantized_model_path = run_quantization(tempdir)
        convert_model(quantized_model_path)
    end_time = time.time()
    print(f"Quantized and converted MobileNetV2 in {end_time - start_time:.2f} seconds.")
