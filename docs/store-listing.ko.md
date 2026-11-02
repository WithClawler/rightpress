# Google Play store listing — 한국어

Copy prepared from the current app implementation. Saving this document does not publish or approve a production release. Character counts include spaces and line breaks.

## App name (19/30)

RightPress: 마우스·키보드

## Short description (38/80)

우클릭을 길게 누르기로 바꾸고 외장 키보드 단축키로 뒤로·홈·앱 실행

## Full description (1368/4000)

RightPress로 Android 태블릿과 휴대폰의 마우스 우클릭 동작과 외장 키보드 단축키를 설정하세요. Android 14 이상에서 사용할 수 있습니다.

마우스 우클릭
• 길게 누르기, 뒤로, 홈, 최근 앱, 알림 열기 중에서 선택
• 길게 누르기를 지원하는 화면 요소는 버튼을 누르는 순간 실행
• 즉시 실행이 지원되지 않으면 버튼을 뗀 뒤 터치 길게 누르기로 처리
• 터치 길게 누르기 시간 조절

외장 키보드 단축키
• Ctrl 또는 Alt와 일반 키를 조합해 단축키 추가. Shift도 함께 사용 가능
• 뒤로, 홈, 최근 앱, 알림, 빠른 설정, 앱 실행, 마우스 변환 켜기·끄기 지정
• 단축키마다 사용 여부 설정
• Ctrl+Alt+R로 마우스 변환을 빠르게 켜거나 끄기

마우스와 키보드 기능은 각각 켜고 끌 수 있습니다. 30개 언어를 지원하며 중국어는 간체와 번체를 제공합니다. 별도 폰트를 내려받지 않고 Android 시스템 폰트를 사용합니다.

시작과 백그라운드 동작
앱에서 접근성 사용 안내에 동의한 뒤 Android 접근성 설정에서 RightPress 입력 도우미를 켜세요. 다른 앱을 사용하는 동안 입력을 처리하려면 이 서비스가 켜져 있어야 합니다. 설정 화면을 계속 열어 둘 필요는 없습니다. Android가 서비스의 시작과 재연결을 관리합니다.

전체 입력 처리를 멈추려면 Android 접근성 설정에서 서비스를 끄세요. 마우스 변환만 끄거나 등록한 키보드 단축키만 끄는 것도 가능합니다.

접근성 API 사용
RightPress는 일반 마우스·키보드 입력 유틸리티입니다. 접근성 API로 키 입력 이벤트를 등록 단축키와 비교하고, 화면 요소의 위치·계층·지원 동작을 확인하며, 사용자가 지정한 터치 제스처와 시스템 동작을 실행합니다.

화면 요소의 텍스트를 읽거나 화면 내용·스크린샷·입력 기록을 저장하지 않습니다. 설정과 동의 상태는 기기에 저장하며 개발자에게 전송하지 않습니다. 계정 가입과 광고가 없습니다.

사용 범위
마우스 변환을 켜면 클릭·드래그·휠을 터치 입력으로 처리하므로 호버, 정밀 드래그, 텍스트 선택은 원래 마우스 동작과 달라질 수 있습니다. 필요할 때 마우스 변환을 끄고 키보드 단축키만 사용할 수 있습니다. 시스템·보안 화면이나 앱에서 제한하는 동작은 실행되지 않을 수 있습니다. 키-대-키 변경, 매크로, 문구 자동 입력은 지원하지 않습니다.

개인정보 안내: https://github.com/WithClawler/rightpress/blob/main/PRIVACY.md
문의: support@mibstudio.top
오류 제보: https://github.com/WithClawler/rightpress/issues
공개 게시물에는 개인정보나 비공개 화면을 포함하지 마세요.
