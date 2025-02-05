class ContentProcessor:
    def __init__(self):
        self.summary_prompts = {
            "short": """請用 100 字左右總結以下內容的精華：
1. 抓住核心觀點
2. 保留關鍵信息
3. 簡潔扼要

內容：""",
            
            "medium": """請用 300 字左右總結以下內容：
1. 主要論點（請條列出 3-5 個重點）
2. 關鍵論據或數據
3. 重要結論
4. 保持邏輯連貫性

內容：""",
            
            "long": """請用 500 字以上詳細總結以下內容：
1. 完整的論點架構
2. 重要論據和例證
3. 細節和背景信息
4. 結論和建議
5. 分段整理，使用標題

內容："""
        }
        
        self.structure_prompt = """請將以下內容進行結構化整理：
1. 主題分類
2. 層次關係
3. 重點標記
4. 邏輯連接

內容："""

    def generate_summary(self, content, length="medium"):
        # 檢查內容長度
        content_length = len(content)
        
        if content_length > 5000:
            # 對於特長文本，先進行分段處理
            prompt = f"""這是一個較長的文本（{content_length} 字），請：
1. 先將內容分為幾個主要段落
2. 為每個段落擬定小標題
3. 分別總結每個段落的要點
4. 最後給出整體{self.get_length_desc(length)}摘要

內容：{content}"""
        else:
            # 一般長度文本直接使用標準提示詞
            prompt = self.summary_prompts.get(length, self.summary_prompts["medium"]) + content
        
        return prompt
    
    def get_length_desc(self, length):
        return {
            "short": "100字簡要",
            "medium": "300字",
            "long": "500字完整"
        }.get(length, "300字")
    
    def structure_content(self, content, format_type="outline"):
        format_templates = {
            "outline": "請以大綱形式整理：",
            "table": "請以表格形式整理：",
            "list": "請以列表形式整理：",
            "hierarchy": "請以層級結構整理："
        }
        return format_templates.get(format_type, self.structure_prompt) + content
    
    def format_converter(self, content, target_format):
        format_prompts = {
            "markdown": "請將內容轉換為Markdown格式：",
            "json": "請將內容轉換為JSON格式：",
            "csv": "請將內容轉換為CSV格式：",
            "html": "請將內容轉換為HTML格式："
        }
        return format_prompts.get(target_format, "") + content
    
    def extract_keywords(self, content):
        prompt = """請從以下內容中提取關鍵詞：
1. 核心概念
2. 重要術語
3. 關鍵人物/地點
4. 重要數據

內容：""" + content
        return prompt 