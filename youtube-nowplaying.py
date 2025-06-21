# msedge.exe --remote-debugging-port=9222
# chrome.exe --remote-debugging-port=9222
# 위와 같이, Chromium 기반 브라우저에서 디버깅 모드로 브라우저를 실행해야 함.
# TroubleShooting: 실행이 안되는 경우 taskkill /f /im (브라우저).exe로 완전 종료 후 실행
# YouTube에서 현재 재생 중인 탭의 제목을 가져옵니다. 

from flask import Flask, Response
import requests
import threading
import time

app = Flask(__name__)
current_title = "No Playing Detected"

def fetch_title():
    global current_title
    while True:
        try:
            tabs = requests.get("http://localhost:9222/json/list").json()
            for tab in tabs:
                if tab["type"] == "page" and tab["url"].startswith("https://www.youtube.com/watch"):
                    raw_title = tab.get("title", "No Title")
                    title = raw_title.split(' - YouTube')[0][:70]
                    if title and title != current_title:
                        current_title = title
        except Exception as e:
            print(f"Error fetching title: {e}")
        time.sleep(1)

threading.Thread(target=fetch_title, daemon=True).start()


@app.route('/')
def index():
    html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Now Playing Overlay</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
        
        body {
            background-color: transparent;
            margin: 0;
            padding: 0;
            font-family: 'Noto Sans KR', 'Arial', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        
        #container {
            background: linear-gradient(135deg, rgba(30, 30, 30, 0.95), rgba(0, 0, 0, 0.85));
            color: #ffffff;
            border-radius: 16px;
            border: 2px solid rgba(255, 107, 107, 0.3);
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            padding: 24px 32px;
            display: flex;
            align-items: center;
            width: 90vw;
            max-width: 800px;
            min-width: 400px;
            box-sizing: border-box;
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        
        #container::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        #music-icon {
            font-size: 32px;
            margin-right: 16px;
            color: #FF6B6B;
            animation: pulse 2s ease-in-out infinite;
            flex-shrink: 0;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.1); opacity: 0.8; }
        }
        
        #now-playing {
            font-size: 20px;
            font-weight: 700;
            color: #FF6B6B;
            margin-right: 20px;
            white-space: nowrap;
            flex-shrink: 0;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        #title-container {
            flex-grow: 1;
            overflow: hidden;
            position: relative;
            height: 40px;
            display: flex;
            align-items: center;
        }
        
        #title {
            white-space: nowrap;
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            animation-timing-function: linear;
            font-size: 28px;
            font-weight: 600;
            color: #ffffff;
            text-shadow: 
                0 3px 6px rgba(0, 0, 0, 0.6),
                0 0 12px rgba(0, 0, 0, 0.4);
            line-height: 1.2;
        }
        
        @keyframes scroll-left {
            0% { transform: translate(100%, -50%); }
            100% { transform: translate(-100%, -50%); }
        }
        
        /* 방송 환경 최적화 */
        @media (max-width: 768px) {
            #container {
                padding: 20px 24px;
                max-width: 600px;
            }
            #music-icon {
                font-size: 28px;
            }
            #now-playing {
                font-size: 18px;
                margin-right: 16px;
            }
            #title {
                font-size: 24px;
            }
            #title-container {
                height: 36px;
            }
        }
        
        /* 고해상도 디스플레이 최적화 */
        @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
            #container {
                border-width: 1px;
            }
        }
    </style>
    <script>
        function updateTitle() {
            fetch('/title')
                .then(response => response.text())
                .then(title => {
                    const titleElem = document.getElementById('title');
                    titleElem.textContent = title;
                    const container = document.getElementById('title-container');
                    
                    // 스크롤 애니메이션 조건
                    if (titleElem.scrollWidth > container.clientWidth) {
                        const scrollDistance = titleElem.scrollWidth + container.clientWidth;
                        const duration = Math.max(10, scrollDistance / 30); // 더 천천히
                        titleElem.style.animation = `scroll-left ${duration}s linear infinite`;
                        titleElem.style.animationDelay = '1s';
                    } else {
                        titleElem.style.animation = 'none';
                        titleElem.style.transform = 'translateY(-50%)';
                        titleElem.style.left = '0';
                    }
                });
            setTimeout(updateTitle, 1000);
        }
        
        window.onload = updateTitle;
        
        document.addEventListener('visibilitychange', function() {
            if (document.hidden) {
                document.getElementById('title').style.animationPlayState = 'paused';
            } else {
                document.getElementById('title').style.animationPlayState = 'running';
            }
        });
    </script>
</head>
<body>
    <div id="container">
        <div id="music-icon">🎵</div>
        <span id="now-playing">Now Playing</span>
        <div id="title-container">
            <div id="title">Loading...</div>
        </div>
    </div>
</body>
</html>
"""
    return Response(html_content, mimetype='text/html')

@app.route('/title')
def get_title():
    return Response(current_title, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
