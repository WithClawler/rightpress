package io.github.doctor_clawler.rightpress;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Path;
import android.os.SystemClock;
import android.view.MotionEvent;
import android.view.View;

import java.util.ArrayList;

/** Receives mouse events while the saved capture mode is enabled. */
public final class CaptureOverlay extends View {
    private final MouseLongPressService service;
    private boolean primaryDown;
    private boolean secondaryDown;
    private boolean secondaryHandled;
    private float startX, startY;
    private long startAt;
    private float pointerX, pointerY;
    private final ArrayList<float[]> samples = new ArrayList<>();

    public CaptureOverlay(Context context, MouseLongPressService service) {
        super(context);
        this.service = service;
        setBackgroundColor(Color.TRANSPARENT);
        setFocusable(false);
        setClickable(false);
        setImportantForAccessibility(IMPORTANT_FOR_ACCESSIBILITY_NO);
    }

    private float dp(float v) { return v * getResources().getDisplayMetrics().density; }

    void resetInput() {
        primaryDown = false;
        secondaryDown = false;
        secondaryHandled = false;
        samples.clear();
    }

    @Override public boolean onHoverEvent(MotionEvent event) {
        pointerX = event.getRawX();
        pointerY = event.getRawY();
        return true;
    }

    @Override public boolean onGenericMotionEvent(MotionEvent event) {
        pointerX = event.getRawX();
        pointerY = event.getRawY();
        int action = event.getActionMasked();
        if (action == MotionEvent.ACTION_BUTTON_PRESS) {
            if (event.getActionButton() == MotionEvent.BUTTON_SECONDARY) {
                beginSecondary(pointerX, pointerY);
                return true;
            }
            if (event.getActionButton() == MotionEvent.BUTTON_PRIMARY && !primaryDown) {
                beginPrimary(pointerX, pointerY);
                return true;
            }
        } else if (action == MotionEvent.ACTION_BUTTON_RELEASE) {
            if (event.getActionButton() == MotionEvent.BUTTON_SECONDARY && secondaryDown) {
                endSecondary(pointerX, pointerY);
                return true;
            }
            if (event.getActionButton() == MotionEvent.BUTTON_PRIMARY && primaryDown) {
                endPrimary(pointerX, pointerY);
                return true;
            }
            return true;
        } else if (action == MotionEvent.ACTION_SCROLL) {
            float v = event.getAxisValue(MotionEvent.AXIS_VSCROLL);
            float h = event.getAxisValue(MotionEvent.AXIS_HSCROLL);
            if (v != 0 || h != 0) service.scroll(pointerX, pointerY, v, h);
            return true;
        } else if (action == MotionEvent.ACTION_MOVE && primaryDown) {
            remember(pointerX, pointerY);
            return true;
        }
        return true;
    }

    @Override public boolean onTouchEvent(MotionEvent event) {
        pointerX = event.getRawX();
        pointerY = event.getRawY();
        int action = event.getActionMasked();
        switch (action) {
            case MotionEvent.ACTION_DOWN:
                if ((event.getButtonState() & MotionEvent.BUTTON_SECONDARY) != 0) {
                    beginSecondary(pointerX, pointerY);
                } else if (!primaryDown) {
                    beginPrimary(pointerX, pointerY);
                }
                return true;
            case MotionEvent.ACTION_MOVE:
                if (primaryDown) remember(pointerX, pointerY);
                return true;
            case MotionEvent.ACTION_UP:
                if (secondaryDown) endSecondary(pointerX, pointerY);
                else if (primaryDown) endPrimary(pointerX, pointerY);
                return true;
            case MotionEvent.ACTION_CANCEL:
                resetInput();
                return true;
            default:
                return true;
        }
    }

    private void beginSecondary(float x, float y) {
        if (secondaryDown) return; // DOWN and BUTTON_PRESS describe the same click.
        primaryDown = false;
        samples.clear();
        secondaryDown = true;
        secondaryHandled = service.handleSecondaryDown(x, y);
    }

    private void endSecondary(float x, float y) {
        secondaryDown = false;
        boolean handled = secondaryHandled;
        secondaryHandled = false;
        // Only unsupported long-press targets need a synthetic touch. Its start must wait
        // until UP because physical release cancels an in-flight injected touch.
        if (!handled) service.longPress(x, y);
    }

    private void beginPrimary(float x, float y) {
        primaryDown = true;
        startX = x;
        startY = y;
        startAt = SystemClock.uptimeMillis();
        samples.clear();
        remember(x, y);
    }

    private void remember(float x, float y) {
        if (samples.size() < 100) samples.add(new float[]{x, y});
    }

    private void endPrimary(float x, float y) {
        primaryDown = false;
        remember(x, y);
        float dx = x - startX;
        float dy = y - startY;
        if (Math.hypot(dx, dy) < dp(12)) {
            service.tap(x, y);
        } else {
            Path p = new Path();
            p.moveTo(startX, startY);
            for (float[] point : samples) p.lineTo(point[0], point[1]);
            p.lineTo(x, y);
            service.swipe(p, SystemClock.uptimeMillis() - startAt);
        }
        samples.clear();
    }
}
