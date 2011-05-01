package us.bravender.android.dongsa;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.widget.Toast;
import android.widget.ListView;
import android.content.Context;
import android.content.res.Configuration;
import java.util.ArrayList;
import android.widget.ArrayAdapter;

public class Dongsa extends Activity {
    private ArrayList<String> lnames;
    private ListView list;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        this.lnames = new ArrayList<String>();

        WebView engine = (WebView) findViewById(R.id.webview);
        engine.getSettings().setJavaScriptEnabled(true);
        engine.addJavascriptInterface(new JavaScriptInterface(this), "Android");

        this.list = (ListView) findViewById(R.id.listview);
        this.list.setAdapter(new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, this.lnames));

        engine.loadUrl("file:///android_asset/html/index.html");
    }

    public synchronized void clearList() {
        this.lnames.clear();
        ((ArrayAdapter)this.list.getAdapter()).notifyDataSetChanged();
    }

    public synchronized void add(String item) {
        this.lnames.add(item);
    }

    public synchronized void displayList() {
        ((ArrayAdapter)this.list.getAdapter()).notifyDataSetChanged();
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
    }

    public class JavaScriptInterface {
        Context mContext;
        JavaScriptInterface(Context c) {
            mContext = c;
        }

        public void showToast(String toast) {
            Toast.makeText(mContext, toast, Toast.LENGTH_SHORT).show();
        }

        public void clearList() {
            ((Dongsa)mContext).clearList();
        }

        public void add(String item) {
            ((Dongsa)mContext).add(item);
        }
    }
}
