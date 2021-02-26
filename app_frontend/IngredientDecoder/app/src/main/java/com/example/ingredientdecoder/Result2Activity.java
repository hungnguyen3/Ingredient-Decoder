package com.example.ingredientdecoder;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

public class Result2Activity extends AppCompatActivity {

    @SuppressLint("SetTextI18n")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result2);
        String namei = getIntent().getStringExtra("namei");
        String ili = getIntent().getStringExtra("ili");
        String imagei = getIntent().getStringExtra("imagei");
        String ownerii = getIntent().getStringExtra("ownerii");
        TextView textresult = findViewById(R.id.textresult);
        ImageView imageresult = findViewById(R.id.imageresult);
        textresult.setText("Item name:" + namei + "\n\n" + "Ingredient list:" + ili + "\n\n" + "Store Owner:" + ownerii);

        RequestQueue requestQueue = Volley.newRequestQueue(Result2Activity.this);
        JSONObject postData = new JSONObject();
        try {
            postData.put("search_id", imagei);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, "http:52.138.39.36:3000/image_get", postData, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                System.out.println(response);
                try {
                    byte[] decodedString = new byte[0];
                    decodedString = Base64.decode(response.getJSONObject("message").getString("item_image"), Base64.DEFAULT);
                    Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
                    imageresult.setImageBitmap(decodedByte);
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