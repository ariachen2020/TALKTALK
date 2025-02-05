from anthropic import Anthropic
import json

class ChatManager:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)
        self.conversation_history = []
        self.max_history = 10  # 保留最近10條對話
        self.system_prompt = "你是一個智能助手，能夠幫助用戶進行思維發想、內容整理和知識管理。請用繁體中文回答。"

    def get_response(self, message):
        try:
            # 構建消息列表並確保正確的編碼
            messages = []
            for msg in self.conversation_history:
                if msg["role"] == "user":
                    messages.append({"role": "user", "content": str(msg["content"])})
                elif msg["role"] == "assistant":
                    messages.append({"role": "assistant", "content": str(msg["content"])})
            
            messages.append({"role": "user", "content": str(message)})
            
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                system=str(self.system_prompt),
                messages=messages
            )
            
            response_text = response.content[0].text
            
            # 保存對話歷史
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": response_text})
            
            # 保持歷史記錄在限制範圍內
            if len(self.conversation_history) > self.max_history * 2:
                self.conversation_history = self.conversation_history[-self.max_history * 2:]
                
            return response_text
        except Exception as e:
            return f"錯誤：{str(e)}"

    def clear_history(self):
        self.conversation_history = [] 