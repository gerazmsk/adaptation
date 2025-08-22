#!/usr/bin/env python3
"""
Test cases for the simplified Financial Advisor Bot
"""

import unittest
from unittest.mock import Mock, AsyncMock, patch
import asyncio

# Import Telegram types for mocking
from telegram import Update, User, Chat, Message
from telegram.ext import ContextTypes

# Import the bot class
from bot import FinancialAdvisorBot

class TestFinancialAdvisorBot(unittest.TestCase):
    """Test cases for the Financial Advisor Bot"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.bot = FinancialAdvisorBot()
        
        # Mock user data
        self.mock_user = Mock(spec=User)
        self.mock_user.id = 12345
        
        # Mock chat data
        self.mock_chat = Mock(spec=Chat)
        self.mock_chat.id = 67890
        
        # Mock message data
        self.mock_message = Mock(spec=Message)
        self.mock_message.text = "Hello bot!"
        self.mock_message.chat = self.mock_chat
        self.mock_message.reply_text = AsyncMock()
        
        # Mock update data
        self.mock_update = Mock(spec=Update)
        self.mock_update.effective_user = self.mock_user
        self.mock_update.message = self.mock_message
        
        # Mock context
        self.mock_context = Mock(spec=ContextTypes.DEFAULT_TYPE)
    
    def test_bot_initialization(self):
        """Test that the bot initializes correctly"""
        self.assertIsInstance(self.bot, FinancialAdvisorBot)
        self.assertEqual(self.bot.user_conversations, {})
    
    def test_start_command_clears_conversation(self):
        """Test that /start command clears previous user conversation"""
        # Set up initial conversation
        self.bot.user_conversations[12345] = [{"role": "user", "content": "old message"}]
        
        # Run start command
        asyncio.run(self.bot.start_command(self.mock_update, self.mock_context))
        
        # Check that conversation was cleared
        self.assertNotIn(12345, self.bot.user_conversations)
    
    @patch('bot.InlineKeyboardMarkup')
    @patch('bot.InlineKeyboardButton')
    def test_start_command_creates_greeting(self, mock_button, mock_markup):
        """Test that start command creates proper greeting"""
        asyncio.run(self.bot.start_command(self.mock_update, self.mock_context))
        
        # Verify greeting was sent
        self.mock_message.reply_text.assert_called_once()
        call_args = self.mock_message.reply_text.call_args[0][0]
        self.assertIn("Финансовый Помощник для Иммигрантов", call_args)
    
    def test_handle_message_creates_conversation(self):
        """Test that handle_message creates conversation for new users"""
        # Ensure user has no conversation
        if 12345 in self.bot.user_conversations:
            del self.bot.user_conversations[12345]
        
        # Run message handler
        asyncio.run(self.bot.handle_message(self.mock_update, self.mock_context))
        
        # Check that conversation was created
        self.assertIn(12345, self.bot.user_conversations)
    
    def test_help_command(self):
        """Test help command"""
        asyncio.run(self.bot.help_command(self.mock_update, self.mock_context))
        
        # Check that help text was sent
        self.mock_message.reply_text.assert_called_once()
        call_args = self.mock_message.reply_text.call_args[0][0]
        self.assertIn("Финансовый Помощник для Иммигрантов", call_args)
        self.assertIn("/start", call_args)
        self.assertIn("/help", call_args)

if __name__ == "__main__":
    unittest.main()
