package com.cortxt.app.mmcui.utils;

import com.cortxt.app.mmcutility.ICallbacks;

/**
 * Created by bscheurman on 16-03-17.
 */

public class Constants {
    static ICallbacks callbacks;
    public static void init (ICallbacks cb)
    {
        callbacks = cb;
    }
}
