# Web Crawler Project

## Description
This project is a simple web crawler that searches for relevant URLs based on a search term and creates an index. The addition of a control centre facilitates restting the index, seed url and stopping the crawl. It uses various libraries such as `requests`, `beautifulsoup4`, and `nltk`.

## GitHub Setup

### Setting Up SSH Keys for GitHub
1. Generate an SSH key:
    ```sh
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ```
2. Add the SSH key to your GitHub account:
    - Copy the SSH key:
      ```sh
      cat ~/.ssh/id_ed25519.pub
      ```
    - Paste the key into your GitHub SSH settings.
3. Set your Git remote URL to use SSH:
    ```sh
    git remote set-url origin git@github.com:YourUsername/YourRepoName.git
    ```

### Commands
- **Stage changes**:
    ```sh
    git add .
    ```
- **Commit changes**:
    ```sh
    git commit -m "Your commit message"
    ```
- **Push changes**:
    ```sh
    git push origin master
    ```
