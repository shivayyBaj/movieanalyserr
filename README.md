# 🎬 Movie Analyzer AI 

An interactive AI-powered movie analysis web app built using **Streamlit + Deep Learning (RNN)**.
This application allows users to search movies, explore genres, and analyze sentiment of movie plots using a trained neural network.

---

## 🚀 Features

✨ **Smart Movie Search**

* Search movies with real-time suggestions
* Displays posters, ratings, and details

🎭 **Genre-Based Browsing**

* Select genres like Action, Comedy, Horror, etc.
* View latest movies by genre

🌍 **Industry Filter**

* Filter movies by:

  * Hollywood
  * Bollywood
  * Other

🎤 **Voice Search**

* Speak movie name using microphone
* Converts speech to text and fetches results

🧠 **AI Sentiment Analysis**

* Uses **Simple RNN (Recurrent Neural Network)**
* Predicts sentiment of movie plot:

  * Positive 😊
  * Negative 😞
  * Neutral 😐

🎯 **Movie Recommendations**

* Suggests similar movies based on genre

🎨 **Modern UI**

* Netflix-inspired dark theme
* Interactive cards and smooth animations

---

## 🧠 Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Deep Learning:** TensorFlow / Keras (SimpleRNN)
* **Dataset:** IMDb Movie Reviews
* **API:** OMDb API
* **Voice Recognition:** SpeechRecognition

---

## 📂 Project Structure

```
📦 movie-analyzer
 ┣ 📜 app.py
 ┣ 📜 simple_rnn_imdb.h5
 ┣ 📜 requirements.txt
 ┣ 📜 .env
 ┗ 📜 README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/shivayyBaj/movieanalyserr.git
cd movieanalyserr
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv myenv
myenv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add OMDb API Key

Create a `.env` file:

```
OMDB_API_KEY=your_api_key_here
```

Get API key from: http://www.omdbapi.com/

---

### 5️⃣ Run the App

```bash
streamlit run app.py
```

---

## 📊 How It Works

1. User selects/searches a movie
2. App fetches movie data using OMDb API
3. Movie plot is processed using NLP
4. RNN model predicts sentiment
5. Results + recommendations are displayed

---

## 🖼️ Screenshots (Optional)

*Add screenshots here for better presentation*

---

## 🔮 Future Improvements

* 🎯 Personalized recommendations (ML-based)
* 📊 Dashboard with analytics
* 🌐 Multi-language support
* ❤️ User login & watchlist
* 📱 Mobile responsive UI

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork this repo and submit a pull request.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

**Shivesh Bajpai**
📌 GitHub: https://github.com/shivayyBaj

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
