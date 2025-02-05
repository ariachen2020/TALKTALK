import networkx as nx
from datetime import datetime

class KnowledgeManager:
    def __init__(self):
        self.knowledge_graph = nx.Graph()
        self.tags = {}
        self.knowledge_base = {}
    
    def add_knowledge(self, content, tags=None, title=None):
        if tags is None:
            tags = []
            
        # 生成知識節點ID
        knowledge_id = str(datetime.now().timestamp())
        
        # 儲存知識內容
        self.knowledge_base[knowledge_id] = {
            'title': title or f"Knowledge_{knowledge_id}",
            'content': content,
            'tags': tags,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        # 更新標籤索引
        for tag in tags:
            if tag not in self.tags:
                self.tags[tag] = set()
            self.tags[tag].add(knowledge_id)
        
        # 添加到知識圖譜
        self.knowledge_graph.add_node(knowledge_id, 
                                    type='knowledge',
                                    title=title,
                                    tags=tags)
        return knowledge_id
    
    def add_relation(self, source_id, target_id, relation_type):
        if source_id in self.knowledge_base and target_id in self.knowledge_base:
            self.knowledge_graph.add_edge(source_id, target_id, 
                                        relation=relation_type)
            return True
        return False
    
    def get_related_knowledge(self, tag=None, keyword=None):
        results = set()
        
        if tag and tag in self.tags:
            results.update(self.tags[tag])
            
        if keyword:
            # 簡單的關鍵字搜索
            for k_id, knowledge in self.knowledge_base.items():
                if (keyword.lower() in knowledge['content'].lower() or
                    keyword.lower() in knowledge['title'].lower()):
                    results.add(k_id)
        
        return [self.knowledge_base[k_id] for k_id in results]
    
    def get_knowledge_graph(self, center_id=None, depth=1):
        if center_id:
            # 返回以特定節點為中心的子圖
            nodes = {center_id}
            for _ in range(depth):
                neighbors = set()
                for node in nodes:
                    neighbors.update(self.knowledge_graph.neighbors(node))
                nodes.update(neighbors)
            return self.knowledge_graph.subgraph(nodes)
        return self.knowledge_graph 