# Download meta_Books.json from http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ and put it under dataset/amazon/books

pipenv run python3 src/preprocess/scripts/amazon/generate_items_file.py

# subcategories do not exist in amazon dataset but we generate it in order to conform with mind config
cat dummy > dataset/amazon/books/processed/subcategories.txt

# Download local_train_splitByUser and local_test_splitByUser from DIEN repository (https://github.com/YafeiWu/DIEN) and put it under dataset/amazon/books
pipenv run python3 src/preprocess/scripts/amazon/generate_behavior_files.py

pipenv run preprocess params.dataset_name=amazon params.dataset_type=books target_jobs=[precompute_article_input_for_word_embedding] params.target_data_categories=[train] job_definitions.precompute_article_input_for_word_embedding.precompute_attributes=[title,body,category]

ln -s ${PWD}/dataset/amazon/books/processed/train/article_inputs_word_embedding.pkl ${PWD}/dataset/amazon/books/processed/valid/article_inputs_word_embedding.pkl

#TRAIN
#pipenv run python3 -m src.train.main  dataset_name=amazon dataset_type=books hparams.n_negatives=1 model=perceiver_io hparams.word_pos_emb=True hparams.feat_type_emb=True  hparams.article_attributes=[title,body,category] dataset=precomputed
