# Google Play store listing — English

Copy prepared from the current app implementation. Saving this document does not publish or approve a production release. Character counts include spaces and line breaks.

## App name (28/30)

RightPress: Mouse & Keyboard

## Short description (77/80)

Set mouse right-click actions and external keyboard shortcuts on Android 14+.

## Full description (2609/4000)

Choose what your mouse right-click does and set external keyboard shortcuts on an Android tablet or phone. RightPress requires Android 14 or later.

Mouse right-click actions
• Choose long press, Back, Home, Recent apps or Notifications.
• Run a long press on button down when the screen element supports it.
• Fall back to a touch long press after button release when instant action is unavailable.
• Adjust the touch long-press duration.

External keyboard shortcuts
• Add a shortcut with Ctrl or Alt and another key. Shift can be included.
• Assign Back, Home, Recent apps, Notifications, Quick Settings, app launch or a mouse remapping toggle.
• Enable or disable individual shortcuts.
• Press Ctrl+Alt+R to toggle mouse remapping while the service is active.

Mouse and keyboard features have separate switches. RightPress supports 30 languages, with both Simplified and Traditional Chinese. It uses Android system fonts without downloading extra font files.

Getting started and background operation
Read and accept the accessibility disclosure in RightPress, then enable RightPress input helper in Android accessibility settings. The service must remain enabled to handle input while you use other apps. You do not need to keep the settings screen open. Android manages service startup and reconnection.

To stop all input handling, turn off the service in Android accessibility settings. You can also turn off mouse remapping or your configured keyboard shortcuts separately.

Accessibility API use
RightPress is a general mouse and keyboard utility. It uses the Accessibility API to match key events against your shortcuts, inspect screen element positions, hierarchy and supported actions, and perform the touch gestures and system actions you select.

It does not read element text or save screen contents, screenshots or input history. Settings and consent stay on your device and are not sent to the developer. No account or advertisements.

Compatibility
When mouse remapping is on, clicks, dragging and wheel input are relayed as touch gestures. Hover, precise dragging and text selection can behave differently from normal mouse input. You can turn mouse remapping off and keep keyboard shortcuts on. System or security screens and individual apps can restrict actions. Key-to-key remapping, macros and text expansion are not supported.

Privacy notice: https://github.com/WithClawler/rightpress/blob/main/PRIVACY.md
Support: support@mibstudio.top
Bug reports: https://github.com/WithClawler/rightpress/issues
Reports are public. Do not include personal information or private screen contents.
