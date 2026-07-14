import json
import datasets


logger = datasets.logging.get_logger(__name__)
_VERSION = "0.1.0"
_NAME = "tweet_sentiment_multilingual"
_DESCRIPTION = "Multilingual sentiment analysis dataset on Twitter."
_CITATION = """
@inproceedings{barbieri-etal-2022-xlm,
    title = "{XLM}-{T}: Multilingual Language Models in {T}witter for Sentiment Analysis and Beyond",
    author = "Barbieri, Francesco  and
      Espinosa Anke, Luis  and
      Camacho-Collados, Jose",
    booktitle = "Proceedings of the Thirteenth Language Resources and Evaluation Conference",
    month = jun,
    year = "2022",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2022.lrec-1.27",
    pages = "258--266",
    abstract = "Language models are ubiquitous in current NLP, and their multilingual capacity has recently attracted considerable attention. However, current analyses have almost exclusively focused on (multilingual variants of) standard benchmarks, and have relied on clean pre-training and task-specific corpora as multilingual signals. In this paper, we introduce XLM-T, a model to train and evaluate multilingual language models in Twitter. In this paper we provide: (1) a new strong multilingual baseline consisting of an XLM-R (Conneau et al. 2020) model pre-trained on millions of tweets in over thirty languages, alongside starter code to subsequently fine-tune on a target task; and (2) a set of unified sentiment analysis Twitter datasets in eight different languages and a XLM-T model trained on this dataset.",
}
"""
_HOMEPAGE = "https://github.com/cardiffnlp/xlm-t"
_BASE_URL = "https://huggingface.co/datasets/cardiffnlp/tweet_sentiment_multilingual/resolve/main/data"
_LANGUAGE = ["arabic", "english", "french", "german", "hindi", "italian", "portuguese", "spanish"]
_URLS = {l: {
    k: [f'{_BASE_URL}/{l}/{k}.jsonl'] for k in [str(datasets.Split.TEST), str(datasets.Split.TRAIN), str(datasets.Split.VALIDATION)]
} for l in _LANGUAGE}
_URLS['all'] = {k: [f'{_BASE_URL}/{l}/{k}.jsonl' for l in _LANGUAGE] for k in [str(datasets.Split.TEST), str(datasets.Split.TRAIN), str(datasets.Split.VALIDATION)]}


class TweetSentimentMultilingualConfig(datasets.BuilderConfig):
    """BuilderConfig"""

    def __init__(self, **kwargs):
        """BuilderConfig
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(TweetSentimentMultilingualConfig, self).__init__(**kwargs)


class TweetSentimentMultilingual(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        TweetSentimentMultilingualConfig(name=l, version=datasets.Version(_VERSION), description=_DESCRIPTION) for l in _LANGUAGE
    ]
    BUILDER_CONFIGS += [TweetSentimentMultilingualConfig(name='all', version=datasets.Version(_VERSION), description=_DESCRIPTION)]
    
    def _info(self):
        names = ["negative", "neutral", "positive"]
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"text": datasets.Value("string"), "label": datasets.features.ClassLabel(names=names)}
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION
        )

    def _split_generators(self, dl_manager):
        downloaded_file = dl_manager.download_and_extract(_URLS[self.config.name])
        return [datasets.SplitGenerator(name=i, gen_kwargs={"filepaths": downloaded_file[str(i)]})
                for i in [datasets.Split.TRAIN, datasets.Split.VALIDATION, datasets.Split.TEST]]

    def _generate_examples(self, filepaths):
        """This function returns the examples in the raw (text) form."""
        _key = 0
        for filepath in filepaths:
            logger.info("generating examples from = %s", filepath)
            with open(filepath, encoding="utf-8") as f:
                _list = f.read().split('\n')
                if _list[-1] == '':
                    _list = _list[:-1]
                for i in _list:
                    data = json.loads(i)
                    yield _key, data
                    _key += 1