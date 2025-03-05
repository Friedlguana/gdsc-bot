
# GDSC Bot 🎉  
A smart and versatile Discord bot that can play music, manage reminders, run polls, and even tap into **Google Gemini AI** to answer questions or summarize text. Whether you're hosting a study session or just vibing with friends, GDSC Bot's got your back.

---

## 🚀 Features
✅ Stream music directly into voice channels (with auto-join and queue support)  
✅ Set, list, edit, and delete reminders — never miss a deadline again  
✅ Create polls for quick group decisions  
✅ Ask questions and summarize text using **Gemini AI**  
✅ Clean and simple command system  
✅ Easy setup (just a few files and some keys)  

---

## 🛠️ Pre-requisites
Before you run the bot, make sure you have the following installed:

✅ Python 3.10.11 ([Download here](https://www.python.org/downloads/release/python-31011/))  
✅ [FFmpeg](https://ffmpeg.org/download.html) (Add to system PATH after download — this is needed for music playback)  
✅ A Discord Bot Token ([Get yours here](https://discord.com/developers/applications))  
✅ A Google Gemini API Key ([Get yours here](https://ai.google.dev/))  

---

## 📂 Setup Guide
1. Clone this repository or copy the files into a folder.  
2. Create a `.env` file in the project directory and add these 2 lines:
    ```
    DISCORD_TOKEN=your-discord-bot-token-here
    GEMINI_TOKEN=your-gemini-api-key-here
    ```
3. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```
4. Make sure **FFmpeg** is installed and available in your PATH (you can check by running `ffmpeg -version` in your terminal).  
5. Run the bot:
    ```bash
    python bot.py
    ```
6. Invite the bot to your server using the URL from your Discord Developer Portal.

---

## 💬 Commands List (with examples)

### 🎶 Music Commands
| Command | What It Does | Example |
|---|---|---|
| `!play <song_name_or_url>` | Plays a song (auto joins VC if needed, queues if something's already playing) | `!play Skeletons by Travis Scott` |
| `!queue` | Shows the current song queue | `!queue` |
| `!skip` | Skips the current song | `!skip` |
| `!stop` | Stops music, clears queue, leaves VC | `!stop` |
| `!leave` | Makes the bot leave the voice channel | `!leave` |

---

### 🕒 Reminder Commands
| Command | What It Does | Example |
|---|---|---|
| `!setreminder <date> <time> <message>` | Sets a reminder for a specific date and time | `!setreminder 2025-03-06 15:30 Finish the project` |
| `!reminders` | Lists all active reminders | `!reminders` |
| `!deletereminder <id>` | Deletes a specific reminder by its number | `!deletereminder 1` |
| `!modifyreminder <id> <date> <time> <new_message>` | Edits an existing reminder | `!modifyreminder 2 2025-03-10 14:00 Team Meeting` |

⏰ **Date format:** `YYYY-MM-DD`  
🕒 **Time format:** `HH:MM` (24-hour format)

---

### 🗳️ Poll Command
| Command | What It Does | Example |
|---|---|---|
| `!poll "question" option1 option2 ...` | Creates a quick poll | `!poll "Best programming language?" Python Java C++` |

---

### 🤖 AI Commands (Powered by Gemini)
| Command | What It Does | Example |
|---|---|---|
| `!ask <question>` | Ask Gemini anything | `!ask What is the capital of Japan?` |
| `!summarize <text>` | Summarize any chunk of text | `!summarize This is a long article about machine learning...` |

---

### 📖 Help Command
| Command | What It Does | Example |
|---|---|---|
| `!help` | Shows a help menu with all commands | `!help` |

---
