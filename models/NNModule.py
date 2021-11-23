import torch
import torch.utils.data
from torch.utils.data import random_split
import torch.nn as nn

dropoutProb = 0.3


def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))

class Model(nn.Module):
    def __init__(self, in_size, layer_array=[512, 512, 256, 256], out_size=28):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(in_size, layer_array[0]),
            nn.ReLU(),
            nn.Dropout(dropoutProb),
            nn.Linear(layer_array[0], layer_array[1]),
            nn.ReLU(),
            nn.Dropout(dropoutProb),
            nn.Linear(layer_array[1], out_size)
        )

    def forward(self, xb):
        softmax = nn.Softmax(dim=0)
        return softmax(self.network(xb))

    def training_step(self, batch):
        values, labels, f_id = batch
        out = self(values)                  # Generate predictions
        loss = nn.functional.nll_loss(out, labels)  # Calculate loss
        return loss

    def validation_step(self, batch):
        values, labels, f_id = batch
        out = self(values)                    # Generate predictions
        loss = nn.functional.nll_loss(out, labels)   # Calculate loss
        acc = accuracy(out, labels)           # Calculate accuracy
        return {'val_loss': loss, 'val_acc': acc}

    def validation_epoch_end(self, outputs):
        batch_losses = [x['val_loss'] for x in outputs]
        epoch_loss = torch.stack(batch_losses).mean()   # Combine losses
        batch_accs = [x['val_acc'] for x in outputs]
        epoch_acc = torch.stack(batch_accs).mean()      # Combine accuracies
        return {'val_loss': epoch_loss.item(), 'val_acc': epoch_acc.item()}

    def epoch_end(self, epoch, result):
        print("Epoch [{}], val_loss: {:.4f}, val_acc: {:.4f}".format(
            epoch, result['val_loss'], result['val_acc']))
