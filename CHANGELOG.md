# Changelog

## 1.0.3 (versionCode 13) — Google Play production review requested (2026-11-05)

- Add a wheel scroll amount slider in all 31 locales: 10–100% of the previous swipe distance, defaulting to 30%. Apply adjustments immediately and preserve them across app and service restarts.

- Remove the floating Stop mouse button and its reserved click region so other apps remain unobstructed.
- Move Stop mouse to a quiet notification while mouse conversion is active. Ask once for notification permission; keep the app switch and Ctrl+Alt+R available when declined.
- Preserve mouse input, keyboard settings and localized notification controls through service reconnection and language changes.

The signed AAB was built from clean `release` source at tag `v1.0.3-13` (`8c6b07e`) and accepted by Play Console as release 3. The 100% production rollout request was submitted on November 5, 2026 at 22:57 KST; A later Console readback confirms changes are in review after the automated-check panel disappeared. Publication is pending Google approval. The signed APK passed an update-install from 1.0.2 and nine focused input/settings regressions; lint reported 0 errors and 7 existing warnings.

## 1.0.2 (versionCode 12) — Google Play production release (2026-11-04)

- Add a separate accessibility setup guide in all 31 locales before opening system settings from the main connection button or Help.
- Show the Samsung Installed apps path or the general Downloaded apps path with the localized service name.
- Keep first-use consent separate from setup instructions. Existing consent is not requested again; canceling the guide does not change settings or saved consent.
- Retain the supported-settings hint to scroll to or highlight the service entry. A direct jump to its detailed switch is not guaranteed.

The release was built from clean `release` source at tag `v1.0.2-12`. QA passed 38 regression tests and one narrow-screen check covering all 31 locales; the final release APK separately passed an update-install, launch and Help → guide → Android settings smoke check. Lint reported 0 errors and 7 warnings, and CI passed. Google Play accepted the 100% production rollout request at 21:17 KST on November 4, 2026 (submission 2) and records it as **Published** at 21:44 KST. A November 5 readback confirmed the Console status and version 1.0.2 in the Korean and US public listings. See the [release record](docs/play-production-release.md).

## 1.0.1 (versionCode 11) — earlier unreleased candidate

- Add a hint for supported Android settings screens to scroll to and highlight the RightPress service entry. It does not guarantee opening the detailed switch.

This candidate was not uploaded to Google Play and is superseded by 1.0.2.

## 1.0.0 — Google Play production release (2026-11-04)

- Add a privacy-policy link to the in-app help in all 31 locales.
- Display the installed app version and keep help readable on narrow screens with larger text.
- Prepare Korean and English Play descriptions, current app screenshots and an accessibility disclosure demonstration.
- Keep the package, signing certificate, Android 14 minimum and input behavior unchanged.

Google Play accepted versionCode 10 for production review at 00:25 KST on November 3, 2026. Submission 1 included the production release, Korean and English store listings, app content and store settings. The Console records it as **Published** at 14:43 KST on November 4, 2026; the [public store listing](https://play.google.com/store/apps/details?id=io.github.doctor_clawler.rightpress) offers installation without test enrollment. See the [release record](docs/play-production-release.md).

## 0.6.1-beta.1 — Google Play internal test (2026-10-27)

- Target Android 16 (API 36) while retaining Android 14 as the minimum version.
- Update Android Gradle Plugin to 8.10.1 and Gradle to 8.11.1; compile instrumentation against the selected SDK.
- Prepare a signed Android App Bundle with all 31 locales included for offline language selection.
- Keep the existing package, APK signing certificate, accessibility consent and saved settings.
- Publish versionCode 9 to the Google Play internal track for the five registered beta tester accounts. [Test invitation](https://play.google.com/apps/internaltest/4701300851549043962).
- Enroll the existing app signing key in Play App Signing and verify that the Play app signing certificate matches the official GitHub APK certificate.

The Console initially reported the release as available to internal testers and unreviewed. The invitation used the temporary name `io.github.doctor_clawler.rightpress (unreviewed)`; opening it with a registered account was verified. A later 2026-11-02 check downloaded, installed and opened this version through Play on an Android 14 XCover 5; the test app was then removed. Physical-tablet accessibility remains unverified. Play installation does not automatically grant accessibility access or establish standard policy approval. The latest GitHub APK release remains 0.6.0-beta.1.

## 0.6.0-beta.1

- Add 30 languages / 31 locales, including Simplified and Traditional Chinese.
- Follow the system language by default, with an in-app native-name picker and Android per-app language settings.
- Extract interface text, accessibility descriptions, validation messages and consent/help text into native Android string resources.
- Support RTL layouts and use system fonts without bundled font files or a localization SDK.
- Generate the language catalog from resource folders; add a standard-library Python tool to scaffold translations and check completeness and format arguments in CI.
- Keep the selected language after accessibility service reconnection and size the overlay stop control for translated text and screen readers.
- Keep the public package, release signing key, saved shortcuts and action identifiers unchanged. The signed APK updates the official 0.5.0 beta in place.

Translations are an initial beta and have not received native-speaker review. The market-based language selection is not a measured user ranking. See [LOCALIZATION.md](LOCALIZATION.md) for coverage and contribution steps; the [release page](https://github.com/WithClawler/rightpress/releases/tag/v0.6.0-beta.1) records build-specific verification and APK size when published.

## 0.5.0-beta.1

First public GitHub beta. Android 14 or later. Not a Google Play release.

- Publish the original RightPress source under MIT, with Gradle third-party notices.
- Use package `io.github.doctor_clawler.rightpress` and a dedicated signing key for public beta APKs.
- Add accessibility-use disclosure and explicit consent before activating input handling.
- Add a local-data privacy notice and public reporting instructions.
- Retain the Console interface, five mouse actions and seven keyboard actions.
- Add pinned GitHub Actions builds for debug APKs, lint and instrumentation-test compilation.

The beta installs separately from the former `com.example.rightpress` debug app. Disable its accessibility service and record settings before switching; there is no automatic settings migration. Release notes describe build-specific verification.

## 0.4.0-test

Private prototype.

- Apply the Console design: graphite background, blue accents, native mouse illustration and thin dividers.
- Adapt navigation to tablet side rail and narrow-screen bottom tabs.
- Preserve mouse/keyboard actions and stored settings.
- Check tablet portrait/landscape, narrow screens and larger text on an Android 15 emulator.

## 0.3.x-test

Private prototypes.

- Add configurable mouse actions and independent external-keyboard shortcuts.
- Add shortcut recording, app-launch targets and individual rule switches.
- Improve portrait layout and shorten Korean labels.

## 0.2.x-test

Private prototypes.

- Persist mouse-conversion state across service reconnection.
- Request accessibility long-click on right-button down, with a release-based touch fallback.
