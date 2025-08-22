# Financial Advisor Telegram Bot

A simple, clean Telegram bot that provides Russian-speaking financial advice to established immigrants in the USA using OpenAI's ChatGPT.

## 🎯 **What This Bot Does**

- **Russian-speaking financial advisor** for immigrants in the USA
- **Target audience**: People 25-55 years old, living in USA 1-7 years, earning $70k+, with work documents
- **Focus areas**: Financial protection, retirement savings, wealth preservation
- **AI-powered**: Uses OpenAI GPT-4 for intelligent, personalized responses

## 🚀 **Features**

- **Simple interface**: No buttons, just direct text conversation
- **AI integration**: Powered by OpenAI ChatGPT
- **Russian language**: All responses in Russian
- **Context-aware**: Remembers conversation history
- **Financial expertise**: Specialized in US financial instruments

## 📋 **Requirements**

- Python 3.8+
- Telegram Bot Token
- OpenAI API Key

## 🛠️ **Installation**

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd telegram-gpt-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env_template.txt .env
   # Edit .env and add your API keys
   ```

4. **Run the bot**
   ```bash
   python3 bot.py
   ```

## 🔑 **Environment Variables**

Create a `.env` file with:
```
TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

## 💬 **Usage**

1. **Start the bot**: Send `/start` in Telegram
2. **Ask questions**: Type any financial question in Russian
3. **Get advice**: Receive personalized financial guidance
4. **Continue conversation**: Ask follow-up questions

## 🧪 **Testing**

Run the test suite:
```bash
python3 -m unittest test_bot.py
```

## 📁 **Project Structure**

```
telegram-gpt-bot/
├── bot.py              # Main bot code
├── test_bot.py         # Test suite
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .env               # Environment variables (create this)
```

## 🤖 **Bot Commands**

- `/start` - Begin financial planning session
- `/help` - Show help information

## 🔧 **Technical Details**

- **Framework**: python-telegram-bot v20.7
- **AI**: OpenAI GPT-4 integration
- **Language**: Python 3.8+
- **Architecture**: Simple, clean, no unnecessary complexity

## 📝 **License**

MIT License - feel free to use and modify!
