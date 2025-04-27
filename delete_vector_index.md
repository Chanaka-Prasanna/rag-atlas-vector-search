# How to Delete a MongoDB Atlas Search Index

First, you must install `jq` because it is needed to extract the index ID.

Install jq:

- Ubuntu/macOS:
  ```bash
  sudo apt install jq
  ```

- Windows (with Chocolatey):
  ```bash
  choco install jq
  ```

Or download manually from: https://stedolan.github.io/jq/

---

## Steps

You need these details:

- Cluster Name: `<CLUSTER_NAME>`
- Database Name: `<DATABASE_NAME>`
- Collection Name: `<COLLECTION_NAME>`
- Index Name: `<INDEX_NAME>`

---

## Command
Run using  `bash` terminal
```bash
INDEX_ID=$(atlas clusters search indexes list \
--clusterName <CLUSTER_NAME> \
--db <DATABASE_NAME> \
--collection <COLLECTION_NAME> \
--output=json | \
jq '.[] | select(.name=="<INDEX_NAME>") .indexID' | \
tr -d '"')

atlas clusters search indexes delete $INDEX_ID \
--clusterName <CLUSTER_NAME>
```

---

## Example

If your details are:

- Cluster Name: `genai`
- Database Name: `book_mongodb_chunks`
- Collection Name: `chunked_data`
- Index Name: `vector_index`

Then the command will be:

```bash
INDEX_ID=$(atlas clusters search indexes list \
--clusterName genai \
--db book_mongodb_chunks \
--collection chunked_data \
--output=json | \
jq '.[] | select(.name=="vector_index") .indexID' | \
tr -d '"')

atlas clusters search indexes delete $INDEX_ID \
--clusterName genai
```

---

# Notes

- Make sure jq is installed.
- Replace placeholders with your actual cluster/database/collection/index names.
- Deleting a search index is permanent.
