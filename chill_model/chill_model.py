import torch
from torch import nn
import helper_functions
from chill_loader import ChillLoader

class ChillModel:
    def __init__(self,
                 model: nn.module,
                 train_dataloader: torch.utils.data.Dataloader,
                 test_dataloader: torch.utils.data.Dataloader,
                 problem_type: str,
                 is_custom: bool):
        """ Creates an instance of ChillModel. 
            Currently available problem types: [lin-reg, multi-class, binary-class]
        """
        self.train_dataloader = train_dataloader
        self.test_dataloader = test_dataloader
        self.problem_type = helper_functions.select_mode(problem_type)
        self.model = helper_functions.select_model(model, self.problem_type, is_custom)

    def  __call__(self, input):
        return self.model.fit(input)