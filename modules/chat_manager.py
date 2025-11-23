from anthropic import Anthropic, APIError, APIConnectionError, RateLimitError, APIStatusError
import json
import time

class ChatManager:
    def __init__(self, api_key, temperature=0.7):
        self.client = Anthropic(api_key=api_key)
        self.conversation_history = []
        self.max_history = 10  # 保留最近10條對話
        self.temperature = temperature  # 控制回應的創意性 (0.0-1.0)
        self.system_prompt = "你是一個智能助手，能夠幫助用戶進行思維發想、內容整理和知識管理。請用繁體中文回答。"

    def get_response(self, message, stream=False, max_retries=3):
        """
        獲取 AI 回應
        
        Args:
            message: 使用者訊息
            stream: 是否使用串流模式
            max_retries: 最大重試次數
        
        Returns:
            AI 回應文字
        """
        for attempt in range(max_retries):
            try:
                # 構建消息列表並確保正確的編碼
                messages = []
                for msg in self.conversation_history:
                    if msg["role"] == "user":
                        messages.append({"role": "user", "content": str(msg["content"])})
                    elif msg["role"] == "assistant":
                        messages.append({"role": "assistant", "content": str(msg["content"])})
                
                messages.append({"role": "user", "content": str(message)})
                
                # 呼叫 API
                response = self.client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=4096,  # 提升到 4096 以支援更長的回應
                    temperature=self.temperature,  # 控制創意性
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
                
            except RateLimitError as e:
                # Rate limit 錯誤 - 使用指數退避重試
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 1  # 1秒, 2秒, 4秒...
                    time.sleep(wait_time)
                    continue
                else:
                    return f"錯誤：API 請求頻率過高，請稍後再試。詳細信息：{str(e)}"
                    
            except APIConnectionError as e:
                # 連接錯誤 - 重試
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                else:
                    return f"錯誤：無法連接到 API 服務，請檢查網路連接。詳細信息：{str(e)}"
                    
            except APIStatusError as e:
                # API 狀態錯誤
                return f"錯誤：API 返回錯誤狀態 {e.status_code}。詳細信息：{str(e)}"
                
            except APIError as e:
                # 其他 API 錯誤
                return f"錯誤：API 請求失敗。詳細信息：{str(e)}"
                
            except Exception as e:
                # 未預期的錯誤
                return f"錯誤：發生未預期的錯誤。詳細信息：{str(e)}"
        
        return "錯誤：已達到最大重試次數，請稍後再試。"

    def get_streaming_response(self, message):
        """
        獲取串流式 AI 回應（用於即時顯示）
        
        Args:
            message: 使用者訊息
            
        Yields:
            回應文字片段
        """
        try:
            # 構建消息列表
            messages = []
            for msg in self.conversation_history:
                if msg["role"] == "user":
                    messages.append({"role": "user", "content": str(msg["content"])})
                elif msg["role"] == "assistant":
                    messages.append({"role": "assistant", "content": str(msg["content"])})
            
            messages.append({"role": "user", "content": str(message)})
            
            # 串流呼叫 API
            full_response = ""
            with self.client.messages.stream(
                model="claude-sonnet-4-5",
                max_tokens=4096,
                temperature=self.temperature,
                system=str(self.system_prompt),
                messages=messages
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    yield text
            
            # 保存對話歷史
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": full_response})
            
            # 保持歷史記錄在限制範圍內
            if len(self.conversation_history) > self.max_history * 2:
                self.conversation_history = self.conversation_history[-self.max_history * 2:]
                
        except Exception as e:
            yield f"錯誤：{str(e)}"

    def set_temperature(self, temperature):
        """設定回應的創意性 (0.0 = 確定性, 1.0 = 創意性)"""
        self.temperature = max(0.0, min(1.0, temperature))
    
    def set_system_prompt(self, prompt):
        """更新系統提示詞"""
        self.system_prompt = str(prompt)

    def clear_history(self):
        """清除對話歷史"""
        self.conversation_history = []
    
    def get_conversation_length(self):
        """獲取當前對話長度"""
        return len(self.conversation_history) // 2 