import torch
class ClassificationModel(torch.nn.Module):
    def __init__(self, news_encoder, n_classes,
                 loss_func = torch.nn.CrossEntropyLoss(), user_encoder=None):
        super().__init__()

        self.news_encoder = news_encoder
        self.user_encoder = user_encoder


        self.loss_func = loss_func
        self.n_classes = n_classes+1

        self.FCs = [torch.nn.Linear(self.news_encoder.output_dim, self.n_classes)] # TODO: parametrize output dim

    def prepare_for_CELoss(self, cand_embs):
        preds = []

        for FC in self.FCs:
            pred = FC.to(device=cand_embs.device)(cand_embs.type(torch.float32))
        preds.append(pred)
        
        return torch.cat(preds).squeeze()

    def loss_input(self, candidates):
        return self.prepare_for_CELoss(candidates)

    def forward(self, candidates, histories, __):

        embeddings = self.user_encoder(histories, self.news_encoder)
        
        if self.training:
            return self.loss_input(embeddings)
        else:
            return self.loss_input(embeddings).argmax(1)
