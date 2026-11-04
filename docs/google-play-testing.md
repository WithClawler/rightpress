# Google Play 테스트 배포

이전 Play 내부 테스트 기록: **`0.6.1-beta.1` / versionCode `9`**. 2026-10-27 01:57 KST에 Console의 **내부 테스터에게 제공됨** 상태와 **검토되지 않음** 표시를 확인했다.

[Google Play 테스트 참여](https://play.google.com/apps/internaltest/4701300851549043962). 당시 기존 `Stack Rush App Tester Beta` 목록의 등록 계정 5개를 대상으로 배포했다. GitHub APK의 최신 공개 버전은 [0.6.0-beta.1](https://github.com/WithClawler/rightpress/releases/tag/v0.6.0-beta.1)이다.

정식 **1.0.0 (10)**은 2026-11-04 14:43 KST에 Console **출시됨**으로 확인됐다. [공개 스토어](https://play.google.com/store/apps/details?id=io.github.doctor_clawler.rightpress)에서 테스트 참여 없이 설치할 수 있다. [출시 기록](play-production-release.md)을 참조한다.

후속 **1.0.2 (12)**는 별도 접근성 설정 안내를 31개 로캘에 추가한 후보이며 아직 Play 업로드·심사 제출 전이다. 후보의 빌드·기기 검사 결과와 배포 상태는 별도로 기록한다.

## 이전 내부 테스트 설치 절차

1. 등록된 테스터 Google 계정으로 로그인한 상태에서 위 참여 링크를 연다.
2. **Accept invite**로 초대를 수락한 뒤 Google Play 설치 링크를 따른다.
3. RightPress를 실행하고 접근성 사용 안내를 읽고 동의한다.
4. 앱에서 Android 접근성 설정을 열어 **RightPress 입력 도우미**를 켠다.
5. 앱으로 돌아와 마우스·키보드 기능을 설정한다.

당시 초대 페이지의 임시 이름은 `io.github.doctor_clawler.rightpress (unreviewed)`였다. 지정된 5계정 대상 내부 테스트 기록이며, 이후 공개된 1.0.0 프로덕션 출시와 구분한다.

2026-11-02 Galaxy XCover 5(SM-G525N, Android 14)에서 실제 Play 다운로드·설치·앱 첫 화면 실행을 확인했다. 패키지 관리자의 버전은 `0.6.1-beta.1 (9)`, 설치 출처는 `com.android.vending`이었다. 이후 사용자 요청으로 앱을 삭제하고 패키지·서비스가 남지 않은 것을 확인했다. 전원 설정은 상시 켜짐 OFF·화면 꺼짐 30초로 유지했다. 접근성 서비스 활성화·외장 입력 동작은 이 검사에 포함되지 않았다.

Galaxy Tab A9(Android 16)의 다운로드 실패는 원인 미확정이다. Play 웹의 원격 설치 접수나 ‘이미 설치됨’ 표시를 실기기 설치 성공으로 취급하지 않는다. Android 16 에뮬레이터에서는 Play 서명 APK의 ADB 설치만 성공했고, 라이선스 확인이 로그인되지 않은 Play 스토어로 이어져 앱 첫 화면 실행·Play 다운로드는 검증하지 못했다.

## 빌드

- application ID: `io.github.doctor_clawler.rightpress`
- minSdk 34 / targetSdk 36 / compileSdk 36
- JDK 17 / Android Gradle Plugin 8.10.1 / Gradle 8.11.1
- 공식 APK와 같은 배포 서명 사용. 비밀 정보는 로컬 환경 변수로만 제공.

```sh
python3 tools/localization.py check
./gradlew :app:bundleRelease :app:assembleRelease :app:lintRelease
```

AAB: `app/build/outputs/bundle/release/app-release.aab`.
모든 언어를 포함하며 별도 폰트·네이티브 라이브러리를 추가하지 않는다.

## API 업로드

Play Developer API로 테스트 트랙 업로드를 자동화한다. 서비스 계정은 `play-publisher@mib-support-mail-20261022.iam.gserviceaccount.com`(MIB Operations 프로젝트)이고, 키는 저장소 밖 `~/.config/works/google-play/play-publisher.json`(0600)에 둔다. Play Console의 **사용자 및 권한**에서 이 계정을 RightPress 앱에 한정해 초대해야 동작한다.

```sh
python3 tools/play_publish.py check     # 권한 확인, 변경 없음
python3 tools/play_publish.py upload --aab <signed.aab> --track internal
python3 tools/play_publish.py status    # 트랙별 출시 재조회
```

출시 노트는 `fastlane/metadata/android/<언어>/changelogs/<versionCode>.txt`에서 읽는다. 업로드 후 같은 명령이 트랙 상태를 다시 읽어 출력한다.

## 기존 설치와 서명

Play App Signing에 **기존 앱 서명키**를 등록했다. PEPK 암호화 파일 업로드·저장 후 Console의 **앱 서명 인증서**가 기존 공식 APK 인증서와 일치함을 확인했다. AAB 업로드 인증서만 비교한 결과가 아니다.

기존 공식 APK의 앱 서명 인증서 SHA-256:

```text
28:BB:0C:A0:7D:34:46:6F:92:AD:DA:DE:BB:06:14:F9:EE:EB:52:7F:CD:1D:B8:76:4B:DA:74:C9:8F:00:EA:E0
```

키 원본·암호·암호화한 키 파일은 저장소나 GitHub 릴리스에 올리지 않는다. 향후 서명 변경 시에도 앱 서명 인증서를 비교하며, 삭제 후 재설치를 업데이트 검증의 대체로 삼지 않는다.

## code 9 내부 테스트 배포 검증 기록

- 제출한 AAB SHA-256: `db33c990f7d69a8aad0ea819200426af9fbafd6dae96a911a0fc59efb0a439ac`.
- Console이 AAB를 수락한 뒤 package `io.github.doctor_clawler.rightpress`, versionCode `9`, minSdk `34`, targetSdk `36`을 확인했다.
- 내부 트랙의 `0.6.1-beta.1 (9)`가 활성 상태이며 내부 테스터에게 제공됨을 확인했다.
- `Stack Rush App Tester Beta` 5계정 목록만 선택되어 있고, 다른 목록은 미선택이며 저장 버튼이 비활성화된 저장 상태를 확인했다.
- Console에서 발급한 참여 링크를 등록 계정으로 열어 초대 페이지가 표시됨을 확인했다. 명단 등록·사용자 참여·실제 설치는 각각 별도 단계다.

## 내부 테스트 완료 기준

1. 앱 등록과 필요한 정책·수출 규정·앱 서명 설정 완료.
2. 서명된 AAB 업로드 후 Console에 표시된 패키지·versionCode·targetSdk 확인.
3. 테스터가 실제 사용할 Google 계정을 내부 테스트 대상으로 등록.
4. 내부 테스트 출시 상태와 Console에서 발급된 참여 URL 확인.
5. 등록 계정으로 참여 페이지가 열리는지 확인. Play 설치 후 접근성 연결·입력 동작은 기기에서 별도 검증.

내부 테스트 배포를 일반 공개 출시나 Google 정책 심사 통과로 표현하지 않는다. Play 설치도 접근성 권한을 자동으로 허용하지 않는다. 기기 정책이나 고급 보호 제한은 별도로 적용될 수 있다.

## 접근성 설정

공개된 1.0.0은 RightPress 실행 → 접근성 안내에 동의 → Android 접근성 설정에서 서비스를 켜는 흐름이다. 삼성은 **설치된 앱 → 현재 언어의 RightPress 입력 도우미 → 사용 ON → 허용**, 일반 기기는 **다운로드한 앱 → 서비스 → 사용 ON → 허용** 경로를 확인한다.

1.0.2 후보는 메인 연결 버튼과 도움말 모두에서 시스템 설정을 열기 전에 별도 경로 안내를 보여준다. 서비스명은 현재 언어의 `service_name`을 사용한다. 기존 동의를 다시 요청하지 않고, 안내 취소는 설정·저장된 동의 상태를 변경하지 않는다. 목록 스크롤·강조는 지원하는 설정 화면에 전달하는 힌트이며 상세 스위치 화면으로 바로 열리는 것을 보장하지 않는다. 이 후보는 아직 업로드·제출 전이다.

동의 없이 시스템 설정에서 먼저 서비스를 켜면 앱이 서비스를 종료한다.

직접 받은 APK에서 '제한된 설정'이 표시되면 Android 앱 정보의 '제한된 설정 허용' 경로를 확인한다. Play Protect 해제나 `isAccessibilityTool=true` 허위 선언으로 제한을 우회하지 않는다. RightPress는 일반 마우스·키보드 유틸로 `isAccessibilityTool=false`를 유지한다.

## 백그라운드 동작

다른 앱에서 마우스·키보드 입력을 처리하려면 접근성 서비스가 켜져 있어야 한다. 설정 화면을 닫아도 작동하며 화면을 항상 켜 둘 필요는 없다. 기능별 ON/OFF는 저장된다. Android가 서비스 시작·재연결을 관리하므로 재부팅이나 시스템 제한 후에는 앱과 접근성 설정에서 상태를 확인한다. 기기별 중단 없는 실행·배터리 영향은 추가 검증이 필요하다.

## 참고

- [Google Play 대상 API 요구사항](https://support.google.com/googleplay/android-developer/answer/11926878)
- [내부·비공개·공개 테스트](https://support.google.com/googleplay/android-developer/answer/9845334)
- [앱 서명 및 기존 키 등록](https://developer.android.com/studio/publish/app-signing)
- [접근성 API 정책](https://support.google.com/googleplay/android-developer/answer/10964491)
- [Android 제한된 설정](https://support.google.com/android/answer/12623953)
