import requests
import pandas as pd

def get_source(url):
    response = requests.get(url)
    data = response.json()
    records = [
        {
            "date": record["date"],
            "title": record["brief"]["title"],
            "job_number": record["job_number"],
            "tender_api_url": record["tender_api_url"]
        }
        for record in data["records"]
    ]
    return pd.DataFrame(records)

def get_budget(df):
    budget_list = []
    for url in df['tender_api_url']:
        response = requests.get(url)
        tender_data = response.json()
        try:
            # 取出type為"決標公告"的項目，然後提取"決標資料:總決標金額"
            for record in tender_data['records']:
                if record['detail']['type'] == '決標公告':
                    budget_amount = record['detail']['決標資料:總決標金額']
                    # 將預算金額轉換為整數
                    budget_amount_int = int(budget_amount.replace(',', '').replace('元', ''))
                    budget_list.append(budget_amount_int)
                    break
            else:
                budget_list.append(None)
        except Exception as e:
            print(f"Error processing {url}: {e}")
            budget_list.append(None)
    return budget_list

def concat_df(df, budget_list):
    df['budget_amount'] = budget_list
    return df

if __name__ == "__main__":
    res = pd.DataFrame()
    input_keyword = ["資料分析", "大數據", "資料探勘", "人工智慧"]
    
    for word in input_keyword:
        page = 1
        while True:
            url = f"https://pcc.g0v.ronny.tw/api/searchbytitle?query={word}&page={page}"
            df = get_source(url)
            
            if df.empty:
                break
            
            budget_list = get_budget(df)
            final_df = concat_df(df=df, budget_list=budget_list)
            
            # 合併結果
            res = pd.concat([res, final_df], ignore_index=True)
            
            # 檢查日期條件
            if (final_df['date'].astype(int) < 20220101).any():
                break
                
            page += 1
    
    # 去重複
    res = res.drop_duplicates(subset=['job_number', 'title'])

    # 去掉預算金額為 None 的行
    res = res.dropna(subset=['budget_amount'])

    # 按照預算金額降序排序
    res = res.sort_values(by='budget_amount', ascending=False)

    # 取前10高的記錄
    top_10_res = res.head(10)
    top_10_res.to_csv("top_10_budget.csv", index=False, encoding='utf-8-sig')
    
    # 顯示最終結果
    print(top_10_res)
