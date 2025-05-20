import sys
import subprocess


def update_remote(new_repo_url):
    """Update the Git remote URL for the project."""
    try:
        # Check if git is initialized
        result = subprocess.run(['git', 'status'],
                                capture_output=True,
                                text=True)
        if result.returncode != 0:
            print("Git repository not initialized. Initializing now...")
            subprocess.run(['git', 'init'], check=True)

        # Check if remote exists
        result = subprocess.run(['git', 'remote'],
                                capture_output=True,
                                text=True)
        if 'origin' in result.stdout:
            print("Updating existing remote origin...")
            subprocess.run(['git', 'remote', 'set-url', 'origin',
                            new_repo_url],
                            check=True)
        else:
            print("Adding new remote origin...")
            subprocess.run(['git', 'remote', 'add', 'origin',
                            new_repo_url],
                            check=True)

        print(f"Remote successfully updated to: {new_repo_url}")
        print("\nTo push your project to this repository, use:")
        print("  git add .")
        print("  git commit -m \"Initial commit\"")
        print("  git push -u origin main")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_remote.py <new_repository_url>")
        print("Example: python update_remote.py" "https://github.com/username/repo-name.git")
        sys.exit(1)

    new_repo_url = sys.argv[1]
    update_remote(new_repo_url)
