package com.example.ingredientdecoder;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class MenuSActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu_s);
        Button addup = findViewById(R.id.addup);
        Button checkall = findViewById(R.id.checkall);
        String username = getIntent().getStringExtra("input_username");
        TextView welcome_s = findViewById(R.id.welcome_s);
        welcome_s.setText("Welcome! "+ username);
        addup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MenuSActivity.this, MainActivity3.class);
                intent.putExtra("input_username", username);
                startActivity(intent);
            }
        });
        checkall.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MenuSActivity.this, checkallActivity.class);
                intent.putExtra("input_username", username);
                startActivity(intent);
            }
        });
    }
}