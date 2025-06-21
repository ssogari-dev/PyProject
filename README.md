# 🐍 PyProject
가끔씩 유용하지만 잡다한 Python Script를 모아둡니다. 언젠가는 쓸 일이 있을 그런 것들을 끄적입니다.

## 📁 무엇을 올리나요?
대형 프로젝트는 아니지만, 한 번씩 쓸 수도 있는 Python 도구들을 올립니다. 각 스크립트는 독립적으로 동작하며, 간단한 설명이나 주석을 포함합니다. 해당 README에서 각 스크립트에 대한 정보를 보실 수 있습니다.

## 🛠️ 사용 방법
각 코드마다 다운로드를 받거나, Repository를 Clone하여 필요한 Script만 실행하세요. 
스크립트마다 필요한 모듈은 각 스크립트 명과 동일한 텍스트(.txt) 파일에 정리되어 있으므로, 흔히 `requirements.txt`로 저장하여 사용하는 방식대로 설치를 진행해주십시오.

```bash
git clone https://github.com/ssogari-dev/PyProject.git
cd PyProject
pip install -r {script-name}.txt
python {script-name}.py
```

## 📌 참고사항
* 모든 도구는 개인적인 용도로 개발되어 완성도가 높지 않습니다.
  * 적당히 제가 쓸 정도로만 만들어져 있으므로, 기능 개선 버전을 올려주시는 건 환영입니다.
* 실험용 코드가 포함되어 있습니다. 때문에, Python 코드에 대한 이해도가 높은 분의 사용을 권장합니다.
* 피드백이나 개선 아이디어는 환영입니다. 또, PR이나 Fork 또한 환영합니다.

## 📄 라이선스
MIT License

---
# 스크립트별 설명
## YouTube Now Playing Widget (youtube-nowplaying.py)
Python Flask를 사용합니다.
Chromium 기반 브라우저에서 YouTube를 재생하면, 해당 탭의 제목을 가져와 화면에 출력합니다.
OBS를 통해 오버레이로 사용하기 위해 제작하였습니다.
