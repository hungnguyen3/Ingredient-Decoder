package com.example.ingredientdecoder;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class checkallActivity extends AppCompatActivity {
    private ArrayList<String> al;
    private ArrayAdapter<String> aa;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_checkall);
        ListView listvi = findViewById(R.id.listvi);
        Button clearall = findViewById(R.id.clearall);
        String username = getIntent().getStringExtra("input_username");
        String[] base = {};
        al = new ArrayList<>(Arrays.asList(base));
        aa = new ArrayAdapter<>(this,R.layout.plist, R.id.item, al);
        listvi.setAdapter(aa);

        RequestQueue requestQueue = Volley.newRequestQueue(checkallActivity.this);
        JSONObject postData = new JSONObject();
        try {
            postData.put("username", username);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, "http:52.138.39.36:3000/ilist", postData, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                System.out.println(response);
                try {
                    JSONArray arr = response.getJSONArray("message");
                    List<String> list = new ArrayList<String>();
                    for(int i = 0; i < arr.length(); i++){
                        list.add(arr.getJSONObject(i).getString("item_name") +" (" + arr.getJSONObject(i).getString("item_list")+")");
                    }
                    al.addAll(list);
                    aa.notifyDataSetChanged();
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                error.printStackTrace();
                Log.d("myTag", "no resp");
            }
        });
        requestQueue.add(jsonObjectRequest);


        clearall.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                al.clear();
                aa.notifyDataSetChanged();
                RequestQueue requestQueue = Volley.newRequestQueue(checkallActivity.this);
                JSONObject postData = new JSONObject();
                try {
                    postData.put("username", username);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, "http:52.138.39.36:3000/ilist_clear", postData, new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println(response);
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        error.printStackTrace();
                        Log.d("myTag", "no resp");
                    }
                });
                requestQueue.add(jsonObjectRequest);

            }
        });
    }
}