package us.bravender.android.dongsa;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.content.res.Configuration;

public class Dongsa extends Activity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        WebView engine = (WebView) findViewById(R.id.web_engine);
        engine.getSettings().setJavaScriptEnabled(true);

        engine.loadUrl("file:///android_asset/html/index.html");
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
    }
}
