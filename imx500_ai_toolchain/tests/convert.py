import os
import sys
import subprocess
import tempfile
import shutil

def convert_model(input_path, out_folder=None):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Path {input_path} does not exist.")
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Path {input_path} is not a file.")
    if not input_path.endswith(".keras") and not input_path.endswith(".onnx"):
        raise ValueError(f"File {input_path} is not a Keras or ONNX model.")

    is_tf = input_path.endswith(".keras")

    # Handle temporary output folder
    temp_out_folder = None
    if out_folder is None:
        temp_out_folder = tempfile.mkdtemp()
        out_folder = temp_out_folder

    cmd = ["imxconv-tf" if is_tf else "imxconv-pt",
           "-i", input_path,
           "-o", out_folder, "--overwrite-output"]

    env_bin_path = os.path.dirname(sys.executable)
    os.environ["PATH"] = f"{env_bin_path}:{os.environ['PATH']}"
    env = os.environ.copy()

    try:
        res = subprocess.run(cmd, env=env, check=True)
        assert res.returncode == 0

        output_files = os.listdir(out_folder)
        assert "packerOut.zip" in output_files
        assert "dnnParams.xml" in output_files
    finally:
        # Clean up temporary folder if created
        if temp_out_folder is not None:
            shutil.rmtree(temp_out_folder)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: convert.py <model_path> [out_folder]")
        sys.exit(1)

    input_path = sys.argv[1]
    out_folder = sys.argv[2] if len(sys.argv) == 3 else None

    convert_model(input_path, out_folder)
