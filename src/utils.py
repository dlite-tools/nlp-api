"""Util functions."""
from typing import List
import nlpiper
import torch

from inference.architectures.text_classification import BaselineModel
from inference.data_processors.transformers.preprocessing import (
    NLPiperIntegration,
    VocabTransform
)


# Constants
MODEL_PATH = "ml/model.ckpt"
VOCABULARY_PATH = "ml/vocabulary.pth"
NEWS_CLASSIFICATION = {
    1: "World",
    2: "Sports",
    3: "Business",
    4: "Sci/Tec"
}
EMBED_DIM = 64

VOCAB_TRANSFORM = VocabTransform(torch.load(VOCABULARY_PATH))


def get_model() -> BaselineModel:
    """Load machine learning model.

    Returns
    -------
    BaselineModel
        Machine learning model to be used for inference.
    """
    model = BaselineModel(
        vocab_size=len(VOCAB_TRANSFORM),
        embed_dim=EMBED_DIM,
        num_class=len(NEWS_CLASSIFICATION)
    )
    model.load_from_checkpoint(MODEL_PATH)
    return model


def get_preprocessing() -> List:
    """Load preprocessing pipeline.

    Returns
    -------
    List
        Preprocessing pipeline steps to be applied before inference.
    """
    return [
        NLPiperIntegration(
            pipeline=nlpiper.core.Compose(
                [
                    nlpiper.transformers.cleaners.CleanPunctuation(),
                    nlpiper.transformers.tokenizers.BasicTokenizer(),
                    nlpiper.transformers.normalizers.CaseTokens(),
                ]
            )
        ),
        VOCAB_TRANSFORM
    ]
