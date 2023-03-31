import onnxruntime as ort
import numpy as np

ort_session = ort.InferenceSession("C:/Users/25779/Desktop/DIAD/DIAD/DIAD/weight.onnx", providers=['CUDAExecutionProvider'])

outputs = ort_session.run(
    None,
    {"images": np.random.randn(1, 3, 640, 640).astype(np.float32)},
)
print(outputs[0].shape)
