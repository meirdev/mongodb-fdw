import logging
from typing import Any, ClassVar, Iterable, Optional, TypedDict

import pymongo
import multicorn
from bson.objectid import ObjectId


logger = logging.getLogger("mongodb_fdw")

file_handler = logging.FileHandler("/var/log/mongodb_fdw.txt")
file_handler.setLevel(logging.DEBUG)

logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

logger.debug("loaded")


JSON = dict[str, Any]


class Options(TypedDict):
    host: str
    port: str
    username: str
    password: str
    db: str
    collection: str


class MongoDB(multicorn.ForeignDataWrapper):
    client: ClassVar[Optional[pymongo.MongoClient]] = None

    def __init__(self, options: Options, columns: dict[str, multicorn.ColumnDefinition]) -> None:
        super().__init__(options, columns)

        logger.debug("init: %s %s", options, columns)

        self.options = options
        self.columns = columns

        if MongoDB.client is None:
            logger.debug("connecting to MongoDB")

            MongoDB.client = pymongo.MongoClient(
                host=options["host"],
                port=int(options["port"]),
                username=options["username"],
                password=options["password"],
            )

        self.collection = MongoDB.client[options["db"]][options["collection"]]

    @property
    def rowid_column(self) -> str:
        return "_id"

    def insert(self, doc: JSON) -> JSON:
        logger.debug("insert: %s", doc)

        doc.pop("_id")

        doc_id = self.collection.insert_one(doc).inserted_id

        return {"_id": str(doc_id), **doc}

    def update(self, id: int, doc: JSON) -> JSON:
        logger.debug("update: %s %s", id, doc)

        doc.pop("_id")

        self.collection.update_one({"_id": ObjectId(id)}, {"$set": doc})

    def delete(self, id: int) -> None:
        logger.debug("delete: %s", id)

        self.collection.delete_one({"_id": ObjectId(id)})

    def execute(self, quals: list[multicorn.Qual], columns: list[str]) -> Iterable[JSON]:
        logger.debug("execute: %s %s", quals, columns)

        return self.collection.find()
