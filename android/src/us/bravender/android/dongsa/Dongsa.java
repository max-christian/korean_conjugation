package us.bravender.android.dongsa;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.widget.Toast;
import android.widget.ListView;
import android.widget.EditText;
import android.widget.TextView;
import android.view.KeyEvent;
import android.view.inputmethod.EditorInfo;
import android.text.Editable;
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

        final WebView engine = new WebView(this);
        engine.getSettings().setJavaScriptEnabled(true);
        engine.addJavascriptInterface(new JavaScriptInterface(this), "Android");

        final EditText edittext = (EditText) findViewById(R.id.searchEdit);
        edittext.setOnEditorActionListener(new TextView.OnEditorActionListener() {
            public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
                engine.loadUrl("javascript:update('" + v.getText() + "', false);");
                return true;
            }
        });

        this.list = (ListView) findViewById(R.id.listview);
        this.list.setAdapter(new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, this.lnames));

        engine.loadUrl("file:///android_asset/html/android.html");
    }

    public void clearList() {
        synchronized (this.lnames) {
            this.lnames.clear();
            final ArrayAdapter adapter = (ArrayAdapter)this.list.getAdapter();
            this.list.post(new Runnable() {
                public void run() {
                    adapter.notifyDataSetChanged();
                }
            });
        }
    }

    public void add(String item) {
        synchronized (this.lnames) {
            this.lnames.add(item);
        }
    }

    public void displayList() {
        synchronized (this.lnames) {
            final ArrayAdapter adapter = (ArrayAdapter)this.list.getAdapter();
            this.list.post(new Runnable() {
                public void run() {
                    adapter.notifyDataSetChanged();
                }
            });
        }
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

        public void displayList() {
            ((Dongsa)mContext).displayList();
        }
    }
}
