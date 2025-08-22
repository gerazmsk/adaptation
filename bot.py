#!/usr/bin/env python3
"""
Simple Financial Advisor Telegram Bot with OpenAI ChatGPT Integration
Russian-speaking financial advisor for established immigrants in the USA
"""

import os
import logging
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import threading
import time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8155289579:AAHG2OujfC2mnxcga4dp2GDFBXeFVOtn5sM")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")  # or "gpt-3.5-turbo" for cost efficiency

# Web server configuration for cloud deployment
PORT = int(os.getenv("PORT", 8080))

# Financial Advisor System Prompt
FINANCIAL_ADVISOR_PROMPT = """[РОЛЬ]  
Ты — русскоязычный финансовый помощник для иммигрантов в США.  
Твоя задача — помогать людям 25–55 лет, которые живут в США от 1 до 7 лет, зарабатывают от $70 000 в год, уже имеют все документы для работы и планируют остаться жить в США.  

[ФОКУС]  
Ты даёшь только общую образовательную информацию, а не бухгалтерские или юридические советы.  
Ты объясняешь простыми словами, как работают финансовые инструменты в США.  

Ключевые темы:  
- Финансовая защита семьи (жизнь, здоровье, доход, долгосрочный уход).  
- Накопления (пенсия, образование детей, создание капитала).  
- Сохранение и передача активов (наследство, защита капитала, пожизненный доход).  

[ПИРАМИДА ФИНАНСОВЫХ НУЖД]  
Ты должен выявить приоритетность целей пользователя, двигаясь от базовых к стратегическим:  
1. **Решения по защите** — страхование жизни, защита дохода, долгосрочный уход.  
2. **Решения по накоплению** — пенсионные планы, накопительные программы, фонды для образования детей.  
3. **Решения по сохранению капитала** — создание пожизненного дохода, планирование наследства, сохранение активов.  

[ИММИГРАЦИЯ]  
Ты можешь отвечать на простые вопросы по адаптации (ID, SSN, жильё, школа), но не даёшь юридических консультаций и не выступаешь как адвокат.  

[ТОН]  
— Дружелюбный, поддерживающий, экспертный.  
— Объясняй так, чтобы человек чувствовал уверенность и понимал свои шаги.  
— Используй примеры и сравнения.  

[СТРУКТУРА РАБОТЫ]  
1. Сначала задай вопросы, чтобы понять приоритеты (например: «Что для вас сейчас важнее — защита семьи, накопления или сохранение капитала?»).  
2. Дай обзор соответствующих решений (без названий компаний, только описания продуктов).  
3. Объясни, почему именно этот уровень важен сейчас.  
4. Добавь советы, что можно изучить в течение ближайших недель.  
5. В конце предлагай варианты продолжения диалога (например: «Хочу узнать про защиту семьи», «Интересуют пенсионные накопления», «Как сохранить капитал»).  

[ПРИМЕР ПОВЕДЕНИЯ]  
Пользователь: «С чего начать, если я думаю о будущем семьи?»  
Ассистент:  
- Объясняет, что фундамент — это защита: страховка жизни, дохода, долгосрочный уход.  
- Рассказывает, что когда защита обеспечена, следующим шагом будут накопительные решения (пенсия, образование детей).  
- В долгосрочной перспективе — сохранение капитала и планирование наследства.  
- Предлагает кнопки: [Финансовая защита] [Накопления] [Сохранение капитала].  

[ФОРМАТ ВЫВОДА]  
— Краткий обзор ситуации пользователя.  
— Чёткие и простые шаги/идеи.  
— Объяснение «почему это важно».  
— В конце 2–3 кнопки для выбора следующего направления."""

class FinancialAdvisorBot:
    """Simple Financial Advisor Bot with OpenAI ChatGPT integration"""
    
    def __init__(self):
        self.user_conversations = {}  # Store conversation history for AI
        
        # Initialize OpenAI
        if OPENAI_API_KEY and OPENAI_API_KEY != "your-openai-api-key-here":
            openai.api_key = OPENAI_API_KEY
            self.openai_available = True
            logger.info("✅ OpenAI API configured")
        else:
            self.openai_available = False
            logger.warning("⚠️ OpenAI API key not configured")
    
    async def get_ai_response(self, user_message: str, user_id: int) -> str:
        """Get AI response from OpenAI using the financial advisor system prompt"""
        if not self.openai_available:
            return "Извините, AI сервис временно недоступен. Пожалуйста, попробуйте позже."
        
        try:
            # Get or create conversation history for this user
            if user_id not in self.user_conversations:
                self.user_conversations[user_id] = [
                    {"role": "system", "content": FINANCIAL_ADVISOR_PROMPT}
                ]
            
            # Add user message to conversation
            self.user_conversations[user_id].append({"role": "user", "content": user_message})
            
            # Get AI response
            response = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=self.user_conversations[user_id],
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Add AI response to conversation history
            self.user_conversations[user_id].append({"role": "assistant", "content": ai_response})
            
            # Keep conversation history manageable (last 10 messages)
            if len(self.user_conversations[user_id]) > 10:
                # Keep system prompt and last 9 messages
                self.user_conversations[user_id] = (
                    [self.user_conversations[user_id][0]] + 
                    self.user_conversations[user_id][-9:]
                )
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            return "Извините, произошла ошибка при получении ответа. Пожалуйста, попробуйте еще раз."
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        
        # Clear any previous conversation for this user
        if user_id in self.user_conversations:
            del self.user_conversations[user_id]
        
        greeting_text = (
            "🤖 **Добро пожаловать в Финансовый Помощник для Иммигрантов!**\n\n"
            "Я — ваш русскоязычный финансовый консультант для иммигрантов в США. "
            "Помогу разобраться с финансовой защитой семьи, накоплениями и сохранением капитала.\n\n"
            "Просто напишите мне ваш вопрос или опишите ситуацию, и я помогу составить персональный финансовый план."
        )
        
        await update.message.reply_text(greeting_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages from users"""
        user_id = update.effective_user.id
        user_message = update.message.text
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Get AI response
        ai_response = await self.get_ai_response(user_message, user_id)
        
        # Send the AI response back to the user
        await update.message.reply_text(
            f"🤖 **AI Помощник:**\n\n{ai_response}",
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **Финансовый Помощник для Иммигрантов - Справка**

**Команды:**
/start - Начать финансовое планирование
/help - Показать эту справку

**Возможности:**
• **AI-консультант** - Получайте персональные финансовые планы
• **Русскоязычная поддержка** - Помощь на русском языке
• **Экспертные знания** - Объяснение финансовых инструментов США

**Как это работает:**
1. Начните с /start для знакомства
2. Просто напишите ваш вопрос или опишите ситуацию
3. Получите персональный финансовый план
4. Задавайте уточняющие вопросы

**Примеры вопросов:**
• "С чего начать, если я думаю о финансовой защите семьи?"
• "Как правильно планировать пенсионные накопления в США?"
• "Как сохранить и приумножить капитал?"

Просто начните с /start и пишите ваши вопросы!
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    def start_web_server(self):
        """Start a simple web server for cloud deployment health checks"""
        try:
            import http.server
            import socketserver
            
            class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
                def do_GET(self):
                    if self.path == '/health':
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(b'Bot is running!')
                    else:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(b'<h1>Financial Advisor Bot is Running!</h1>')
            
            with socketserver.TCPServer(("", PORT), HealthCheckHandler) as httpd:
                logger.info(f"Web server started on port {PORT}")
                httpd.serve_forever()
        except Exception as e:
            logger.error(f"Web server error: {e}")
    
    def run(self):
        """Start the bot"""
        # Create application
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Start web server in a separate thread for cloud deployment
        web_server_thread = threading.Thread(target=self.start_web_server, daemon=True)
        web_server_thread.start()
        
        # Start the bot
        logger.info(f"Starting Financial Advisor Bot with OpenAI ChatGPT integration on port {PORT}...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = FinancialAdvisorBot()
    bot.run()
