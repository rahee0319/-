import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

# OpenWeatherMap API와 통신하여 날씨 정보 가져오기
def get_weather_data(city, api_key):
    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=kr"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        if weather_data['cod'] == 200:
            temp = weather_data['main']['temp']
            weather_description = weather_data['weather'][0]['description']
            return temp, weather_description
        else:
            return None, None
    except Exception as e:
        messagebox.showerror("Error", f"Weather API 오류: {e}")
        return None, None

# OpenWeatherMap API로 기상 경고 가져오기
def get_weather_alerts(city, api_key):
    try:
        alerts_url = f"http://api.openweathermap.org/data/2.5/alerts?q={city}&appid={api_key}"
        alerts_response = requests.get(alerts_url)
        alerts_data = alerts_response.json()
        
        alerts = ""
        if 'alerts' in alerts_data:
            for alert in alerts_data['alerts']:
                alerts += f"경고: {alert['event']} - {alert['description']}\n"
        
        return alerts
    except Exception as e:
        messagebox.showerror("Error", f"Weather Alerts API 오류: {e}")
        return ""

# NewsAPI로 입력한 지역과 관련된 뉴스 가져오기
def get_weather_news(city, api_key):
    try:
        # 도시명과 관련된 뉴스 검색
        news_url = f"https://newsapi.org/v2/everything?q={city} weather&apiKey={api_key}"
        news_response = requests.get(news_url)
        news_data = news_response.json()
        
        news = ""
        if news_data['status'] == 'ok' and 'articles' in news_data:
            for article in news_data['articles'][:5]:  # 최신 5개의 기사만 가져오기
                news += f"{article['title']} - {article['source']['name']}\n{article['url']}\n\n"
        
        return news
    except Exception as e:
        messagebox.showerror("Error", f"News API 오류: {e}")
        return ""

# 날씨 정보 및 뉴스 업데이트
def update_weather():
    city = city_entry.get()
    weather_api_key = "your api"  # OpenWeatherMap API 키 입력
    news_api_key = "yout api"  # NewsAPI API 키 입력

    # 날씨 데이터 가져오기
    temp, weather_description = get_weather_data(city, weather_api_key)
    if temp is None:
        return

    # 기상 경고 가져오기
    alerts = get_weather_alerts(city, weather_api_key)

    # 지역 관련 날씨 뉴스 가져오기
    news = get_weather_news(city, news_api_key)

    # UI 업데이트
    weather_label.config(text=f"현재 날씨: {weather_description} / 기온: {temp}°C")
    news_text.delete(1.0, tk.END)
    news_text.insert(tk.END, f"기상 경고:\n{alerts}\n\n날씨 관련 뉴스:\n{news}")

# UI 구성
root = tk.Tk()
root.title("날씨 및 기상 뉴스 제공 소프트웨어")

# 도시 입력 필드
city_label = tk.Label(root, text="도시명 입력:")
city_label.pack(padx=10, pady=5)

city_entry = tk.Entry(root)
city_entry.pack(padx=10, pady=5)

# 날씨 정보 표시 라벨
weather_label = tk.Label(root, text="날씨 정보", font=("Helvetica", 14))
weather_label.pack(padx=10, pady=10)

# 날씨 뉴스 및 경고 표시 영역
news_label = tk.Label(root, text="기상 뉴스 및 경고:", font=("Helvetica", 12))
news_label.pack(padx=10, pady=5)

news_text = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD)
news_text.pack(padx=10, pady=5)

# 날씨 업데이트 버튼
update_button = tk.Button(root, text="날씨 업데이트", command=update_weather)
update_button.pack(padx=10, pady=10)

# 실행
root.mainloop()
