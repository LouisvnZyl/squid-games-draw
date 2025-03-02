from Services.ImageEvaluationService import predict_image

prediction_result = predict_image("DrawnImages/drawing_output.png")

print(prediction_result)