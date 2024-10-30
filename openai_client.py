import os

from openai import OpenAI

gpt_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


async def chat_with_gpt(user_message):
    try:
        print(f'User message:\n{user_message}')

        system_message = {
            'role': 'system',
            'content': (
                '你是奇幻 MMORPG 資深製作人，有多年的製作經驗與遊戲經驗，精通使用台灣的中文用字，我會給你情境資料，請產生對應文本或遊戲內容。\n'
                '我會給你各種標籤，如果標籤是：\n'

                '1. [monster_name_gen]：請根據提供的地圖名與難度，設計會出現在這裡的敵人的名稱，一個名字就好，不要多餘的解釋和標點符號。'
                '請使用現實存在的動物或植物去想像，單一物種。\n'

                '2. [battle]：請產生緊湊的輕小說風格的一場戰鬥文本，請忠實呈現名字。'
                '請在最多200字左右完成，不需要換行分段落。數字必須是阿拉伯數字、前後留空白、粗體化。\n'

                '3. [shop_owner_talk]：請根據提供的地圖名，設計這裡的商店老闆的歡迎對話，給我一段簡短對話即可，請幫我用「」括起來。'

                '4. [map_description]：我會告訴你玩家從哪張地圖到哪張地圖，請設計玩家進入過場的描述，不要超過150字，地圖名稱幫我粗體化。'

                '5. [born_message]：請根據提供的玩家名稱與地圖名，設計玩家從異世界轉生過來描述，不要超過100字，玩家名稱幫我粗體化。'
            )
        }

        current_message = {
            'role': 'user',
            'content': user_message
        }

        response = gpt_client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[system_message, current_message],
            max_tokens=500,
            temperature=0.8,
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f'Error while calling OpenAI API: {e}')
        return 'Sorry, something went wrong with the API.'
