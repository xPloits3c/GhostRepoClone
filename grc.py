import os
import json
import requests

REPO_FILE = "repos.json"
GITHUB_SEARCH_API = "https://api.github.com/search/repositories?q="

def load_repos():
    if not os.path.exists(REPO_FILE):
        return {}
    with open(REPO_FILE, "r") as f:
        return json.load(f)

def save_repos(repos):
    with open(REPO_FILE, "w") as f:
        json.dump(repos, f, indent=4)

def menu(repos):
    os.system("clear" if os.name == "posix" else "cls")
    print("\033[94m                == GhostRepoClone ==")
    print("\033[91m                 ᴳᴿᑦ_ᵛ¹_ᵇʸ_ˣᴾˡᵒⁱᵗˢ³ᶜ \033[0m\n")
    for num, (name, url) in enumerate(repos.items(), start=1):
        print(f"[{num}] {name}")
    print(f"[{len(repos)+1}] Add new repository")
    print(f"[{len(repos)+2}] Search on GitHub")
    print("\033[91m[0] Exit \033[0m\n")

def clone_repo(name, url):
    dest = f"./tools/{name.replace(' ', '_')}"
    if not os.path.exists("tools"):
        os.mkdir("tools")
    if os.path.exists(dest):
        print(f"{name} It's already there. Do you want to update it? (y/n)")
        if input("> ").lower() == "y":
            os.system(f"cd {dest} && git pull")
        return
    print(f"cloning of {name}...")
    os.system(f"git clone {url} {dest}")
    print(f"{name} installed in {dest}")

def add_new_repo(repos):
    name = input("Name of repository: ").strip()
    url = input("URL of repository GitHub: ").strip()
    if name and url:
        repos[name] = url
        save_repos(repos)
        print(f"{name} successfully added.")
    else:
        print("\033[91m Invalid name or url! \033[0m\n")

def search_github():
    query = input("What do you want to search on GitHub? ").strip()
    if not query:
        print("Empty search.")
        return
    print("\033[93m Searching on GitHub...\033[0m\n")
    try:
        response = requests.get(GITHUB_SEARCH_API + query)
        data = response.json()
        items = data.get("items", [])[:10]
        if not items:
            print("\033[91m No results found! \033[0m\n")
            return
        for i, repo in enumerate(items, start=1):
            print(f"[{i}] {repo['full_name']} - {repo['description']}")
        choice = input("Select a number to clone (or 0 to cancel): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(items):
            selected = items[int(choice)-1]
            name = selected["name"]
            url = selected["clone_url"]
            clone_repo(name, url)
        else:
            print("\033[91m Operation cancelled. \033[0m\n")
    except Exception as e:
        print("Error while searching:", e)

def main():
    repos = load_repos()
    while True:
        menu(repos)
        choice = input("Choice a number: ").strip()
        if choice == "0":
            break
        elif choice == str(len(repos) + 1):
            add_new_repo(repos)
        elif choice == str(len(repos) + 2):
            search_github()
        elif choice.isdigit() and 1 <= int(choice) <= len(repos):
            repo_list = list(repos.items())
            name, url = repo_list[int(choice)-1]
            clone_repo(name, url)
        else:
             print("\033[91m Invalid choice! \033[0m\n")
        input("Press enter to continue...")

if __name__ == "__main__":
    main()
