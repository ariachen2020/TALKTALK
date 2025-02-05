class ThoughtProcessor:
    def __init__(self):
        self.brainstorm_prompts = {
            "概念延伸": """請針對以下主題進行概念延伸和相關聯想：
1. 核心概念分析
2. 相關領域連結
3. 應用場景探討
4. 創新可能性
請條理分明地展開討論。

主題：""",
            
            "架構整理": """請幫我整理以下內容的邏輯架構：
1. 主要概念框架
2. 層次關係
3. 邏輯連接
4. 關鍵要素
請用結構化的方式呈現。

內容：""",
            
            "腦力激盪": """請針對以下主題進行開放式的腦力激盪：
1. 不同角度的思考
2. 可能的解決方案
3. 創新的應用方式
4. 潛在的機會與挑戰
請盡可能發散思維。

主題："""
        }
        
        self.thought_templates = {
            "mind_map": "請以心智圖的形式組織以下內容：\n",
            "swot": "請進行SWOT分析：\n",
            "five_why": "請進行五個為什麼分析：\n"
        }
    
    def process_thought(self, mode, content, template=None):
        base_prompt = self.brainstorm_prompts.get(mode, "")
        if template:
            base_prompt = self.thought_templates.get(template, "") + base_prompt
        
        return base_prompt + content
    
    def generate_mind_map(self, content):
        prompt = f"""請將以下內容組織成心智圖的形式：
- 使用層級結構
- 標明關鍵概念
- 顯示概念間關係
- 加入簡短說明

內容：{content}"""
        return prompt
    
    def analyze_structure(self, content):
        prompt = f"""請分析以下內容的結構：
1. 核心主題
2. 主要分支
3. 邏輯關係
4. 重要元素

內容：{content}"""
        return prompt 