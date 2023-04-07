import torch
from torch import nn
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
import lightning.pytorch as pl
from . import helper_functions

class ChillModel:
    def __init__(self,
                 model: nn.Module,
                 train_dataloader: DataLoader,
                 test_dataloader: DataLoader,
                 problem_type: str,
                 forward_override: bool,
                 optim: nn.Module = None,
                 pretrained: bool = False,
                 lr: float = 1e-3):
        """ 
            Args:
                model: Torch model with layers initialized. 
                train_dataloader: Dataloader that can be received from using data_loading.py
                test_dataloader: Dataloader that can be received from using data_loading.py
                problem_type: Accepts problems types from [lin-reg, img-class, reg-class]
        """
        self.train_dataloader = train_dataloader
        self.test_dataloader = test_dataloader
        self.problem_type = helper_functions.select_mode(problem_type)
        self.model = helper_functions.select_model(model = model,
                                                   problem_type = self.problem_type,
                                                   forward_override = forward_override,
                                                   optim = optim,
                                                   lr = lr,
                                                   pretrained = pretrained)
        self.trainer = pl.Trainer()

    def train(self):
        self.trainer.fit(model = self.model, train_dataloaders = self.train_dataloader)
    
    def test(self):
        self.trainer.test(dataloaders = self.test_dataloader)

    def validate(self):
        trainer = pl.Trainer()
        trainer.validate(self.model)
    
    def predict(self, predict_dataloader: DataLoader):
        preds = self.trainer.predict(dataloaders = predict_dataloader)
        return preds
            

class DataLoaderError(Exception): pass
