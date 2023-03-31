import onnx

# Load the ONNX model
model = onnx.load("C:/Users/25779/Desktop/DIAD/DIAD/DIAD/weight.onnx")

# Check that the model is well formed
onnx.checker.check_model(model)

# Print a human readable representation of the graph
print(onnx.helper.printable_graph(model.graph))
