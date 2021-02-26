package com.example.ingredientdecoder;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Parcelable;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

public class LoginActivity extends AppCompatActivity {
    private EditText username_t;
    private EditText password_t;
    private Button login_b;
    private Button signup_b;
    private TextView loginmes;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        username_t = findViewById(R.id.username);
        password_t = findViewById(R.id.password);
        login_b = findViewById(R.id.login);
        loginmes = findViewById(R.id.loginmes);
        signup_b = findViewById(R.id.signup);
        login_b.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(!(username_t.getText().toString().equals("") || password_t.getText().toString().equals(""))){
                    RequestQueue requestQueue = Volley.newRequestQueue(LoginActivity.this);
                    JSONObject postData = new JSONObject();
                    try {
                        postData.put("username", username_t.getText().toString());
                        postData.put("password", password_t.getText().toString());
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, "http:52.138.39.36:3000/login", postData, new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            System.out.println(response);
                            try {
                                if(response.getString("message").equals("clogin")){
                                    Intent intent = new Intent(LoginActivity.this, MenuCActivity.class);
                                    intent.putExtra("input_username", username_t.getText().toString());
                                    startActivity(intent);
                                }else if(response.getString("message").equals("slogin")){
                                    Intent intent = new Intent(LoginActivity.this, MenuSActivity.class);
                                    intent.putExtra("input_username", username_t.getText().toString());
                                    startActivity(intent);
                                }
                                else{
                                    loginmes.setText("wrong username or password!");
                                    password_t.setText("");
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                                loginmes.setText("offline???");
                                password_t.setText("");
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
                else{
                    loginmes.setText("empty username or password!");
                    password_t.setText("");
                }
            }
        });
        signup_b.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(LoginActivity.this, SignupActivity.class);
                startActivity(intent);
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