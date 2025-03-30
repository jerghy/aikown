import json
import re
import time
from openai import OpenAI
from datetime import datetime

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

subjects = [
    "数学", "物理", "化学", "生物",
    # "历史", "地理", "政治", 
    "语文", "英语"
]

knowledge_db = []

def save_knowledge():
    filename = f"result.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(knowledge_db, f, ensure_ascii=False, indent=2)
    print(f"\n已保存{len(knowledge_db)}条知识点到 {filename}")

start_time = time.time()
timeout = 5 * 60  # 30分钟

try:
    while time.time() - start_time < timeout:
        for subject in subjects:
            print(f"\n当前学科：{subject}")
            
            response = client.chat.completions.create(
                model="deepseek/deepseek-v3-base:free",
                messages=[{
                    "role": "user",
                    "content": f"请提出一个高中{subject}的重要知识点或常见易错点，并用<knowledge></knowledge>标签严格封装回答"
                }]
            )
            
            content = response.choices[0].message.content
            if match := re.search(r'<knowledge>(.*?)</knowledge>', content, re.DOTALL):
                knowledge = match.group(1).strip()
                entry = {
                    "subject": subject,
                    "content": knowledge,
                    "timestamp": datetime.now().isoformat()
                }
                knowledge_db.append(entry)
                print(f"发现新知识点：{knowledge[:50]}...")
            else:
                print("未检测到有效知识点格式")
            
            time.sleep(5)  # 每个问题间隔10秒

except KeyboardInterrupt:
    pass
finally:
    save_knowledge()
