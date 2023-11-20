import os
# TODO: Declare environment variables here
# e.g. ENV_VAR = os.getenv("ENV_KEY", default=...)
ENTITY_FILE_LOCATION = os.getenv('ENTITY_FILE_LOCATION', "app/data/entity2id.txt")
RELATION_FILE_LOCATION = os.getenv('RELATION_FILE_LOCATION', "app/data/relation2id.txt")
TRAIN_FILE_LOCATION = os.getenv('TRAIN_FILE_LOCATION', "app/data/train2id.txt")

TEST_ENTITY_FILE_LOCATION = os.getenv('TEST_ENTITY_FILE_LOCATION', "tests/data/test_entity.txt")
TEST_RELATION_FILE_LOCATION = os.getenv('TEST_RELATION_FILE_LOCATION', "tests/data/test_relation.txt")
TEST_TRAIN_FILE_LOCATION = os.getenv('TEST_TRAIN_FILE_LOCATION', "tests/data/test_graph.txt")

