#!/usr/bin/env python3
"""
Test OpenAI AI Integration with Russian Script
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_ai_integration():
    """Test the AI integration with the Russian script"""
    
    print("🚀 Testing OpenAI AI Integration with Russian Script...")
    print("=" * 60)
    
    # Check if OpenAI API key is configured
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-openai-api-key-here":
        print("❌ OpenAI API key not configured!")
        print("Please set OPENAI_API_KEY in your .env file")
        return False
    
    print("✅ OpenAI API key found")
    
    # Test the exact phrase you specified
    test_message = "Я только что приехал в США. Что делать?"
    print(f"\n📝 Testing with message: '{test_message}'")
    
    try:
        import openai
        openai.api_key = api_key
        
        # Import the bot class to test the AI response method
        from bot import USAAdaptationBot
        
        bot = USAAdaptationBot()
        
        # Test AI response
        print("\n🤖 Getting AI response...")
        ai_response = await bot.get_ai_response(test_message, 12345)
        
        if ai_response and "Извините" not in ai_response:
            print("✅ AI Response received successfully!")
            print(f"\n📋 Response length: {len(ai_response)} characters")
            print(f"\n📝 Response preview:")
            print("-" * 40)
            print(ai_response[:500] + "..." if len(ai_response) > 500 else ai_response)
            print("-" * 40)
            
            # Check if response follows the Russian script structure
            if any(keyword in ai_response for keyword in ["7 ДНЕЙ", "30 ДНЕЙ", "ПОЛЕЗНО", "Кнопки"]):
                print("\n✅ Response follows Russian script structure!")
            else:
                print("\n⚠️ Response may not follow expected structure")
            
            return True
            
        else:
            print("❌ AI response failed or returned error message")
            print(f"Response: {ai_response}")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing AI integration: {e}")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(test_ai_integration())
        if success:
            print("\n🎉 AI Integration Test Complete!")
            print("\n💡 Your bot is now ready to:")
            print("• Use the Russian script as system prompt")
            print("• Provide personalized USA adaptation plans")
            print("• Follow the exact structure you specified")
            print("• Handle Russian language input")
        else:
            print("\n⚠️ AI Integration Test Failed!")
            print("Please check your OpenAI API key and configuration")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
