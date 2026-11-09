"""Frozen vision-language encoders (image + text) used as the neural perception layer.

FLAIR (Silva-Rodriguez et al., Medical Image Analysis 2025; weights jusiro2/FLAIR) is a retina-specific
CLIP model trained with expert lesion descriptions, so its text tower can embed lesion concepts.
The FLAIR inference path mirrors MVLM04_WP1_Feature_Extraction.py (reference commit d6652d5), so image
embeddings computed here are identical to the cached MVLM04 features.
BiomedCLIP (microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224) is the general biomedical encoder.
All weights are loaded from the local Hugging Face cache only.
"""
import numpy as np
import torch
import torch.nn.functional as F


class _FlairProjection(torch.nn.Module):
    def __init__(self, d_in):
        super().__init__()
        self.projection = torch.nn.Linear(d_in, 512, bias=False)

    def forward(self, x):
        return F.normalize(self.projection(F.normalize(x, dim=-1)), dim=-1)


class FLAIR:
    HUB = "jusiro2/FLAIR"
    BERT = "emilyalsentzer/Bio_ClinicalBERT"

    def __init__(self, device="cpu", load_vision=True):
        import torchvision
        from huggingface_hub import hf_hub_download
        from safetensors.torch import load_file
        from transformers import AutoConfig, AutoTokenizer, BertModel

        self.device = device
        vision = torch.nn.Module()
        vision.model = torchvision.models.resnet50(weights=None)
        vision.model.fc = torch.nn.Identity()
        vision.projection_head_vision = _FlairProjection(2048)
        text = torch.nn.Module()
        text.model = BertModel(AutoConfig.from_pretrained(self.BERT, local_files_only=True), add_pooling_layer=True)
        text.projection_head_text = _FlairProjection(768)
        net = torch.nn.Module()
        net.vision_model, net.text_model = vision, text
        net.logit_scale = torch.nn.Parameter(torch.zeros(()))
        state = load_file(hf_hub_download(self.HUB, "model.safetensors", local_files_only=True))
        state = {k: v for k, v in state.items() if not k.endswith("position_ids")}
        missing, unexpected = net.load_state_dict(state, strict=False)
        missing = [k for k in missing if not k.endswith("position_ids")]
        if missing or unexpected:
            raise SystemExit(f"FLAIR weights mismatch: {missing[:3]} {unexpected[:3]}")
        self.net = net.eval().to(device)
        self.tok = AutoTokenizer.from_pretrained(self.BERT, local_files_only=True)
        self.tok.model_max_length = 77

    @staticmethod
    def preprocess(im):
        x = torch.from_numpy(np.asarray(im, dtype=np.float32) / 255.0).permute(2, 0, 1)
        h, w = x.shape[-2:]
        s = max(h, w) / 512
        x = F.interpolate(x[None], size=(int(h / s), int(w / s)), mode="bilinear", antialias=True, align_corners=False)[0]
        return F.pad(x, (0, 512 - x.shape[-1], 0, 512 - x.shape[-2]))

    @torch.inference_mode()
    def encode_image(self, batch):
        return self.net.vision_model.projection_head_vision(self.net.vision_model.model(batch.to(self.device))).float().cpu()

    @torch.inference_mode()
    def encode_text(self, prompts):
        out = []
        for p in prompts:  # one prompt per call (no padding), as FLAIR compute_text_embeddings
            t = self.tok([p], truncation=True, return_tensors="pt")
            hs = self.net.text_model.model(input_ids=t["input_ids"].to(self.device),
                                           attention_mask=t["attention_mask"].to(self.device),
                                           output_hidden_states=True).hidden_states
            emb = torch.stack([hs[1], hs[2], hs[-1]]).permute(1, 0, 2, 3).mean(2).mean(1)
            out.append(self.net.text_model.projection_head_text(emb))
        return torch.cat(out).float().cpu()


class BiomedCLIP:
    HUB = "hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224"

    def __init__(self, device="cpu", load_vision=True):
        import open_clip
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(self.HUB)
        self.model.eval().to(device)
        self.tok = open_clip.get_tokenizer(self.HUB)
        self.device = device

    @torch.inference_mode()
    def encode_image(self, batch):
        return F.normalize(self.model.encode_image(batch.to(self.device)).float(), dim=-1).cpu()

    @torch.inference_mode()
    def encode_text(self, prompts):
        return F.normalize(self.model.encode_text(self.tok(prompts).to(self.device)).float(), dim=-1).cpu()


ENCODER_CLASSES = {"flair": FLAIR, "biomedclip": BiomedCLIP}
