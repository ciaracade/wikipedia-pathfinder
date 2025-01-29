# 📚 Wikipedia Pathfinder  
**Find the shortest hyperlinked path between any two Wikipedia pages**  

![Wikipedia Pathfinder](https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Wikipedia-logo-transparent.png/200px-Wikipedia-logo-transparent.png)
---

## 📝 Project Overview  
Wikipedia Pathfinder is a graph-based tool for finding the shortest hyperlink path between two Wikipedia pages. To optimize performance, Neo4j is used for graph storage, FastAPI for querying, and Redis for caching.  

---

## 🚀 Features  
✅ **Shortest Path Algorithm** (BFS & A*)  
✅ **Graph Database Storage** (Neo4j)  
✅ **Fast Query Caching** (Redis)  
✅ **REST API** for developer access  
✅ **Interactive Web UI** (React + D3.js)  
✅ **Scalable & Cloud-Deployable**  

---

## 🛠️ Tech Stack  
| Component      | Technologies |
|---------------|-------------|
| **Backend**   | FastAPI (Python) |
| **Graph DB**  | Neo4j |
| **Caching**   | Redis |
| **Frontend**  | React + D3.js |
| **Data Source** | Wikipedia API & Wikipedia Dumps |
| **Deployment** | Docker, AWS/GCP |

---

## 🛠️ Installation & Setup  
### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/yourusername/wikipedia-pathfinder.git
cd wikipedia-pathfinder
```

### 2️⃣ Set Up Backend  
#### Install Dependencies  
```bash
cd backend
pip install -r requirements.txt
```

#### Start Neo4j Database  
```bash
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest
```
- **Neo4j UI:** [http://localhost:7474](http://localhost:7474)

#### Set Up Redis Cache  
```bash
docker run -d --name redis -p 6379:6379 redis
```

#### Run Backend API  
```bash
uvicorn backend.api:app --reload
```
- **API URL:** `http://localhost:8000`

---

### 3️⃣ Set Up Frontend  
```bash
cd frontend
npm install
npm start
```
- **Frontend URL:** `http://localhost:3000`

---

## 🔗 API Endpoints  
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/shortest-path?start={A}&end={B}` | Finds the shortest path between two Wikipedia pages |
| `GET`  | `/cached-path?start={A}&end={B}` | Returns cached path if available |
| `GET`  | `/random-path` | Suggests a random Wikipedia connection |

Example request:  
```bash
curl "http://localhost:8000/shortest-path?start=Banana&end=Albert_Einstein"
```

Example response:  
```json
{
    "start": "Banana",
    "end": "Albert_Einstein",
    "path": ["Banana", "Fruit", "Biology", "Physics", "Albert_Einstein"],
    "cached": false
}
```

---

## 🖥️ Deployment  
### Containerize with Docker  
#### 1. Build Docker Images  
```bash
docker build -t wikipedia-pathfinder-backend ./backend
docker build -t wikipedia-pathfinder-frontend ./frontend
```

#### 2. Run Containers  
```bash
docker-compose up -d
```

---

## 📜 License  
This project is open-source and available under the **MIT License**.  
