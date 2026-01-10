# PromoBot

**PromoBot** is an autonomous "Marketing Agent" that turns code into content. It reads your project's source code or README and automatically generates and publishes launch posts to **Reddit, Dev.to, Twitter (X), and Peerlist**.

It uses **AI (Google Gemini)** to adapt the tone for each platform and **Browser Automation (Playwright)** to post to sites without public APIs.

## 🏗️ Architecture

PromoBot follows an Event-Driven, Microservices-like architecture:

* **Brain:** Google Gemini 1.5 Flash (via Custom REST Client) for content generation.
* **Hands:** Playwright (Python) for browser automation (Reddit/X/Peerlist).
* **Nerves:** Redis & Celery for asynchronous task queues.
* **Memory:** PostgreSQL (SQLAlchemy) for campaign tracking.
* **Pattern:** Strategy Pattern (Plugin-based architecture for adding new platforms).

## Features

* **Universal Auth:** Logs into Reddit/X once and saves session state to `secrets/`.
* **Context Aware:** Reads the `README.md` of any project you are working on.
* **Stealth Mode:** Bypasses "Bot Detection" on X and Reddit using advanced browser flags.
* **Tone Matching:** * *Reddit:* Casual, humble, "I built this" vibe.
    * *Dev.to:* Technical, tutorial style.
    * *Twitter:* Short, punchy, hashtag-optimized.
    * *Peerlist:* Professional "Indie Hacker" tone.

## Tech Stack

* **Language:** Python 3.11
* **Frameworks:** Celery, SQLAlchemy
* **Infrastructure:** Docker Compose (Redis, Postgres)
* **Automation:** Playwright

## Usage

Navigate to any project folder and run:

```bash
promobot all