package com.example.ingredientdecoder;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

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
import java.util.List;

public class bynameActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_byname);
        Button submitname = findViewById(R.id.submitname);
        Button gotoimage = findViewById(R.id.gotoimage);
        EditText byname = findViewById(R.id.byname);
        String username = getIntent().getStringExtra("input_username");
        submitname.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(!(byname.getText().toString().equals(""))){

                    RequestQueue requestQueue = Volley.newRequestQueue(bynameActivity.this);
                    JSONObject postData = new JSONObject();
                    try {
                        postData.put("to_search", byname.getText().toString());
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, "http:52.138.39.36:3000/search_byname", postData, new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            System.out.println(response);
                            JSONArray arr = null;
                            try {
                                arr = response.getJSONArray("message");
                                List<String> name_list = new ArrayList<String>();
                                List<String> il_list = new ArrayList<String>();
                                List<String> image_list = new ArrayList<String>();
                                List<String> owner_list = new ArrayList<String>();
                                for(int i = 0; i < arr.length(); i++){
                                    name_list.add(arr.getJSONObject(i).getString("item_name"));
                                    il_list.add(arr.getJSONObject(i).getString("item_list"));
                                    image_list.add(arr.getJSONObject(i).getString("_id"));
                                    owner_list.add(arr.getJSONObject(i).getString("owner"));
                                }
                                Intent intent = new Intent(bynameActivity.this, Result2_listActivity.class);
                                intent.putExtra("name_list", name_list.toArray(new String[0]));
                                intent.putExtra("il_list", il_list.toArray(new String[0]));
                                intent.putExtra("image_list", image_list.toArray(new String[0]));
                                intent.putExtra("owner_list", owner_list.toArray(new String[0]));
                                startActivity(intent);
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

                }
            }
        });
        gotoimage.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                    Intent intent = new Intent(bynameActivity.this, MainActivity2.class);
                    startActivity(intent);
            }
        });
    }
}