package us.bravender.android.dongsa;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.widget.Toast;
import android.widget.ListView;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.SimpleAdapter;
import android.view.KeyEvent;
import android.view.inputmethod.EditorInfo;
import android.text.Editable;
import android.content.Context;
import android.content.res.Configuration;
import java.util.ArrayList;
import java.util.HashMap;

public class Dongsa extends Activity {
    private ArrayList<HashMap<String,String>> conjugations = new ArrayList<HashMap<String,String>>();
    private ListView list;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

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
        this.list.setAdapter(new SimpleAdapter(
            this,
            this.conjugations,
            R.layout.simple_expandable_list_item_2,
            new String[] { "conjugation_name", "conjugated" },
            new int[] { R.id.text1, R.id.text2 }
        ));

        edittext.setText("\ud558\ub2e4");
        engine.loadUrl("file:///android_asset/html/android.html");
    }

    public void clearList() {
        synchronized (this.conjugations) {
            this.conjugations.clear();
        }
    }

    public void add(String conjugation_name, String conjugated) {
        synchronized (this.conjugations) {
            HashMap<String,String> item = new HashMap<String,String>();
            item.put("conjugation_name", conjugation_name);
            item.put("conjugated", conjugated);
            this.conjugations.add(item);
        }
    }

    public void displayList() {
        synchronized (this.conjugations) {
            final SimpleAdapter adapter = (SimpleAdapter)this.list.getAdapter();
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

        public void add(String conjugation_name, String conjugated) {
            ((Dongsa)mContext).add(conjugation_name, conjugated);
        }

        public void displayList() {
            ((Dongsa)mContext).displayList();
        }
    }

    public class ConjugationEntry {
        public String conjugated;
        public String conjugation_name;

        public ConjugationEntry(String conjugation_name, String conjugated) {
            this.conjugated = conjugated;
            this.conjugation_name = conjugation_name;
        }
    }
}
