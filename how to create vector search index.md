
# 🎯 Creating a Vector Index in MongoDB Atlas using Atlas CLI

---

## 📄 Step 1: Create a JSON File for the Index Definition

First, create a JSON file that defines the fields and settings for your vector index.

**File Name:** `search_index.json`

### Sample Content
```json
{
  "collectionName": "<your-collection-name>",
  "database": "<your-database-name>",
  "type": "vectorSearch",
  "name": "<your-index-name>",
  "fields": [
    {
      "numDimensions": <number-of-dimensions>,
      "path": "<vector-field-path>",
      "similarity": "cosine",
      "type": "vector"
    },
    {
      "path": "<filter-field-path>",
      "type": "filter"
    }
  ]
}
```

### 🔹 Description of placeholders:
- `<your-collection-name>` : Name of your MongoDB collection.
- `<your-database-name>` : Name of your MongoDB database.
- `<your-index-name>` : Name you want to assign to the search index.
- `<number-of-dimensions>` : Dimension size of your vector embeddings (example: 1536).It vary according to the model you use. Just check the documentation
- `<vector-field-path>` : Field path where vector embeddings are stored.
- `<filter-field-path>` : Field path for additional filtering (example: a boolean or categorical field).

> 💾 Save this file in your project folder.

---

## 🛠️ Step 2: Run Atlas CLI Command to Create the Index

Once the `search_index.json` file is ready, run the following command in your terminal:

```bash
atlas deployments search indexes create \
  --deploymentName <your-deployment-name> \
  --file search_index.json \
  --output json \
  --type ATLAS \
  --watch
```

### 🔹 Description of placeholders:
- `<your-deployment-name>` : Name of your MongoDB Atlas Cluster (deployment).

### ⚡ Important Notes:
- Ensure the `atlas` CLI is installed and authenticated properly.
- Ensure you are running the command from the folder where `search_index.json` exists.
- If the file is in a different location, provide the correct relative or absolute path.

---

## 📌 Example Command (for understanding only):

```bash
atlas deployments search indexes create --deploymentName genai --file search_index.json --output json --type ATLAS --watch
```

(Replace placeholders with your real data!)

---

## ✅ Done!
Your vector search index will be created and ready to use!
