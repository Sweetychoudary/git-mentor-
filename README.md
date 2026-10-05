# 🧑‍💻 GitMentor

### AI-Powered GitHub Project Mentor

GitMentor is an AI-powered application that helps students and developers understand GitHub repositories more easily.

Instead of manually going through many files, users can provide a **public GitHub repository URL** and ask questions about the project. GitMentor analyzes the repository's source code and uses **Ollama + Llama 3.2** to provide simple explanations.

---

## ✨ Features

* 🔗 Analyze a public GitHub repository
* 📂 Extract source code from the repository
* 🤖 Ask questions about the project
* 💬 Get AI-generated explanations
* 🧑‍💻 Understand code in simple language
* 📄 Identify relevant files in explanations
* 🦙 Uses Llama 3.2 locally through Ollama
* 🖥️ Simple and interactive Streamlit interface

---

## 🏗️ How It Works

```text
GitHub Repository URL
        ↓
   GitHub API
        ↓
   Repository Files
        ↓
  Project Context
        ↓
   Ollama + Llama 3.2
        ↓
    AI Response
```

---

## 🛠️ Tech Stack

| Technology    | Purpose                           |
| ------------- | --------------------------------- |
| Python        | Application development           |
| Streamlit     | Web interface                     |
| GitHub API    | Repository and source-code access |
| Requests      | API communication                 |
| Ollama        | Local AI model interface          |
| Llama 3.2     | AI model                          |
| python-dotenv | Environment configuration         |

---

## 📂 Project Structure

```text
git-mentor/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── venv/
```

> `venv/` should not be uploaded to GitHub.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd git-mentor
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## 🦙 Ollama Setup

Install Ollama and download the Llama 3.2 model.

```bash
ollama pull llama3.2
```

Make sure Ollama is running before starting GitMentor.

---

## ▶️ Run the Application

Run:

```bash
python -m streamlit run app.py
```

The application will open in your browser.

---

## 💡 Example Questions

After analyzing a repository, you can ask:

```text
What does this project do?
```

```text
Explain this project like a beginner.
```

```text
What technologies are used?
```

```text
Explain app.py.
```

```text
Where is the main logic of the project?
```

```text
How does the application work?
```

```text
Why is Streamlit used in this project?
```

```text
Give me interview questions based on this project.
```

---

## 🔐 Privacy

GitMentor V1 uses **Ollama locally** for AI responses.

Only **public GitHub repositories** are intended to be analyzed in this version.

Do not upload or expose private credentials, API keys, passwords, or other sensitive information.

---

## 🚧 Current Version

### GitMentor V1

The current version uses repository source-code extraction and passes the collected project context to the Llama 3.2 model.

Current limitations include:

* Limited number of files analyzed
* Limited amount of code loaded from each file
* Works with supported source-file extensions
* Not yet using vector-based semantic retrieval

---

## 🔮 Future Improvements

### GitMentor V2 — RAG

Planned improvements:

* ✂️ Code-aware chunking
* 🧠 Embeddings
* 🗄️ ChromaDB vector database
* 🔍 Semantic code retrieval
* 📚 Better support for large repositories
* 🎯 More accurate answers

### GitMentor V3 — Advanced AI

Future features may include:

* 🏗️ Project architecture visualization
* 🐛 Bug detection
* 🧪 Test-case generation
* 📝 README generation
* 🔄 Git history analysis
* 🎤 Viva/interview mode
* 🤖 Agentic AI capabilities

---

## 🎯 Project Goal

GitMentor is designed to make GitHub projects easier to understand, especially for **students and beginners who are learning software development and AI**.

---

## 👩‍💻 Author

**C. Sweety Kumari**

B.Tech — Computer Science and Engineering

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

### 📌 Version

**GitMentor V1.0**
