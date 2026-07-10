
---
license: cc-by-nc-4.0
language: 
- vie
pretty_name: Vispamreviews
task_categories: 
- sentiment-analysis
tags: 
- sentiment-analysis
---


The dataset was collected from leading online shopping platforms in Vietnam. Some of the most recent
selling products for each product category were selected and up to 15 reviews per product were collected.
Each review was then labeled as either NO-SPAM, SPAM-1 (fake review), SPAM-2 (review on brand only), or
SPAM-3 (irrelevant content).


## Languages

vie

## Supported Tasks

Sentiment Analysis

## Dataset Usage
### Using `datasets` library
```
from datasets import load_dataset
dset = datasets.load_dataset("SEACrowd/vispamreviews", trust_remote_code=True)
```
### Using `seacrowd` library
```import seacrowd as sc
# Load the dataset using the default config
dset = sc.load_dataset("vispamreviews", schema="seacrowd")
# Check all available subsets (config names) of the dataset
print(sc.available_config_names("vispamreviews"))
# Load the dataset using a specific config
dset = sc.load_dataset_by_config_name(config_name="<config_name>")
```

More details on how to load the `seacrowd` library can be found [here](https://github.com/SEACrowd/seacrowd-datahub?tab=readme-ov-file#how-to-use).


## Dataset Homepage

[https://github.com/sonlam1102/vispamdetection/](https://github.com/sonlam1102/vispamdetection/)

## Dataset Version

Source: 1.0.0. SEACrowd: 2024.06.20.

## Dataset License

Creative Commons Attribution Non Commercial 4.0 (cc-by-nc-4.0)

## Citation

If you are using the **Vispamreviews** dataloader in your work, please cite the following:
```

@InProceedings{10.1007/978-3-031-21743-2_48,
author="Van Dinh, Co
and Luu, Son T.
and Nguyen, Anh Gia-Tuan",
editor="Nguyen, Ngoc Thanh
and Tran, Tien Khoa
and Tukayev, Ualsher
and Hong, Tzung-Pei
and Trawi{'{n}}ski, Bogdan
and Szczerbicki, Edward",
title="Detecting Spam Reviews on Vietnamese E-Commerce Websites",
booktitle="Intelligent Information and Database Systems",
year="2022",
publisher="Springer International Publishing",
address="Cham",
pages="595--607",
abstract="The reviews of customers play an essential role in online shopping.
People often refer to reviews or comments of previous customers to decide whether
to buy a new product. Catching up with this behavior, some people create untruths and
illegitimate reviews to hoax customers about the fake quality of products. These are called
spam reviews, confusing consumers on online shopping platforms and negatively affecting online
shopping behaviors. We propose the dataset called ViSpamReviews, which has a strict annotation
procedure for detecting spam reviews on e-commerce platforms. Our dataset consists of two tasks:
the binary classification task for detecting whether a review is spam or not and the multi-class
classification task for identifying the type of spam. The PhoBERT obtained the highest results on
both tasks, 86.89%, and 72.17%, respectively, by macro average F1 score.",
isbn="978-3-031-21743-2"
}


@article{lovenia2024seacrowd,
    title={SEACrowd: A Multilingual Multimodal Data Hub and Benchmark Suite for Southeast Asian Languages}, 
    author={Holy Lovenia and Rahmad Mahendra and Salsabil Maulana Akbar and Lester James V. Miranda and Jennifer Santoso and Elyanah Aco and Akhdan Fadhilah and Jonibek Mansurov and Joseph Marvin Imperial and Onno P. Kampman and Joel Ruben Antony Moniz and Muhammad Ravi Shulthan Habibi and Frederikus Hudi and Railey Montalan and Ryan Ignatius and Joanito Agili Lopo and William Nixon and Börje F. Karlsson and James Jaya and Ryandito Diandaru and Yuze Gao and Patrick Amadeus and Bin Wang and Jan Christian Blaise Cruz and Chenxi Whitehouse and Ivan Halim Parmonangan and Maria Khelli and Wenyu Zhang and Lucky Susanto and Reynard Adha Ryanda and Sonny Lazuardi Hermawan and Dan John Velasco and Muhammad Dehan Al Kautsar and Willy Fitra Hendria and Yasmin Moslem and Noah Flynn and Muhammad Farid Adilazuarda and Haochen Li and Johanes Lee and R. Damanhuri and Shuo Sun and Muhammad Reza Qorib and Amirbek Djanibekov and Wei Qi Leong and Quyet V. Do and Niklas Muennighoff and Tanrada Pansuwan and Ilham Firdausi Putra and Yan Xu and Ngee Chia Tai and Ayu Purwarianti and Sebastian Ruder and William Tjhi and Peerat Limkonchotiwat and Alham Fikri Aji and Sedrick Keh and Genta Indra Winata and Ruochen Zhang and Fajri Koto and Zheng-Xin Yong and Samuel Cahyawijaya},
    year={2024},
    eprint={2406.10118},
    journal={arXiv preprint arXiv: 2406.10118}
}

```