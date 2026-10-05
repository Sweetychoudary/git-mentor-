import streamlit as st
import requests
import base64
import os

from dotenv import load_dotenv


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

st.set_page_config(
    page_title="GitMentor",
    page_icon="🧑‍💻",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🧑‍💻 GitMentor")

st.write(
    "Your AI mentor for understanding GitHub projects."
)

st.info(
    "Enter a public GitHub repository and ask questions "
    "about its code."
)


# =========================================================
# GITHUB FUNCTIONS
# =========================================================

def parse_github_url(url):

    url = url.strip()

    if url.endswith("/"):
        url = url[:-1]

    parts = url.split("/")

    if len(parts) < 5:
        return None, None

    owner = parts[3]
    repo = parts[4]

    if repo.endswith(".git"):
        repo = repo[:-4]

    return owner, repo


def get_repository_contents(owner, repo):

    api_url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/git/trees/main?recursive=1"
    )

    response = requests.get(api_url)

    # Try master branch if main doesn't exist
    if response.status_code != 200:

        api_url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/git/trees/master?recursive=1"
        )

        response = requests.get(api_url)

    if response.status_code != 200:
        return None, f"GitHub Error: {response.status_code}"

    data = response.json()

    return data.get("tree", []), None


# =========================================================
# FILE FILTER
# =========================================================

SUPPORTED_EXTENSIONS = (
    ".py",
    ".java",
    ".js",
    ".ts",
    ".html",
    ".css",
    ".cpp",
    ".c",
    ".sql",
    ".json",
    ".md"
)


def is_supported_file(filename):

    return filename.lower().endswith(
        SUPPORTED_EXTENSIONS
    )


# =========================================================
# READ FILE FROM GITHUB
# =========================================================

def get_file_content(owner, repo, path):

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/contents/{path}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if "content" not in data:
        return None

    try:

        content = base64.b64decode(
            data["content"]
        ).decode(
            "utf-8",
            errors="ignore"
        )

        return content

    except Exception:

        return None


# =========================================================
# BUILD PROJECT CONTEXT
# =========================================================

def build_project_context(
    owner,
    repo,
    tree
):

    project_context = []

    file_count = 0

    for item in tree:

        if item.get("type") != "blob":
            continue

        path = item.get("path", "")

        if not is_supported_file(path):
            continue

        # Avoid huge repositories
        if file_count >= 20:
            break

        content = get_file_content(
            owner,
            repo,
            path
        )

        if content:

            # Limit each file size
            content = content[:8000]

            project_context.append(
                f"""
==================================================
FILE: {path}
==================================================

{content}
"""
            )

            file_count += 1

    return "\n".join(project_context)


# =========================================================
# OLLAMA FUNCTION
# =========================================================

def ask_ollama(question, context):

    prompt = f"""
You are GitMentor, an AI mentor for understanding
GitHub software projects.

You are given source code from a GitHub repository.

Your job is to help a student understand the project.

IMPORTANT RULES:

1. Use the provided repository context.
2. Do not invent files or functionality.
3. If the information is not available, say so.
4. Explain technical concepts clearly.
5. Use simple language when possible.
6. Mention relevant filenames in your answer.

REPOSITORY:

{context}

USER QUESTION:

{question}

Give a clear and useful answer.
"""

    payload = {

        "model": "llama3.2",

        "messages": [

            {
                "role": "user",
                "content": prompt
            }

        ],

        "stream": False
    }

    response = requests.post(
        "http://localhost:11434/api/chat",
        json=payload,
        timeout=120
    )

    if response.status_code != 200:

        return (
            "Ollama Error: "
            + response.text
        )

    data = response.json()

    return data["message"]["content"]


# =========================================================
# SESSION STATE
# =========================================================

if "context" not in st.session_state:

    st.session_state.context = None


if "repo_name" not in st.session_state:

    st.session_state.repo_name = None


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("📂 GitHub Repository")

repo_url = st.sidebar.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/user/project"
)


analyze_button = st.sidebar.button(
    "🔍 Analyze Repository"
)


# =========================================================
# ANALYZE REPOSITORY
# =========================================================

if analyze_button:

    if not repo_url:

        st.sidebar.error(
            "Please enter a GitHub URL."
        )

    else:

        owner, repo = parse_github_url(
            repo_url
        )

        if not owner or not repo:

            st.sidebar.error(
                "Invalid GitHub URL."
            )

        else:

            with st.spinner(
                "Analyzing GitHub repository..."
            ):

                tree, error = (
                    get_repository_contents(
                        owner,
                        repo
                    )
                )

                if error:

                    st.error(error)

                else:

                    context = build_project_context(
                        owner,
                        repo,
                        tree
                    )

                    if not context:

                        st.warning(
                            "No supported source files found."
                        )

                    else:

                        st.session_state.context = (
                            context
                        )

                        st.session_state.repo_name = (
                            f"{owner}/{repo}"
                        )

                        st.success(
                            "✅ Repository analyzed successfully!"
                        )


# =========================================================
# PROJECT STATUS
# =========================================================

if st.session_state.context:

    st.subheader(
        f"📦 Project: {st.session_state.repo_name}"
    )

    st.success(
        "GitMentor is ready. Ask a question below."
    )


# =========================================================
# CHAT
# =========================================================

st.divider()

st.subheader("💬 Ask GitMentor")

question = st.chat_input(
    "Ask something about this project..."
)


if question:

    if not st.session_state.context:

        st.warning(
            "Please analyze a GitHub repository first."
        )

    else:

        with st.chat_message("user"):

            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner(
                "GitMentor is thinking..."
            ):

                try:

                    answer = ask_ollama(
                        question,
                        st.session_state.context
                    )

                    st.write(answer)

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Cannot connect to Ollama. "
                        "Please make sure Ollama is running."
                    )

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )