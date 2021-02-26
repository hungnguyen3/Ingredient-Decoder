package com.example.ingredientdecoder;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class SignupActivity extends AppCompatActivity {
    private TextView signuoinfro;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);
        Button signupsib = findViewById(R.id.signupsib);
        EditText signupu = findViewById(R.id.signupu);
        EditText signupp = findViewById(R.id.signupp);
        RadioButton radioButton = findViewById(R.id.radioButton);
        signuoinfro= findViewById(R.id.signupinfro);

        signupsib.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                if(!(signupu.getText().toString().equals("") || signupp.getText().toString().equals(""))){
                    RequestQueue requestQueue = Volley.newRequestQueue(SignupActivity.this);
                    JSONObject postData = new JSONObject();
                    try {
                        postData.put("username", signupu.getText().toString());
                        postData.put("password", signupp.getText().toString());
                        if(radioButton.isChecked()) postData.put("type", "s");
                        else postData.put("type", "c");
                        JSONArray ilist = new JSONArray();
                        postData.put("itemlist", ilist);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    requestQueue.add(sendapi(postData, "http:52.138.39.36:3000/signup"));
                }else {
                    signuoinfro.setText("Please provide all information");
                }
            }
        });



    }


    private JsonObjectRequest sendapi(JSONObject a, String url) {

        JSONObject postData = new JSONObject();
        postData = a;
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, url, postData, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                System.out.println(response);
                try {
                    signuoinfro.setText(response.getString("message"));
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

        return jsonObjectRequest;

    }
}