from torchvision import transforms
from ts.torch_handler.image_classifier import ImageClassifier
import torch
import numpy as np
import json
import base64
import cv2

class PillClassifier(ImageClassifier):
    """
    MNISTDigitClassifier handler class. This handler extends class ImageClassifier from image_classifier.py, a
    default handler. This handler takes an image and returns the number in that image.
    Here method postprocess() has been overridden while others are reused from parent class.
    """
    def __init__(self):
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        with open('/home/model-server/pretrain/graph_data.json', 'r') as f:
            graph_data_json = json.load(f)
            self.graph_data = np.array(graph_data_json['graph'], dtype=np.float32)

    image_processing = transforms.Compose([transforms.Resize((224, 224)),
                                        transforms.ToTensor(),
                                        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.485, 0.456, 0.406])])

    def postprocess(self, data):
        """The post process of MNIST converts the predicted output response to a label.
        Args:
            data (list): The predicted output from the Inference with probabilities is passed
            to the post-process function
        Returns:
            list : A list of dictionaries with predictions and explanations is returned
        """
        pill_ids = data.argmax(1).tolist()
        result = []

        with open('/home/model-server/pretrain/index_to_name.json', 'r') as f:
            class_names = json.load(f)
            result = [{ "pill_id": pill_id,
                        "pill_label": class_names[str(pill_id)]
                      } for pill_id in pill_ids]

        print(result)
        return result

    def preprocess(self, data):
        """
        Preprocess function to convert the request input to a tensor(Torchserve supported format).
        The user needs to override to customize the pre-processing

        Args :
            data (list): List of the data from the request input.

        Returns:
            tensor: Returns the tensor data of the input
        """
        # print('HJHJHJHJ')
        # print(data)
        file = data[0]['body']
        file = json.loads(file)
        # print(f'FILE: {file}')
  
        base64_image_blob = np.fromstring(base64.b64decode(file['image']), np.uint8)
        image = cv2.imdecode(base64_image_blob, cv2.IMREAD_COLOR)
        image = np.transpose(image).astype(np.float32) / 255
        print(f'Image shape: {image.shape}')

        graph = self.graph_data

        img_tensor = torch.from_numpy(image).unsqueeze(0).to(self.device)
        graph_tensor = torch.from_numpy(graph).to(self.device)

        return img_tensor, graph_tensor

    def inference(self, data, *args, **kwargs):
        """
        The Inference Function is used to make a prediction call on the given input request.
        The user needs to override the inference function to customize it.

        Args:
            data (Torch Tensor): A Torch Tensor is passed to make the Inference Request.
            The shape should match the model input shape.

        Returns:
            Torch Tensor : The Predicted Torch Tensor is returned in this function.
        """
        x, graph_embedding = data
        marshalled_x = x.to(self.device)
        marshalled_g = graph_embedding.to(self.device)
        with torch.no_grad():
            results = self.model(marshalled_x, marshalled_g, *args, **kwargs)

        return results
