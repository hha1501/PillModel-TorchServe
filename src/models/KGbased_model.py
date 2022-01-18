import torch
import torch.nn as nn
import json
import numpy as np
# from models.modules import ImageEncoder
from torchvision import models


class KGBasedModel(nn.Module):
    class ImageEncoder(nn.Module):
        """
        Encode images to a fixed size vector
        """
        def __init__(self, model_name='resnet50', pretrained=True, trainable=True, image_num_classes=76):
            super().__init__()
            if model_name == "resnet50":
                self.model = models.resnet50(pretrained=pretrained)
                for param in self.model.parameters():
                    param.requires_grad = trainable
                self.img_num_classes = image_num_classes
                
                self.visual_features = self.model.fc.in_features

                self.model.fc = nn.Identity()
                self.classifier = nn.Linear(self.visual_features, image_num_classes)
        
        def forward(self, x):
            visual_embedding = self.model(x)
            y = self.classifier(visual_embedding)
            return visual_embedding, y

    def __init__(self, hidden_size=64, num_class=76):
        super().__init__()

        self.backbone = self.ImageEncoder()
        self.backbone.model = models.resnet50(pretrained=False)
        
        self.visual_features = self.backbone.model.fc.in_features

        self.backbone.model.fc = nn.Identity()
        self.backbone.classifier = nn.Linear(self.visual_features, 76)

        # self.backbone = self.setup_backborn_model()
        
        hidden_visual_features = self.visual_features

        self.projection = nn.Sequential(
            nn.Linear(hidden_visual_features, hidden_size * 2),
            nn.ReLU(),
            nn.Linear(hidden_size * 2, hidden_size),
            nn.ReLU(),
        ) 

        self.attention_dense = nn.Linear(hidden_size * 2, hidden_size)
        self.classifier = nn.Linear(hidden_size, num_class)

    
    # def setup_backborn_model(self):
    #     model = ImageEncoder()
    #     model.load_state_dict(torch.load('checkpoints/baseline_best.pt'))
    #     for param in model.parameters():
    #         param.requires_grad = False
        
    #     return model
    
    def forward(self, x, g_embedding):
        visual_embedding, pseudo_classifier_output = self.backbone.model(x), self.backbone.classifier(self.backbone.model(x))
        
        mapped_visual_embedding = self.projection(visual_embedding)
        # print(mapped_visual_embedding.shape)
        condensed_graph_embedding = torch.mm(pseudo_classifier_output, g_embedding)
        # print(condensed_graph_embedding.shape)
        # context attention module
        scores = torch.mm(mapped_visual_embedding, condensed_graph_embedding.t())
        # print(scores.shape)
        distribution = nn.Softmax(dim=-1)(scores)
        # print(distribution.shape)
        context_val = torch.mm(distribution, mapped_visual_embedding)
        # print(context_val.shape)
        context_and_visual_vec = torch.cat([context_val, mapped_visual_embedding], dim=-1)
        # print(context_and_visual_vec.shape)
        attention_vec = nn.Tanh()(self.attention_dense(context_and_visual_vec))
        # print(attention_vec.shape)

        output = self.classifier(attention_vec)
        return output


if __name__ == '__main__':
    # kg_based_model = KGBasedModel()
    # kg_based_model.load_state_dict(torch.load('checkpoints/kg_w_best.pt'))
    # x = torch.randn(32, 3, 224, 224)
    # # print(kg_based_model.g_embedding_np)
    # graph_embedding = torch.randn(76, 64)
    # output = kg_based_model(x, graph_embedding)
    # print(output.shape)

    def __get_g_embedding(path='data/condened_g_embedding_deepwalk_w.json'):
        g_embedding = json.load(open(path, 'r'))
        g_embedding_np = np.zeros((76, 64), dtype=np.float32)
        
        map_dict = json.load(open('data/mapdict.json', 'r'))

        for k, v in map_dict.items():
            g_embedding[v] = g_embedding[k]
            g_embedding.pop(k)

            g_embedding_np[v] = np.array(g_embedding[v])
        
        # print(g_embedding_np.shape)

        return g_embedding, g_embedding_np.tolist()

    g_embedding, g_embedding_np = __get_g_embedding()
    
    # json.dump(g_embedding_np, open('data/ebd.json', 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False, sort_keys=False)
    a = np.random.rand(3, 224, 224).tolist()
    json.dump(a, open('data/img.json', 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False, sort_keys=False)