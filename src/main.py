import os
import argparse
from pathlib import Path
from src.config import Config, logger

# Import all publishers
from src.publishers.reddit import RedditPublisher
from src.publishers.devto import DevtoPublisher
from src.publishers.twitter import TwitterPublisher
from src.publishers.peerlist import PeerlistPublisher
from src.ai import AIEngine

def read_local_context():
    """Reads README.md from current folder."""
    path = Path(os.getcwd()) / "README.md"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return f.read()[:3000]
    return input("📝 No README found. What should I post about? ")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["all", "reddit", "devto", "twitter", "peerlist"])
    args = parser.parse_args()

    # 1. Read Project
    logger.info(f"📂 Reading context from {os.getcwd()}...")
    context = read_local_context()
    project_name = os.path.basename(os.getcwd())
    repo_link = input(f"🔗 Enter Repo Link for {project_name} (press Enter to skip): ")

    ai = AIEngine()

    # 2. Define The Jobs
    jobs = []
    if args.command == "all":
        jobs = ["devto", "reddit", "peerlist", "twitter"]
    else:
        jobs = [args.command]

    # 3. Execute Jobs
    for platform in jobs:
        print(f"\n" + "="*50)
        print(f"🚀 EXECUTING: {platform.upper()}")
        print("="*50)

        # A. Generate Content
        logger.info(f"🧠 Generating {platform} content...")
        draft = ai.rewrite(context, platform=platform)
        
        # B. Append Link (If provided)
        final_body = draft
        if repo_link and platform != "twitter": 
            # Twitter gets link in body usually, others get it appended
            final_body += f"\n\n🔗 {repo_link}"
        elif repo_link and platform == "twitter":
             final_body += f" {repo_link}"

        print(f"\n📝 PREVIEW ({platform}):\n{final_body}\n")
        
        # C. Confirm & Publish
        if input("👉 Publish? (y/n): ").lower() == 'y':
            try:
                publisher = None
                payload = {"body": final_body, "title": f"Launch: {project_name}"}

                if platform == "devto":
                    publisher = DevtoPublisher()
                    # Devto needs a strict title separate from body
                    payload["title"] = f"Building {project_name}: {draft[:30]}..."
                
                elif platform == "reddit":
                    publisher = RedditPublisher()
                    payload["subreddit"] = "r/SideProject"
                    payload["title"] = f"I built {project_name} - {draft[:50]}..."

                elif platform == "twitter":
                    publisher = TwitterPublisher()
                    
                elif platform == "peerlist":
                    publisher = PeerlistPublisher()

                # GO!
                if publisher:
                    publisher.publish(payload)
            except Exception as e:
                logger.error(f"💥 Failed {platform}: {e}")

    print("\n✅ All done. Back to coding.")

if __name__ == "__main__":
    main()