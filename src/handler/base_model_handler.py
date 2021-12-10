from ts.torch_handler.base_handler import BaseHandler
import torch
import numpy as np

class BasePredictDailyHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


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
        # file = json.load(file)
        print(f'FILE: {file}')
        test_data = file['test_data']
        
        test_ls = []
        for k, v in test_data.items():
            test_ls.append(v)
        print(test_ls)

        test_np = np.transpose(np.array(test_ls, dtype=np.float32)[np.newaxis, :], (0, 2, 1))
        print(test_np.shape)

        test_tensor = torch.from_numpy(test_np).to(self.device)
        test_mean = test_tensor.mean(dim=1, keepdim=True)
        test_std = test_tensor.mean(dim=1, keepdim=True)

        return test_tensor, test_mean, test_std

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
        data, data_mean, data_std = data
        marshalled_data = data.to(self.device)
        marshalled_data_mean = data_mean.to(self.device)
        marshalled_data_std = data_std.to(self.device)
        # print(f'Marshalled Data: {marshalled_data}')
        with torch.no_grad():
            results = self.model(marshalled_data, marshalled_data_mean, marshalled_data_std, *args, **kwargs)

        return results
