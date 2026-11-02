# Changelog

## 1.0.0 — submitted for production review (2026-11-03)

- Add a privacy-policy link to the in-app help in all 31 locales.
- Display the installed app version and keep help readable on narrow screens with larger text.
- Prepare Korean and English Play descriptions, current app screenshots and an accessibility disclosure demonstration.
- Keep the package, signing certificate, Android 14 minimum and input behavior unchanged.

Google Play accepted versionCode 10 for production review at 00:25 KST on November 3, 2026. Submission 1 includes the production release, Korean and English store listings, app content and store settings; its status is **In review**. It has not been approved or publicly released. Managed publishing is off, so publication is set to proceed after approval. See the [release record](docs/play-production-release.md).

## 0.6.1-beta.1 — Google Play internal test (2026-10-27)

- Target Android 16 (API 36) while retaining Android 14 as the minimum version.
- Update Android Gradle Plugin to 8.10.1 and Gradle to 8.11.1; compile instrumentation against the selected SDK.
- Prepare a signed Android App Bundle with all 31 locales included for offline language selection.
- Keep the existing package, APK signing certificate, accessibility consent and saved settings.
- Publish versionCode 9 to the Google Play internal track for the five registered beta tester accounts. [Test invitation](https://play.google.com/apps/internaltest/4701300851549043962).
- Enroll the existing app signing key in Play App Signing and verify that the Play app signing certificate matches the official GitHub APK certificate.

The Console reports the release as available to internal testers and unreviewed. The invitation currently uses the temporary name `io.github.doctor_clawler.rightpress (unreviewed)`; opening it with a registered account was verified. A later 2026-11-02 check downloaded, installed and opened this version through Play on an Android 14 XCover 5; the test app was then removed. Physical-tablet accessibility remains unverified. Play installation does not automatically grant accessibility access or establish standard policy approval. The latest GitHub APK release remains 0.6.0-beta.1.

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
