# 🎬 CineMatch — Movie Recommendation System

A **content-based Movie Recommendation System** that recommends movies similar to a movie selected by the user.

The application is built using **Python and Streamlit** and uses **Cosine Similarity** to identify movies with similar features. Movie posters are dynamically fetched using the **TMDB API**.

## 🌐 Live Demo

👉 **[CineMatch — Movie Recommender](https://cinematchrecommendersystem.streamlit.app/)**

---

## 📌 Project Overview

Finding a movie to watch can be difficult when there are thousands of options available.

CineMatch solves this problem by allowing users to select a movie they already like and receiving a list of similar movies as recommendations.

The system uses pre-computed similarity scores to efficiently generate recommendations and integrates the TMDB API to display movie posters.

---

## ✨ Features

- 🎬 Movie selection through an interactive interface
- 🤖 Content-based movie recommendations
- 📊 Cosine Similarity for finding similar movies
- 🖼️ Movie posters fetched using TMDB API
- ⚡ Fast recommendations using pre-computed similarity data
- 🌙 Modern dark-themed Streamlit interface
- ☁️ Deployed using Streamlit Community Cloud

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and processing |
| Streamlit | Web application and user interface |
| Requests | API requests |
| Pickle | Saving and loading processed model data |
| TMDB API | Fetching movie information and posters |
| Git & GitHub | Version control and project hosting |
| Git LFS | Storing the large similarity model file |
| Streamlit Community Cloud | Deployment |

---

## 🧠 How the Recommendation System Works

The project follows a **content-based recommendation approach**.

### Workflow

```text
Movie Dataset
      ↓
Data Preprocessing
      ↓
Feature Extraction
      ↓
Feature Combination
      ↓
Cosine Similarity
      ↓
Similarity Matrix
      ↓
Save Model using Pickle
      ↓
Streamlit Application
      ↓
User Selects a Movie
      ↓
Top Similar Movies
      ↓
TMDB API → Movie Posters
```

When a user selects a movie:

1. The selected movie is identified from the movie dataset.
2. Its similarity scores are retrieved from the pre-computed similarity matrix.
3. Movies are sorted according to their similarity scores.
4. The top similar movies are selected.
5. Their posters are retrieved using the TMDB API.
6. The recommendations are displayed in the Streamlit application.
---
## 🔑 TMDB API

The application uses the **TMDB API** to retrieve movie poster information.

The API key is stored securely using Streamlit Secrets rather than directly inside the source code.

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.
### Live Application

👉 **https://cinematchmovie-recommender.streamlit.app/**
---

## 🎓 Project Objective

The main objective of this project is to develop a practical **Machine Learning-based recommendation system** and deploy it as an interactive web application.

The project demonstrates the complete workflow from:

**Data Processing → Machine Learning → Model Serialization → API Integration → Web Application → Cloud Deployment**

---

## 👩‍💻 Author

**Ishika Gupta**

B.Tech — Artificial Intelligence & Machine Learning

Manipal University Jaipur
---

## ⭐ Acknowledgements

- **TMDB** for providing movie information and poster data through its API.
- **Streamlit** for providing the framework used to build and deploy the web application.
- **GitHub & Git LFS** for version control and storage of the large model file.
