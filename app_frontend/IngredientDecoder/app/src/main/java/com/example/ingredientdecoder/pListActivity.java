package com.example.ingredientdecoder;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
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

public class pListActivity extends AppCompatActivity { // personalized list function page
    private ArrayList<String> al;
    private ArrayAdapter<String> aa;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_plist);
        String username = getIntent().getStringExtra("input_username");
        Button add = findViewById(R.id.add);
        Button clear = findViewById(R.id.clear);
        EditText input = findViewById(R.id.input);
        ListView listV = findViewById(R.id.listV);
        // variables
        String[] base = {};
        al = new ArrayList<>(Arrays.asList(base));
        aa = new ArrayAdapter<>(this,R.layout.plist, R.id.item, al);
        listV.setAdapter(aa);
        // set up the list view
        RequestQueue requestQueue = Volley.newRequestQueue(pListActivity.this);
        JSONObject postData = new JSONObject();
        try {
            postData.put("username", username);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        // prepare the API req
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, "http:52.138.39.36:3000/plist", postData, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                System.out.println(response);
                try {
                    JSONArray arr = response.getJSONArray("message");
                    List<String> list = new ArrayList<String>();
                    for(int i = 0; i < arr.length(); i++){
                        list.add(arr.getJSONObject(i).getString("p"));
                    }
                    al.addAll(list);
                    aa.notifyDataSetChanged();
                    // init the listView with the result
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
        // send the request



        add.setOnClickListener(new View.OnClickListener() { // add button
            @Override
            public void onClick(View v) {
                String newi = input.getText().toString();
                al.add(newi);
                aa.notifyDataSetChanged();
                // add one in listView
                RequestQueue requestQueue = Volley.newRequestQueue(pListActivity.this);
                JSONObject postData = new JSONObject();
                try {
                    postData.put("username", username);
                    postData.put("plist_add", newi);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                // prepare the API req
                JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, "http:52.138.39.36:3000/plist_add", postData, new Response.Listener<JSONObject>() {
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
                // send the request to add one in plist of user's account
            }
        });
        clear.setOnClickListener(new View.OnClickListener() { // clear button
            @Override
            public void onClick(View v) {
                al.clear();
                aa.notifyDataSetChanged();
                // clear the ListView
                RequestQueue requestQueue = Volley.newRequestQueue(pListActivity.this);
                JSONObject postData = new JSONObject();
                try {
                    postData.put("username", username);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                // prepare the API req
                JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, "http:52.138.39.36:3000/plist_clear", postData, new Response.Listener<JSONObject>() {
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
                // send the req
            }
        });
    }
}